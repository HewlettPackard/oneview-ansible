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
from oneview_interconnect_type_facts import InterconnectTypeFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="HP VC Flex-10 Enet Module"
)

PRESENT_TYPES = [{
    "name": "HP VC Flex-10 Enet Module",
    "uri": "/rest/interconnect-types/e6d938ac-0588-44c9-95f2-610f3da4a941"
}]


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class InterconnectTypeFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_type_facts.AnsibleModule')
    def test_should_get_all_interconnect_types(self, mock_ansible_module,
                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_types.get_all.return_value = PRESENT_TYPES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectTypeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_type_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_types.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectTypeFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_type_facts.AnsibleModule')
    def test_should_get_interconnect_type_by_name(self, mock_ansible_module,
                                                  mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_types.get_by.return_value = PRESENT_TYPES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectTypeFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_type_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_types.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectTypeFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
