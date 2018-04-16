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

import pytest

from hpe_test_utils import ImageStreamerBaseTest
from oneview_module_loader import BuildPlanModule

FAKE_MSG_ERROR = 'Fake message error'

BUILD_PLAN_CREATE = dict(
    config='config.json',
    api_version=600,
    state='present',
    data=dict(
        name='Demo OS Build Plan',
        description="oebuildplan",
        oeBuildPlanType="deploy"
    ))

BUILD_PLAN_UPDATE = dict(
    config='config.json',
    api_version=600,
    state='present',
    data=dict(
        name='Demo OS Build Plan',
        newName='OS Build Plan Renamed',
        description="oebuildplan"
    ))

BUILD_PLAN_DELETE = dict(
    config='config.json',
    api_version=600,
    state='absent',
    data=dict(
        name='Demo OS Build Plan',
    ))


@pytest.mark.resource(TestBuildPlanModule='build_plans')
class TestBuildPlanModule(ImageStreamerBaseTest):
    """
    ImageStreamerBaseTest has tests for main function,
    also provides the mocks used in this test case
    """

    @pytest.fixture(autouse=True)
    def specific_set_up(self):
        # Load scenarios from module examples
        self.BUILD_PLAN_CREATE = BUILD_PLAN_CREATE
        self.BUILD_PLAN_UPDATE = BUILD_PLAN_UPDATE
        self.BUILD_PLAN_DELETE = BUILD_PLAN_DELETE

    def test_should_create_new_build_plan(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_CREATE

        BuildPlanModule().run()

        self.resource.create.assert_called_once_with(
            {'name': 'Demo OS Build Plan',
             'description': "oebuildplan",
             'oeBuildPlanType': "deploy"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_CREATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_update_the_build_plan(self):
        self.resource.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_UPDATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [self.BUILD_PLAN_UPDATE['data']]
        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(build_plan=self.BUILD_PLAN_UPDATE['data'])
        )

    def test_should_delete_the_build_plan(self):
        self.resource.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_build_plan(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
