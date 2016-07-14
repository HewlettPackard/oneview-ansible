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
from oneview_firmware_driver import FirmwareDriverModule, FIRMWARE_DRIVER_DELETED, FIRMWARE_DRIVER_ALREADY_ABSENT

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

PARAMS_ABSENT = dict(
    config='config.json',
    state='absent',
    name=FIRMWARE_DRIVER_NAME
)

FIRMWARE_DRIVER = dict(name=FIRMWARE_DRIVER_NAME)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


def define_mocks(mock_ov_client_from_json_file, mock_ansible_module, params):
    mock_ov_instance = mock.Mock()
    mock_ov_client_from_json_file.return_value = mock_ov_instance

    mock_ansible_instance = create_ansible_mock(params)
    mock_ansible_module.return_value = mock_ansible_instance
    return mock_ov_instance, mock_ansible_instance


class FirmwareDriverSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_firmware_driver.AnsibleModule')
    def test_should_remove_firmware_driver(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance, mock_ansible_instance = define_mocks(mock_ov_client_from_json_file,
                                                               mock_ansible_module,
                                                               PARAMS_ABSENT)

        firmwares = [FIRMWARE_DRIVER]
        mock_ov_instance.firmware_drivers.get_by.return_value = firmwares

        FirmwareDriverModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FIRMWARE_DRIVER_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_firmware_driver.AnsibleModule')
    def test_should_do_nothing_when_firmware_driver_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance, mock_ansible_instance = define_mocks(mock_ov_client_from_json_file,
                                                               mock_ansible_module,
                                                               PARAMS_ABSENT)
        mock_ov_instance.firmware_drivers.get_by.return_value = []

        FirmwareDriverModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=FIRMWARE_DRIVER_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_firmware_driver.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_error(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance, mock_ansible_instance = define_mocks(mock_ov_client_from_json_file,
                                                               mock_ansible_module,
                                                               PARAMS_ABSENT)

        mock_ov_instance.firmware_drivers.get_by.side_effect = Exception()
        FirmwareDriverModule().run()
        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
