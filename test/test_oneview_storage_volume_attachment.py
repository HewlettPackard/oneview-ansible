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

from oneview_storage_volume_attachment import StorageVolumeAttachmentModule, PRESENTATIONS_REMOVED, PROFILE_NOT_FOUND
from utils import ModuleContructorTestCase
from utils import ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'

SERVER_PROFILE_NAME = "SV-1001"

YAML_EXTRA_REMOVED_BY_NAME = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "SV-1001"
        """
YAML_EXTRA_REMOVED_BY_URI = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
        """

REPAIR_DATA = {
    "type": "ExtraUnmanagedStorageVolumes",
    "resourceUri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
}

MOCK_SERVER_PROFILE = {
    "affinity": "BayAndServer",
    "associatedServer": "SGH106X8RN",
    "name": "SV-1001",
    "uri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d",
    "sanStorage": {
        "manageSanStorage": True,
        "volumeAttachments": [
            {
                "id": 1,
                "lun": "1",
                "lunType": "Auto",
                "state": "AttachFailed",
                "storagePaths": [
                    {
                        "connectionId": 1,
                        "isEnabled": True,
                        "storageTargets": [
                            "20:00:00:02:AC:00:08:F7"
                        ]
                    }
                ],
                "volumeStoragePoolUri": "/rest/storage-pools/280FF951-F007-478F-AC29-E4655FC76DDC",
                "volumeStorageSystemUri": "/rest/storage-systems/TXQ1010307",
                "volumeUri": "/rest/storage-volumes/89118052-A367-47B6-9F60-F26073D1D85E"
            }
        ]
    },
}


class StorageVolumeAttachmentSpec(unittest.TestCase,
                                  ModuleContructorTestCase,
                                  ErrorHandlingTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageVolumeAttachmentModule)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.mock_ov_client.server_profiles.get_by_name,
                                        ansible_params=yaml.load(YAML_EXTRA_REMOVED_BY_NAME))

    def test_should_remove_extra_presentation_by_profile_name(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = MOCK_SERVER_PROFILE
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ov_client.server_profiles.get_by_name.assert_called_once_with(SERVER_PROFILE_NAME)
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )

    def test_should_fail_when_profile_name_not_found(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=PROFILE_NOT_FOUND)

    def test_should_remove_extra_presentation_by_profile_uri(self):
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_URI)

        StorageVolumeAttachmentModule().run()

        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )


if __name__ == '__main__':
    unittest.main()
