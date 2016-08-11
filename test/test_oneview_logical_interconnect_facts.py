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

ERROR_MSG = 'Fake message error'

LOGICAL_INTERCONNECT_NAME = "test"

LOGICAL_INTERCONNECT_URI = "/rest/logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME,
    options=None
)

PARAMS_GET_BY_NAME_WITH_QOS = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME,
    options=['qos_aggregated_configuration']
)

PARAMS_GET_BY_NAME_WITH_SNMP = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME,
    options=['snmp_configuration']
)

PARAMS_GET_BY_NAME_WITH_PORT_MONITOR = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME,
    options=['port_monitor']
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME,
    options=[
        'qos_aggregated_configuration',
        'snmp_configuration',
        'port_monitor'
    ]
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

LOGICAL_INTERCONNECT = dict(
    name=LOGICAL_INTERCONNECT_NAME,
    uri=LOGICAL_INTERCONNECT_URI
)

ALL_INTERCONNECTS = [LOGICAL_INTERCONNECT]


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


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
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=LOGICAL_INTERCONNECT)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name_with_qos_configuration(self,
                                                                               mock_ansible_module,
                                                                               mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_QOS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

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
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_SNMP)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

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
    def test_should_get_a_logical_interconnects_by_name_with_port_monitor(self,
                                                                          mock_ansible_module,
                                                                          mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_PORT_MONITOR)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

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
    def test_should_get_a_logical_interconnects_by_name_with_multiple_options(self,
                                                                              mock_ansible_module,
                                                                              mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.return_value = QOS_CONFIGURATION
        mock_ov_instance.logical_interconnects.get_snmp_configuration.return_value = SNMP_CONFIGURATION
        mock_ov_instance.logical_interconnects.get_port_monitor.return_value = PORT_MONITOR
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

        mock_ov_instance.logical_interconnects.get_qos_aggregated_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ov_instance.logical_interconnects.get_snmp_configuration.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ov_instance.logical_interconnects.get_port_monitor.assert_called_once_with(
            id_or_uri=LOGICAL_INTERCONNECT_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                logical_interconnects=LOGICAL_INTERCONNECT,
                qos_aggregated_configuration=QOS_CONFIGURATION,
                snmp_configuration=SNMP_CONFIGURATION,
                port_monitor=PORT_MONITOR
            )
        )


class LogicalInterconnectFactsErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_an_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
