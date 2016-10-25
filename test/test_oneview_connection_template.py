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
from oneview_connection_template import ConnectionTemplateModule, \
    CONNECTION_TEMPLATE_MANDATORY_FIELD_MISSING, CONNECTION_TEMPLATE_NOT_FOUND, \
    CONNECTION_TEMPLATE_ALREADY_UPDATED, CONNECTION_TEMPLATE_UPDATED
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

FAKE_MSG_ERROR = 'Fake message error'

YAML_CONNECTION_TEMPLATE = """
        config: "{{ config }}"
        state: present
        data:
            name: 'name1304244267-1467656930023'
            type : "connection-template"
            bandwidth :
                maximumBandwidth : 10000
                typicalBandwidth : 2000
          """

YAML_CONNECTION_TEMPLATE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            name: 'name1304244267-1467656930023'
            type : "connection-template"
            bandwidth :
                maximumBandwidth : 10000
                typicalBandwidth : 2000
            newName : "CT-23"
      """

YAML_CONNECTION_TEMPLATE_MISSING_KEY = """
        config: "{{ config }}"
        state: present
        data:
            state: "Configured"
    """

DICT_DEFAULT_CONNECTION_TEMPLATE = yaml.load(YAML_CONNECTION_TEMPLATE)["data"]
DICT_DEFAULT_CONNECTION_TEMPLATE_CHANGED = yaml.load(YAML_CONNECTION_TEMPLATE_CHANGE)["data"]


class ConnectionTemplateClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ConnectionTemplateModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ConnectionTemplateModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ConnectionTemplatePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_update_the_connection_template(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]
        mock_ov_instance.connection_templates.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_CONNECTION_TEMPLATE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        ConnectionTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=CONNECTION_TEMPLATE_UPDATED,
            ansible_facts=dict(connection_template={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_CONNECTION_TEMPLATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ConnectionTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=CONNECTION_TEMPLATE_ALREADY_UPDATED,
            ansible_facts=dict(connection_template=DICT_DEFAULT_CONNECTION_TEMPLATE)
        )


class ConnectionTemplateErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]
        mock_ov_instance.connection_templates.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_CONNECTION_TEMPLATE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ConnectionTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_raise_exception_when_key_is_missing(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_CONNECTION_TEMPLATE_MISSING_KEY)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ConnectionTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=CONNECTION_TEMPLATE_MANDATORY_FIELD_MISSING
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_connection_template.AnsibleModule')
    def test_should_raise_exception_when_connection_template_was_not_found(self, mock_ansible_module,
                                                                           mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.connection_templates.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_CONNECTION_TEMPLATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ConnectionTemplateModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=CONNECTION_TEMPLATE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
