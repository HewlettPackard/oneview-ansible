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
from oneview_switch_facts import SwitchFactsModule
from utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

SWITCH_NAME = '172.18.20.1'

SWITCH_URI = '/rest/switches/028e81d0-831b-4211-931c-8ac63d687ebd'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=['environmentalConfiguration']
)

SWITCH = dict(name=SWITCH_NAME, uri=SWITCH_URI)

ALL_SWITCHES = [SWITCH, dict(name='172.18.20.2')]


class SwitchFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class SwitchFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_get_all(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.switches.get_all.return_value = ALL_SWITCHES
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=ALL_SWITCHES)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_get_by_name(self, mock_ansible_module, mock_ov_from_file):
        switches = [SWITCH]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.switches.get_by.return_value = switches
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule().run()

        mock_ov_instance.switches.get_by.assert_called_once_with('name', SWITCH_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_error(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.switches.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_fail_when_get_by_raises_error(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.switches.get_by.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_switch_facts.AnsibleModule')
    def test_should_get_by_name_with_options(self, mock_ansible_module, mock_ov_from_file):
        switches = [SWITCH]
        environmental_configuration = dict(calibratedMaxPower=0, capHistorySupported=False)

        mock_ov_instance = mock.Mock()
        mock_ov_instance.switches.get_by.return_value = switches
        mock_ov_instance.switches.get_environmental_configuration.return_value = environmental_configuration
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        SwitchFactsModule().run()

        mock_ov_instance.switches.get_by.assert_called_once_with('name', SWITCH_NAME)
        mock_ov_instance.switches.get_environmental_configuration.assert_called_once_with(id_or_uri=SWITCH_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches, switch_environmental_configuration=environmental_configuration)
        )


if __name__ == '__main__':
    unittest.main()
