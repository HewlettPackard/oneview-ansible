#!/usr/bin/python
# -*- coding: utf-8 -*-
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

from oneview_module_loader import TaskFactsModule

from hpe_test_utils import FactsParamsTestCase

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


class TaskFactsSpec(unittest.TestCase,
                    FactsParamsTestCase):

    def setUp(self):
        self.configure_mocks(self, TaskFactsModule)
        FactsParamsTestCase.configure_client_mock(self, self.mock_ov_client.tasks)

    def test_get_all(self):
        self.mock_ov_client.tasks.get_all.return_value = ALL_TASKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        TaskFactsModule().run()

        self.mock_ov_client.tasks.get_all.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )

    def test_get_all_with_filter(self):
        self.mock_ov_client.tasks.get_all.return_value = ALL_TASKS
        self.mock_ansible_module.params = PARAMS_GET_ALL_WITH_FILTER

        TaskFactsModule().run()

        self.mock_ov_client.tasks.get_all.assert_called_once_with(filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )

    def test_get_all_with_filter_and_count(self):
        self.mock_ov_client.tasks.get_all.return_value = ALL_TASKS
        self.mock_ansible_module.params = PARAMS_GET_ALL_WITH_FILTER_AND_COUNT

        TaskFactsModule().run()

        self.mock_ov_client.tasks.get_all.assert_called_once_with(
            filter=FILTER_BY_ASSOCIATED_RESOURCE_NAME,
            count=COUNT
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(tasks=ALL_TASKS)
        )


if __name__ == '__main__':
    unittest.main()
