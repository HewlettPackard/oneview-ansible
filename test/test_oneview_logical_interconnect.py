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

import mock
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import LogicalInterconnectModule

FAKE_MSG_ERROR = 'Fake message error'

LOGICAL_INTERCONNECT = {'uri': '/rest/logical-interconnects/id',
                        'ethernetSettings': {
                            'enableIgmpSnooping': True,
                            'macRefreshInterval': 10
                        },
                        'fcoeSettings': {
                            'fcoeMode': 'Unknown'
                        },
                        'telemetryConfiguration': {
                            'category': 'telemetry-configurations',
                            'enableTelemetry': True,
                            'modified': None,
                            'name': 'name-670923271-1482252496500',
                            'sampleCount': 10,
                            'sampleInterval': 250,
                            'uri': '/rest/logical-interconnects/123/telemetry-configurations/abc'
                        },
                        'scopeUris': 'rest/scopes/test'
                        }

TELEMETRY_CONFIG = dict(
    sampleCount=12,
    enableTelemetry=True,
    sampleInterval=300
)

TELEMETRY_PARAMS_CONFIGURATION = dict(
    config='config.json',
    state='telemetry_configuration_updated',
    data=dict(name='Test', telemetryConfiguration=TELEMETRY_CONFIG))

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

PARAMS_SETTINGS = dict(
    config='config.json',
    state='settings_updated',
    data=dict(name='Name of the Logical Interconnect',
              ethernetSettings=dict(macRefreshInterval=12),
              fcoeSettings=dict(fcoeMode='NotApplicable'))
)

