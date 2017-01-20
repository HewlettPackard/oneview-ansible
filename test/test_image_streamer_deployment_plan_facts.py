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

from image_streamer_deployment_plan_facts import DeploymentPlanFactsModule, EXAMPLES
from test.utils import ModuleContructorTestCase
from test.utils import FactsParamsTestCase
from test.utils import ErrorHandlingTestCase

ERROR_MSG = 'Fake message error'


class DeploymentPlanFactsSpec(unittest.TestCase,
                              ModuleContructorTestCase,
                              FactsParamsTestCase,
                              ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for the class constructor and the main function, and also provides the
    mocks used in this test class.

    FactsParamsTestCase has common tests for the parameters support.

    ErrorHandlingTestCase has common tests for the module error handling.
    """
    def setUp(self):
        self.configure_mocks(self, DeploymentPlanFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.deployment_plans)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.i3s.deployment_plans.get_by)

        # Load scenarios from module examples
        self.DEPLOYMENT_PLAN_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.DEPLOYMENT_PLAN_FACTS_EXAMPLES[0]['image_streamer_deployment_plan_facts']
        self.TASK_GET_BY_NAME = self.DEPLOYMENT_PLAN_FACTS_EXAMPLES[4]['image_streamer_deployment_plan_facts']

        self.DEPLOYMENT_PLAN = dict(
            name="Deployment Plan name",
            uri="/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_deployment_plans(self):
        self.i3s.deployment_plans.get_all.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )

    def test_get_a_deployment_plan_by_name(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )


if __name__ == '__main__':
    unittest.main()
