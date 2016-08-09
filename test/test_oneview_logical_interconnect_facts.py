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
from oneview_logical_interconnect_facts import LogicalInterconnectFactsModule

ERROR_MSG = 'Fake message error'

LOGICAL_INTERCONNECT_NAME = "test"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=LOGICAL_INTERCONNECT_NAME
)

LOGICAL_INTERCONNECT = dict(name=LOGICAL_INTERCONNECT_NAME)

ALL_INTERCONNECTS = [LOGICAL_INTERCONNECT]


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class LogicalInterconnectFactsSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_all_logical_interconnects(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_all.return_value = ALL_INTERCONNECTS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=ALL_INTERCONNECTS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_get_a_logical_interconnects_by_name(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with(
            name=LOGICAL_INTERCONNECT_NAME
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnects=LOGICAL_INTERCONNECT)
        )


class LogicalInterconnectFactsErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_facts.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_an_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnects.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
