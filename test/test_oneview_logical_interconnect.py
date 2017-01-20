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

from utils import ValidateEtagTestCase, ModuleContructorTestCase, PreloadedMocksBaseTestCase, ErrorHandlingTestCase

from oneview_logical_interconnect import (LogicalInterconnectModule,
                                          LOGICAL_INTERCONNECT_CONSISTENT,
                                          LOGICAL_INTERCONNECT_NOT_FOUND,
                                          LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED,
                                          LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED,
                                          LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED,
                                          LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED,
                                          LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND,
                                          LOGICAL_INTERCONNECT_SETTINGS_UPDATED,
                                          LOGICAL_INTERCONNECT_QOS_UPDATED,
                                          LOGICAL_INTERCONNECT_SNMP_UPDATED,
                                          LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED,
                                          LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED,
                                          LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED)

FAKE_MSG_ERROR = 'Fake message error'

LOGICAL_INTERCONNECT = {'uri': '/rest/logical-interconnects/id',
                        'ethernetSettings': {
                            'enableIgmpSnooping': True,
                            'macRefreshInterval': 10
                        },
                        'fcoeSettings': {
                            'fcoeMode': 'Unknown'
                        }}


class LogicalInterconnectModuleSpec(unittest.TestCase,
                                    ModuleContructorTestCase,
                                    ValidateEtagTestCase,
                                    ErrorHandlingTestCase):
    """
    Test the module constructor and shared functions
    ModuleContructorTestCase has common tests for class constructor and main function
    ValidateEtagTestCase has common tests for the validate_etag attribute, also provides the mocks used in this test
    case.
    """

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects
        ErrorHandlingTestCase.configure(self, method_to_fire=self.resource.get_by_name)

    def test_should_fail_when_option_is_invalid(self):
        self.mock_ansible_module.params = dict(
            config='config.json',
            state='ethernet_settings_updated',
            data=dict(name='Name of the Logical Interconnect')
        )

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED
        )


class LogicalInterconnectCompliantStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """
    PARAMS_COMPLIANCE = dict(
        config='config.json',
        state='compliant',
        data=dict(name='Name of the Logical Interconnect')
    )

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_return_to_a_consistent_state(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_compliance.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_COMPLIANCE

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_CONSISTENT,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_COMPLIANCE

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectEthernetSettingsUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_ethernet_settings(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_ETHERNET_SETTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_ethernet_with_merged_data(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_ETHERNET_SETTINGS

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
        expected_data = {'enableIgmpSnooping': True, 'macRefreshInterval': 7}
        self.resource.update_ethernet_settings.assert_called_once_with(expected_uri, expected_data)

    def test_should_do_nothing_when_no_changes(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_ETHERNET_SETTINGS_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_ETHERNET_SETTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectInternalNetworksUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

    PARAMS_INTERNAL_NETWORKS = dict(
        config='config.json',
        state='internal_networks_updated',
        data=dict(name='Name of the Logical Interconnect',
                  internalNetworks=[dict(name='Network Name 1'), dict(name='Network Name 2'), dict(uri='/path/3')])
    )

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_internal_networks(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        self.resource.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_internal_networks_with_given_list(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        self.resource.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        expected_uri = '/rest/logical-interconnects/id'
        expected_list = ['/path/1', '/path/2', '/path/3']
        self.resource.update_internal_networks.assert_called_once_with(expected_uri,
                                                                       expected_list)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    def test_should_fail_when_ethernet_network_not_found(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], []]
        self.resource.update_internal_networks.return_value = {}

        self.mock_ansible_module.params = self.PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND + "Network Name 2"
        )


class LogicalInterconnectSettingsUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_settings(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_SETTTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_ethernet_settings(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_SETTTINGS_ETHERNET

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
        self.resource.update_settings.assert_called_once_with(expected_uri, expected_settings)

    def test_should_update_fcoe_settings(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_SETTTINGS_FCOE

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
        self.resource.update_settings.assert_called_once_with(expected_uri, expected_settings)

    def test_update_settings_should_do_nothing_when_data_was_not_modified(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        params = self.PARAMS_SETTTINGS.copy()
        params['data']['ethernetSettings']['macRefreshInterval'] = 10
        params['data']['fcoeSettings']['fcoeMode'] = 'Unknown'

        self.mock_ansible_module.params = self.PARAMS_SETTTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_SETTTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )

    def test_should_fail_when_settings_are_invalid(self):
        self.mock_ansible_module.params = dict(
            config='config.json',
            state='settings_updated',
            data=dict(name='Name of the Logical Interconnect')
        )

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED
        )


class LogicalInterconnectForwardingInformationBaseGeneratedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_generate_interconnect_fib(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.create_forwarding_information_base.return_value = self.response_body

        self.mock_ansible_module.params = self.PARAMS_GENERATE_FIB

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=self.status,
            ansible_facts=dict(interconnect_fib=self.response_body)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_GENERATE_FIB

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectQosAggregatedConfigurationUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_qos_aggreg_config(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_qos_aggregated_configuration.return_value = self.qos_config
        self.resource.update_qos_aggregated_configuration.return_value = self.qos_config

        self.mock_ansible_module.params = self.PARAMS_QOS_AGGREG_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_QOS_UPDATED,
            ansible_facts=dict(qos_configuration=self.qos_config)
        )

    def test_should_do_nothing_when_no_changes(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_qos_aggregated_configuration.return_value = self.qos_config

        self.mock_ansible_module.params = self.PARAMS_QOS_AGGREG_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_QOS_AGGREG_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectSnmpConfigurationUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_snmp_configuration(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_snmp_configuration.return_value = self.snmp_config
        self.resource.update_snmp_configuration.return_value = self.snmp_config

        self.mock_ansible_module.params = self.PARAMS_SNMP_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_SNMP_UPDATED,
            ansible_facts=dict(snmp_configuration=self.snmp_config)
        )

    def test_should_do_nothing_when_no_changes(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_snmp_configuration.return_value = self.snmp_config
        self.resource.update_snmp_configuration.return_value = self.snmp_config

        self.mock_ansible_module.params = self.PARAMS_SNMP_CONFIG_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_SNMP_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectPortMonitorUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

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

    def test_should_update_port_monitor_configuration(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_port_monitor.return_value = self.monitor_config
        self.resource.update_port_monitor.return_value = self.monitor_config

        self.mock_ansible_module.params = self.PARAMS_PORT_MONITOR_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED,
            ansible_facts=dict(port_monitor=self.monitor_config)
        )

    def test_should_do_nothing_when_no_changes(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.get_port_monitor.return_value = self.monitor_config
        self.resource.update_port_monitor.return_value = self.monitor_config

        self.mock_ansible_module.params = self.PARAMS_PORT_MONITOR_CONFIGURATION_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_PORT_MONITOR_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectConfigurationUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

    PARAMS_CONFIGURATION = dict(
        config='config.json',
        state='configuration_updated',
        data=dict(name='Name of the Logical Interconnect', enabled=True)
    )

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_update_configuration(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.update_configuration.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = self.PARAMS_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


class LogicalInterconnectFirmwareUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    """
    PreloadedMocksBaseTestCase provides the mocks used in this test case.
    """

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

    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectModule)
        self.resource = self.mock_ov_client.logical_interconnects

    def test_should_install_firmware(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = self.PARAMS_FIRMWARE_WITH_SPP_NAME

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED,
            ansible_facts=dict(li_firmware=self.response)
        )

    def test_should_install_firmware_when_spp_name_set(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = self.PARAMS_FIRMWARE_WITH_SPP_NAME

        LogicalInterconnectModule().run()

        self.resource.install_firmware.assert_called_once_with(self.expected_data, mock.ANY)

    def test_should_update_firmware_when_spp_uri_set(self):
        self.resource.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = self.PARAMS_FIRMWARE_WITH_SPP_URI

        LogicalInterconnectModule().run()

        self.resource.install_firmware.assert_called_once_with(self.expected_data, mock.ANY)

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_FIRMWARE_WITH_SPP_URI

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LOGICAL_INTERCONNECT_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
