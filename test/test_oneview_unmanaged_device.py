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
from oneview_unmanaged_device import UnmanagedDeviceModule, UNMANAGED_DEVICE_ADDED, UNMANAGED_DEVICE_UPDATED, \
    UNMANAGED_DEVICE_REMOVED, UNMANAGED_DEVICE_SET_REMOVED, NOTHING_TO_DO

ERROR_MSG = "Fake message error"

UNMANAGED_DEVICE_ID = "6a71ad03-70cd-4d2b-9893-fe8e78d79c3c"
UNMANAGED_DEVICE_NAME = "MyUnmanagedDevice"
UNMANAGED_DEVICE_URI = "/rest/unmanaged-devices/" + UNMANAGED_DEVICE_ID

FILTER = "name matches '%'"

UNMANAGED_DEVICE_FOR_PRESENT = dict(
    name=UNMANAGED_DEVICE_NAME,
    model="Procurve 4200VL",
    deviceType="Server"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=UNMANAGED_DEVICE_FOR_PRESENT
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=UNMANAGED_DEVICE_NAME)
)

PARAMS_FOR_REMOVE_ALL = dict(
    config='config.json',
    state='absent',
    data=dict(filter=FILTER)
)

UNMANAGED_DEVICE = dict(
    category="unmanaged-devices",
    deviceType="Server",
    id=UNMANAGED_DEVICE_ID,
    model="Procurve 4200VL",
    name=UNMANAGED_DEVICE_NAME,
    state="Unmanaged",
    status="Disabled",
    uri=UNMANAGED_DEVICE_URI,
)


class UnmanagedDevicePresentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_add(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = []
        mock_ov_instance.unmanaged_devices.add.return_value = UNMANAGED_DEVICE

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UNMANAGED_DEVICE_ADDED,
            ansible_facts=dict(unmanaged_device=UNMANAGED_DEVICE)
        )

    @mock.patch('oneview_unmanaged_device.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_from_file, mock_resource_compare):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = [UNMANAGED_DEVICE_FOR_PRESENT]

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        mock_resource_compare.return_value = True

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=NOTHING_TO_DO,
            ansible_facts=dict(unmanaged_device=UNMANAGED_DEVICE_FOR_PRESENT)
        )

    @mock.patch('oneview_unmanaged_device.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_update_the_unmanaged_device(self, mock_ansible_module, mock_ov_from_file, mock_resource_compare):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = [UNMANAGED_DEVICE_FOR_PRESENT]
        mock_ov_instance.unmanaged_devices.update.return_value = UNMANAGED_DEVICE

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        mock_resource_compare.return_value = False

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.get_by.assert_called_once_with('name', UNMANAGED_DEVICE_NAME)
        mock_ov_instance.unmanaged_devices.update.assert_called_once_with(UNMANAGED_DEVICE_FOR_PRESENT)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UNMANAGED_DEVICE_UPDATED,
            ansible_facts=dict(unmanaged_device=UNMANAGED_DEVICE)
        )


class UnmanagedDeviceAbsentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_remove_the_unmanaged_device(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = [UNMANAGED_DEVICE]
        mock_ov_instance.unmanaged_devices.remove.return_value = True

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.remove.assert_called_once_with(UNMANAGED_DEVICE)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UNMANAGED_DEVICE_REMOVED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_do_nothing_when_not_exist(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = []

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=NOTHING_TO_DO
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_delete_all_resources(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.remove_all.return_value = [UNMANAGED_DEVICE]

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REMOVE_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.remove_all.assert_called_once_with(filter=FILTER)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UNMANAGED_DEVICE_SET_REMOVED
        )


class UnmanagedDeviceErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = []
        mock_ov_instance.unmanaged_devices.add.side_effect = Exception(ERROR_MSG)

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.add.assert_called_once_with(UNMANAGED_DEVICE_FOR_PRESENT)
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch('oneview_unmanaged_device.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_unmanaged_device.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module,
                                                      mock_ov_from_file, mock_resource_compare):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.unmanaged_devices.get_by.return_value = [UNMANAGED_DEVICE]
        mock_ov_instance.unmanaged_devices.update.side_effect = Exception(ERROR_MSG)

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        mock_resource_compare.return_value = False

        UnmanagedDeviceModule().run()

        mock_ov_instance.unmanaged_devices.update.assert_called_once_with(UNMANAGED_DEVICE)
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
