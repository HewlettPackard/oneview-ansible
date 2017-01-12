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

from oneview_san_manager_facts import SanManagerFactsModule
from test.utils import ModuleContructorTestCase, FactsParamsTestCase


class SanManagerFactsSpec(unittest.TestCase,
                          ModuleContructorTestCase,
                          FactsParamsTestCase):
    """
    ModuleContructorTestCase has common tests for the class constructor and the main function, and also provides the
    mocks used in this test class.

    FactsParamsTestCase has common tests for the parameters support.
    """

    ERROR_MSG = 'Fake message error'

    PARAMS_GET_ALL = dict(
        config='config.json',
        provider_display_name=None
    )

    PARAMS_GET_BY_PROVIDER_DISPLAY_NAME = dict(
        config='config.json',
        provider_display_name="Brocade Network Advisor"
    )

    PRESENT_SAN_MANAGERS = [{
        "providerDisplayName": "Brocade Network Advisor",
        "uri": "/rest/fc-sans/device-managers//d60efc8a-15b8-470c-8470-738d16d6b319"
    }]

    def setUp(self):
        self.configure_mocks(self, SanManagerFactsModule)
        self.san_managers = self.mock_ov_client.san_managers

        FactsParamsTestCase.configure_client_mock(self, self.san_managers)

    def test_should_get_all(self):
        self.san_managers.get_all.return_value = self.PRESENT_SAN_MANAGERS
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        SanManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(san_managers=(self.PRESENT_SAN_MANAGERS))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.san_managers.get_all.side_effect = Exception(self.ERROR_MSG)
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        SanManagerFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_by_display_name(self):
        self.san_managers.get_by_provider_display_name.return_value = self.PRESENT_SAN_MANAGERS[0]
        self.mock_ansible_module.params = self.PARAMS_GET_BY_PROVIDER_DISPLAY_NAME

        SanManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(san_managers=(self.PRESENT_SAN_MANAGERS))
        )

    def test_should_fail_when_get_by_provider_display_name_raises_exception(self):
        self.san_managers.get_by_provider_display_name.side_effect = Exception(self.ERROR_MSG)
        self.mock_ansible_module.params = self.PARAMS_GET_BY_PROVIDER_DISPLAY_NAME

        SanManagerFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
