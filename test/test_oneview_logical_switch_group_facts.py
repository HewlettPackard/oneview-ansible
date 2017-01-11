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
from oneview_logical_switch_group_facts import LogicalSwitchGroupFactsModule, EXAMPLES
from test.utils import FactsParamsTestCase
from test.utils import ModuleContructorTestCase

ERROR_MSG = 'Fake message error'


class LogicalSwitchGroupFactsSpec(unittest.TestCase, ModuleContructorTestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchGroupFactsModule)
        self.logical_switch_groups = self.mock_ov_client.logical_switch_groups
        FactsParamsTestCase.configure_client_mock(self, self.logical_switch_groups)

        LSG_EXAMPLES = yaml.load(EXAMPLES)

        self.PARAMS_GET_ALL = LSG_EXAMPLES[0]['oneview_logical_switch_group_facts']
        self.PARAMS_GET_BY_NAME = LSG_EXAMPLES[4]['oneview_logical_switch_group_facts']

    def test_should_get_logical_switch_group_by_name(self):
        self.logical_switch_groups.get_by.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )

    def test_should_fail_when_get_by_raises_error(self):
        self.logical_switch_groups.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_all_logical_switch_groups(self):
        self.logical_switch_groups.get_all.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )

    def test_should_fail_when_get_all_raises_error(self):
        self.logical_switch_groups.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
