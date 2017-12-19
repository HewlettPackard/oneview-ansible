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

from oneview_module_loader import OsVolumeFactsModule
from hpe_test_utils import ImageStreamerBaseFactsTest

ERROR_MSG = 'Fake message error'


@pytest.mark.resource(TestOsVolumeFactsModule='os_volumes')
class TestOsVolumeFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    OS_VOLUME = dict(
        name="OS Volume Name",
        uri="/rest/os-volumes/a3b3c234-2ei0-b99o-jh778jsdkl2n5")

    def test_get_all_os_volumes(self):
        self.resource.get_all.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.EXAMPLES[0]['image_streamer_os_volume_facts']

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )

    def test_get_os_volume_by_name(self):
        self.resource.get_by.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.EXAMPLES[4]['image_streamer_os_volume_facts']

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )


if __name__ == '__main__':
    pytest.main([__file__])
