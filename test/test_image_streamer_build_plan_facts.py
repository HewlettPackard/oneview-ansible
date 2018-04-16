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

from hpe_test_utils import ImageStreamerBaseFactsTest
from oneview_module_loader import BuildPlanFactsModule

ERROR_MSG = 'Fake message error'

BUILD_PLAN_FACTS = dict(
    config='config.json'
)

BUILD_PLAN_BY_NAME = dict(
    config='config.json',
    name='name'
)


@pytest.mark.resource(TestBuildPlanFactsModule='build_plans')
class TestBuildPlanFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """
    BUILD_PLAN = dict(name="Build Plan name", uri="/rest/build-plans/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_build_plans(self):
        self.resource.get_all.return_value = [self.BUILD_PLAN]
        self.mock_ansible_module.params = BUILD_PLAN_FACTS

        BuildPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(build_plans=[self.BUILD_PLAN])
        )

    def test_get_a_build_plan_by_name(self):
        self.resource.get_by.return_value = [self.BUILD_PLAN]
        self.mock_ansible_module.params = BUILD_PLAN_BY_NAME

        BuildPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(build_plans=[self.BUILD_PLAN])
        )


if __name__ == '__main__':
    pytest.main([__file__])
