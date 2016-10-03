###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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
import mock
import yaml

from hpOneView.oneview_client import OneViewClient
from oneview_storage_system import StorageSystemModule, STORAGE_SYSTEM_ADDED, STORAGE_SYSTEM_ALREADY_UPDATED, \
    STORAGE_SYSTEM_UPDATED, STORAGE_SYSTEM_DELETED, STORAGE_SYSTEM_ALREADY_ABSENT, \
    STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING, STORAGE_SYSTEM_CREDENTIALS_MANDATORY

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


def create_ansible_mock(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class StorageSystemPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_create_new_storage_system(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = None
        mock_ov_instance.storage_systems.add.return_value = {"name": "name"}
        mock_ov_instance.storage_systems.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_SYSTEM_ADDED,
            ansible_facts=dict(storage_system={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM
        mock_ov_instance.storage_systems.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_SYSTEM_ALREADY_UPDATED,
            ansible_facts=dict(storage_system=DICT_DEFAULT_STORAGE_SYSTEM)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_not_update_when_data_is_equals_using_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        dict_by_name = yaml.load(YAML_STORAGE_SYSTEM_BY_NAME)["data"]

        mock_ov_instance.storage_systems.get_by_name.return_value = dict_by_name

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_SYSTEM_ALREADY_UPDATED,
            ansible_facts=dict(storage_system=dict_by_name.copy())
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_fail_with_missing_required_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = mock.Mock()
        mock_ansible_instance.params = {"state": "present",
                                        "config": "config",
                                        "data":
                                            {"field": "invalid"}}
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_fail_when_credentials_attribute_is_missing(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_name.return_value = []
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=STORAGE_SYSTEM_CREDENTIALS_MANDATORY
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DICT_DEFAULT_STORAGE_SYSTEM.copy()
        data_merged['credentials']['newIp_hostname'] = '10.10.10.10'
        # del data_merged['credentials']['password']

        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM
        mock_ov_instance.storage_systems.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_SYSTEM_UPDATED,
            ansible_facts=dict(storage_system=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = []
        mock_ov_instance.storage_systems.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageSystemModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class StorageSystemAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_remove_storage_system(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = DICT_DEFAULT_STORAGE_SYSTEM

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=STORAGE_SYSTEM_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_do_nothing_when_storage_system_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=STORAGE_SYSTEM_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = [DICT_DEFAULT_STORAGE_SYSTEM]
        mock_ov_instance.storage_systems.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_SYSTEM_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageSystemModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
