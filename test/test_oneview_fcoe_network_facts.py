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

from oneview_fcoe_network_facts import FcoeNetworkFactsModule
from test.utils import ParamsTestCase
from test.utils import ModuleContructorTestCase

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


class FcoeNetworkFactsSpec(unittest.TestCase, ModuleContructorTestCase, ParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, FcoeNetworkFactsModule)
        self.fcoe_networks = self.mock_ov_client.fcoe_networks
        ParamsTestCase.configure_client_mock(self, self.fcoe_networks)

    def test_should_get_all_fcoe_network(self):
        self.fcoe_networks.get_all.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=(PRESENT_NETWORKS))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.fcoe_networks.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_fcoe_network_by_name(self):
        self.fcoe_networks.get_by.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=(PRESENT_NETWORKS))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.fcoe_networks.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
