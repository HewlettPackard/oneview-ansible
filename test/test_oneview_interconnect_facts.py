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
from oneview_interconnect_facts import InterconnectFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

INTERCONNECT_NAME = "0000A66102, interconnect 2"

PARAMS_FOR_GET_ALL = dict(
    config='config.json',
    name=None,
)

PARAMS_FOR_GET_BY_NAME = dict(
    config='config.json',
    name=INTERCONNECT_NAME
)

PARAMS_FOR_GET_NAME_SERVERS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['nameServers']
)


INTERCONNECT_URI = "/rest/interconnects/53fa7d35-1cc8-46c1-abf0-6af091a1aed3"
PORT_NAME = "d1"
SUBPORT_NUMBER = 1

PARAMS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['statistics']
)

PARAMS_FOR_PORT_STATISTICS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=[{'portStatistics': PORT_NAME}]
)

PARAMS_FOR_SUBPORT_STATISTICS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=[{'subPortStatistics': {'portName': PORT_NAME, 'subportNumber': SUBPORT_NUMBER}}]
)

MOCK_INTERCONNECTS = [
    dict(uidState='On', uri=INTERCONNECT_URI)
]


class InterconnectFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class InterconnectFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_all_interconnects(self, mock_ansible_module, mock_ov_from_file):
        fake_interconnects = [dict(uidState='On', name=INTERCONNECT_NAME)]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_all.return_value = fake_interconnects

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_all.assert_called_once()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=fake_interconnects)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, InterconnectFactsModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_interconnects_by_interconnect_name(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = MOCK_INTERCONNECTS

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_by.assert_called_once_with('name', INTERCONNECT_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_interconnect_name_servers(self, mock_ansible_module, mock_ov_from_file):
        fake_name_servers = [dict(t=1)]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = MOCK_INTERCONNECTS
        mock_ov_instance.interconnects.get_name_servers.return_value = fake_name_servers

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_NAME_SERVERS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_by.assert_called_once_with('name', INTERCONNECT_NAME)
        mock_ov_instance.interconnects.get_name_servers.assert_called_once_with(INTERCONNECT_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS, interconnect_name_servers=fake_name_servers)
        )


class InterconnectStatisticsFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_interconnect_statistics_by_interconnect_name(self, mock_ansible_module,
                                                                     mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = MOCK_INTERCONNECTS

        fake_statistics = dict()
        mock_ov_instance.interconnects.get_statistics.return_value = fake_statistics

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_statistics.assert_called_once_with(INTERCONNECT_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_statistics=fake_statistics,

            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_gather_facts_about_interconnect_port_statistics(self, mock_ansible_module, mock_ov_from_file):
        fake_statistics = dict(name='test')

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = MOCK_INTERCONNECTS
        mock_ov_instance.interconnects.get_statistics.return_value = fake_statistics

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PORT_STATISTICS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_statistics.assert_called_once_with(INTERCONNECT_URI, PORT_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_port_statistics=fake_statistics,
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_gather_facts_about_interconnect_subport_statistics(self, mock_ansible_module, mock_ov_from_file):
        fake_statistics = dict(name='test')

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = MOCK_INTERCONNECTS
        mock_ov_instance.interconnects.get_subport_statistics.return_value = fake_statistics

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_SUBPORT_STATISTICS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_subport_statistics.assert_called_once_with(
            INTERCONNECT_URI,
            PORT_NAME,
            SUBPORT_NUMBER
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_subport_statistics=fake_statistics
            )
        )


if __name__ == '__main__':
    unittest.main()
