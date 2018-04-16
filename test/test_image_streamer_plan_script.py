#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import mock
import pytest

from hpe_test_utils import ImageStreamerBaseTest
from oneview_module_loader import PlanScriptModule

FAKE_MSG_ERROR = 'Fake message error'

PARAMS_CREATE = {"config": "config.json",
                 "state": "present",
                 "data": {"name": "Demo Plan Script"}}

PARAMS_UPDATE = {"config": "config.json",
                 "state": "present",
                 "data": {"name": "Demo Plan Script"}}

PARAMS_DIFFERENCE = {"config": "config.json",
                     "state": "differences_retrieved",
                     "data": {"name": "Demo Plan Script",
                              "content": "test script"}}

PARAMS_DELETE = {"config": "config.json",
                 "state": "absent",
                 "data": {"name": "Demo Plan Script"}}


@pytest.mark.resource(TestPlanScriptModule='plan_scripts')
class TestPlanScriptModule(ImageStreamerBaseTest):
    """
    ImageStreamerBaseTest has common test for main function
    """

    @pytest.fixture(autouse=True)
    def specific_set_up(self):
        self.PLAN_SCRIPT = dict(
            name="Plan Script name",
            uri="/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_create_new_plan_script(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "Demo Plan Script"}

        self.mock_ansible_module.params = PARAMS_CREATE

        PlanScriptModule().run()

        self.resource.create.assert_called_once_with({'name': 'Demo Plan Script'})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_CREATED,
            ansible_facts=dict(plan_script={"name": "Demo Plan Script"})
        )

    def test_update_plan_script(self):
        self.resource.get_by.return_value = [self.PLAN_SCRIPT]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_UPDATED,
            ansible_facts=dict(plan_script={"name": "name"})
        )

    def test_retrieve_plan_script_content_differences(self):
        self.resource.get_by.return_value = [self.PLAN_SCRIPT]
        self.resource.retrieve_differences.return_value = {"differences": []}

        self.mock_ansible_module.params = PARAMS_DIFFERENCE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_DIFFERENCES_RETRIEVED,
            ansible_facts=dict(plan_script_differences={"differences": []})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [PARAMS_UPDATE['data']]
        self.mock_ansible_module.params = PARAMS_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(plan_script=PARAMS_UPDATE['data'])
        )

    def test_delete_plan_script(self):
        self.resource.get_by.return_value = [self.PLAN_SCRIPT]

        self.mock_ansible_module.params = PARAMS_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_plan_script(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_mandatory_attributes_are_missing(self):
        self.resource.get_by.return_value = []

        del PARAMS_DIFFERENCE['data']['content']

        self.mock_ansible_module.params = PARAMS_DIFFERENCE

        PlanScriptModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=PlanScriptModule.MSG_CONTENT_ATTRIBUTE_MANDATORY)


if __name__ == '__main__':
    pytest.main([__file__])
