#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

import pytest
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import HypervisorClusterProfileModule

YAML_CLUSTER_PROFILE = """
    config: "{{ config }}"
    state: present
    create_vswitch_layout: True
    data:
        uri: /rest/hypervisor-cluster-profiles/4671582d-1746-4122-9cf0-642a59543509
        name: "hcp"
        hypervisorHostProfileTemplate:
            virtualSwitches: "test"
    """

YAML_CLUSTER_PROFILE_PRESENT = """
        config: "{{ config }}"
        state: present
        create_vswitch_layout: True
        data:
            name: "hcp"
            hypervisorHostProfileTemplate:
                virtualSwitches: "test"
        """

YAML_CLUSTER_PROFILE_RENAME = """
        config: "{{ config }}"
        state: present
        create_vswitch_layout: True
        data:
            name: "hcp"
            newName: "hcp (renamed)"
            hypervisorHostProfileTemplate:
                virtualSwitches: "test"
        """

YAML_CLUSTER_PROFILE_NO_RENAME = """
    config: "{{ config }}"
    state: present
    create_vswitch_layout: True
    data:
        name: "hcp (renamed)"
        newName: "hcp"
        hypervisorHostProfileTemplate:
            virtualSwitches: "test"
    """

YAML_CLUSTER_PROFILE_ABSENT = """
        config: "{{ config }}"
        state: absent
        params:
            force: True
        data:
            name: "hcp"
        """

DICT_DEFAULT_CLUSTER_PROFILE = yaml.load(YAML_CLUSTER_PROFILE)["data"]


@pytest.mark.resource(TestHypervisorClusterProfileModule='hypervisor_cluster_profiles')
class TestHypervisorClusterProfileModule(OneViewBaseTest):
    def test_should_create_when_resource_not_exist(self):
        self.resource.get_by_name.return_value = None
        self.resource.create_virtual_switch_layout.return_value = "test"
        self.resource.create.return_value = self.resource
        self.resource.data = DICT_DEFAULT_CLUSTER_PROFILE
        self.mock_ansible_module.params = yaml.load(YAML_CLUSTER_PROFILE_PRESENT)

        HypervisorClusterProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorClusterProfileModule.MSG_CREATED,
            ansible_facts=dict(hypervisor_cluster_profile=DICT_DEFAULT_CLUSTER_PROFILE)
        )

    def test_should_not_update_when_existing_data_is_equals(self):
        self.resource.create_virtual_switch_layout.return_value = "test"
        self.resource.data = DICT_DEFAULT_CLUSTER_PROFILE
        self.mock_ansible_module.params = yaml.load(YAML_CLUSTER_PROFILE_NO_RENAME)

        HypervisorClusterProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=HypervisorClusterProfileModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(hypervisor_cluster_profile=DICT_DEFAULT_CLUSTER_PROFILE)
        )

    def test_should_update_when_data_has_modified_attributes(self):
        self.resource.create_virtual_switch_layout.return_value = "test"
        data_merged = DICT_DEFAULT_CLUSTER_PROFILE.copy()
        data_merged['newName'] = 'New Name'

        self.resource.data = DICT_DEFAULT_CLUSTER_PROFILE
        self.mock_ansible_module.params = yaml.load(YAML_CLUSTER_PROFILE_RENAME)

        HypervisorClusterProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorClusterProfileModule.MSG_UPDATED,
            ansible_facts=dict(hypervisor_cluster_profile=DICT_DEFAULT_CLUSTER_PROFILE)
        )

    def test_should_delete_hypervisor_cluster_profile_when_resource_exist(self):
        self.resource.data = DICT_DEFAULT_CLUSTER_PROFILE
        self.resource.delete.return_value = True
        self.mock_ansible_module.params = yaml.load(YAML_CLUSTER_PROFILE_ABSENT)

        HypervisorClusterProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorClusterProfileModule.MSG_DELETED,
            ansible_facts=dict(hypervisor_cluster_profile=None)
        )

    def test_should_do_nothing_when_resource_already_absent(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_CLUSTER_PROFILE_ABSENT)

        HypervisorClusterProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=HypervisorClusterProfileModule.MSG_ALREADY_ABSENT,
            ansible_facts=dict(hypervisor_cluster_profile=None)
        )


if __name__ == '__main__':
    pytest.main([__file__])
