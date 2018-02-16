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
from oneview_module_loader import GoldenImageFactsModule

ERROR_MSG = 'Fake message error'


@pytest.mark.resource(TestGoldenImageFactsModule='golden_images')
class TestGoldenImageFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    GOLDEN_IMAGE = dict(
        name="Golden Image name",
        uri="/rest/golden-image/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_golden_images(self):
        self.resource.get_all.return_value = [self.GOLDEN_IMAGE]
        self.mock_ansible_module.params = self.EXAMPLES[0]['image_streamer_golden_image_facts']

        GoldenImageFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(golden_images=[self.GOLDEN_IMAGE])
        )

    def test_get_a_golden_image_by_name(self):
        self.resource.get_by.return_value = [self.GOLDEN_IMAGE]
        self.mock_ansible_module.params = self.EXAMPLES[4]['image_streamer_golden_image_facts']

        GoldenImageFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(golden_images=[self.GOLDEN_IMAGE])
        )


if __name__ == '__main__':
    pytest.main([__file__])
