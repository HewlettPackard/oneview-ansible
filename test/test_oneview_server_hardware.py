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
from oneview_server_hardware import ServerHardwareModule, SERVER_HARDWARE_ADDED, SERVER_HARDWARE_ALREADY_ADDED, \
    SERVER_HARDWARE_DELETED, SERVER_HARDWARE_ALREADY_ABSENT, SERVER_HARDWARE_MANDATORY_FIELD_MISSING, \
    SERVER_HARDWARE_POWER_STATE_UPDATED, SERVER_HARDWARE_NOT_FOUND, SERVER_HARDWARE_REFRESH_STATE_UPDATED, \
    SERVER_HARDWARE_ILO_FIRMWARE_VERSION_UPDATED, SERVER_HARDWARE_ENV_CONFIG_UPDATED
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

FAKE_MSG_ERROR = 'Fake message error'

YAML_SERVER_HARDWARE = """
        config: "{{ config }}"
        state: present
        data:
             hostname : "172.18.6.15"
             username : "dcs"
             password : "dcs"
             force : false
             licensingIntent: "OneView"
             configurationState: "Managed"
          """

YAML_SERVER_HARDWARE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            hostname : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_POWER_STATE = """
        config: "{{ config }}"
        state: power_state_set
        data:
            hostname : "172.18.6.15"
            powerStateData:
                powerState: "On"
                powerControl: "MomentaryPress"
"""

YAML_SERVER_HARDWARE_REFRESH_STATE = """
        config: "{{ config }}"
        state: refresh_state_set
        data:
            hostname : "172.18.6.15"
            refreshStateData:
                refreshState : "RefreshPending"
"""

YAML_SERVER_HARDWARE_ILO_FIRMWARE = """
        config: "{{ config }}"
        state: ilo_firmware_version_updated
        data:
            hostname : '{{ server_hardware_hostname }}'
"""

YAML_SERVER_HARDWARE_SET_CALIBRATED_MAX_POWER = """
        config: "{{ config }}"
        state: present
        data:
            hostname : 'server_hardware_hostname'
            calibratedMaxPower: 2500
"""

DICT_DEFAULT_SERVER_HARDWARE = yaml.load(YAML_SERVER_HARDWARE)["data"]


class ServerHardwareClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ServerHardwarePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_add_new_server_hardware(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []
        mock_ov_instance.server_hardware.add.return_value = {"name": "name"}
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_ADDED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_not_add_when_it_already_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"name": "name"}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SERVER_HARDWARE_ALREADY_ADDED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_calibrate_max_power_server_hardware(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"name": "name",
                                                                 "uri": "uri"}]

        mock_ov_instance.server_hardware.update_environmental_configuration.return_value = {"name": "name"}
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_SET_CALIBRATED_MAX_POWER)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_ENV_CONFIG_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name",
                                                        "uri": "uri"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_with_missing_required_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = mock.Mock()
        mock_ansible_instance.params = {"state": "present",
                                        "config": "config",
                                        "data":
                                            {"field": "invalid"}}
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_MANDATORY_FIELD_MISSING
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []
        mock_ov_instance.server_hardware.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ServerHardwareModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class ServerHardwareAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_remove_server_hardware(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{'name': 'name'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=SERVER_HARDWARE_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_do_nothing_when_server_hardware_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=SERVER_HARDWARE_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_when_remove_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{'name': 'name'}]
        mock_ov_instance.server_hardware.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ServerHardwareModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class ServerHardwarePowerStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_set_power_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.server_hardware.update_power_state.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_POWER_STATE_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_when_the_server_hardware_was_not_found(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_NOT_FOUND
        )


class ServerHardwareRefreshStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_set_refresh_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.server_hardware.refresh_state.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_REFRESH_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_REFRESH_STATE_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_when_the_server_hardware_was_not_found(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_REFRESH_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_NOT_FOUND
        )


class ServerHardwareIloFirmwareUpdateStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_set_refresh_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = [{"uri": "resourceuri"}]
        mock_ov_instance.server_hardware.update_mp_firware_version.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_ILO_FIRMWARE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_ILO_FIRMWARE_VERSION_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware.AnsibleModule')
    def test_should_fail_when_the_server_hardware_was_not_found(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_ILO_FIRMWARE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
