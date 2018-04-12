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
from oneview_module_loader import OsVolumeFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = {"config": "config.json"}

PARAMS_GET_BY_NAME = {"config": "config.json", "name": "Test OS Volume"}

PARAMS_GET_STORAGE = {"config": "config.json", "name": "Test OS Volume",
                      "options": ["getStorage"]}


@pytest.mark.resource(TestOsVolumeFactsModule='os_volumes')
class TestOsVolumeFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    OS_VOLUME = {"name": "OS Volume Name",
                 "uri": "/rest/os-volumes/a3b3c234-2ei0-b99o-jh778jsdkl2n5"}

    OS_VOLUME_STORAGE = {"name": "OS Volume Name", "snapshots": []}

    def test_get_all_os_volumes(self):
        self.resource.get_all.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = PARAMS_GET_ALL

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )

    def test_get_os_volume_by_name(self):
        self.resource.get_by.return_value = [self.OS_VOLUME]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )

<<<<<<< 471aa3cbff01d3d78ad937f082ccfba9165d8e92
    def test_get_storage(self):
        self.resource.get_storage.return_value = [self.OS_VOLUME_STORAGE]
        self.resource.get_by.return_value = [self.OS_VOLUME]

        self.mock_ansible_module.params = PARAMS_GET_STORAGE
=======
    def test_get_os_volume_get_storage(self):
        self.resource.get_storage.return_value = [self.OS_VOLUME_STORAGE]
        self.mock_ansible_module.params = self.EXAMPLES[4]['image_streamer_os_volume_facts']
>>>>>>> Done with testing

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
<<<<<<< 471aa3cbff01d3d78ad937f082ccfba9165d8e92
            ansible_facts=dict(os_volumes=[self.OS_VOLUME], storage=[self.OS_VOLUME_STORAGE])
=======
            ansible_facts=dict(os_volumes=[self.OS_VOLUME_STORAGE])
>>>>>>> Done with testing
        )


if __name__ == '__main__':
    pytest.main([__file__])
