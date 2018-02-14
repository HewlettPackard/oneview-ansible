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

import mock
import pytest

from hpe_test_utils import ImageStreamerBaseTest
from oneview_module_loader import GoldenImageModule

FAKE_MSG_ERROR = 'Fake message error'


@pytest.mark.resource(TestGoldenImageModule='golden_images')
class TestGoldenImageModule(ImageStreamerBaseTest):
    """
    ImageStreamerBaseTest has common test for main function,
    also provides the mocks used in this test case
    """

    @pytest.fixture(autouse=True)
    def specific_set_up(self):
        # Load scenarios from module examples
        self.GOLDEN_IMAGE_CREATE = self.EXAMPLES[0]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_UPLOAD = self.EXAMPLES[1]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_UPDATE = self.EXAMPLES[2]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_DOWNLOAD = self.EXAMPLES[3]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_ARCHIVE_DOWNLOAD = self.EXAMPLES[4]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_DELETE = self.EXAMPLES[5]['image_streamer_golden_image']

    def test_create_new_golden_image(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "name"}
        self.mock_ov_client.os_volumes.get_by_name.return_value = {'uri': '/rest/os-volumes/1'}
        self.mock_ov_client.build_plans.get_by.return_value = [{'uri': '/rest/build-plans/1'}]

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.resource.create.assert_called_once_with(
            {'osVolumeURI': '/rest/os-volumes/1',
             'description': 'Test Description',
             'buildPlanUri': '/rest/build-plans/1',
             'name': 'Demo Golden Image creation',
             'imageCapture': 'true'})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_CREATED,
            ansible_facts=dict(golden_image={"name": "name"})
        )

    def test_upload_a_golden_image(self):
        self.resource.get_by.return_value = []
        self.resource.upload.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPLOAD

        file_path = self.GOLDEN_IMAGE_UPLOAD['data']['localImageFilePath']

        GoldenImageModule().run()

        self.resource.upload.assert_called_once_with(
            file_path,
            self.GOLDEN_IMAGE_UPLOAD['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_UPLOADED,
            ansible_facts=dict(golden_image={"name": "name"})
        )

    def test_update_golden_image(self):
        self.resource.get_by.return_value = [self.GOLDEN_IMAGE_CREATE['data']]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPDATE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_UPDATED,
            ansible_facts=dict(golden_image={"name": "name"})
        )

    def test_golden_image_download(self):
        golden_image = self.GOLDEN_IMAGE_CREATE['data']
        golden_image['uri'] = '/rest/golden-images/1'

        self.resource.get_by.return_value = [golden_image]
        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DOWNLOAD

        GoldenImageModule().run()

        download_file = self.GOLDEN_IMAGE_DOWNLOAD['data']['destination_file_path']
        self.resource.download.assert_called_once_with('/rest/golden-images/1', download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_DOWNLOADED,
            ansible_facts={})

    def test_golden_image_download_nonexistent(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DOWNLOAD

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_WAS_NOT_FOUND,)

    def test_golden_image_archive_download(self):
        golden_image = self.GOLDEN_IMAGE_CREATE['data']
        golden_image['uri'] = '/rest/golden-images/1'

        self.resource.get_by.return_value = [golden_image]
        self.mock_ansible_module.params = self.GOLDEN_IMAGE_ARCHIVE_DOWNLOAD

        GoldenImageModule().run()

        download_file = self.GOLDEN_IMAGE_ARCHIVE_DOWNLOAD['data']['destination_file_path']
        self.resource.download_archive.assert_called_once_with('/rest/golden-images/1', download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_ARCHIVE_DOWNLOADED,
            ansible_facts={})

    def test_golden_image_archive_download_nonexistent(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = self.GOLDEN_IMAGE_ARCHIVE_DOWNLOAD

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_WAS_NOT_FOUND)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [self.GOLDEN_IMAGE_UPDATE['data']]

        del self.GOLDEN_IMAGE_UPDATE['data']['newName']

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPDATE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=GoldenImageModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(golden_image=self.GOLDEN_IMAGE_UPDATE['data'])
        )

    def test_delete_golden_image(self):
        self.resource.get_by.return_value = [self.GOLDEN_IMAGE_CREATE['data']]

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DELETE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GoldenImageModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_golden_image(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DELETE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=GoldenImageModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_present_is_incosistent(self):
        self.resource.get_by.return_value = []
        self.mock_ov_client.os_volumes.get_by_name.return_value = {'uri': '/rest/os-volumes/1'}

        self.GOLDEN_IMAGE_CREATE['data']['localImageFilePath'] = 'filename'

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_CANT_CREATE_AND_UPLOAD)

    def test_should_fail_when_mandatory_attributes_are_missing(self):
        self.resource.get_by.return_value = []

        del self.GOLDEN_IMAGE_CREATE['data']['osVolumeName']

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_MISSING_MANDATORY_ATTRIBUTES)

    def test_should_fail_when_os_volume_not_found(self):
        self.resource.get_by.return_value = []

        self.mock_ov_client.os_volumes.get_by_name.return_value = None

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_OS_VOLUME_WAS_NOT_FOUND)

    def test_should_fail_when_build_plan_not_found(self):
        self.resource.get_by.return_value = []
        self.mock_ov_client.build_plans.get_by.return_value = None

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=GoldenImageModule.MSG_BUILD_PLAN_WAS_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
