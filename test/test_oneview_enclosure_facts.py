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
from oneview_enclosure_facts import EnclosureFactsModule
from utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=['utilization', 'environmentalConfiguration', 'script']
)

PARAMS_GET_UTILIZATION_WITH_PARAMS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[dict(utilization=dict(fields='AveragePower',
                                   filter=['startDate=2016-06-30T03:29:42.000Z',
                                           'endDate=2016-07-01T03:29:42.000Z'],
                                   view='day',
                                   refresh=True))]
)

PRESENT_ENCLOSURES = [{
    "name": "Test-Enclosure",
    "uri": "/rest/enclosures/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

ENCLOSURE_SCRIPT = '# script content'

ENCLOSURE_UTILIZATION = {
    "isFresh": "True"
}

ENCLOSURE_ENVIRONMENTAL_CONFIG = {
    "calibratedMaxPower": "2500"
}


class EnclosureFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class EnclosureFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_get_all_enclosures(self, mock_ansible_module,
                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_all.return_value = PRESENT_ENCLOSURES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=(PRESENT_ENCLOSURES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_get_enclosure_by_name(self, mock_ansible_module,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=(PRESENT_ENCLOSURES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_get_enclosure_by_name_with_options(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        mock_ov_instance.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        mock_ov_instance.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosures=PRESENT_ENCLOSURES,
                               enclosure_script=ENCLOSURE_SCRIPT,
                               enclosure_environmental_configuration=ENCLOSURE_ENVIRONMENTAL_CONFIG,
                               enclosure_utilization=ENCLOSURE_UTILIZATION)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_script_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.side_effect = Exception(ERROR_MSG)
        mock_ov_instance.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        mock_ov_instance.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_utilization_raises_exception(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        mock_ov_instance.enclosures.get_utilization.side_effect = Exception(ERROR_MSG)
        mock_ov_instance.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_environmental_configuration_raises_exception(self, mock_ansible_module,
                                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        mock_ov_instance.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        mock_ov_instance.enclosures.get_environmental_configuration.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_get_all_utilization_data(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        mock_ov_instance.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        mock_ov_instance.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(PRESENT_ENCLOSURES[0]['uri'],
                                                                            fields='',
                                                                            filter='',
                                                                            view='',
                                                                            refresh='')

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_facts.AnsibleModule')
    def test_should_get_utilization_with_parameters(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_script.return_value = ENCLOSURE_SCRIPT
        mock_ov_instance.enclosures.get_utilization.return_value = ENCLOSURE_UTILIZATION
        mock_ov_instance.enclosures.get_environmental_configuration.return_value = ENCLOSURE_ENVIRONMENTAL_CONFIG

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_UTILIZATION_WITH_PARAMS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureFactsModule().run()

        date_filter = ["startDate=2016-06-30T03:29:42.000Z", "endDate=2016-07-01T03:29:42.000Z"]

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(PRESENT_ENCLOSURES[0]['uri'],
                                                                            fields='AveragePower',
                                                                            filter=date_filter,
                                                                            view='day',
                                                                            refresh=True)


if __name__ == '__main__':
    unittest.main()
