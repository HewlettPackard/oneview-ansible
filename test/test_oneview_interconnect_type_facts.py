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
from oneview_interconnect_type_facts import InterconnectTypeFactsModule
from test.utils import FactsParamsTestCase
from test.utils import ModuleContructorTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="HP VC Flex-10 Enet Module"
)

PRESENT_TYPES = [{
    "name": "HP VC Flex-10 Enet Module",
    "uri": "/rest/interconnect-types/e6d938ac-0588-44c9-95f2-610f3da4a941"
}]


class InterconnectTypeFactsSpec(unittest.TestCase, ModuleContructorTestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, InterconnectTypeFactsModule)
        self.interconnect_types = self.mock_ov_client.interconnect_types
        FactsParamsTestCase.configure_client_mock(self, self.interconnect_types)

    def test_should_get_all_interconnect_types(self):
        self.interconnect_types.get_all.return_value = PRESENT_TYPES

        self.mock_ansible_module.params = PARAMS_GET_ALL

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.interconnect_types.get_all.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_ALL

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_interconnect_type_by_name(self):
        self.interconnect_types.get_by.return_value = PRESENT_TYPES

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.interconnect_types.get_by.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
