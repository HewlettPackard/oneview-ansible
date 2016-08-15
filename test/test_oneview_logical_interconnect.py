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

from utils import create_ansible_mock
from hpOneView.oneview_client import OneViewClient
from oneview_logical_interconnect import LogicalInterconnectModule
from oneview_logical_interconnect import LOGICAL_INTERCONNECT_CONSISTENT, LOGICAL_INTERCONNECT_NOT_FOUND, \
    LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED, LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED, \
    LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED, LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND, \
    LOGICAL_INTERCONNECT_SETTINGS_UPDATED, LOGICAL_INTERCONNECT_QOS_UPDATED, LOGICAL_INTERCONNECT_SNMP_UPDATED, \
    LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED, LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED, \
    LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED

FAKE_MSG_ERROR = 'Fake message error'

LOGICAL_INTERCONNECT = {'uri': '/rest/logical-interconnects/id',
                        'ethernetSettings': {
                            'enableIgmpSnooping': True,
                            'macRefreshInterval': 10
                        },
                        'fcoeSettings': {
                            'fcoeMode': 'Unknown'
                        }}


class LogicalInterconnectCompliantStateSpec(unittest.TestCase):
    PARAMS_COMPLIANCE = dict(
        config='config.json',
        state='compliant',
        data=dict(name='Name of the Logical Interconnect')
    )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_return_to_a_consistent_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_compliance.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_COMPLIANCE)
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

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_COMPLIANCE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_compliance_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_compliance.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_COMPLIANCE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectEthernetSettingsUpdatedStateSpec(unittest.TestCase):
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

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_ethernet_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_ETHERNET_SETTINGS)
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_ETHERNET_SETTINGS_NO_CHANGES)
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

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_ethernet_raises_exception(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_ethernet_settings.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_ETHERNET_SETTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectInternalNetworksUpdatedStateSpec(unittest.TestCase):
    PARAMS_INTERNAL_NETWORKS = dict(
        config='config.json',
        state='internal_networks_updated',
        data=dict(name='Name of the Logical Interconnect',
                  internalNetworks=[dict(name='Network Name 1'), dict(name='Network Name 2'), dict(uri='/path/3')])
    )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_internal_networks(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        mock_ov_instance.logical_interconnects.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_INTERNAL_NETWORKS)
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
        expected_list = ['/path/1', '/path/2', '/path/3']
        mock_ov_instance.logical_interconnects.update_internal_networks.assert_called_once_with(expected_uri,
                                                                                                expected_list)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_INTERNAL_NETWORKS)
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND + "Network Name 2"
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_INTERNAL_NETWORKS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectSettingsUpdatedStateSpec(unittest.TestCase):
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

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_settings(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_settings.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SETTTINGS)
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SETTTINGS_ETHERNET)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
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
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SETTTINGS_FCOE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
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

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SETTTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_settings_raises_exception(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_settings.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SETTTINGS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectForwardingInformationBaseGeneratedStateSpec(unittest.TestCase):
    PARAMS_GENERATE_FIB = dict(
        config='config.json',
        state='forwarding_information_base_generated',
        data=dict(name='Name of the Logical Interconnect')
    )
    status = "Forwarding information base dump for logical interconnect yielded no results and ended with warnings."
    response_body = {
        'status': status,
        'state': 'Warning'
    }

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_generate_interconnect_fib(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.create_forwarding_information_base.return_value = self.response_body

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_GENERATE_FIB)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=self.status,
            ansible_facts=dict(interconnect_fib=self.response_body)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_GENERATE_FIB)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_generate_fib_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.create_forwarding_information_base.side_effect = \
            Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_GENERATE_FIB)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectQosAggregatedConfigurationUpdatedStateSpec(unittest.TestCase):
    PARAMS_QOS_AGGREG_CONFIG = dict(
        config='config.json',
        state='qos_aggregated_configuration_updated',
        data=dict(name='Name of the Logical Interconnect',
                  qosConfiguration=dict(activeQosConfig=dict(category='qos-aggregated-configuration',
                                        configType='Passthrough',
                                        downlinkClassificationType=None,
                                        uplinkClassificationType=None,
                                        qosTrafficClassifiers=[],
                                        type='QosConfiguration')))
    )
    PARAMS_QOS_AGGREG_NO_CHANGES = dict(
        config='config.json',
        state='qos_aggregated_configuration_updated',
        data=dict(name='Name of the Logical Interconnect',
                  qosConfiguration=dict(activeQosConfig=dict(category='qos-aggregated-configuration',
                                        configType='CustomNoFCoE',
                                        downlinkClassificationType='DSCP',
                                        uplinkClassificationType=None,
                                        qosTrafficClassifiers=['a', 'list', 'with', 'classifiers'],
                                        type='QosConfiguration')))
    )
    qos_config = {
        'inactiveFCoEQosConfig': None,
        'inactiveNonFCoEQosConfig': None,
        'activeQosConfig': {
            'category': 'qos-aggregated-configuration',
            'configType': 'CustomNoFCoE',
            'downlinkClassificationType': 'DSCP',
            'uplinkClassificationType': None,
            'qosTrafficClassifiers': ['a', 'list', 'with', 'classifiers'],
            'type': 'QosConfiguration'
        }
    }

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_qos_aggreg_config(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = self.qos_config
        mock_ov_instance.logical_interconnects.update_qos_aggregated_configuration.return_value = self.qos_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_QOS_AGGREG_CONFIG)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_QOS_UPDATED,
            ansible_facts=dict(qos_configuration=self.qos_config)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_do_nothing_when_no_changes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = self.qos_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_QOS_AGGREG_NO_CHANGES)
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

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_QOS_AGGREG_CONFIG)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

        @mock.patch.object(OneViewClient, 'from_json_file')
        @mock.patch('oneview_logical_interconnect.AnsibleModule')
        def test_should_fail_when_update_qos_raises_exception(self, mock_ansible_module,
                                                              mock_ov_client_from_json_file):
            mock_ov_instance = mock.Mock()
            mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
            mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = self.qos_config
            mock_ov_instance.logical_interconnects.update_qos_aggregated_configuration.side_effect = \
                Exception(FAKE_MSG_ERROR)

            mock_ov_client_from_json_file.return_value = mock_ov_instance
            mock_ansible_instance = create_ansible_mock(self.PARAMS_QOS_AGGREG_CONFIG)
            mock_ansible_module.return_value = mock_ansible_instance

            self.assertRaises(Exception, LogicalInterconnectModule().run())

            mock_ansible_instance.fail_json.assert_called_once_with(
                msg=FAKE_MSG_ERROR
            )


