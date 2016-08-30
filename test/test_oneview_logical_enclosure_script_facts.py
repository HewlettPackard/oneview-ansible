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
from oneview_logical_enclosure_script_facts import LogicalEnclosureScriptFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Enclosures"
)


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class LogicalEnclosureScriptFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure_script_facts.AnsibleModule')
    def test_should_get_an_logical_enclosure_script(self, mock_ansible_module,
                                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = {"uri": "Logical Enclosure Name"}
        mock_ov_instance.logical_enclosures.get_script.return_value = "the script"

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureScriptFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosure_script="the script")
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure_script_facts.AnsibleModule')
    def test_should_fail_when_get_by_raises_exception(self, mock_ansible_module,
                                                      mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureScriptFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure_script_facts.AnsibleModule')
    def test_should_fail_when_get_script_raises_exception(self, mock_ansible_module,
                                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = {"uri": "Logical Enclosure Name"}
        mock_ov_instance.logical_enclosures.get_script.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureScriptFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
