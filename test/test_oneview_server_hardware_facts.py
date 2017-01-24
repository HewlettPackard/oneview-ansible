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

from oneview_server_hardware_facts import ServerHardwareFactsModule
from test.utils import ModuleContructorTestCase, FactsParamsTestCase, ErrorHandlingTestCase

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


class ServerHardwareFactsSpec(unittest.TestCase,
                              ModuleContructorTestCase,
                              FactsParamsTestCase,
                              ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for the class constructor and the main function, and also provides the
    mocks used in this test class.

    FactsParamsTestCase has common tests for the parameters support.
    """
    def setUp(self):
        self.configure_mocks(self, ServerHardwareFactsModule)
        self.server_hardware = self.mock_ov_client.server_hardware

        FactsParamsTestCase.configure_client_mock(self, self.server_hardware)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.server_hardware.get_by)

    def test_should_get_all_server_hardware(self):
        self.server_hardware.get_all.return_value = {"name": "Server Hardware Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    def test_should_get_server_hardware_by_name(self):
        self.server_hardware.get_by.return_value = {"name": "Server Hardware Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    def test_should_get_server_hardware_by_name_with_options(self):
        self.server_hardware.get_by.return_value = [{"name": "Server Hardware Name", "uri": "resuri"}]
        self.server_hardware.get_bios.return_value = {'subresource': 'value'}
        self.server_hardware.get_environmental_configuration.return_value = {'subresource': 'value'}
        self.server_hardware.get_java_remote_console_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_ilo_sso_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_remote_console_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_utilization.return_value = {'subresource': 'value'}
        self.server_hardware.get_firmware.return_value = {'subresource': 'firmware'}
        self.mock_ansible_module.params = PARAMS_WITH_OPTIONS

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
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

    def test_should_get_all_firmwares_across_the_servers(self):
        self.server_hardware.get_all.return_value = []
        self.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]
        self.mock_ansible_module.params = PARAMS_WITH_ALL_FIRMWARES_WITHOUT_FILTER

        ServerHardwareFactsModule().run()

        self.server_hardware.get_all_firmwares.assert_called_once_with()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )

    def test_should_get_all_firmwares_with_filters(self):
        self.server_hardware.get_all.return_value = []
        self.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]
        self.mock_ansible_module.params = PARAMS_WITH_ALL_FIRMWARES_WITH_FILTERS

        ServerHardwareFactsModule().run()

        self.server_hardware.get_all_firmwares.assert_called_once_with(filters=FIRMWARE_FILTERS)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )


if __name__ == '__main__':
    unittest.main()