class LogicalInterconnectSnmpConfigurationUpdatedStateSpec(unittest.TestCase):
    PARAMS_SNMP_CONFIG = dict(
        config='config.json',
        state='snmp_configuration_updated',
        data=dict(name='Name of the Logical Interconnect',
                  snmpConfiguration=dict(enabled=True))
    )
    PARAMS_SNMP_CONFIG_NO_CHANGES = dict(
        config='config.json',
        state='snmp_configuration_updated',
        data=dict(name='Name of the Logical Interconnect',
                  snmpConfiguration=dict(enabled=False))
    )
    snmp_config = {'enabled': False}

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_snmp_configuration(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = self.snmp_config
        mock_ov_instance.logical_interconnects.update_snmp_configuration.return_value = self.snmp_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SNMP_CONFIG)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_SNMP_UPDATED,
            ansible_facts=dict(snmp_configuration=self.snmp_config)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_do_nothing_when_no_changes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = self.snmp_config
        mock_ov_instance.logical_interconnects.update_snmp_configuration.return_value = self.snmp_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SNMP_CONFIG_NO_CHANGES)
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

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SNMP_CONFIG)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_snmp_raises_exception(self, mock_ansible_module,
                                                           mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = self.snmp_config
        mock_ov_instance.logical_interconnects.update_snmp_configuration.side_effect = \
            Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_SNMP_CONFIG)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectPortMonitorUpdatedStateSpec(unittest.TestCase):
    PARAMS_PORT_MONITOR_CONFIGURATION = dict(
        config='config.json',
        state='port_monitor_updated',
        data=dict(name='Name of the Logical Interconnect',
                  portMonitor=dict(enablePortMonitor=False))
    )
    PARAMS_PORT_MONITOR_CONFIGURATION_NO_CHANGES = dict(
        config='config.json',
        state='port_monitor_updated',
        data=dict(name='Name of the Logical Interconnect',
                  portMonitor=dict(enablePortMonitor=True))
    )
    monitor_config = {'enablePortMonitor': True}

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_port_monitor_configuration(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = self.monitor_config
        mock_ov_instance.logical_interconnects.update_port_monitor.return_value = self.monitor_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_PORT_MONITOR_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED,
            ansible_facts=dict(port_monitor=self.monitor_config)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_do_nothing_when_no_changes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = self.monitor_config
        mock_ov_instance.logical_interconnects.update_port_monitor.return_value = self.monitor_config

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_PORT_MONITOR_CONFIGURATION_NO_CHANGES)
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

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_PORT_MONITOR_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_port_monitor_raises_exception(self, mock_ansible_module,
                                                                   mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = self.monitor_config
        mock_ov_instance.logical_interconnects.update_port_monitor.side_effect = \
            Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_PORT_MONITOR_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectConfigurationUpdatedStateSpec(unittest.TestCase):
    PARAMS_CONFIGURATION = dict(
        config='config.json',
        state='configuration_updated',
        data=dict(name='Name of the Logical Interconnect', enabled=True)
    )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_configuration(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_configuration.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_update_configuration_raises_exception(self, mock_ansible_module,
                                                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.update_configuration.side_effect = \
            Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_CONFIGURATION)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class LogicalInterconnectFirmwareUpdatedStateSpec(unittest.TestCase):
    PARAMS_FIRMWARE_WITH_SPP_NAME = dict(
        config='config.json',
        state='firmware_installed',
        data=dict(name='Name of the Logical Interconnect',
                  firmware=dict(command='Update',
                                spp='filename-of-the-firmware-to-install')))
    PARAMS_FIRMWARE_WITH_SPP_URI = dict(
        config='config.json',
        state='firmware_installed',
        data=dict(name='Name of the Logical Interconnect',
                  firmware=dict(command='Update',
                                sppUri='/rest/firmware-drivers/filename-of-the-firmware-to-install')))
    expected_data = {
        'command': 'Update',
        'sppUri': '/rest/firmware-drivers/filename-of-the-firmware-to-install'
    }
    response = {
        "response": "data"
    }

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_install_firmware(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.install_firmware.return_value = self.response

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_FIRMWARE_WITH_SPP_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED,
            ansible_facts=dict(li_firmware=self.response)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_install_firmware_when_spp_name_set(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.install_firmware.return_value = self.response

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_FIRMWARE_WITH_SPP_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ov_instance.logical_interconnects.install_firmware.assert_called_once_with(self.expected_data, mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_update_firmware_when_spp_uri_set(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.install_firmware.return_value = self.response

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_FIRMWARE_WITH_SPP_URI)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ov_instance.logical_interconnects.install_firmware.assert_called_once_with(self.expected_data, mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_FIRMWARE_WITH_SPP_URI)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect.AnsibleModule')
    def test_should_fail_when_install_firmware_raises_exception(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.install_firmware.side_effect = \
            Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(self.PARAMS_FIRMWARE_WITH_SPP_URI)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
