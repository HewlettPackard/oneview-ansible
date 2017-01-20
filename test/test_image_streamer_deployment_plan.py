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

from image_streamer_deployment_plan import DeploymentPlanModule, DEPLOYMENT_PLAN_ALREADY_UPDATED, \
    DEPLOYMENT_PLAN_ALREADY_ABSENT, DEPLOYMENT_PLAN_CREATED, DEPLOYMENT_PLAN_DELETED, EXAMPLES, \
    DEPLOYMENT_PLAN_UPDATED, I3S_BUILD_PLAN_WAS_NOT_FOUND
from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'


class DeploymentPlanSpec(unittest.TestCase,
                         ModuleContructorTestCase,
                         ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case

    ErrorHandlingTestCase has common tests for the module error handling.
    """
    def setUp(self):
        self.configure_mocks(self, DeploymentPlanModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        ErrorHandlingTestCase.configure(self, method_to_fire=self.i3s.deployment_plans.get_by)

        # Load scenarios from module examples
        self.DEPLOYMENT_PLAN_EXAMPLES = yaml.load(EXAMPLES)
        self.DEPLOYMENT_PLAN_CREATE = self.DEPLOYMENT_PLAN_EXAMPLES[0]['image_streamer_deployment_plan']
        self.DEPLOYMENT_PLAN_UPDATE = self.DEPLOYMENT_PLAN_EXAMPLES[1]['image_streamer_deployment_plan']
        self.DEPLOYMENT_PLAN_DELETE = self.DEPLOYMENT_PLAN_EXAMPLES[2]['image_streamer_deployment_plan']
        self.DEPLOYMENT_PLAN = dict(
            name="Deployment Plan name",
            uri="/rest/deployment-plans/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_create_new_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = []
        self.i3s.build_plans.get_by.return_value = [{'uri': '/rest/build-plans/1'}]
        self.i3s.deployment_plans.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_CREATE

        DeploymentPlanModule().run()

        self.i3s.deployment_plans.create.assert_called_once_with(
            {'oeBuildPlanURI': '/rest/build-plans/1',
             'hpProvided': 'false',
             'description': 'Description of this Deployment Plan',
             'name': 'Demo Deployment Plan'}
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DEPLOYMENT_PLAN_CREATED,
            ansible_facts=dict(deployment_plan={"name": "name"})
        )

    def test_update_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.i3s.deployment_plans.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_UPDATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DEPLOYMENT_PLAN_UPDATED,
            ansible_facts=dict(deployment_plan={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN_UPDATE['data']]
        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_UPDATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DEPLOYMENT_PLAN_ALREADY_UPDATED,
            ansible_facts=dict(deployment_plan=self.DEPLOYMENT_PLAN_UPDATE['data'])
        )

    def test_delete_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN]

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_DELETE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=DEPLOYMENT_PLAN_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = []

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_DELETE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=DEPLOYMENT_PLAN_ALREADY_ABSENT
        )

    def test_should_fail_when_build_plan_not_found(self):
        self.i3s.deployment_plans.get_by.return_value = []
        self.i3s.build_plans.get_by.return_value = None

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_CREATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=I3S_BUILD_PLAN_WAS_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
