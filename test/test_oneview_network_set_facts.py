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
from oneview_module_loader import NetworkSetFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_ALL_WITHOUT_ETHERNET = dict(
    config='config.json',
    name=None,
    options=['withoutEthernet']
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name='Network Set 1'
)

PARAMS_GET_BY_NAME_WITHOUT_ETHERNET = dict(
    config='config.json',
    name='Network Set 1',
    options=['withoutEthernet']
)


@pytest.mark.resource(TestNetworkSetFactsModule='network_sets')
class TestNetworkSetFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_network_sets(self):
        network_sets = [{
            "name": "Network Set 1",
            "networkUris": ['/rest/ethernet-networks/aaa-bbb-ccc']
        }, {
            "name": "Network Set 2",
            "networkUris": ['/rest/ethernet-networks/ddd-eee-fff', '/rest/ethernet-networks/ggg-hhh-fff']
        }]

        self.resource.get_all.return_value = network_sets
        self.mock_ansible_module.params = PARAMS_GET_ALL

        NetworkSetFactsModule().run()

        self.resource.get_all.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(network_sets=network_sets))

    def test_should_get_all_network_sets_without_ethernet(self):
        network_sets = [{
            "name": "Network Set 1",
            "networkUris": []
        }, {
            "name": "Network Set 2",
            "networkUris": []
        }]

        self.resource.get_all.return_value = network_sets
        self.mock_ansible_module.params = PARAMS_GET_ALL

        NetworkSetFactsModule().run()

        self.resource.get_all.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(network_sets=network_sets))

    def test_should_get_network_set_by_name(self):
        network_sets = [{
            "name": "Network Set 1",
            "networkUris": ['/rest/ethernet-networks/aaa-bbb-ccc']
        }]

        self.resource.get_by.return_value = network_sets
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        NetworkSetFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', 'Network Set 1')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(network_sets=network_sets))

    def test_should_get_network_set_by_name_without_ethernet(self):
        network_sets = [{
            "name": "Network Set 1",
            "networkUris": []
        }]

        self.resource.get_all_without_ethernet.return_value = network_sets
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITHOUT_ETHERNET

        NetworkSetFactsModule().run()

        expected_filter = "\"'name'='Network Set 1'\""
        self.resource.get_all_without_ethernet.assert_called_once_with(filter=expected_filter)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(network_sets=network_sets))


if __name__ == '__main__':
    pytest.main([__file__])
