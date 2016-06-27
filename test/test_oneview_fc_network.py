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
from oneview_fc_network import FcNetworkModule
from oneview_fc_network import FC_NETWORK_CREATED, FC_NETWORK_ALREADY_EXIST, FC_NETWORK_UPDATED
from oneview_fc_network import FC_NETWORK_DELETED, FC_NETWORK_ALREADY_ABSENT

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'],
              fabricType='DirectAttach')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class FcNetworkPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_create_new_fc_network(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = []
        mock_ov_instance.fc_networks.create.return_value = DEFAULT_FC_NETWORK_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FC_NETWORK_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=FC_NETWORK_ALREADY_EXIST,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]
        mock_ov_instance.fc_networks.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FC_NETWORK_UPDATED,
            ansible_facts=dict(fc_network=data_merged)
        )


class FcNetworkAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_remove_fc_network(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FC_NETWORK_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_do_nothing_when_fc_network_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=FC_NETWORK_ALREADY_ABSENT
        )


class FcNetworkErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_not_update_when_create_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = []
        mock_ov_instance.fc_networks.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, FcNetworkModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_fc_network.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]
        mock_ov_instance.fc_networks.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, FcNetworkModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
