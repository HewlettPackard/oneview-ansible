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
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_storage_volume_attachment_facts import StorageVolumeAttachmentFactsModule
from oneview_storage_volume_attachment_facts import ATTACHMENT_KEY_REQUIRED

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


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class StorageVolumeAttachmentFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_all(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        attachments = [ATTACHMENT, ATTACHMENT]
        mock_ov_instance.storage_volume_attachments.get_all.return_value = attachments

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=attachments)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_all_and_unmanaged_volumes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        attachments = [ATTACHMENT, ATTACHMENT]
        mock_ov_instance.storage_volume_attachments.get_all.return_value = attachments
        mock_ov_instance.storage_volume_attachments.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        params = dict(
            config='config.json',
            options=[{'extraUnmanagedStorageVolumes': {'start': 1, 'count': 5, 'filter': 'test', 'sort': 'test'}}]
        )

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get_extra_unmanaged_storage_volumes.assert_called_once_with(
            start=1, count=5, filter='test', sort='test'
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=attachments,
                extra_unmanaged_storage_volumes={'subresource': 'value'})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_all_and_unmanaged_volumes_without_params(self, mock_ansible_module,
                                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        attachments = [ATTACHMENT, ATTACHMENT]
        mock_ov_instance.storage_volume_attachments.get_all.return_value = attachments
        mock_ov_instance.storage_volume_attachments.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        params = dict(
            config='config.json',
            options=['extraUnmanagedStorageVolumes']
        )

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get_extra_unmanaged_storage_volumes.assert_called_once_with()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=attachments,
                extra_unmanaged_storage_volumes={'subresource': 'value'})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_by_server_name_and_volume_uri(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ONE)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([ATTACHMENT]))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_by_server_name_and_volume_name(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance
        mock_ov_instance.volumes.get_by.return_value = [{"uri": "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"}]

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ONE_VOLUME_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.volumes.get_by.assert_called_once_with('name', 'VolumeTest')
        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([ATTACHMENT]))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_fail_when_get_by_volume_name_and_not_inform_server_name(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        params = PARAMS_GET_ONE_VOLUME_NAME.copy()
        params['serverProfileName'] = None

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=ATTACHMENT_KEY_REQUIRED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_fail_when_get_by_server_name_and_not_inform_volume(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_from_json.return_value = mock_ov_instance

        params = PARAMS_GET_ONE_VOLUME_NAME.copy()
        params['storageVolumeName'] = None

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=ATTACHMENT_KEY_REQUIRED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_by_storage_volume_attachment_uri(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.return_value = {"name": "Storage Volume Attachment Name"}
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        params_get_by_uri = dict(
            config='config.json',
            storageVolumeAttachmentUri="/rest/storage-volume-attachments/ED247E27-011B-44EB-9E1B-5891011"
        )

        mock_ansible_instance = create_ansible_mock(params_get_by_uri)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_attachments=([{"name": "Storage Volume Attachment Name"}]))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_one_and_paths(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get_paths.return_value = [{'subresource': 'value'}]
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        params_get_paths = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=['paths']
        )

        mock_ansible_instance = create_ansible_mock(params_get_paths)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)
        mock_ov_instance.storage_volume_attachments.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27")

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_one_and_path_id(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get_paths.return_value = {'subresource': 'value'}
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        params_get_path = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=[{'paths': {'pathId': 'AAA-NNN-878787H'}}]
        )

        mock_ansible_instance = create_ansible_mock(params_get_path)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)
        mock_ov_instance.storage_volume_attachments.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27", 'AAA-NNN-878787H')

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_one_and_path_uri(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get_paths.return_value = {'subresource': 'value'}
        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"
        mock_from_json.return_value = mock_ov_instance

        params_get_path = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=[{'paths': {'pathUri': '/test/uri/AAA-NNN-878787H'}}]
        )

        mock_ansible_instance = create_ansible_mock(params_get_path)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)
        mock_ov_instance.storage_volume_attachments.get_paths.assert_called_once_with(
            "/rest/storage-volume-attachments/ED247E27", '/test/uri/AAA-NNN-878787H')

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=[ATTACHMENT],
                storage_volume_attachment_paths=[{'subresource': 'value'}]
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_get_one_with_options(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.URI = "/rest/storage-volume-attachments"

        mock_ov_instance.storage_volume_attachments.get.return_value = RETURN_GET_BY_PROFILE_AND_VOLUME
        mock_from_json.return_value = mock_ov_instance

        params_get_all_options = dict(
            config='config.json',
            serverProfileName="ProfileTest",
            storageVolumeUri="/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA",
            options=['extraUnmanagedStorageVolumes', 'paths']
        )

        mock_ansible_instance = create_ansible_mock(params_get_all_options)
        mock_ansible_module.return_value = mock_ansible_instance

        mock_ov_instance.storage_volume_attachments.get_extra_unmanaged_storage_volumes.return_value = {
            'subresource': 'value'}
        mock_ov_instance.storage_volume_attachments.get_paths.return_value = {'subresource': 'value'}

        StorageVolumeAttachmentFactsModule().run()

        mock_ov_instance.storage_volume_attachments.get.assert_called_once_with(URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_volume_attachments=([ATTACHMENT]),
                storage_volume_attachment_paths={'subresource': 'value'},
                extra_unmanaged_storage_volumes={'subresource': 'value'}
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_attachment_facts.AnsibleModule')
    def test_should_fail_when_get_one_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_attachments.get.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ONE)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeAttachmentFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
