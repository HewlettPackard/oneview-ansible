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
from oneview_logical_interconnect import LogicalInterconnectModule
from oneview_logical_interconnect import LOGICAL_INTERCONNECT_CONSISTENT, LOGICAL_INTERCONNECT_NOT_FOUND, \
    LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED, LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED, \
    LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED, LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND, \
    LOGICAL_INTERCONNECT_SETTINGS_UPDATED

FAKE_MSG_ERROR = 'Fake message error'

LOGICAL_INTERCONNECT = {'uri': '/rest/logical-interconnect/id',
                        'ethernetSettings': {
                            'enableIgmpSnooping': True,
                            'macRefreshInterval': 10
                        },
                        'fcoeSettings': {
                            'fcoeMode': 'Unknown'
                        }}


PARAMS_COMPLIANCE = dict(
    config='config.json',
    state='compliant',
    data=dict(name='Name of the Logical Interconnect')
)

PARAMS_ETHERNET_SETTINGS = dict(
    config='config.json',
    state='ethernet_settings_updated',
    data=dict(name='Name of the Logical Interconnect', ethernetSettings=dict(macRefreshInterval=7))
)

PARAMS_ETHERNET_SETTINGS_NO_CHANGES = dict(
    config='config.json',
    state='ethernet_settings_updated',
    data=dict(name='Name of the Logical Interconnect', ethernetSettings=dict(macRefreshInterval=10))
)

PARAMS_INTERNAL_NETWORKS = dict(
    config='config.json',
    state='internal_networks_updated',
    data=dict(name='Name of the Logical Interconnect',
              internalNetworks=[dict(name='Network Name 1'), dict(name='Network Name 2'), dict(uri='/path/3')])
)

PARAMS_SETTTINGS = dict(
    config='config.json',
    state='settings_updated',
    data=dict(name='Name of the Logical Interconnect',
              ethernetSettings=dict(macRefreshInterval=12),
              fcoeSettings=dict(fcoeMode='NotApplicable'))
)

PARAMS_SETTTINGS_ETHERNET = dict(
    config='config.json',
    state='settings_updated',
    data=dict(name='Name of the Logical Interconnect',
              ethernetSettings=dict(macRefreshInterval=12))
)

PARAMS_SETTTINGS_FCOE = dict(
    config='config.json',
    state='settings_updated',
    data=dict(name='Name of the Logical Interconnect',
              fcoeSettings=dict(fcoeMode='NotApplicable'))
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class LogicalInterconnectCompliantStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_return_to_a_consistent_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_compliance.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_COMPLIANCE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_CONSISTENT,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None
        mock_ov_instance.logical_interconnects.update_compliance.return_value = {}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_COMPLIANCE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectEthernetSettingsUpdatedStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_ethernet_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_ethernet_with_merged_data(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnect/id'
        expected_data = {'enableIgmpSnooping': True, 'macRefreshInterval': 7}
        mock_ov_instance.logical_interconnects.update_ethernet_settings.assert_called_once_with(expected_uri,
                                                                                                expected_data)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_do_nothing_when_no_changes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_ETHERNET_SETTINGS_NO_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None
        mock_ov_instance.logical_interconnects.update_ethernet_settings.return_value = {}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectInternalNetworksUpdatedStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_internal_networks(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        mock_ov_instance.logical_interconnects.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_internal_networks_with_given_list(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        mock_ov_instance.logical_interconnects.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnect/id'
        expected_list = ['/path/1', '/path/2', '/path/3']
        mock_ov_instance.logical_interconnects.update_internal_networks.assert_called_once_with(expected_uri,
                                                                                                expected_list)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None
        mock_ov_instance.logical_interconnects.update_internal_networks.return_value = {}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_ethernet_network_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], []]
        mock_ov_instance.logical_interconnects.update_internal_networks.return_value = {}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND + "Network Name 2"
        )


class LogicalInterconnectSettingsUpdatedStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_SETTTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_ethernet_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_SETTTINGS_ETHERNET)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnect/id'
        expected_settings = {
            'ethernetSettings': {
                'enableIgmpSnooping': True,
                'macRefreshInterval': 12
            },
            'fcoeSettings': {
                'fcoeMode': 'Unknown'
            }
        }
        mock_ov_instance.logical_interconnects.update_settings.assert_called_once_with(expected_uri, expected_settings)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_fcoe_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_SETTTINGS_FCOE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnect/id'
        expected_settings = {
            'ethernetSettings': {
                'enableIgmpSnooping': True,
                'macRefreshInterval': 10
            },
            'fcoeSettings': {
                'fcoeMode': 'NotApplicable'
            }
        }
        mock_ov_instance.logical_interconnects.update_settings.assert_called_once_with(expected_uri, expected_settings)


class LogicalInterconnectHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_compliance_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_compliance.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_COMPLIANCE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_ethernet_raises_exception(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_internal_networks_raises_exception(self, mock_ansible_module,
                                                                        mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        mock_ov_instance.logical_interconnects.update_internal_networks.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
