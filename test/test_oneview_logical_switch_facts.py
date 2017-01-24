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
import yaml
from oneview_logical_switch_facts import LogicalSwitchFactsModule, EXAMPLES
from test.utils import FactsParamsTestCase
from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

ERROR_MSG = 'Fake message error'

PRESENT_LOGICAL_SWITCHES = [{
    "name": "Test Logical Switch",
    "uri": "/rest/logical-switches/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class LogicalSwitchFactsSpec(unittest.TestCase,
                             ModuleContructorTestCase,
                             FactsParamsTestCase,
                             ErrorHandlingTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchFactsModule)
        self.logical_switches = self.mock_ov_client.logical_switches
        FactsParamsTestCase.configure_client_mock(self, self.logical_switches)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.logical_switches.get_by)

        LOGICAL_SWITCH_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.PARAMS_GET_ALL = LOGICAL_SWITCH_FACTS_EXAMPLES[0]['oneview_logical_switch_facts']
        self.PARAMS_GET_BY_NAME = LOGICAL_SWITCH_FACTS_EXAMPLES[4]['oneview_logical_switch_facts']

    def test_should_get_all_logical_switches(self):
        self.logical_switches.get_all.return_value = PRESENT_LOGICAL_SWITCHES
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        LogicalSwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switches=(PRESENT_LOGICAL_SWITCHES))
        )

    def test_should_get_logical_switch_by_name(self):
        self.logical_switches.get_by.return_value = PRESENT_LOGICAL_SWITCHES
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        LogicalSwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switches=(PRESENT_LOGICAL_SWITCHES))
        )


if __name__ == '__main__':
    unittest.main()
