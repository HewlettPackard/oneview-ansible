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
from oneview_module_loader import StoragePoolFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Pools"
)


class StoragePoolFactsSpec(unittest.TestCase,
                           FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StoragePoolFactsModule)
        self.storage_pools = self.mock_ov_client.storage_pools
        FactsParamsTestCase.configure_client_mock(self, self.storage_pools)

    def test_should_get_all_storage_pool(self):
        self.storage_pools.get_all.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=({"name": "Storage Pool Name"}))
        )

    def test_should_get_storage_pool_by_name(self):
        self.storage_pools.get_by.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=({"name": "Storage Pool Name"}))
        )


if __name__ == '__main__':
    unittest.main()
