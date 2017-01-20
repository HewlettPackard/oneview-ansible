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

from image_streamer_os_volume_facts import OsVolumeFactsModule, EXAMPLES
from utils import ModuleContructorTestCase
from utils import FactsParamsTestCase
from utils import ErrorHandlingTestCase

ERROR_MSG = 'Fake message error'


class OsVolumeFactsSpec(unittest.TestCase,
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
        self.configure_mocks(self, OsVolumeFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()
        ErrorHandlingTestCase.configure(self, method_to_fire=self.i3s.os_volumes.get_by)

        FactsParamsTestCase.configure_client_mock(self, self.i3s.os_volumes)

        # Load scenarios from module examples
        self.OS_VOLUME_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.PLAY_GET_ALL = self.OS_VOLUME_FACTS_EXAMPLES[0]['image_streamer_os_volume_facts']
        self.PLAY_GET_BY_NAME = self.OS_VOLUME_FACTS_EXAMPLES[4]['image_streamer_os_volume_facts']

        self.OS_VOLUME = dict(
            name="OS Volume Name",
            uri="/rest/os-volumes/a3b3c234-2ei0-b99o-jh778jsdkl2n5")

    def test_get_all_os_volumes(self):
        self.i3s.os_volumes.get_all.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.PLAY_GET_ALL

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )

    def test_get_os_volume_by_name(self):
        self.i3s.os_volumes.get_by.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.PLAY_GET_BY_NAME

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )


if __name__ == '__main__':
    unittest.main()
