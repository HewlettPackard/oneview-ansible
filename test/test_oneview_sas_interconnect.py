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
from oneview_sas_interconnect import SasInterconnectModule
from utils import create_ansible_mock
from mock import patch
import copy


SAS_INTERCONNECT_NAME = "0000A66103, interconnect 4"
SAS_INTERCONNECT_URI = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'


def create_params(state):
    return dict(
        config='config.json',
        state=state,
        name=SAS_INTERCONNECT_NAME
    )


REFRESH_CONFIGURATION = dict(refreshState="RefreshPending")
PARAMS_FOR_REFRESH = create_params('refreshed')
PARAMS_FOR_UID_ON = create_params('uid_on')
PARAMS_FOR_UID_OFF = create_params('uid_off')
PARAMS_FOR_POWERED_ON = create_params('powered_on')
PARAMS_FOR_POWERED_OFF = create_params('powered_off')
PARAMS_FOR_SOFT_RESET = create_params('soft_reset')
PARAMS_FOR_HARD_RESET = create_params('hard_reset')

SAS_INTERCONNECT = dict(
    name=SAS_INTERCONNECT_NAME,
    uri=SAS_INTERCONNECT_URI
)


class SasInterconnectModuleSpec(unittest.TestCase):

    def setUp(self):
        patcher = patch.object(OneViewClient, 'from_json_file')
        mock_from_json_file = patcher.start()

        mock_ov_client = mock.Mock()
        mock_from_json_file.return_value = mock_ov_client

        self.resource = mock_ov_client.sas_interconnects
        self.addCleanup(patcher.stop)

        patcher_ansible = patch('oneview_sas_interconnect.AnsibleModule')
        mock_ansible_module = patcher_ansible.start()

        self.mock_ansible_instance = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_instance

        self.addCleanup(patcher_ansible.stop)

    def test_should_refresh_the_sas_interconnect(self):
        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.refresh_state.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_REFRESH)

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)

        self.resource.refresh_state.assert_called_once_with(
            id_or_uri=SAS_INTERCONNECT_URI,
            configuration=REFRESH_CONFIGURATION
        )

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_turn_on_the_uid_when_uid_is_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_UID_ON)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['uid_on']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)
        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_UID_ON)

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_off_the_uid_when_uid_is_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_UID_OFF)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['uid_off']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)
        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_UID_OFF)

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_off_when_the_sas_interconnect_is_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_POWERED_OFF)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['powered_off']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_off(self):
        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)
        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_POWERED_OFF)

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_on_when_the_sas_interconnect_is_powered_off(self):
        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_POWERED_ON)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['powered_on']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)
        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_POWERED_ON)

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_perform_soft_reset(self):
        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_SOFT_RESET)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['soft_reset']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_perform_hard_reset(self):
        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_HARD_RESET)

        SasInterconnectModule().run()

        state = SasInterconnectModule.states['hard_reset']
        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state)

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )


class SasInterconnectClientConfigurationSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_interconnect.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        SasInterconnectModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_interconnect.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        SasInterconnectModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


if __name__ == '__main__':
    unittest.main()
