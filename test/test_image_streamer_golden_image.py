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

from image_streamer_golden_image import GoldenImageModule, GOLDEN_IMAGE_ALREADY_UPDATED, GOLDEN_IMAGE_UPLOADED, \
    GOLDEN_IMAGE_ALREADY_ABSENT, GOLDEN_IMAGE_CREATED, GOLDEN_IMAGE_DELETED, EXAMPLES, I3S_BUILD_PLAN_WAS_NOT_FOUND, \
    GOLDEN_IMAGE_UPDATED, I3S_CANT_CREATE_AND_UPLOAD, I3S_MISSING_MANDATORY_ATTRIBUTES, I3S_OS_VOLUME_WAS_NOT_FOUND, \
    GOLDEN_IMAGE_DOWNLOADED
from test.utils import ModuleContructorTestCase, PreloadedMocksBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class GoldenImageSpec(unittest.TestCase, ModuleContructorTestCase, PreloadedMocksBaseTestCase):
    """
    Test the module constructor
    ModuleContructorTestCase has common tests for class constructor and main function
    """

    def setUp(self):
        self.configure_mocks(self, GoldenImageModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        # Load scenarios from module examples
        self.GOLDEN_IMAGE_EXAMPLES = yaml.load(EXAMPLES)
        self.GOLDEN_IMAGE_CREATE = self.GOLDEN_IMAGE_EXAMPLES[0]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_UPLOAD = self.GOLDEN_IMAGE_EXAMPLES[1]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_UPDATE = self.GOLDEN_IMAGE_EXAMPLES[2]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_DOWNLOAD = self.GOLDEN_IMAGE_EXAMPLES[3]['image_streamer_golden_image']
        self.GOLDEN_IMAGE_DELETE = self.GOLDEN_IMAGE_EXAMPLES[4]['image_streamer_golden_image']

    def test_create_new_golden_image(self):
        self.i3s.golden_images.get_by.return_value = []
        self.i3s.golden_images.create.return_value = {"name": "name"}
        self.i3s.os_volumes.get_by_name.return_value = {'uri': '/rest/os-volumes/1'}
        self.i3s.build_plans.get_by.return_value = [{'uri': '/rest/build-plans/1'}]

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.i3s.golden_images.create.assert_called_once_with(
            {'osVolumeURI': '/rest/os-volumes/1',
             'description': 'Test Description',
             'buildPlanUri': '/rest/build-plans/1',
             'name': 'Demo Golden Image creation',
             'imageCapture': 'true'})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GOLDEN_IMAGE_CREATED,
            ansible_facts=dict(golden_image={"name": "name"})
        )

    def test_upload_a_golden_image(self):
        self.i3s.golden_images.get_by.return_value = []
        self.i3s.golden_images.upload.return_value = True

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPLOAD

        file_path = self.GOLDEN_IMAGE_UPLOAD['data']['localImageFilePath']

        GoldenImageModule().run()

        self.i3s.golden_images.upload.assert_called_once_with(
            file_path,
            self.GOLDEN_IMAGE_UPLOAD['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GOLDEN_IMAGE_UPLOADED,
            ansible_facts=dict(golden_image=None)
        )

    def test_update_golden_image(self):
        self.i3s.golden_images.get_by.return_value = [self.GOLDEN_IMAGE_CREATE['data']]
        self.i3s.golden_images.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPDATE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GOLDEN_IMAGE_UPDATED,
            ansible_facts=dict(golden_image={"name": "name"})
        )

    def test_golden_image_download(self):
        golden_image = self.GOLDEN_IMAGE_CREATE['data']
        golden_image['uri'] = '/rest/golden-images/1'

        self.i3s.golden_images.get_by.return_value = [golden_image]
        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DOWNLOAD

        GoldenImageModule().run()

        download_file = self.GOLDEN_IMAGE_DOWNLOAD['data']['destination_file_path']
        self.i3s.golden_images.download.assert_called_once_with('/rest/golden-images/1', download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=GOLDEN_IMAGE_DOWNLOADED,
            ansible_facts={})

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.golden_images.get_by.return_value = [self.GOLDEN_IMAGE_UPDATE['data']]

        del self.GOLDEN_IMAGE_UPDATE['data']['newName']

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_UPDATE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=GOLDEN_IMAGE_ALREADY_UPDATED,
            ansible_facts=dict(golden_image=self.GOLDEN_IMAGE_UPDATE['data'])
        )

    def test_delete_golden_image(self):
        self.i3s.golden_images.get_by.return_value = [self.GOLDEN_IMAGE_CREATE['data']]

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DELETE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=GOLDEN_IMAGE_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_golden_image(self):
        self.i3s.golden_images.get_by.return_value = []

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DELETE

        GoldenImageModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=GOLDEN_IMAGE_ALREADY_ABSENT
        )

    def test_should_fail_when_create_raises_exception(self):
        self.i3s.golden_images.get_by.return_value = []
        self.i3s.golden_images.create.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_present_is_incosistent(self):
        self.i3s.golden_images.get_by.return_value = []
        self.i3s.os_volumes.get_by_name.return_value = {'uri': '/rest/os-volumes/1'}

        self.GOLDEN_IMAGE_CREATE['data']['localImageFilePath'] = 'filename'

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=I3S_CANT_CREATE_AND_UPLOAD
        )

    def test_should_fail_when_mandatory_attributes_are_missing(self):
        self.i3s.golden_images.get_by.return_value = []

        del self.GOLDEN_IMAGE_CREATE['data']['osVolumeName']

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=I3S_MISSING_MANDATORY_ATTRIBUTES
        )

    def test_should_fail_when_os_volume_not_found(self):
        self.i3s.golden_images.get_by.return_value = []

        self.i3s.os_volumes.get_by_name.return_value = None

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=I3S_OS_VOLUME_WAS_NOT_FOUND
        )

    def test_should_fail_when_build_plan_not_found(self):
        self.i3s.golden_images.get_by.return_value = []
        self.i3s.build_plans.get_by.return_value = None

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_CREATE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=I3S_BUILD_PLAN_WAS_NOT_FOUND
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.i3s.golden_images.get_by.return_value = [self.GOLDEN_IMAGE_CREATE]
        self.i3s.golden_images.delete.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = self.GOLDEN_IMAGE_DELETE

        GoldenImageModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
