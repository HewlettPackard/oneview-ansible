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

from oneview_connection_template_facts import ConnectionTemplateFactsModule
from test.utils import ParamsTestCase
from test.utils import ModuleContructorTestCase

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="name1304244267-1467656930023"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_DEFAULT = dict(
    config='config.json',
    options=['defaultConnectionTemplate']
)


class ConnectionTemplatesFactsSpec(unittest.TestCase, ModuleContructorTestCase, ParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ConnectionTemplateFactsModule)
        self.connection_templates = self.mock_ov_client.connection_templates
        ParamsTestCase.configure_client_mock(self, self.connection_templates)

    def test_should_get_all_connection_templates(self):
        self.connection_templates.get_all.return_value = {"name": "Storage System Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(connection_templates=({"name": "Storage System Name"}))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.connection_templates.get_all.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_ALL

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_connection_template_by_name(self):
        self.connection_templates.get_by.return_value = {"name": "Storage System Name"}

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(connection_templates=({"name": "Storage System Name"}))
        )

    def test_should_fail_when_get_by_raises_exception(self):
        self.connection_templates.get_by.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_default_connection_template(self):
        self.connection_templates.get_default.return_value = {
            "name": "default_connection_template"}

        self.mock_ansible_module.params = PARAMS_GET_DEFAULT

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'default_connection_template': {'name': 'default_connection_template'}}
        )

    def test_should_fail_when_get_default_raises_exception(self):
        self.connection_templates.get_default.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_DEFAULT

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
