###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from oneview_module_loader import LogicalInterconnectFactsModule
from hpe_test_utils import FactsParamsTestCase

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


def create_params(options=[]):
    return dict(config='config.json', name=LOGICAL_INTERCONNECT_NAME, options=options)


class LogicalInterconnectFactsSpec(unittest.TestCase,
                                   FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectFactsModule)
        self.logical_interconnects = self.mock_ov_client.logical_interconnects
        FactsParamsTestCase.configure_client_mock(self, self.logical_interconnects)

    def test_should_get_all_logical_interconnects(self):
        self.logical_interconnects.get_all.return_value = ALL_INTERCONNECTS

        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=ALL_INTERCONNECTS)
        )

    def test_should_get_a_logical_interconnects_by_name(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.mock_ansible_module.params = create_params()

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_by_name.assert_called_once_with(name=LOGICAL_INTERCONNECT_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=LOGICAL_INTERCONNECT)
        )

    def test_should_get_a_logical_interconnects_by_name_with_qos_configuration(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION

        self.mock_ansible_module.params = create_params(['qos_aggregated_configuration'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_qos_aggregated_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                qos_aggregated_configuration=QOS_CONFIGURATION
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_snmp_configuration(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION
        self.mock_ansible_module.params = create_params(['snmp_configuration'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_snmp_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                snmp_configuration=SNMP_CONFIGURATION
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_port_monitor(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR
        self.mock_ansible_module.params = create_params(['port_monitor'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_port_monitor.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                port_monitor=PORT_MONITOR
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_internal_vlans(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_internal_vlans.return_value = INTERNAL_VLANS
        self.mock_ansible_module.params = create_params(['internal_vlans'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_internal_vlans.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                internal_vlans=INTERNAL_VLANS
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_forwarding_information_base(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_internal_vlans.return_value = INTERNAL_VLANS
        self.mock_ansible_module.params = create_params(['internal_vlans'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_internal_vlans.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                internal_vlans=INTERNAL_VLANS
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_firmware(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_firmware.return_value = FIRMWARE
        self.mock_ansible_module.params = create_params(['firmware'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_firmware.assert_called_once_with(id_or_uri=LOGICAL_INTERCONNECT_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                firmware=FIRMWARE
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_unassigned_uplink_ports(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_unassigned_uplink_ports.return_value = UNASSIGNED_UPLINK_PORTS
        self.mock_ansible_module.params = create_params(['unassigned_uplink_ports'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_unassigned_uplink_ports.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                unassigned_uplink_ports=UNASSIGNED_UPLINK_PORTS
            )
        )

    def test_should_get_a_logical_interconnect_by_name_with_ethernet_settings(self):
        ethernet_settings = {
            "id": "235d50d7-cf4a-4362-aec3-c4914c6ebab4",
            "igmpIdleTimeoutInterval": 260,
            "interconnectType": "Ethernet",
            "macRefreshInterval": 5,
            "modified": "2016-12-20T16:48:08.626Z",
            "name": "ES634039453",
            "uri": "/rest/logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0/ethernetSettings"
        }
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_ethernet_settings.return_value = ethernet_settings
        self.mock_ansible_module.params = create_params(['ethernet_settings'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_ethernet_settings.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                ethernet_settings=ethernet_settings
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_telemetry_configuration(self):
        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_telemetry_configuration.return_value = TELEMETRY_CONFIGURATION
        self.mock_ansible_module.params = create_params(['telemetry_configuration'])

        LogicalInterconnectFactsModule().run()

        self.logical_interconnects.get_telemetry_configuration.assert_called_once_with(
            telemetry_configuration_uri=TELEMETRY_CONF_URI
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                telemetry_configuration=TELEMETRY_CONFIGURATION
            )
        )

    def test_should_get_a_logical_interconnects_by_name_with_multiple_options(self):
        params = create_params(['qos_aggregated_configuration', 'snmp_configuration', 'port_monitor',
                                'unassigned_uplink_ports', 'telemetry_configuration'])

        self.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        self.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION
        self.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION
        self.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR
        self.logical_interconnects.get_unassigned_uplink_ports.return_value = UNASSIGNED_UPLINK_PORTS
        self.logical_interconnects.get_telemetry_configuration.return_value = TELEMETRY_CONFIGURATION
        self.mock_ansible_module.params = params

        LogicalInterconnectFactsModule().run()

        expected_uri = dict(id_or_uri=LOGICAL_INTERCONNECT_URI)
        telemetry_uri = dict(telemetry_configuration_uri=TELEMETRY_CONF_URI)

        # validate the calls to the OneView SDK
        self.logical_interconnects.get_by_name.assert_called_once_with(name=LOGICAL_INTERCONNECT_NAME)
        self.logical_interconnects.get_qos_aggregated_configuration.assert_called_once_with(**expected_uri)
        self.logical_interconnects.get_snmp_configuration.assert_called_once_with(**expected_uri)
        self.logical_interconnects.get_port_monitor.assert_called_once_with(**expected_uri)
        self.logical_interconnects.get_unassigned_uplink_ports.assert_called_once_with(**expected_uri)
        self.logical_interconnects.get_telemetry_configuration.assert_called_once_with(**telemetry_uri)

        # Validate the result data
        self.mock_ansible_module.exit_json.assert_called_once_with(
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

    def test_should_fail_when_logical_interconnect_not_exist(self):
        params = create_params(['unassigned_uplink_ports'])

        self.logical_interconnects.get_by_name.return_value = None

        self.mock_ansible_module.params = params

        LogicalInterconnectFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=LogicalInterconnectFactsModule.MSG_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
