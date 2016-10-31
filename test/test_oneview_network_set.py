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
from oneview_network_set import NetworkSetModule
from oneview_network_set import NETWORK_SET_CREATED, NETWORK_SET_UPDATED, NETWORK_SET_DELETED, \
    NETWORK_SET_ALREADY_EXIST, NETWORK_SET_ALREADY_ABSENT, NETWORK_SET_NEW_NAME_INVALID, \
    NETWORK_SET_ENET_NETWORK_NOT_FOUND
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'

NETWORK_SET = dict(
    name='OneViewSDK Test Network Set',
    networkUris=['/rest/ethernet-networks/aaa-bbb-ccc']
)

NETWORK_SET_WITH_NEW_NAME = dict(name='OneViewSDK Test Network Set - Renamed')

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              newName=NETWORK_SET['name'] + " - Renamed",
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc', 'Name of a Network'])
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=NETWORK_SET['name'])
)


class NetworkSetClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class NetworkSetPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_create_new_network_set(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = []
        mock_ov_instance.network_sets.create.return_value = NETWORK_SET

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_CREATED,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = [NETWORK_SET]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=NETWORK_SET_ALREADY_EXIST,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = dict(name=NETWORK_SET['name'] + " - Renamed",
                           networkUris=['/rest/ethernet-networks/aaa-bbb-ccc', '/rest/ethernet-networks/ddd-eee-fff'])

        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.side_effect = [NETWORK_SET], []
        mock_ov_instance.network_sets.update.return_value = data_merged
        mock_ov_instance.ethernet_networks.get_by.return_value = [{'uri': '/rest/ethernet-networks/ddd-eee-fff'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_UPDATED,
            ansible_facts=dict(network_set=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_raise_exception_when_new_name_already_used(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.side_effect = [NETWORK_SET], [NETWORK_SET_WITH_NEW_NAME]
        mock_ov_instance.ethernet_networks.get_by.return_value = [{'uri': '/rest/ethernet-networks/ddd-eee-fff'}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=NETWORK_SET_NEW_NAME_INVALID)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_raise_exception_when_ethernet_network_not_found(self, mock_ansible_module,
                                                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.side_effect = [NETWORK_SET], []
        mock_ov_instance.ethernet_networks.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=NETWORK_SET_ENET_NETWORK_NOT_FOUND +
                                                                "Name of a Network")


class NetworkSetAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_remove_network(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = [NETWORK_SET]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_do_nothing_when_network_set_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        NetworkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=NETWORK_SET_ALREADY_ABSENT
        )


class NetworkSetErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_not_create_when_create_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = []
        mock_ov_instance.network_sets.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, NetworkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_not_update_when_update_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.side_effect = [NETWORK_SET], []
        mock_ov_instance.ethernet_networks.get_by.return_value = [{'uri': '/rest/ethernet-networks/ddd-eee-fff'}]
        mock_ov_instance.network_sets.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, NetworkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_network_set.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.network_sets.get_by.return_value = [NETWORK_SET]
        mock_ov_instance.network_sets.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, NetworkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
