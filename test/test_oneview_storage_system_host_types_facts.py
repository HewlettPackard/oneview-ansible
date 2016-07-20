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
from oneview_storage_system_host_types_facts import StorageSystemHostTypesFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_HOST_TYPES = dict(
    config='config.json'
)

HOST_TYPES = [
    "Citrix Xen Server 5.x/6.x",
    "IBM VIO Server",
]


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class StorageSystemHostTypesFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_host_types_facts.AnsibleModule')
    def test_should_get_all_host_types(self, mock_ansible_module,
                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_host_types.return_value = HOST_TYPES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_HOST_TYPES)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemHostTypesFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(oneview_storage_host_types_facts=(HOST_TYPES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_host_types_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_error(self,
                                                       mock_ansible_module,
                                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_host_types.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_HOST_TYPES)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemHostTypesFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
