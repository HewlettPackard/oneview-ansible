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

from oneview_fc_network_facts import FcNetworkFactsModule
from test.utils import ParamsTestCase
from test.utils import ModuleContructorTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test FC Network"
)

PRESENT_NETWORKS = [{
    "name": "Test FC Network",
    "uri": "/rest/fc-networks/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class FcNetworkFactsSpec(unittest.TestCase, ModuleContructorTestCase, ParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, FcNetworkFactsModule)
        self.fc_networks = self.mock_ov_client.fc_networks
        ParamsTestCase.configure_client_mock(self, self.fc_networks)

    def test_should_get_all_fc_networks(self):
        self.fc_networks.get_all.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fc_networks=(PRESENT_NETWORKS))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.fc_networks.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcNetworkFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_fc_network_by_name(self):
        self.fc_networks.get_by.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fc_networks=(PRESENT_NETWORKS))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.fc_networks.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcNetworkFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
