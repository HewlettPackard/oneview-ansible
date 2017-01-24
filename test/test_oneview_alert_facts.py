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
from oneview_alert_facts import AlertFactsModule
from utils import ModuleContructorTestCase
from utils import ErrorHandlingTestCase
import copy

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    params=None
)

ALL_ALERTS = [{
    "type": "AlertResourceV3",
    "alertState": "Active",
    "severity": "Warning",
    "urgency": "None",
    "description": "Utilization data has not been successfully collected for 38 minutes and 5 attempts.",
    "category": "alerts",
    "uri": "/rest/alerts/98"
}]


class TaskFactsSpec(unittest.TestCase,
                    ModuleContructorTestCase,
                    ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case

    ErrorHandlingTestCase has common tests for the module error handling.
    """

    def setUp(self):
        self.configure_mocks(self, AlertFactsModule)
        self.resource = self.mock_ov_client.alerts

        ErrorHandlingTestCase.configure(self, method_to_fire=self.resource.get_all)

    def test_get_all(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter_and_count(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )


if __name__ == '__main__':
    unittest.main()
