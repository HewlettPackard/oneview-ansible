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
from oneview_firmware_bundle import FirmwareBundleModule
from oneview_firmware_bundle import FIRMWARE_BUNDLE_UPLOADED

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_FIRMWARE_FILE_PATH = '/path/to/file.rpm'

DEFAULT_FIRMWARE_TEMPLATE = dict(
    bundleSize='4837926',
    bundleType='Hotfix',
    category='firmware-drivers',
    description='Provides firmware for the following drive model: MB1000GCWCV and MB4000GCWDC Drives',
    fwComponents=[dict(componentVersion='HPGH',
                       fileName='hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm',
                       name='Supplemental Update',
                       swKeyNameList=['hp-firmware-hdd-a1b08f8a6b'])]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    file_path=DEFAULT_FIRMWARE_FILE_PATH
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class FirmwareBundlePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_firmware_bundle.AnsibleModule')
    def test_should_upload(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.firmware_drivers.get_by_file_name.return_value = None
        mock_ov_instance.firmware_bundles.upload.side_effect = [DEFAULT_FIRMWARE_TEMPLATE]

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FirmwareBundleModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FIRMWARE_BUNDLE_UPLOADED,
            ansible_facts=dict(firmware_bundle=DEFAULT_FIRMWARE_TEMPLATE)
        )


class FirmwareBundleErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_firmware_bundle.AnsibleModule')
    def test_should_call_fail_json_when_upload_raises_exception(self, mock_ansible_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.firmware_drivers.get_by_file_name.return_value = []
        mock_ov_instance.firmware_bundles.upload.side_effect = Exception(FAKE_MSG_ERROR)

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, FirmwareBundleModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
