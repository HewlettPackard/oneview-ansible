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

import unittest
from oneview_module_loader import StorageSystemFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Systems"
)

PARAMS_GET_BY_IP_HOSTNAME = dict(
    config='config.json',
    ip_hostname='10.0.0.0'
)

PARAMS_GET_HOST_TYPES = dict(
    config='config.json',
    options=["hostTypes"]

)

HOST_TYPES = [
    "Citrix Xen Server 5.x/6.x",
    "IBM VIO Server",
]

PARAMS_GET_POOL_BY_NAME = dict(
    config='config.json',
    name="Test Storage Systems",
    options=["storagePools"]
)

PARAMS_GET_POOL_BY_IP_HOSTNAME = dict(
    config='config.json',
    ip_hostname='10.0.0.0',
    options=["storagePools"]
)


class StorageSystemFactsSpec(unittest.TestCase,
                             FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageSystemFactsModule)
        self.storage_systems = self.mock_ov_client.storage_systems
        FactsParamsTestCase.configure_client_mock(self, self.storage_systems)

    def test_should_get_all_storage_system(self):
        self.storage_systems.get_all.return_value = {"name": "Storage System Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=({"name": "Storage System Name"}))
        )

    def test_should_get_storage_system_by_name(self):
        self.storage_systems.get_by_name.return_value = {"name": "Storage System Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=({"name": "Storage System Name"}))
        )

    def test_should_get_storage_system_by_ip_hostname(self):
        self.storage_systems.get_by_ip_hostname.return_value = {"ip_hostname": "10.0.0.0"}
        self.mock_ansible_module.params = PARAMS_GET_BY_IP_HOSTNAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=({"ip_hostname": "10.0.0.0"}))
        )

    def test_should_get_all_host_types(self):
        self.storage_systems.get_host_types.return_value = HOST_TYPES
        self.storage_systems.get_all.return_value = [{"name": "Storage System Name"}]
        self.mock_ansible_module.params = PARAMS_GET_HOST_TYPES

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_host_types=HOST_TYPES,
                storage_systems=[{"name": "Storage System Name"}])
        )

    def test_should_get_storage_pools_system_by_name(self):
        self.storage_systems.get_by_name.return_value = {"name": "Storage System Name", "uri": "uri"}
        self.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}
        self.mock_ansible_module.params = PARAMS_GET_POOL_BY_NAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_pools=({"name": "Storage Pool"}),
                storage_systems={"name": "Storage System Name", "uri": "uri"}
            )
        )

    def test_should_get_storage_system_pools_by_ip_hostname(self):
        self.storage_systems.get_by_ip_hostname.return_value = {"ip_hostname": "10.0.0.0", "uri": "uri"}
        self.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}
        self.mock_ansible_module.params = PARAMS_GET_POOL_BY_IP_HOSTNAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_pools=({"name": "Storage Pool"}),
                storage_systems={"ip_hostname": "10.0.0.0", "uri": "uri"}
            )
        )


if __name__ == '__main__':
    unittest.main()
