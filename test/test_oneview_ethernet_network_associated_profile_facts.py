##
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

from hpOneView.oneview_client import OneViewClient
from oneview_ethernet_network_associated_profile_facts import EthernetNetworkAssociatedProfileModule
from oneview_ethernet_network_associated_profile_facts import ETHERNET_NETWORK_NOT_FOUND

ERROR_MSG = 'Fake message error'

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Ethernet Network"
)

PRESENT_ENETS = [{
    "name": "Test Ethernet Network",
    "uri": "/rest/ethernet-networks/c7084d14-524d-40df-b6e5-b466a8110986"
}]

ASSOCIATED_PROFILES = [
    "/rest/server-profiles/83e2e117-59dc-4e33-9f24-462af951cbbe",
    "/rest/server-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea4d"
]


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class EthernetNetworkAssociatedProfileFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network_associated_profile_facts.AnsibleModule')
    def test_should_get_associated_profiles(self, mock_ansible_module,
                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = PRESENT_ENETS
        mock_ov_instance.ethernet_networks.get_associated_profiles.return_value = ASSOCIATED_PROFILES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkAssociatedProfileModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enet_associated_profiles=ASSOCIATED_PROFILES)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network_associated_profile_facts.AnsibleModule')
    def test_should_fail_when_get_associated_profiles_raises_error(self, mock_ansible_module,
                                                                   mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = PRESENT_ENETS
        mock_ov_instance.ethernet_networks.get_associated_profiles.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkAssociatedProfileModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network_associated_profile_facts.AnsibleModule')
    def test_should_fail_when_get_enet_by_name_raises_error(self,
                                                            mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.side_effect = Exception(ERROR_MSG)
        mock_ov_instance.ethernet_networks.get_associated_profiles.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkAssociatedProfileModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network_associated_profile_facts.AnsibleModule')
    def test_should_do_nothing_when_enet_not_exist(self,
                                                   mock_ansible_module,
                                                   mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = []
        mock_ov_instance.ethernet_networks.get_associated_profiles.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkAssociatedProfileModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enet_associated_profiles=None),
            msg=ETHERNET_NETWORK_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
