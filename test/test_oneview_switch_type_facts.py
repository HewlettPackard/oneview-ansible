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

from oneview_switch_type_facts import SwitchTypeFactsModule
from test.utils import ModuleContructorTestCase, FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Switch Type 2"
)

SWITCH_TYPES = [{"name": "Test Switch Type 1"}, {"name": "Test Switch Type 2"}, {"name": "Test Switch Type 3"}]


class SwitchTypeFactsSpec(unittest.TestCase, ModuleContructorTestCase, FactsParamsTestCase):

    def setUp(self):
        self.configure_mocks(self, SwitchTypeFactsModule)
        self.resource = self.mock_ov_client.switch_types
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_switch_types(self):
        self.resource.get_all.return_value = SWITCH_TYPES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switch_types=(SWITCH_TYPES))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.resource.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_switch_type_by_name(self):
        self.resource.get_by.return_value = [SWITCH_TYPES[1]]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switch_types=([SWITCH_TYPES[1]]))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.resource.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
