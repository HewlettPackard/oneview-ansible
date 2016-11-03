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
from oneview_sas_logical_jbod_facts import SasLogicalJbodFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="SAS Logical JBOD 2"
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="SAS Logical JBOD 2",
    options=['drives']
)

SAS_LOGICAL_JBOD_1 = dict(name="SAS Logical JBOD 1", uri='/sas-logical-jbods/a0336853-58d7-e021-b740-511cf971e21f0')
SAS_LOGICAL_JBOD_2 = dict(name="SAS Logical JBOD 2", uri='/sas-logical-jbods/b3213123-44sd-y334-d111-asd34sdf34df3')

ALL_SAS_LOGICAL_JBODS = [SAS_LOGICAL_JBOD_1, SAS_LOGICAL_JBOD_2]


class SasLogicalJbodsFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_logical_jbod_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalJbodFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_logical_jbod_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalJbodFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class SasLogicalJbodsFactsSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ov_client_from_json_file = patch.object(OneViewClient, 'from_json_file')
        mock_from_json_file = self.patcher_ov_client_from_json_file.start()

        mock_ov_client = mock.Mock()
        mock_from_json_file.return_value = mock_ov_client

        self.resource = mock_ov_client.sas_logical_jbods

        self.patcher_ansible_module = patch('oneview_sas_logical_jbod_facts.AnsibleModule')
        mock_ansible_module = self.patcher_ansible_module.start()

        self.mock_ansible_instance = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_instance

    def tearDown(self):
        self.patcher_ov_client_from_json_file.stop()
        self.patcher_ansible_module.stop()

    def test_should_get_all_sas_logical_jbods(self):
        self.resource.get_all.return_value = ALL_SAS_LOGICAL_JBODS
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=(ALL_SAS_LOGICAL_JBODS))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.resource.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_ALL)

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once()

    def test_should_get_sas_logical_jbod_attachment_by_name(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_JBOD_2]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=([SAS_LOGICAL_JBOD_2]))
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.resource.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once()

    def test_should_get_sas_logical_jbod_with_options(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_JBOD_2]
        self.resource.get_drives.return_value = [{"name": "Drive 1"}]
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_GET_BY_NAME_WITH_OPTIONS)

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=[SAS_LOGICAL_JBOD_2],
                               sas_logical_jbod_drives=[{"name": "Drive 1"}])
        )


if __name__ == '__main__':
    unittest.main()
