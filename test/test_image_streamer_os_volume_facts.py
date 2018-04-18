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

PARAMS_GET_STORAGE = {"config": "config.json",
                      "name": "Test OS Volume",
                      "options": [{"getStorage": True}]}

PARAMS_GET_LOGS = {"config": "config.json",
                   "name": "Test OS Volume",
                   "options": [{"getArchivedLogs": {"file_path": "fake"}}]}


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

    def test_get_archived_log(self):
        self.resource.get_by.return_value = [self.OS_VOLUME]
        self.resource.download_archived.return_value = 'fake'

        self.mock_ansible_module.params = PARAMS_GET_LOGS

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME], log_file_path="fake")
        )

    def test_get_storage(self):
        self.resource.get_storage.return_value = [self.OS_VOLUME_STORAGE]
        self.resource.get_by.return_value = [self.OS_VOLUME]

        self.mock_ansible_module.params = PARAMS_GET_STORAGE

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME], storage=[self.OS_VOLUME_STORAGE])
        )


if __name__ == '__main__':
    pytest.main([__file__])