PARAMS_SETTINGS_ETHERNET = dict(
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

PARAMS_GENERATE_FIB = dict(
    config='config.json',
    state='forwarding_information_base_generated',
    data=dict(name='Name of the Logical Interconnect')
)

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

PARAMS_CONFIGURATION = dict(
    config='config.json',
    state='configuration_updated',
    data=dict(name='Name of the Logical Interconnect', enabled=True)
)

PARAMS_FIRMWARE_WITH_SPP_NAME = dict(
    config='config.json',
    state='firmware_installed',
    data=dict(name='Name of the Logical Interconnect',
              firmware=dict(command='Update',
                            spp='filename-of-the-firmware-to-install')))

PARAMS_SCOPES = dict(
    config='config.json',
    state='scopes_updated',
    data=dict(name='Name of the Logical Interconnect')
)

PARAMS_FIRMWARE_WITH_SPP_URI = dict(
    config='config.json',
    state='firmware_installed',
    data=dict(name='Name of the Logical Interconnect',
              firmware=dict(command='Update',
                            sppUri='/rest/firmware-drivers/filename-of-the-firmware-to-install')))


@pytest.mark.resource(TestLogicalInterconnectModule='logical_interconnects')
class TestLogicalInterconnectModule(OneViewBaseTest):
    """
    Test the module constructor and shared functions
    OneViewBaseTestCase has common mocks and tests for main function
    """

    status = "Forwarding information base dump for logical interconnect yielded no results and ended with warnings."
    response_body = {
        'status': status,
        'state': 'Warning'
    }
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
    snmp_config = {'enabled': False}
    monitor_config = {'enablePortMonitor': True}
    expected_data = {
        'command': 'Update',
        'sppUri': '/rest/firmware-drivers/filename-of-the-firmware-to-install'
    }
    response = {
        "response": "data"
    }

    telemetry_config_uri = LOGICAL_INTERCONNECT['telemetryConfiguration']['uri']

    def test_should_fail_when_option_is_invalid(self):
        self.mock_ansible_module.params = dict(
            config='config.json',
            state='ethernet_settings_updated',
            data=dict(name='Name of the Logical Interconnect')
        )

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=LogicalInterconnectModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_return_to_a_consistent_state(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_compliance.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_COMPLIANCE

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_CONSISTENT,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_COMPLIANCE

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=LogicalInterconnectModule.MSG_NOT_FOUND)

    def test_should_update_ethernet_settings(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_ETHERNET_SETTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_ETH_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_ethernet_with_merged_data(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_ETHERNET_SETTINGS

        LogicalInterconnectModule().run()

        expected_data = {'enableIgmpSnooping': True, 'macRefreshInterval': 7}
        self.resource.update_ethernet_settings.assert_called_once_with(expected_data)

    def test_should_do_nothing_when_no_changes_ethernet_settings(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_ethernet_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_ETHERNET_SETTINGS_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED)

    def test_should_update_internal_networks(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        self.resource.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_INTERNAL_NETWORKS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_internal_networks_with_given_list(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], [{'uri': '/path/2'}]]
        self.resource.update_internal_networks.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        expected_list = ['/path/1', '/path/2', '/path/3']
        self.resource.update_internal_networks.assert_called_once_with(
            expected_list)

    def test_should_fail_when_ethernet_network_not_found(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.mock_ov_client.ethernet_networks.get_by.side_effect = [[{'uri': '/path/1'}], []]
        self.resource.update_internal_networks.return_value = {}

        self.mock_ansible_module.params = PARAMS_INTERNAL_NETWORKS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=LogicalInterconnectModule.MSG_ETH_NETWORK_NOT_FOUND + "Network Name 2")

    def test_should_update_settings(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_SETTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_SETTINGS_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_update_settings_ethernet(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_SETTINGS_ETHERNET

        LogicalInterconnectModule().run()

        expected_settings = {
            'ethernetSettings': {
                'enableIgmpSnooping': True,
                'macRefreshInterval': 12
            },
            'fcoeSettings': {
                'fcoeMode': 'Unknown'
            }
        }
        self.resource.update_settings.assert_called_once_with(expected_settings)

    def test_should_update_fcoe_settings(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_SETTTINGS_FCOE

        LogicalInterconnectModule().run()

        expected_settings = {
            'ethernetSettings': {
                'enableIgmpSnooping': True,
                'macRefreshInterval': 10
            },
            'fcoeSettings': {
                'fcoeMode': 'NotApplicable'
            }
        }
        self.resource.update_settings.assert_called_once_with(expected_settings)

    def test_update_settings_should_do_nothing_when_data_was_not_modified(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_settings.return_value = LOGICAL_INTERCONNECT

        params = PARAMS_SETTINGS.copy()
        params['data']['ethernetSettings']['macRefreshInterval'] = 10
        params['data']['fcoeSettings']['fcoeMode'] = 'Unknown'

        self.mock_ansible_module.params = PARAMS_SETTINGS

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_settings_are_invalid(self):
        self.mock_ansible_module.params = dict(
            config='config.json',
            state='settings_updated',
            data=dict(name='Name of the Logical Interconnect')
        )

        LogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=LogicalInterconnectModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_generate_interconnect_fib(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.create_forwarding_information_base.return_value = self.response_body

        self.mock_ansible_module.params = PARAMS_GENERATE_FIB

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=self.status,
            ansible_facts=dict(interconnect_fib=self.response_body)
        )

    def test_should_update_qos_aggreg_config(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_qos_aggregated_configuration.return_value = self.qos_config
        self.resource.update_qos_aggregated_configuration.return_value = self.qos_config

        self.mock_ansible_module.params = PARAMS_QOS_AGGREG_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_QOS_UPDATED,
            ansible_facts=dict(qos_configuration=self.qos_config)
        )

    def test_should_do_nothing_when_no_changes_qos(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_qos_aggregated_configuration.return_value = self.qos_config

        self.mock_ansible_module.params = PARAMS_QOS_AGGREG_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED)

    def test_should_update_snmp_configuration(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_snmp_configuration.return_value = self.snmp_config
        self.resource.update_snmp_configuration.return_value = self.snmp_config

        self.mock_ansible_module.params = PARAMS_SNMP_CONFIG

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_SNMP_UPDATED,
            ansible_facts=dict(snmp_configuration=self.snmp_config)
        )

    def test_should_do_nothing_when_no_changes_snmp(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_snmp_configuration.return_value = self.snmp_config
        self.resource.update_snmp_configuration.return_value = self.snmp_config

        self.mock_ansible_module.params = PARAMS_SNMP_CONFIG_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED)

    def test_should_update_port_monitor_configuration(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_port_monitor.return_value = self.monitor_config
        self.resource.update_port_monitor.return_value = self.monitor_config

        self.mock_ansible_module.params = PARAMS_PORT_MONITOR_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_PORT_MONITOR_UPDATED,
            ansible_facts=dict(port_monitor=self.monitor_config)
        )

    def test_should_do_nothing_when_no_changes_port_monitor(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.get_port_monitor.return_value = self.monitor_config
        self.resource.update_port_monitor.return_value = self.monitor_config

        self.mock_ansible_module.params = PARAMS_PORT_MONITOR_CONFIGURATION_NO_CHANGES

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED)

    def test_should_update_configuration(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_configuration.return_value = LOGICAL_INTERCONNECT

        self.mock_ansible_module.params = PARAMS_CONFIGURATION

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_CONFIGURATION_UPDATED,
            ansible_facts=dict(logical_interconnect=LOGICAL_INTERCONNECT)
        )

    def test_should_install_firmware(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = PARAMS_FIRMWARE_WITH_SPP_NAME

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_FIRMWARE_INSTALLED,
            ansible_facts=dict(li_firmware=self.response)
        )

    def test_should_install_firmware_when_spp_name_set(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = PARAMS_FIRMWARE_WITH_SPP_NAME

        LogicalInterconnectModule().run()

        self.resource.install_firmware.assert_called_once_with(self.expected_data)

    def test_should_update_firmware_when_spp_uri_set(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.install_firmware.return_value = self.response

        self.mock_ansible_module.params = PARAMS_FIRMWARE_WITH_SPP_URI

        LogicalInterconnectModule().run()

        self.resource.install_firmware.assert_called_once_with(self.expected_data)

    def test_update_telemetry_configuration(self):
        self.resource.data = LOGICAL_INTERCONNECT
        self.resource.update_telemetry_configurations.return_value = LOGICAL_INTERCONNECT

        telemetry_config = LOGICAL_INTERCONNECT['telemetryConfiguration']

        self.mock_ansible_module.params = TELEMETRY_PARAMS_CONFIGURATION

        LogicalInterconnectModule().run()

        self.resource.update_telemetry_configurations.assert_called_once_with(
            TELEMETRY_CONFIG)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectModule.MSG_TELEMETRY_CONFIGURATION_UPDATED,
            ansible_facts=dict(telemetry_configuration=telemetry_config)
        )

    def test_update_scopes_when_different(self):
        self.resource.data = LOGICAL_INTERCONNECT

        params_to_scope = PARAMS_SCOPES.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        patch_return = LOGICAL_INTERCONNECT.copy()
        patch_return['scopeUris'] = ['test']
        obj = mock.Mock()
        obj.data = patch_return
        self.resource.patch.return_value = obj

        LogicalInterconnectModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope_uris=['test']),
            msg=LogicalInterconnectModule.MSG_SCOPES_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_SCOPES.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = LOGICAL_INTERCONNECT.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.data = resource_data

        LogicalInterconnectModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scope_uris=['test']),
            msg=LogicalInterconnectModule.MSG_NO_CHANGES_PROVIDED
        )

    def test_should_bulk_inconsistent_validate(self):
        logicalInterconnectUris = [
            "/rest/logical-interconnects/d0432852-28a7-4060-ba49-57ca973ef6c2"
        ]

        BULK_INCONSISTENCY_VALIDATION_RESPONSE = {
            'allowUpdateFromGroup': True
        }

        PARAMS_FOR_BULK_INCONSISTENCY_VALIDATE = dict(
            config='config.json',
            state='bulk_inconsistency_validated',
            data=dict(logicalInterconnectUris=[
                "/rest/logical-interconnects/d0432852-28a7-4060-ba49-57ca973ef6c2"
            ])
        )

        self.resource.bulk_inconsistency_validate.return_value = BULK_INCONSISTENCY_VALIDATION_RESPONSE

        self.mock_ansible_module.params = PARAMS_FOR_BULK_INCONSISTENCY_VALIDATE

        LogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            True, True,
            ansible_facts=dict(bulk_inconsistency_validation_result=BULK_INCONSISTENCY_VALIDATION_RESPONSE))

if __name__ == '__main__':
    pytest.main([__file__])
