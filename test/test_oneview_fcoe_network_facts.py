#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import FcoeNetworkFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test FCoE Networks"
)

PRESENT_NETWORKS = [{
    "name": "Test FCoE Networks",
    "uri": "/rest/fcoe-networks/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


@pytest.mark.resource(TestFcoeNetworkFactsModule='fcoe_networks')
class TestFcoeNetworkFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_fcoe_network(self):
        self.resource.get_all.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=PRESENT_NETWORKS)
        )

    def test_should_get_fcoe_network_by_name(self):
        self.resource.get_by.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=PRESENT_NETWORKS)
        )


if __name__ == '__main__':
    pytest.main([__file__])
