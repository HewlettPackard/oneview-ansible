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
from oneview_storage_system_pools_facts import StorageSystemPoolsFactsModule, STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING, \
    STORAGE_SYSTEM_NOT_FOUND

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Systems"
)

PARAMS_GET_BY_IP_HOSTNAME = dict(
    config='config.json',
    ip_hostname='10.0.0.0'
)


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class StorageSystemPoolsFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_should_get_storage_system_by_name(self, mock_ansible_module,
                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_name.return_value = {"name": "Storage System Name",
                                                                     "uri": "uri"}
        mock_ov_instance.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(oneview_storage_pools_facts=({"name": "Storage Pool"}))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_error(self,
                                                       mock_ansible_module,
                                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_name.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_should_get_storage_system_by_ip_hostname(self, mock_ansible_module,
                                                      mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = {"ip_hostname": "10.0.0.0",
                                                                            "uri": "uri"}
        mock_ov_instance.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_IP_HOSTNAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(oneview_storage_pools_facts=({"name": "Storage Pool"}))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_get_storage_system_pool_by_ip_hostname_mandatory_missing(self, mock_ansible_module,
                                                                      mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = {"ip_hostname": "10.0.0.0",
                                                                            "uri": "uri"}
        mock_ov_instance.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_MANDATORY_MISSING)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_get_storage_system_pool_by_ip_hostname_pool_not_found(self, mock_ansible_module,
                                                                   mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.return_value = {}
        mock_ov_instance.storage_systems.get_storage_pools.return_value = {"name": "Storage Pool"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_IP_HOSTNAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=STORAGE_SYSTEM_NOT_FOUND)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_system_pools_facts.AnsibleModule')
    def test_should_fail_when_get_by_ip_hostname_raises_error(self,
                                                              mock_ansible_module,
                                                              mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_systems.get_by_ip_hostname.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_IP_HOSTNAME)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageSystemPoolsFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
