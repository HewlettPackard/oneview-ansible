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
from oneview_task_facts import TaskFactsModule
from utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

COUNT = 2

FILTER_BY_ASSOCIATED_RESOURCE_NAME = "associatedResource.resourceName='ProfileTemplate101'"

PARAMS_GET_ALL = dict(
    config='config.json',
    params=None
)

PARAMS_GET_ALL_WITH_FILTER = dict(
    config='config.json',
    params=dict(
        filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME
    )
)

PARAMS_GET_ALL_WITH_FILTER_AND_COUNT = dict(
    config='config.json',
    params=dict(
        count=COUNT,
        filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME
    )
)

TASK = {
    "associatedResource": {
        "associationType": "MANAGED_BY",
        "resourceCategory": "server-profile-templates",
        "resourceName": "ProfileTemplate101",
        "resourceUri": "/rest/server-profile-templates/fa6d2aff-7579-4240-91d4-89fe8e40d6f9"
    },
    "created": "2016-09-06T15:16:23.638Z",
    "modified": "2016-09-06T15:16:24.249Z",
    "owner": "administrator",
    "taskState": "Completed",
    "taskStatus": "Successfully deleted server profile template: ProfileTemplate101 ",
    "type": "TaskResourceV2",
    "uri": "/rest/tasks/D2B856D2-5939-421B-BDCA-FBF7D8961A89",
}

ALL_TASKS = [TASK]


class TaskFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class TaskFactsSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_get_all(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.tasks.get_all.return_value = ALL_TASKS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule().run()

        mock_ov_instance.tasks.get_all.assert_called_once_with()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_get_all_with_filter(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.tasks.get_all.return_value = ALL_TASKS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL_WITH_FILTER)
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule().run()

        mock_ov_instance.tasks.get_all.assert_called_once_with(filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_get_all_with_filter_and_count(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.tasks.get_all.return_value = ALL_TASKS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL_WITH_FILTER_AND_COUNT)
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule().run()

        mock_ov_instance.tasks.get_all.assert_called_once_with(
            filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME,
            count=COUNT
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_task_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_error(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.tasks.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        TaskFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
