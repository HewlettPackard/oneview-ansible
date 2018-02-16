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
from oneview_module_loader import DeploymentGroupFactsModule


@pytest.mark.resource(TestDeploymentGroupFactsModule='deployment_groups')
class TestDeploymentGroupFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    DEPLOYMENT_GROUP = dict(
        name="OSS",
        uri="/rest/deployment-group/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_deployment_groups(self):
        self.resource.get_all.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.EXAMPLES[0]['image_streamer_deployment_group_facts']

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )

    def test_get_a_deployment_group_by_name(self):
        self.resource.get_by.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.EXAMPLES[4]['image_streamer_deployment_group_facts']

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )


if __name__ == '__main__':
    pytest.main([__file__])
