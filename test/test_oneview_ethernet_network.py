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
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_ethernet_network import EthernetNetworkModule
from oneview_ethernet_network import ETHERNET_NETWORK_CREATED, ETHERNET_NETWORK_ALREADY_EXIST, \
    ETHERNET_NETWORK_UPDATED, ETHERNET_NETWORK_DELETED, ETHERNET_NETWORK_ALREADY_ABSENT

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_ETHERNET_NAME = 'Test Ethernet Network'
RENAMED_ETHERNET = 'Renamed Ethernet Network'

DEFAULT_ENET_TEMPLATE = dict(
    name=DEFAULT_ETHERNET_NAME,
    vlanId=200,
    ethernetNetworkType="Tagged",
    purpose="General",
    smartLink=False,
    privateNetwork=False,
    connectionTemplateUri=None,
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_ETHERNET_NAME)
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_ETHERNET_NAME,
              newName=RENAMED_ETHERNET)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_ETHERNET_NAME,
              purpose='Management')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_ETHERNET_NAME)
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class EthernetNetworkPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_create_new_ethernet_network(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = []
        mock_ov_instance.ethernet_networks.create.return_value = DEFAULT_ENET_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ETHERNET_NETWORK_CREATED,
            ansible_facts=dict(ethernet_network=DEFAULT_ENET_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = [DEFAULT_ENET_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ETHERNET_NETWORK_ALREADY_EXIST,
            ansible_facts=dict(ethernet_network=DEFAULT_ENET_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_ENET_TEMPLATE.copy()
        data_merged['purpose'] = 'Management'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = [DEFAULT_ENET_TEMPLATE]
        mock_ov_instance.ethernet_networks.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ETHERNET_NETWORK_UPDATED,
            ansible_facts=dict(ethernet_network=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_rename_when_resource_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_ENET_TEMPLATE.copy()
        data_merged['name'] = RENAMED_ETHERNET
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = [DEFAULT_ENET_TEMPLATE]
        mock_ov_instance.ethernet_networks.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ov_instance.ethernet_networks.update.assert_called_once_with(data_merged)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_create_with_new_name_when_resource_not_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_ENET_TEMPLATE.copy()
        data_merged['name'] = RENAMED_ETHERNET
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = []
        mock_ov_instance.ethernet_networks.create.return_value = DEFAULT_ENET_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ov_instance.ethernet_networks.create.assert_called_once_with(PARAMS_TO_RENAME['data'])


class EthernetNetworkAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_remove_ethernet_network(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = [DEFAULT_ENET_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ETHERNET_NETWORK_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_do_nothing_when_ethernet_network_not_exist(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EthernetNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ETHERNET_NETWORK_ALREADY_ABSENT
        )


class EthernetNetworkErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_not_update_when_create_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = []
        mock_ov_instance.ethernet_networks.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EthernetNetworkModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_ethernet_network.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.ethernet_networks.get_by.return_value = [DEFAULT_ENET_TEMPLATE]
        mock_ov_instance.ethernet_networks.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EthernetNetworkModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
