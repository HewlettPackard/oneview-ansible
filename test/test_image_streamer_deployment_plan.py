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
import unittest

from oneview_module_loader import DeploymentPlanModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class DeploymentPlanSpec(unittest.TestCase,
                         OneViewBaseTestCase):
    """
    OneViewBaseTestCase has common tests for main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, DeploymentPlanModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        # Load scenarios from module examples
        self.DEPLOYMENT_PLAN_CREATE = self.EXAMPLES[0]['image_streamer_deployment_plan']
        self.DEPLOYMENT_PLAN_UPDATE = self.EXAMPLES[1]['image_streamer_deployment_plan']
        self.DEPLOYMENT_PLAN_DELETE = self.EXAMPLES[2]['image_streamer_deployment_plan']
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
            msg=DeploymentPlanModule.MSG_CREATED,
            ansible_facts=dict(deployment_plan={"name": "name"})
        )

    def test_update_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.i3s.deployment_plans.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_UPDATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DeploymentPlanModule.MSG_UPDATED,
            ansible_facts=dict(deployment_plan={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN_UPDATE['data']]
        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_UPDATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DeploymentPlanModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(deployment_plan=self.DEPLOYMENT_PLAN_UPDATE['data'])
        )

    def test_delete_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = [self.DEPLOYMENT_PLAN]

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_DELETE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DeploymentPlanModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_deployment_plan(self):
        self.i3s.deployment_plans.get_by.return_value = []

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_DELETE

        DeploymentPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DeploymentPlanModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_build_plan_not_found(self):
        self.i3s.deployment_plans.get_by.return_value = []
        self.i3s.build_plans.get_by.return_value = None

        self.mock_ansible_module.params = self.DEPLOYMENT_PLAN_CREATE

        DeploymentPlanModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=DeploymentPlanModule.MSG_BUILD_PLAN_WAS_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
