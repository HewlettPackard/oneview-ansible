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

from utils import create_ansible_mock
from hpOneView.oneview_client import OneViewClient
from oneview_enclosure_group_facts import EnclosureGroupFactsModule

ERROR_MSG = 'Fake message error'

ENCLOSURE_GROUP_NAME = "Enclosure Group Name"
ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/7a298f96-fda8-480e-9747-8ad4c666f756"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=ENCLOSURE_GROUP_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=ENCLOSURE_GROUP_NAME,
    options=["configuration_script"]
)

ENCLOSURE_GROUPS = [{
    "name": ENCLOSURE_GROUP_NAME,
    "uri": ENCLOSURE_GROUP_URI
}]


class EnclosureGroupFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group_facts.AnsibleModule')
    def test_should_get_all_enclosure_group(self, mock_ansible_module,
                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_all.return_value = ENCLOSURE_GROUPS

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_groups=ENCLOSURE_GROUPS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module,
                                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group_facts.AnsibleModule')
    def test_should_get_enclosure_group_by_name(self, mock_ansible_module,
                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = ENCLOSURE_GROUPS

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupFactsModule().run()

        mock_ov_instance.enclosure_groups.get_by.assert_called_once_with('name', ENCLOSURE_GROUP_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_groups=ENCLOSURE_GROUPS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group_facts.AnsibleModule')
    def test_should_get_enclosure_group_by_name_with_options(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        configuration_script = "echo 'test'"

        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = ENCLOSURE_GROUPS
        mock_ov_instance.enclosure_groups.get_script.return_value = configuration_script

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupFactsModule().run()

        mock_ov_instance.enclosure_groups.get_by.assert_called_once_with('name', ENCLOSURE_GROUP_NAME)
        mock_ov_instance.enclosure_groups.get_script.assert_called_once_with(id_or_uri=ENCLOSURE_GROUP_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                enclosure_groups=ENCLOSURE_GROUPS,
                enclosure_group_script=configuration_script
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self,
                                                           mock_ansible_module,
                                                           mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
