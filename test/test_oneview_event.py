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
from oneview_module_loader import EventModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data={
          'description': "This is a very simple test event",
          'eventTypeID': "hp.justATest",
          'eventDetails': [{
              'eventItemName': "ipv4Address",
              'eventItemValue': "198.51.100.5",
              'isThisVarbindData': "false",
              'varBindOrderIndex': -1
          }]
    }
)


class EventModuleSpec(unittest.TestCase, OneViewBaseTestCase):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, EventModule)
        self.resource = self.mock_ov_client.events

    def test_should_create_new_event(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = PARAMS_FOR_PRESENT['data']

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EventModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EventModule.MSG_CREATED,
            ansible_facts=dict(event=PARAMS_FOR_PRESENT['data'])
        )


if __name__ == '__main__':
    unittest.main()
