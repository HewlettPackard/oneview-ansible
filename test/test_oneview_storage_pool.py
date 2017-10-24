#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import yaml

from ansible.compat.tests import unittest, mock
from oneview_module_loader import StoragePoolModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

YAML_STORAGE_POOL = """
        config: "{{ config }}"
        state: present
        data:
           storageSystemUri: "/rest/storage-systems/TXQ1010307"
           poolName: "FST_CPG2"
          """

YAML_STORAGE_POOL_500 = """
        config: "{{ config }}"
        state: present
        data:
           storageSystemUri: "/rest/storage-systems/TXQ1010307"
           name: "FST_CPG2"
           isManaged: True
          """

YAML_STORAGE_POOL_ABSENT_500 = """
        config: "{{ config }}"
        state: absent
        data:
           storageSystemUri: "/rest/storage-systems/TXQ1010307"
           name: "FST_CPG2"
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
DICT_DEFAULT_STORAGE_POOL_500 = yaml.load(YAML_STORAGE_POOL_500)["data"]


class StoragePoolModuleSpec(unittest.TestCase,
                            OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, StoragePoolModule)
        self.mock_ov_client.api_version = 300

    def test_should_create_new_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ov_client.storage_pools.add.return_value = {"name": "name"}
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StoragePoolModule.MSG_CREATED,
            ansible_facts=dict(storage_pool={"name": "name"})
        )

    def test_should_do_nothing_when_storage_pool_already_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(storage_pool=DICT_DEFAULT_STORAGE_POOL)
        )

    def test_should_remove_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StoragePoolModule.MSG_DELETED
        )

    def test_should_do_nothing_when_storage_pool_not_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_key_is_missing_api300(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_MISSING_KEY)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StoragePoolModule.MSG_MANDATORY_FIELD_MISSING)

    def test_should_fail_when_key_is_missing_api500(self):
        self.mock_ov_client.api_version = 500
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_MISSING_KEY)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StoragePoolModule.MSG_MANDATORY_FIELD_MISSING)

    def test_update_when_storage_pool_already_exists_and_is_different_api500(self):
        self.mock_ov_client.api_version = 500
        update_params = yaml.load(YAML_STORAGE_POOL_500)
        update_params['data']['isManaged'] = False
        self.mock_ansible_module.params = update_params

        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL_500]
        self.mock_ov_client.storage_pools.update.return_value = update_params

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StoragePoolModule.MSG_UPDATED,
            ansible_facts=dict(storage_pool=update_params)
        )

    def test_update_should_do_nothing_when_storage_pool_already_exists_and_is_equal_api500(self):
        self.mock_ov_client.api_version = 500
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_500)

        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL_500]

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(storage_pool=DICT_DEFAULT_STORAGE_POOL_500)
        )

    def test_update_should_do_nothing_when_storage_pool_is_absent_and_do_not_exists_api500(self):
        self.mock_ov_client.api_version = 500
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT_500)

        self.mock_ov_client.storage_pools.get_by.return_value = []

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_ABSENT,
            ansible_facts=dict(storage_pool=None)
        )

    def test_should_fail_when_present_but_storage_pool_is_absent_api500(self):
        self.mock_ov_client.api_version = 500
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_500)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StoragePoolModule.MSG_RESOURCE_NOT_FOUND)

    def test_should_fail_when_absent_but_storage_pool_exists_api500(self):
        self.mock_ov_client.api_version = 500
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL_500]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT_500)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StoragePoolModule.MSG_RESOURCE_FOUND)


if __name__ == '__main__':
    unittest.main()
