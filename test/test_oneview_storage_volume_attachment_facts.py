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

from oneview_module_loader import StorageVolumeAttachmentFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

URI = "/rest/storage-volume-attachments?" \
      "filter=storageVolumeUri='/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA'" \
      "&filter=hostName='ProfileTest'"

PARAMS_GET_ALL = dict(
    config='config.json'
)

PARAMS_GET_ONE = dict(
    config='config.json',
    serverProfileName="ProfileTest",
    storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"
)

PARAMS_GET_ONE_VOLUME_NAME = dict(
    config='config.json',
    serverProfileName="ProfileTest",
    storageVolumeName="VolumeTest"
)

ATTACHMENT = {
    "name": "Storage Volume Attachment Name",
    "uri": "/rest/storage-volume-attachments/ED247E27"
}

RETURN_GET_BY_PROFILE_AND_VOLUME = {
    'members': [ATTACHMENT]
}


class StorageVolumeAttachmentFactsSpec(unittest.TestCase,
                                       FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageVolumeAttachmentFactsModule)
        self.resource = self.mock_ov_client.storage_volume_attachments
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all(self):
        attachments = [ATTACHMENT, ATTACHMENT]
        self.resource.get_all.return_value = attachments
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StorageVolumeAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=attachments)
        )

    def test_should_get_all_and_unmanaged_volumes(self):
        attachments = [ATTACHMENT, ATTACHMENT]
        self.resource.get_all.return_value = attachments
        self.resource.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}

        params = dict(
            config='config.json',
            options=[{'extraUnmanagedStorageVolumes': {'start': 1, 'count': 5, 'filter': 'test', 'sort': 'test'}}]
        )

        self.mock_ansible_module.params = params

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get_extra_unmanaged_storage_volumes.assert_called_once_with(
            start=1, count=5, filter='test', sort='test'
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=attachments,
                extra_unmanaged_storage_volumes={'subresource': 'value'})
        )

    def test_should_get_all_and_unmanaged_volumes_without_params(self):
        attachments = [ATTACHMENT, ATTACHMENT]
        self.resource.get_all.return_value = attachments
        self.resource.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}

        params = dict(
            config='config.json',
            options=['extraUnmanagedStorageVolumes']
        )

        self.mock_ansible_module.params = params

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get_extra_unmanaged_storage_volumes.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=attachments,
                extra_unmanaged_storage_volumes={'subresource': 'value'})
        )

    def test_should_get_by_server_name_and_volume_uri(self):
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        self.mock_ansible_module.params = PARAMS_GET_ONE

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get.assert_called_once_with(URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([ATTACHMENT]))
        )

    def test_should_get_by_server_name_and_volume_name(self):
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        self.mock_ov_client.volumes.get_by.return_value = [
            {"uri": "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"}
        ]

        self.mock_ansible_module.params = PARAMS_GET_ONE_VOLUME_NAME

        StorageVolumeAttachmentFactsModule().run()

        self.mock_ov_client.volumes.get_by.assert_called_once_with('name', 'VolumeTest')
        self.resource.get.assert_called_once_with(URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([ATTACHMENT]))
        )

    def test_should_fail_when_get_by_volume_name_and_not_inform_server_name(self):
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        params = PARAMS_GET_ONE_VOLUME_NAME.copy()
        params['serverProfileName'] = None

        self.mock_ansible_module.params = params

        StorageVolumeAttachmentFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=StorageVolumeAttachmentFactsModule.ATTACHMENT_KEY_REQUIRED
        )

    def test_should_fail_when_get_by_server_name_and_not_inform_volume(self):
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME

        params = PARAMS_GET_ONE_VOLUME_NAME.copy()
        params['storageVolumeName'] = None

        self.mock_ansible_module.params = params

        StorageVolumeAttachmentFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=StorageVolumeAttachmentFactsModule.ATTACHMENT_KEY_REQUIRED
        )

    def test_should_get_by_storage_volume_attachment_uri(self):
        self.resource.get.return_value = {"name": "Storage Volume Attachment Name"}
        self.resource.URI = "/rest/storage-volume-attachments"

        params_get_by_uri = dict(
            config='config.json',
            storageVolumeAttachmentUri="/rest/storage-volume-attachments/ED247E27-011B-44EB-9E1B-5891011"
        )

        self.mock_ansible_module.params = params_get_by_uri

        StorageVolumeAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([{"name": "Storage Volume Attachment Name"}]))
        )

    def test_should_get_one_and_paths(self):
        self.resource.get_paths.return_value = [{'subresource': 'value'}]
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        params_get_paths = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=['paths']
        )

        self.mock_ansible_module.params = params_get_paths

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get.assert_called_once_with(URI)
        self.resource.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27")

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    def test_should_get_one_and_path_id(self):
        self.resource.get_paths.return_value = {'subresource': 'value'}
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        params_get_path = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=[{'paths': {'pathId': 'AAA-NNN-878787H'}}]
        )

        self.mock_ansible_module.params = params_get_path

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get.assert_called_once_with(URI)
        self.resource.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27", 'AAA-NNN-878787H')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    def test_should_get_one_and_path_uri(self):
        self.resource.get_paths.return_value = {'subresource': 'value'}
        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        self.resource.URI = "/rest/storage-volume-attachments"

        params_get_path = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=[{'paths': {'pathUri': '/test/uri/AAA-NNN-878787H'}}]
        )

        self.mock_ansible_module.params = params_get_path

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get.assert_called_once_with(URI)
        self.resource.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27", '/test/uri/AAA-NNN-878787H')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    def test_should_get_one_with_options(self):
        self.resource.URI = "/rest/storage-volume-attachments"

        self.resource.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME

        params_get_all_options = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=['extraUnmanagedStorageVolumes', 'paths']
        )

        self.mock_ansible_module.params = params_get_all_options

        self.resource.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}

        self.resource.get_paths.return_value = {'subresource': 'value'}

        StorageVolumeAttachmentFactsModule().run()

        self.resource.get.assert_called_once_with(URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=([ATTACHMENT]),
                storage_volume_attachment_paths={'subresource': 'value'},
                extra_unmanaged_storage_volumes={'subresource': 'value'}
            )
        )


if __name__ == '__main__':
    unittest.main()
