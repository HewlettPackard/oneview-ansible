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
from oneview_logical_interconnect_facts import LogicalInterconnectFactsModule
from oneview_logical_interconnect_facts import LOGICAL_INTERCONNECT_NOT_FOUND
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

LOGICAL_INTERCONNECT_NAME = "test"

LOGICAL_INTERCONNECT_URI = "/rest/logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0"

TELEMETRY_CONF_URI = LOGICAL_INTERCONNECT_URI + "/telemetry-configurations/33845548-eae0-4f8e-b166-38680c2b81e7"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

QOS_CONFIGURATION = dict(
    activeQosConfig=dict(
        category="qos-aggregated-configuration",
        configType="Passthrough",
        type="QosConfiguration"
    ),
    category="qos-aggregated-configuration",
    type="qos-aggregated-configuration",
    uri=None
)

SNMP_CONFIGURATION = dict(
    category="snmp-configuration",
    type="snmp-configuration",
    uri=None
)

PORT_MONITOR = dict(
    category="port-monitor",
    enablePortMonitor=False,
    name="name-2081994975-1467759087361",
    type="port-monitor",
    uri="/rest/logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0/port-monitor"
)

INTERNAL_VLANS = [
    dict(
        generalNetworkUri="/rest/ethernet-networks/ac479ca0-01f3-4bef-bb0d-619e04321b29",
        internalVlanId=5,
        logicalInterconnectUri="/rest/logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0",
        type="internal-vlan-association"
    )
]

FIRMWARE = dict(

)

UNASSIGNED_UPLINK_PORTS = [
    {
        "interconnectName": "Test-Enclosure-Renamed-Updated, interconnect 2",
        "portName": "X1",
        "uri": "/rest/interconnects/a848f968-b51f-4a7f-b071-3a56a0aa0488/ports/a848f968-b51f-4a7f-b071-3a56a0aa0488:X1"
    },
    {
        "interconnectName": "Test-Enclosure-Renamed-Updated, interconnect 2",
        "portName": "X2",
        "uri": "/rest/interconnects/a848f968-b51f-4a7f-b071-3a56a0aa0488/ports/a848f968-b51f-4a7f-b071-3a56a0aa0488:X2"
    }
]

TELEMETRY_CONFIGURATION = {
    "enableTelemetry": True,
    "sampleCount": 12,
    "sampleInterval": 300
}

LOGICAL_INTERCONNECT = dict(
    name=LOGICAL_INTERCONNECT_NAME,
    uri=LOGICAL_INTERCONNECT_URI,
    telemetryConfiguration=dict(uri=TELEMETRY_CONF_URI)
)

ALL_INTERCONNECTS = [LOGICAL_INTERCONNECT]


def define_mocks_for_get_by_name(mock_ov_from_file, mock_ansible_module, PARAMS):
    mock_ov_instance = mock.Mock()
    mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
    mock_ov_from_file.return_value = mock_ov_instance

    mock_ansible_instance = create_ansible_mock(PARAMS)
    mock_ansible_module.return_value = mock_ansible_instance

    return mock_ov_instance, mock_ansible_instance


def create_params(options=[]):
    return dict(config='config.json', name=LOGICAL_INTERCONNECT_NAME, options=options)


class LogicalInterconnectFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class LogicalInterconnectFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_all_logical_interconnects(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_all.return_value = ALL_INTERCONNECTS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=ALL_INTERCONNECTS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            create_params()
        )

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(name=LOGICAL_INTERCONNECT_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_qos_configuration(self,
                                                                               mock_ansible_module,
                                                                               mock_ov_from_file):
        params = create_params(['qos_aggregated_configuration'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                qos_aggregated_configuration=QOS_CONFIGURATION
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_snmp_configuration(self,
                                                                                mock_ansible_module,
                                                                                mock_ov_from_file):
        params = create_params(['snmp_configuration'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_snmp_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                snmp_configuration=SNMP_CONFIGURATION
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_port_monitor(self, mock_ansible_module, mock_ov_from_file):
        params = create_params(['port_monitor'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_port_monitor.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                port_monitor=PORT_MONITOR
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_internal_vlans(self,
                                                                            mock_ansible_module,
                                                                            mock_ov_from_file):
        params = create_params(['internal_vlans'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_internal_vlans.return_value = INTERNAL_VLANS

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_internal_vlans.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                internal_vlans=INTERNAL_VLANS
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_forwarding_information_base(self,
                                                                                         mock_ansible_module,
                                                                                         mock_ov_from_file):
        params = create_params(['internal_vlans'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_internal_vlans.return_value = INTERNAL_VLANS

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_internal_vlans.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                internal_vlans=INTERNAL_VLANS
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_firmware(self, mock_ansible_module, mock_ov_from_file):
        params = create_params(['firmware'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_firmware.return_value = FIRMWARE

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_firmware.assert_called_once_with(id_or_uri=LOGICAL_INTERCONNECT_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                firmware=FIRMWARE
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_unassigned_uplink_ports(self,
                                                                                     mock_ansible_module,
                                                                                     mock_ov_from_file):
        params = create_params(['unassigned_uplink_ports'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_unassigned_uplink_ports.return_value = UNASSIGNED_UPLINK_PORTS

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_unassigned_uplink_ports.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                unassigned_uplink_ports=UNASSIGNED_UPLINK_PORTS
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_telemetry_configuration(self,
                                                                                     mock_ansible_module,
                                                                                     mock_ov_from_file):
        params = create_params(['telemetry_configuration'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_telemetry_configuration.return_value = TELEMETRY_CONFIGURATION

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_telemetry_configuration.assert_called_once_with(
            telemetry_configuration_uri=TELEMETRY_CONF_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                telemetry_configuration=TELEMETRY_CONFIGURATION
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_multiple_options(self,
                                                                              mock_ansible_module,
                                                                              mock_ov_from_file):
        params = create_params(['qos_aggregated_configuration', 'snmp_configuration', 'port_monitor',
                                'unassigned_uplink_ports', 'telemetry_configuration'])

        mock_ov_instance, mock_ansible_instance = define_mocks_for_get_by_name(
            mock_ov_from_file,
            mock_ansible_module,
            params
        )

        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR
        mock_ov_instance.logical_interconnects.get_unassigned_uplink_ports.return_value = UNASSIGNED_UPLINK_PORTS
        mock_ov_instance.logical_interconnects.get_telemetry_configuration.return_value = TELEMETRY_CONFIGURATION

        LogicalInterconnectFactsModule().run()

        expected_uri = dict(id_or_uri=LOGICAL_INTERCONNECT_URI)
        telemetry_uri = dict(telemetry_configuration_uri=TELEMETRY_CONF_URI)

        # validate the calls to the OneView SDK
        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(name=LOGICAL_INTERCONNECT_NAME)
        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.assert_called_once_with(**expected_uri)
        mock_ov_instance.logical_interconnects.get_snmp_configuration.assert_called_once_with(**expected_uri)
        mock_ov_instance.logical_interconnects.get_port_monitor.assert_called_once_with(**expected_uri)
        mock_ov_instance.logical_interconnects.get_unassigned_uplink_ports.assert_called_once_with(**expected_uri)
        mock_ov_instance.logical_interconnects.get_telemetry_configuration.assert_called_once_with(**telemetry_uri)

        # Validate the result data
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                qos_aggregated_configuration=QOS_CONFIGURATION,
                snmp_configuration=SNMP_CONFIGURATION,
                port_monitor=PORT_MONITOR,
                unassigned_uplink_ports=UNASSIGNED_UPLINK_PORTS,
                telemetry_configuration=TELEMETRY_CONFIGURATION
            )
        )


class LogicalInterconnectFactsErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_an_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_fail_when_logical_interconnect_not_exist(self,
                                                             mock_ansible_module,
                                                             mock_ov_from_file):
        params = create_params(['unassigned_uplink_ports'])

        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = None
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=LOGICAL_INTERCONNECT_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
