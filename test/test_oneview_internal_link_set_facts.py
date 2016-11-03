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
from oneview_internal_link_set_facts import InternalLinkSetFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="ILS58"
)

INTERNAL_LINK_SETS = [{"name": "ILS56"}, {"name": "ILS58"}, {"name": "ILS100"}]


class InternalLinkSetFactsClientConfigurationSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch('oneview_internal_link_set_facts.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.patcher_ov_client_from_env_vars = mock.patch.object(OneViewClient, 'from_environment_variables')
        self.mock_ov_client_from_env_vars = self.patcher_ov_client_from_env_vars.start()

        self.patcher_ov_client_from_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client_from_json_file = self.patcher_ov_client_from_json_file.start()

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_ov_client_from_env_vars.stop()
        self.patcher_ov_client_from_json_file.stop()

    def test_should_load_config_from_file(self):
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule()

        self.mock_ov_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ov_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):
        mock_ov_instance = mock.Mock()

        self.mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule()

        self.mock_ov_client_from_env_vars.assert_called_once()
        self.mock_ov_client_from_json_file.not_been_called()


class InternalLinkSetFactsSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch('oneview_internal_link_set_facts.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.patcher_ov_client_from_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client_from_json_file = self.patcher_ov_client_from_json_file.start()

        self.mock_ov_instance = mock.Mock()
        self.mock_ov_client_from_json_file.return_value = self.mock_ov_instance

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_ov_client_from_json_file.stop()

    def test_should_get_all_internal_link_sets(self):
        self.mock_ov_instance.internal_link_sets.get_all.return_value = INTERNAL_LINK_SETS
        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(internal_link_sets=(INTERNAL_LINK_SETS))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.mock_ov_instance.internal_link_sets.get_all.side_effect = Exception(ERROR_MSG)
        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    def test_should_get_by_name(self):
        self.mock_ov_instance.internal_link_sets.get_by.return_value = [INTERNAL_LINK_SETS[1]]
        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(internal_link_sets=([INTERNAL_LINK_SETS[1]]))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.mock_ov_instance.internal_link_sets.get_by.side_effect = Exception(ERROR_MSG)
        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        self.mock_ansible_module.return_value = mock_ansible_instance

        InternalLinkSetFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
