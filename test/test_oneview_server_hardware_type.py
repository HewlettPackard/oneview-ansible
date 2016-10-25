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
from oneview_server_hardware_type import ServerHardwareTypeModule, SERVER_HARDWARE_TYPE_DELETED, \
    SERVER_HARDWARE_TYPE_ALREADY_ABSENT, SERVER_HARDWARE_TYPE_ALREADY_UPDATED, SERVER_HARDWARE_TYPE_UPDATED, \
    SERVER_HARDWARE_TYPE_NOT_FOUND
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

FAKE_MSG_ERROR = 'Fake message error'

YAML_SERVER_HARDWARE_TYPE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          description: "New Description"
          """

YAML_SERVER_HARDWARE_TYPE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          newName: 'My New Server Hardware Type'
          description: "Another Description"
          """

YAML_SERVER_HARDWARE_TYPE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'MyServerHardwareType'
        """

DICT_DEFAULT_SERVER_HARDWARE_TYPE = yaml.load(YAML_SERVER_HARDWARE_TYPE)["data"]
DICT_DEFAULT_SERVER_HARDWARE_TYPE_CHANGED = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)["data"]


class ServerHardwareTypeClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ServerHardwareTypePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_update_the_server_hardware_type(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        srv_hw_type = DICT_DEFAULT_SERVER_HARDWARE_TYPE.copy()
        srv_hw_type['uri'] = '/rest/id'

        mock_ov_instance.server_hardware_types.get_by.return_value = [srv_hw_type]
        mock_ov_instance.server_hardware_types.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_TYPE_UPDATED,
            ansible_facts=dict(server_hardware_type={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SERVER_HARDWARE_TYPE_ALREADY_UPDATED,
            ansible_facts=dict(server_hardware_type=DICT_DEFAULT_SERVER_HARDWARE_TYPE)
        )


class ServerHardwareTypeAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_remove_server_hardware_type(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=SERVER_HARDWARE_TYPE_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_do_nothing_when_server_hardware_type_not_exist(self, mock_ansible_module,
                                                                   mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerHardwareTypeModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=SERVER_HARDWARE_TYPE_ALREADY_ABSENT
        )


class ServerHardwareTypeErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = [{'uri': 'test'}]
        mock_ov_instance.server_hardware_types.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_fail_when_server_hardware_type_was_not_found(self, mock_ansible_module,
                                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_TYPE_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_hardware_type.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_hardware_types.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]
        mock_ov_instance.server_hardware_types.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_HARDWARE_TYPE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
