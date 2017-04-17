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
import unittest

from oneview_module_loader import BuildPlanModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class BuildPlanSpec(unittest.TestCase,
                    OneViewBaseTestCase):
    """
    OneViewBaseTestCase has tests for main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, BuildPlanModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        # Load scenarios from module examples
        self.BUILD_PLAN_CREATE = self.EXAMPLES[0]['image_streamer_build_plan']
        self.BUILD_PLAN_UPDATE = self.EXAMPLES[1]['image_streamer_build_plan']
        self.BUILD_PLAN_DELETE = self.EXAMPLES[2]['image_streamer_build_plan']

    def test_should_create_new_build_plan(self):
        self.i3s.build_plans.get_by.return_value = []
        self.i3s.build_plans.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_CREATE

        BuildPlanModule().run()

        self.i3s.build_plans.create.assert_called_once_with(
            {'name': 'Demo OS Build Plan',
             'description': "oebuildplan",
             'oeBuildPlanType': "deploy"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_CREATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_update_the_build_plan(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]
        self.i3s.build_plans.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_UPDATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_UPDATE['data']]

        del self.BUILD_PLAN_UPDATE['data']['newName']

        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(build_plan=self.BUILD_PLAN_UPDATE['data'])
        )

    def test_should_delete_the_build_plan(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_build_plan(self):
        self.i3s.build_plans.get_by.return_value = []

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
