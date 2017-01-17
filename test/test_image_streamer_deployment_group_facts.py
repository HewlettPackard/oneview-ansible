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

from image_streamer_deployment_group_facts import DeploymentGroupFactsModule, EXAMPLES
from test.utils import ModuleContructorTestCase
from test.utils import FactsParamsTestCase
from test.utils import ErrorHandlingTestCase

ERROR_MSG = 'Fake message error'


class DeploymentGroupFactsSpec(unittest.TestCase,
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
        self.configure_mocks(self, DeploymentGroupFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.deployment_groups)
        ErrorHandlingTestCase.configure_client_mock(self, self.i3s.deployment_groups)

        # Load scenarios from module examples
        self.DEPLOYMENT_GROUP_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.DEPLOYMENT_GROUP_FACTS_EXAMPLES[0]['image_streamer_deployment_group_facts']
        self.TASK_GET_BY_NAME = self.DEPLOYMENT_GROUP_FACTS_EXAMPLES[4]['image_streamer_deployment_group_facts']

        self.DEPLOYMENT_GROUP = dict(
            name="OSS",
            uri="/rest/deployment-group/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_deployment_groups(self):
        self.i3s.deployment_groups.get_all.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )

    def test_get_a_deployment_group_by_name(self):
        self.i3s.deployment_groups.get_by.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )


if __name__ == '__main__':
    unittest.main()
