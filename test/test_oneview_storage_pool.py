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
import yaml

from oneview_storage_pool import StoragePoolModule, STORAGE_POOL_ADDED, STORAGE_POOL_ALREADY_ADDED, \
    STORAGE_POOL_DELETED, STORAGE_POOL_ALREADY_ABSENT, STORAGE_POOL_MANDATORY_FIELD_MISSING
from utils import ModuleContructorTestCase
from utils import ErrorHandlingTestCase

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


class StoragePoolModuleSpec(unittest.TestCase,
                            ModuleContructorTestCase,
                            ErrorHandlingTestCase):
    def setUp(self):
        self.configure_mocks(self, StoragePoolModule)
        ErrorHandlingTestCase.configure(self, ansible_params=yaml.load(YAML_STORAGE_POOL),
                                        method_to_fire=self.mock_ov_client.storage_pools.get_by)

    def test_should_create_new_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ov_client.storage_pools.add.return_value = {"name": "name"}
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_POOL_ADDED,
            ansible_facts=dict(storage_pool={"name": "name"})
        )

    def test_should_do_nothing_when_storage_pool_already_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_POOL_ALREADY_ADDED,
            ansible_facts=dict(storage_pool=DICT_DEFAULT_STORAGE_POOL)
        )

    def test_should_remove_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=STORAGE_POOL_DELETED
        )

    def test_should_do_nothing_when_storage_pool_not_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=STORAGE_POOL_ALREADY_ABSENT
        )

    def test_should_fail_when_key_is_missing(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_MISSING_KEY)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=STORAGE_POOL_MANDATORY_FIELD_MISSING
        )


if __name__ == '__main__':
    unittest.main()
