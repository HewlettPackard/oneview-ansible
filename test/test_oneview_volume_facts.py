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
from oneview_volume_facts import VolumeFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_ALL_WITH_OPTIONS = dict(
    config='config.json',
    name=None,
    options=[
        'attachableVolumes', 'extraManagedVolumePaths'
    ]
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Volume"
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Volume",
    options=[
        'attachableVolumes', 'extraManagedVolumePaths', 'snapshots']
)

PARAMS_GET_SNAPSHOT_BY_NAME = dict(
    config='config.json',
    name="Test Volume",
    options=[{"snapshots": {"name": 'snapshot_name'}}])


class VolumeFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_get_all_volumes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_all.return_value = [{"name": "Test Volume"}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume"}]))

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_get_all_volumes_and_appliance_information(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_all.return_value = [{"name": "Test Volume"}]
        mock_ov_instance.volumes.get_extra_managed_storage_volume_paths.return_value = ['/path1', '/path2']
        mock_ov_instance.volumes.get_attachable_volumes.return_value = [{"name": "attachable Volume 1"}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume"}],
                               attachable_volumes=[{"name": "attachable Volume 1"}],
                               extra_managed_volume_paths=['/path1', '/path2']))

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_get_volume_by_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}]))

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_get_volume_by_name_with_snapshots_and_appliance_information(self, mock_ansible_module,
                                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]
        mock_ov_instance.volumes.get_extra_managed_storage_volume_paths.return_value = ['/path1', '/path2']
        mock_ov_instance.volumes.get_attachable_volumes.return_value = [{"name": "attachable Volume 1"}]
        mock_ov_instance.volumes.get_snapshots.return_value = [{"filename": "snapshot_name"}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}],
                               attachable_volumes=[{"name": "attachable Volume 1"}],
                               extra_managed_volume_paths=['/path1', '/path2'],
                               snapshots=[{"filename": "snapshot_name"}]))

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_get_volume_by_name_with_snapshots_by_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]
        mock_ov_instance.volumes.get_snapshot_by.return_value = [{"filename": "snapshot_name"}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_SNAPSHOT_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}],
                               snapshots=[{"filename": "snapshot_name"}]))

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_volume_facts.AnsibleModule')
    def test_should_fail_when_get_by_raises_error(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.volumes.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        VolumeFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
