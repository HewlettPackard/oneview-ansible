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
import yaml

from oneview_connection_template import ConnectionTemplateModule, \
    CONNECTION_TEMPLATE_MANDATORY_FIELD_MISSING, CONNECTION_TEMPLATE_NOT_FOUND, \
    CONNECTION_TEMPLATE_ALREADY_UPDATED, CONNECTION_TEMPLATE_UPDATED
from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

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


class ConnectionTemplateModuleSpec(unittest.TestCase,
                                   ModuleContructorTestCase,
                                   ErrorHandlingTestCase):
    def setUp(self):
        self.configure_mocks(self, ConnectionTemplateModule)

        ErrorHandlingTestCase.configure(self, method_to_fire=self.mock_ov_client.connection_templates.get_by)

    def test_should_update_the_connection_template(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]
        self.mock_ov_client.connection_templates.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_CONNECTION_TEMPLATE_CHANGE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=CONNECTION_TEMPLATE_UPDATED,
            ansible_facts=dict(connection_template={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]

        self.mock_ansible_module.params = yaml.load(YAML_CONNECTION_TEMPLATE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=CONNECTION_TEMPLATE_ALREADY_UPDATED,
            ansible_facts=dict(connection_template=DICT_DEFAULT_CONNECTION_TEMPLATE)
        )

    def test_should_fail_when_key_is_missing(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [DICT_DEFAULT_CONNECTION_TEMPLATE]

        self.mock_ansible_module.params = yaml.load(YAML_CONNECTION_TEMPLATE_MISSING_KEY)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=CONNECTION_TEMPLATE_MANDATORY_FIELD_MISSING
        )

    def test_should_fail_when_connection_template_was_not_found(self):
        self.mock_ov_client.connection_templates.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_CONNECTION_TEMPLATE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=CONNECTION_TEMPLATE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
