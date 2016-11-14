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
from oneview_server_hardware_facts import ServerHardwareFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Server Hardware"
)

PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Server Hardware",
    options=[
        'bios', 'javaRemoteConsoleUrl', 'environmentalConfig', 'iloSsoUrl', 'remoteConsoleUrl', 'firmware',
        {"utilization": {"fields": 'AveragePower',
                         "filter": 'startDate=2016-05-30T03:29:42.000Z',
                         "view": 'day'}}]
)

PARAMS_WITH_ALL_FIRMWARES_WITHOUT_FILTER = dict(
    config='config.json',
    options=['firmwares']
)

FIRMWARE_FILTERS = [
    "components.componentName='HPE Synergy 3530C 16G Host Bus Adapter'",
    "components.componentVersion matches '1.2%'"
]

PARAMS_WITH_ALL_FIRMWARES_WITH_FILTERS = dict(
    config='config.json',
    options=[dict(firmwares=dict(filters=FIRMWARE_FILTERS))]
)


class ServerHardwareFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ServerHardwareFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_get_all_server_hardware(self, mock_ansible_module,
                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_all.return_value = {"name": "Server Hardware Name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_get_server_hardware_by_name(self, mock_ansible_module,
                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = {"name": "Server Hardware Name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_get_server_hardware_by_name_with_options(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"name": "Server Hardware Name", "uri": "resuri"}]
        mock_ov_instance.server_hardware.get_bios.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_environmental_configuration.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_java_remote_console_url.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_ilo_sso_url.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_remote_console_url.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_utilization.return_value = {'subresource': 'value'}
        mock_ov_instance.server_hardware.get_firmware.return_value = {'subresource': 'firmware'}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_hardwares': [{'name': 'Server Hardware Name', 'uri': 'resuri'}],
                           'server_hardware_remote_console_url': {'subresource': 'value'},
                           'server_hardware_utilization': {'subresource': 'value'},
                           'server_hardware_ilo_sso_url': {'subresource': 'value'},
                           'server_hardware_bios': {'subresource': 'value'},
                           'server_hardware_java_remote_console_url': {'subresource': 'value'},
                           'server_hardware_env_config': {'subresource': 'value'},
                           'server_hardware_firmware': {'subresource': 'firmware'}}
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_get_all_firmwares_across_the_servers(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_all.return_value = []
        mock_ov_instance.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_ALL_FIRMWARES_WITHOUT_FILTER)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ov_instance.server_hardware.get_all_firmwares.assert_called_once_with()
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_get_all_firmwares_with_filters(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_all.return_value = []
        mock_ov_instance.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_ALL_FIRMWARES_WITH_FILTERS)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ov_instance.server_hardware.get_all_firmwares.assert_called_once_with(filters=FIRMWARE_FILTERS)
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
