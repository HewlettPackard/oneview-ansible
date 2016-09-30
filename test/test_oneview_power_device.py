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
import yaml

from hpOneView.oneview_client import OneViewClient
from oneview_power_device import PowerDeviceModule, POWER_DEVICE_ADDED, POWER_DEVICE_ALREADY_PRESENT, \
    POWER_DEVICE_DELETED, POWER_DEVICE_UPDATED, POWER_DEVICE_ALREADY_ABSENT, POWER_DEVICE_MANDATORY_FIELD_MISSING, \
    POWER_DEVICE_POWER_STATE_UPDATED, POWER_DEVICE_NOT_FOUND, POWER_DEVICE_REFRESH_STATE_UPDATED, \
    POWER_DEVICE_UID_STATE_UPDATED, POWER_DEVICE_IPDU_ADDED

FAKE_MSG_ERROR = 'Fake message error'

YAML_POWER_DEVICE = """
        config: "{{ config }}"
        state: present
        data:
            name: 'PDD name'
            ratedCapacity: 40
          """

YAML_POWER_DEVICE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            name: 'PDD name'
            newName: 'PDD new name'
            ratedCapacity: 40
          """

YAML_IPDU = """
        config: "{{ config }}"
        state: discovered
        data:
            hostname : '10.10.10.10'
            username : 'username'
            password : 'password'
          """

YAML_POWER_DEVICE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'PDD name'
"""

YAML_POWER_DEVICE_POWER_STATE = """
        config: "{{ config }}"
        state: power_state_set
        data:
            name: 'PDD name'
            powerStateData:
                powerState: "On"
"""

YAML_POWER_DEVICE_REFRESH_STATE = """
        config: "{{ config }}"
        state: refresh_state_set
        data:
            name: 'PDD name'
            refreshStateData:
                refreshState : "RefreshPending"
"""

YAML_POWER_DEVICE_UID_STATE = """
        config: "{{ config }}"
        state: uid_state_set
        data:
            name: 'PDD name'
            uidStateData:
                powerState: "On"
"""

YAML_POWER_DEVICE_SET_CALIBRATED_MAX_POWER = """
        config: "{{ config }}"
        state: present
        data:
            hostname : 'power_device_hostname'
            calibratedMaxPower: 2500
"""

DICT_DEFAULT_POWER_DEVICE = yaml.load(YAML_POWER_DEVICE)["data"]


def create_ansible_mock(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class PowerDevicePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_add_new_power_device(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []
        mock_ov_instance.power_devices.add.return_value = {"name": "name"}
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_ADDED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_add_new_ipdu(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.add_ipdu.return_value = {"name": "name"}
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_IPDU)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_IPDU_ADDED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_not_update_when_it_already_present(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [DICT_DEFAULT_POWER_DEVICE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=POWER_DEVICE_ALREADY_PRESENT,
            ansible_facts=dict(power_device=DICT_DEFAULT_POWER_DEVICE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_update_when_it_already_exists_with_difference(self, mock_ansible_module,
                                                                  mock_ov_client_from_json_file):

        def inner_get_by(name, value):
            if value == "PDD name":
                return [DICT_DEFAULT_POWER_DEVICE]
            else:
                return []

        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.side_effect = inner_get_by
        mock_ov_instance.power_devices.update.return_value = {'name': 'name'}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_UPDATED,
            ansible_facts=dict(power_device={'name': 'name'})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_with_missing_required_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = mock.Mock()
        mock_ansible_instance.params = {"state": "present",
                                        "config": "config",
                                        "data":
                                            {"field": "invalid"}}
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=POWER_DEVICE_MANDATORY_FIELD_MISSING
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []
        mock_ov_instance.power_devices.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, PowerDeviceModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class PowerDeviceAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_remove_power_device(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [{'name': 'name'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=POWER_DEVICE_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_do_nothing_when_power_device_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=POWER_DEVICE_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_when_remove_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [{'name': 'name'}]
        mock_ov_instance.power_devices.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, PowerDeviceModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class PowerDevicePowerStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_set_power_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.power_devices.update_power_state.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_POWER_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_when_the_power_device_was_not_found(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=POWER_DEVICE_NOT_FOUND
        )


class PowerDeviceRefreshStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_set_refresh_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.power_devices.update_refresh_state.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_REFRESH_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_REFRESH_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_when_the_power_device_was_not_found(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_REFRESH_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=POWER_DEVICE_NOT_FOUND
        )


class PowerDeviceUidStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_set_uid_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.power_devices.update_uid_state.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_UID_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=POWER_DEVICE_UID_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_power_device.AnsibleModule')
    def test_should_fail_when_the_power_device_was_not_found(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.power_devices.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_POWER_DEVICE_UID_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        PowerDeviceModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=POWER_DEVICE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
