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

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import HypervisorManagerModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_HYPERVISOR_MANAGER_TEMPLATE = dict(
    name='172.18.13.11',
    hypervisorType='Vmware',
    displayName='vcenter',
    username='dcs',
    password='dcs'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_HYPERVISOR_MANAGER_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_HYPERVISOR_MANAGER_TEMPLATE['name'],
              displayName="vcenter renamed",
              hypervisorType='Vmware')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_HYPERVISOR_MANAGER_TEMPLATE['name'])
)


@pytest.mark.resource(TestHypervisorManagerModule='hypervisor_managers')
class TestHypervisorManagerModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_hypervisor_manager(self):
        self.resource.get_by_name.return_value = []

        self.resource.data = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        HypervisorManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorManagerModule.MSG_CREATED,
            ansible_facts=dict(hypervisor_manager=DEFAULT_HYPERVISOR_MANAGER_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        HypervisorManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=HypervisorManagerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(hypervisor_manager=DEFAULT_HYPERVISOR_MANAGER_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE.copy()
        data_merged['displayName'] = 'vcenter renamed'

        self.resource.data = data_merged
        self.resource.update.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        HypervisorManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorManagerModule.MSG_UPDATED,
            ansible_facts=dict(hypervisor_manager=data_merged)
        )

    def test_should_remove_hypervisor_manager(self):
        self.resource.data = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        HypervisorManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=HypervisorManagerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_hypervisor_manager_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        HypervisorManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=HypervisorManagerModule.MSG_ALREADY_ABSENT
        )

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/hypervisor-managers/fake'
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        HypervisorManagerModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(hypervisor_manager=patch_return),
            msg=HypervisorManagerModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_HYPERVISOR_MANAGER_TEMPLATE.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.data = resource_data

        HypervisorManagerModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_manager=resource_data),
            msg=HypervisorManagerModule.MSG_ALREADY_PRESENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
