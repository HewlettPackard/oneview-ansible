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
from oneview_volume import VolumeModule
from oneview_volume import VOLUME_CREATED, VOLUME_UPDATED
from oneview_volume import VOLUME_DELETED, VOLUME_ALREADY_ABSENT
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'

EXISTENT_VOLUME = dict(
    name='Volume with Storage Pool',
    description='Test volume with common creation: Storage Pool'
)

PARAMS_FOR_CREATE = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              provisioningParameters=dict(provisionType='Full',
                                          shareable=True,
                                          requestedCapacity=1073741824,
                                          storagePoolUri='/rest/storage-pools/3B1CF17F-7657-4C89-B580-D236507A9182'))
)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              newName='Volume with Storage Pool - Renamed')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name='Volume with Storage Pool')
)

PARAMS_FOR_ABSENT_EXPORT_ONLY = dict(
    config='config.json',
    state='absent',
    data=dict(name='Volume with Storage Pool'),
    export_only=True
)


class VolumeModulePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_create_new_volume(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = []
        mock_ov_instance.volumes.create.return_value = EXISTENT_VOLUME

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_CREATE)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=VOLUME_CREATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [EXISTENT_VOLUME]
        mock_ov_instance.volumes.update.return_value = EXISTENT_VOLUME.copy()

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_UPDATE)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=VOLUME_UPDATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME.copy())
        )


class VolumeAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_delete_volume(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [EXISTENT_VOLUME]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeModule().run()

        mock_ov_instance.volumes.delete.assert_called_once_with(EXISTENT_VOLUME, export_only=False)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=VOLUME_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_remove_volume(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [EXISTENT_VOLUME]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT_EXPORT_ONLY)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeModule().run()

        mock_ov_instance.volumes.delete.assert_called_once_with(EXISTENT_VOLUME, export_only=True)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=VOLUME_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_do_nothing_when_volume_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=VOLUME_ALREADY_ABSENT
        )


class VolumeErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_not_update_when_create_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = []
        mock_ov_instance.volumes.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_CREATE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, VolumeModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [EXISTENT_VOLUME]
        mock_ov_instance.volumes.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, VolumeModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
