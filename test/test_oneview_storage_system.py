###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import unittest
import yaml

from oneview_module_loader import StorageSystemModule
from hpe_test_utils import OneViewBaseTestCase


FAKE_MSG_ERROR = 'Fake message error'

YAML_STORAGE_SYSTEM = """
        config: "{{ config }}"
        state: present
        data:
            credentials:
                ip_hostname: '{{ storage_system_ip_hostname }}'
                username: '{{ storage_system_username }}'
                password: '{{ storage_system_password }}'
            managedDomain: TestDomain
            managedPools:
              - domain: TestDomain
                type: StoragePoolV2
                name: CPG_FC-AO
                deviceType: FC
          """

YAML_STORAGE_SYSTEM_BY_NAME = """
    config: "{{ config }}"
    state: present
    data:
        name: SSName
        managedDomain: TestDomain
        managedPools:
          - domain: TestDomain
            type: StoragePoolV2
            name: CPG_FC-AO
            deviceType: FC
      """

YAML_STORAGE_SYSTEM_CHANGES = """
        config: "{{ config }}"
        state: present
        data:
            credentials:
                ip_hostname: '{{ storage_system_ip_hostname }}'
                newIp_hostname: 'New IP Hostname'
                username: '{{ storage_system_username }}'
                password: '{{ storage_system_password }}'
            managedDomain: TestDomain
            managedPools:
              - domain: TestDomain
                type: StoragePoolV2
                name: CPG_FC-AO
                deviceType: FC
      """

YAML_STORAGE_SYSTEM_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            credentials:
                ip_hostname: 172.18.11.12
"""

DICT_DEFAULT_STORAGE_SYSTEM = yaml.load(YAML_STORAGE_SYSTEM)["data"]
del DICT_DEFAULT_STORAGE_SYSTEM['credentials']['password']


class StorageSystemModuleSpec(unittest.TestCase,
                              OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageSystemModule)
        self.resource = self.mock_ov_client.storage_systems

    def test_should_create_new_storage_system(self):
        self.resource.get_by_ip_hostname.return_value = None
        self.resource.add.return_value = {"name": "name"}
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageSystemModule.MSG_ADDED,
            ansible_facts=dict(storage_system={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StorageSystemModule.MSG_ALREADY_UPDATED,
            ansible_facts=dict(storage_system=DICT_DEFAULT_STORAGE_SYSTEM)
        )

    def test_should_not_update_when_data_is_equals_using_name(self):
        dict_by_name = yaml.load(YAML_STORAGE_SYSTEM_BY_NAME)["data"]

        self.resource.get_by_name.return_value = dict_by_name

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM_BY_NAME)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StorageSystemModule.MSG_ALREADY_UPDATED,
            ansible_facts=dict(storage_system=dict_by_name.copy())
        )

    def test_should_fail_with_missing_required_attributes(self):
        self.mock_ansible_module.params = {"state": "present",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid"}}

        StorageSystemModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=StorageSystemModule.MSG_MANDATORY_FIELDS_MISSING
        )

    def test_should_fail_when_credentials_attribute_is_missing(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM_BY_NAME)

        StorageSystemModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=StorageSystemModule.MSG_CREDENTIALS_MANDATORY
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DICT_DEFAULT_STORAGE_SYSTEM.copy()
        data_merged['credentials']['newIp_hostname'] = '10.10.10.10'

        self.resource.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM_CHANGES)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageSystemModule.MSG_UPDATED,
            ansible_facts=dict(storage_system=data_merged)
        )

    def test_should_remove_storage_system(self):
        self.resource.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM_ABSENT)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageSystemModule.MSG_DELETED
        )

    def test_should_do_nothing_when_storage_system_not_exist(self):
        self.resource.get_by_ip_hostname.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_SYSTEM_ABSENT)

        StorageSystemModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StorageSystemModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
