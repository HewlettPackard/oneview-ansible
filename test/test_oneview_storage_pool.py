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
from oneview_storage_pool import StoragePoolModule, STORAGE_POOL_ADDED, STORAGE_POOL_ALREADY_ADDED, \
    STORAGE_POOL_DELETED, STORAGE_POOL_ALREADY_ABSENT, STORAGE_POOL_MANDATORY_FIELD_MISSING

FAKE_MSG_ERROR = 'Fake message error'

YAML_STORAGE_POOL = """
        config: "{{ config }}"
        state: present
        data:
           storageSystemUri: "/rest/storage-systems/TXQ1010307"
           poolName: "FST_CPG2"
          """

YAML_STORAGE_POOL_MISSING_KEY = """
    config: "{{ config }}"
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
      """

YAML_STORAGE_POOL_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
           poolName: "FST_CPG2"
        """

DICT_DEFAULT_STORAGE_POOL = yaml.load(YAML_STORAGE_POOL)["data"]


def create_ansible_mock(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class StoragePoolPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_create_new_storage_pool(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = []
        mock_ov_instance.storage_pools.add.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL)
        mock_ansible_module.return_value = mock_ansible_instance

        StoragePoolModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_POOL_ADDED,
            ansible_facts=dict(storage_pool={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_do_nothing_when_storage_pool_already_exist(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL)
        mock_ansible_module.return_value = mock_ansible_instance

        StoragePoolModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_POOL_ALREADY_ADDED,
            ansible_facts=dict(storage_pool=DICT_DEFAULT_STORAGE_POOL)
        )


class StoragePoolAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_remove_storage_pool(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StoragePoolModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=STORAGE_POOL_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_do_nothing_when_storage_pool_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StoragePoolModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=STORAGE_POOL_ALREADY_ABSENT
        )


class StoragePoolErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = []
        mock_ov_instance.storage_pools.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StoragePoolModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_fail_when_remove_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        mock_ov_instance.storage_pools.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StoragePoolModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_pool.AnsibleModule')
    def test_should_fail_when_key_is_missing(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_STORAGE_POOL_MISSING_KEY)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StoragePoolModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=STORAGE_POOL_MANDATORY_FIELD_MISSING
        )


if __name__ == '__main__':
    unittest.main()
