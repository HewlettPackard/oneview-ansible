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
from oneview_module_loader import DeploymentPlanFactsModule

ERROR_MSG = 'Fake message error'

DEPLOYMENT_PLAN_NAME = 'Deployment Plan name'
DEPLOYMENT_PLAN_URI = '/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0'

PARAMS_GET_ALL = dict(
    config='config.json',
    state='present'
)
PARAMS_GET_BY_NAME = dict(
    config='config.json',
    state='present',
    name=DEPLOYMENT_PLAN_NAME
)

PARAMS_GET_USEDBY = dict(
    config='config.json',
    options='usedby',
    name=DEPLOYMENT_PLAN_NAME
)

PARAMS_GET_OSDP = dict(
    config='config.json',
    options='osdp',
    name=DEPLOYMENT_PLAN_NAME
)


@pytest.mark.resource(TestDeploymentPlanFactsModule='deployment_plans')
class TestDeploymentPlanFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    DEPLOYMENT_PLAN = dict(
        name=DEPLOYMENT_PLAN_NAME,
        uri=DEPLOYMENT_PLAN_URI)

    def test_get_all_deployment_plans(self):
        self.resource.get_all.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = PARAMS_GET_ALL

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )

    def test_get_a_deployment_plan_by_name(self):
        self.resource.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )

    def test_get_a_deployment_plan_usedby_by_name(self):
        self.resource.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = PARAMS_GET_USEDBY

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )

    def test_get_a_deployment_plan_osdp_by_name(self):
        self.resource.get_by.return_value = [self.DEPLOYMENT_PLAN]
        self.mock_ansible_module.params = PARAMS_GET_OSDP

        DeploymentPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_plans=[self.DEPLOYMENT_PLAN])
        )


if __name__ == '__main__':
    pytest.main([__file__])
