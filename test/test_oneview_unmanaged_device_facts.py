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

from utils import create_ansible_mock
from hpOneView.oneview_client import OneViewClient
from oneview_unmanaged_device_facts import UnmanagedDeviceFactsModule

ERROR_MSG = 'Fake message error'

UNMANAGED_DEVICE_NAME = "New Unmanaged Device Name"
UNMANAGED_DEVICE_URI = "/rest/unmanaged-devices/831083d9-dc9b-46af-8d71-6da55f9fda12"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=UNMANAGED_DEVICE_NAME,
    options=None
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=UNMANAGED_DEVICE_NAME,
    options=['environmental_configuration']
)

UNMANAGED_DEVICE = dict(
    category="unmanaged-devices",
    created="2016-09-22T15:43:07.037Z",
    deviceType="Server",
    height=None,
    id="831083d9-dc9b-46af-8d71-6da55f9fda12",
    model="Procurve 4200VL",
    name=UNMANAGED_DEVICE_NAME,
    state="Unmanaged",
    status="Disabled",
    uri=UNMANAGED_DEVICE_URI,
    uuid="831083d9-dc9b-46af-8d71-6da55f9fda12"
)

ENVIRONMENTAL_CONFIGURATION = dict(
    calibratedMaxPower=-1,
    capHistorySupported=False,
    height=-1,
    historyBufferSize=0
)


class UnmanagedDeviceFactsSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device_facts.AnsibleModule')
    def test_get_all(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_from_file.return_value = mock_ov_instance

        unmanaged_devices = [UNMANAGED_DEVICE]
        mock_ov_instance.unmanaged_devices.get_all.return_value = unmanaged_devices

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceFactsModule().run()

        mock_ov_instance.unmanaged_devices.get_all.assert_called_once()
        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts=dict(unmanaged_devices=unmanaged_devices)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device_facts.AnsibleModule')
    def test_get_by(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_from_file.return_value = mock_ov_instance

        unmanaged_devices = [UNMANAGED_DEVICE]
        mock_ov_instance.unmanaged_devices.get_by.return_value = unmanaged_devices

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceFactsModule().run()

        mock_ov_instance.unmanaged_devices.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)
        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts=dict(unmanaged_devices=unmanaged_devices)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device_facts.AnsibleModule')
    def test_get_by_with_options(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_from_file.return_value = mock_ov_instance

        unmanaged_devices = [UNMANAGED_DEVICE]
        mock_ov_instance.unmanaged_devices.get_by.return_value = unmanaged_devices
        mock_ov_instance.unmanaged_devices.get_environmental_configuration.return_value = ENVIRONMENTAL_CONFIGURATION

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceFactsModule().run()

        mock_ov_instance.unmanaged_devices.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)
        mock_ov_instance.unmanaged_devices.get_environmental_configuration.assert_called_once_with(
            id_or_uri=UNMANAGED_DEVICE_URI
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts=dict(
                unmanaged_devices=unmanaged_devices,
                unmanaged_device_environmental_configuration=ENVIRONMENTAL_CONFIGURATION
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ov_instance.unmanaged_devices.get_all.side_effect = Exception(ERROR_MSG)

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device_facts.AnsibleModule')
    def test_should_fail_when_get_by_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ov_instance.unmanaged_devices.get_by.side_effect = Exception(ERROR_MSG)

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
