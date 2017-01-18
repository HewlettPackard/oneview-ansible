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

from image_streamer_plan_script import PlanScriptModule, PLAN_SCRIPT_ALREADY_UPDATED, \
    PLAN_SCRIPT_ALREADY_ABSENT, PLAN_SCRIPT_CREATED, PLAN_SCRIPT_DELETED, EXAMPLES, \
    PLAN_SCRIPT_UPDATED, PLAN_SCRIPT_CONTENT_ATTRIBUTE_MANDATORY, PLAN_SCRIPT_DIFFERENCES_RETRIEVED
from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'


class PlanScriptSpec(unittest.TestCase,
                     ModuleContructorTestCase,
                     ErrorHandlingTestCase):
    """
    Test the module constructor

    ModuleContructorTestCase has common tests for class constructor and main function

    ErrorHandlingTestCase has common tests for the module error handling.
    """
    def setUp(self):
        self.configure_mocks(self, PlanScriptModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        ErrorHandlingTestCase.configure_client_mock(self, self.i3s.plan_scripts)

        # Load scenarios from module examples
        self.PLAN_SCRIPT_EXAMPLES = yaml.load(EXAMPLES)
        self.PLAN_SCRIPT_CREATE = self.PLAN_SCRIPT_EXAMPLES[0]['image_streamer_plan_script']
        self.PLAN_SCRIPT_UPDATE = self.PLAN_SCRIPT_EXAMPLES[1]['image_streamer_plan_script']
        self.PLAN_SCRIPT_DIFFERENCES = self.PLAN_SCRIPT_EXAMPLES[2]['image_streamer_plan_script']
        self.PLAN_SCRIPT_DELETE = self.PLAN_SCRIPT_EXAMPLES[4]['image_streamer_plan_script']
        self.PLAN_SCRIPT = dict(
            name="Plan Script name",
            uri="/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_create_new_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = []
        self.i3s.plan_scripts.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_CREATE

        PlanScriptModule().run()

        self.i3s.plan_scripts.create.assert_called_once_with(
            {'content': 'echo "test script"',
             'planType': 'deploy',
             'hpProvided': False,
             'description': 'Description of this plan script',
             'name': 'Demo Plan Script'})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PLAN_SCRIPT_CREATED,
            ansible_facts=dict(plan_script={"name": "name"})
        )

    def test_update_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]
        self.i3s.plan_scripts.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PLAN_SCRIPT_UPDATED,
            ansible_facts=dict(plan_script={"name": "name"})
        )

    def test_retrieve_plan_script_content_differences(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]
        self.i3s.plan_scripts.retrieve_differences.return_value = {"differences": []}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DIFFERENCES

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PLAN_SCRIPT_DIFFERENCES_RETRIEVED,
            ansible_facts=dict(plan_script_differences={"differences": []})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT_UPDATE['data']]
        self.mock_ansible_module.params = self.PLAN_SCRIPT_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PLAN_SCRIPT_ALREADY_UPDATED,
            ansible_facts=dict(plan_script=self.PLAN_SCRIPT_UPDATE['data'])
        )

    def test_delete_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=PLAN_SCRIPT_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = []

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=PLAN_SCRIPT_ALREADY_ABSENT
        )

    def test_should_fail_when_mandatory_attributes_are_missing(self):
        self.i3s.plan_scripts.get_by.return_value = []

        del self.PLAN_SCRIPT_DIFFERENCES['data']['content']

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DIFFERENCES

        PlanScriptModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PLAN_SCRIPT_CONTENT_ATTRIBUTE_MANDATORY
        )


if __name__ == '__main__':
    unittest.main()
