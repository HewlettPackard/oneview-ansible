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

import copy
import unittest
import mock
from mock import patch

from hpOneView.oneview_client import OneViewClient
from oneview_scope_facts import ScopeFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Scope 2"
)

SCOPE_1 = dict(name="Scope 1", uri='/rest/scopes/a0336853-58d7-e021-b740-511cf971e21f0')
SCOPE_2 = dict(name="Scope 2", uri='/rest/scopes/b3213123-44sd-y334-d111-asd34sdf34df3')

ALL_SCOPES = [SCOPE_1, SCOPE_2]


class ScopeFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_scope_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ScopeFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_scope_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ScopeFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ScopeFactsSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ov_client_from_json_file = patch.object(OneViewClient, 'from_json_file')
        mock_from_json_file = self.patcher_ov_client_from_json_file.start()

        mock_ov_client = mock.Mock()
        mock_from_json_file.return_value = mock_ov_client

        self.resource = mock_ov_client.scopes

        self.patcher_ansible_module = patch('oneview_scope_facts.AnsibleModule')
        mock_ansible_module = self.patcher_ansible_module.start()

        self.mock_ansible_instance = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_instance

    def tearDown(self):
        self.patcher_ov_client_from_json_file.stop()
        self.patcher_ansible_module.stop()

    def test_should_get_all_scopes(self):
        self.resource.get_all.return_value = ALL_SCOPES
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        ScopeFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=ALL_SCOPES)
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.resource.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        ScopeFactsModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once()

    def test_should_get_scope_by_name(self):
        self.resource.get_by_name.return_value = SCOPE_2
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        ScopeFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=[SCOPE_2])
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.resource.get_by_name.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        ScopeFactsModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
