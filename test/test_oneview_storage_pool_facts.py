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

from hpe_test_utils import OneViewBaseFactsTest
from oneview_module_loader import StoragePoolFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Pools"
)

PARAMS_GET_REACHABLE_STORAGE_POOLS = dict(
    config='config.json',
    name="Test Storage Pools",
    params={},
    options=[{"reachableStoragePools": {
        'networks': ['rest/fake/network'],
        'scope_uris': '/rest/fake/uri',
        'scope_exclusions': ['/rest/storage-pool/fake']}
    }]
)


@pytest.mark.resource(TestStoragePoolFactsModule='storage_pools')
class TestStoragePoolFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_storage_pool(self):
        self.resource.get_all.return_value = [{"name": "Storage Pool Name"}]
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=[{"name": "Storage Pool Name"}])
        )

    def test_should_get_storage_pool_by_name(self):
        self.resource.get_by.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=({"name": "Storage Pool Name"}))
        )

    def test_should_get_reachable_storage_pools(self):
        self.mock_ov_client.api_version = 600
        self.resource.get_reachable_storage_pools.return_value = [{'reachable': 'test'}]
        self.resource.get_by.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_REACHABLE_STORAGE_POOLS

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_pools_reachable_storage_pools=[{'reachable': 'test'}],
                storage_pools={"name": "Storage Pool Name"})
        )


if __name__ == '__main__':
    pytest.main([__file__])
