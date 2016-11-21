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
from oneview_alert_facts import AlertFactsModule
from utils import create_ansible_mock
from mock import patch
import copy

ERROR_MSG = 'Fake message error'

COUNT = 2

FILTER_BY_ALERT_STATE = "alertState='Active'"

PARAMS_GET_ALL = dict(
    config='config.json',
    params=None
)

PARAMS_GET_ALL_WITH_FILTER = dict(
    config='config.json',
    params=dict(
        filter=FILTER_BY_ALERT_STATE
    )
)

PARAMS_GET_ALL_WITH_FILTER_AND_COUNT = dict(
    config='config.json',
    params=dict(
        count=COUNT,
        filter=FILTER_BY_ALERT_STATE
    )
)

ALERT = {
    "type": "AlertResourceV3",
    "alertState": "Active",
    "severity": "Warning",
    "urgency": "None",
    "description": "Utilization data has not been successfully collected for 38 minutes and 5 attempts.",
    "category": "alerts",
    "uri": "/rest/alerts/98"
}

ALL_ALERTS = [ALERT]


class AlertFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_alert_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        AlertFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_alert_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        AlertFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class TaskFactsSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ov_client_from_json_file = patch.object(OneViewClient, 'from_json_file')
        mock_from_json_file = self.patcher_ov_client_from_json_file.start()

        mock_ov_client = mock.Mock()
        mock_from_json_file.return_value = mock_ov_client

        self.resource = mock_ov_client.alerts

        self.patcher_ansible_module = patch('oneview_alert_facts.AnsibleModule')
        mock_ansible_module = self.patcher_ansible_module.start()

        self.mock_ansible_instance = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_instance

    def tearDown(self):
        self.patcher_ov_client_from_json_file.stop()
        self.patcher_ansible_module.stop()

    def test_get_all(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter_and_count(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_should_fail_when_get_all_raises_error(self):

        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)
        self.resource.get_all.side_effect = Exception(ERROR_MSG)

        AlertFactsModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
