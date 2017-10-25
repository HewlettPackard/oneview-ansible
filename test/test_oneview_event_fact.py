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

from ansible.compat.tests import unittest
from oneview_module_loader import EventFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Event"
)

PRESENT_EVENTS = [{
    "name": "Test Event",
    "uri": "/rest/event/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class EventFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, EventFactsModule)
        self.events = self.mock_ov_client.events
        FactsParamsTestCase.configure_client_mock(self, self.events)

    def test_should_get_all_events(self):
        self.events.get_all.return_value = PRESENT_EVENTS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        EventFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(events=PRESENT_EVENTS)
        )


if __name__ == '__main__':
    unittest.main()
