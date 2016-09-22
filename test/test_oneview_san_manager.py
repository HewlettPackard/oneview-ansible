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
from oneview_san_manager import SanManagerModule
from oneview_san_manager import SAN_MANAGER_CREATED, SAN_MANAGER_ALREADY_EXIST, SAN_MANAGER_UPDATED
from oneview_san_manager import SAN_MANAGER_DELETED, SAN_MANAGER_ALREADY_ABSENT

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SAN_MANAGER_TEMPLATE = dict(
    providerDisplayName='Brocade Network Advisor',
    uri='/rest/fc-sans/device-managers/UUU-AAA-BBB'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
              connectionInfo=None)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
              refreshState='RefreshPending',
              connectionInfo=None)
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
              connectionInfo=None)
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class SanManagerPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_add_new_san_manager(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = None
        mock_ov_instance.san_managers.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        mock_ov_instance.san_managers.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_CREATED,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_find_provider_uri_to_add(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = None
        mock_ov_instance.san_managers.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        mock_ov_instance.san_managers.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        provider_display_name = DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName']
        mock_ov_instance.san_managers.get_provider_uri.assert_called_once_with(provider_display_name)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SAN_MANAGER_ALREADY_EXIST,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        mock_ov_instance.san_managers.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_UPDATED,
            ansible_facts=dict(san_manager=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = None
        mock_ov_instance.san_managers.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SanManagerModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        mock_ov_instance.san_managers.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SanManagerModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class SanManagerAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_remove_san_manager(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_do_nothing_when_san_manager_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by_provider_display_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        SanManagerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SAN_MANAGER_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_san_manager.AnsibleModule')
    def test_should_fail_when_remove_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.san_managers.get_by.return_value = [DEFAULT_SAN_MANAGER_TEMPLATE]
        mock_ov_instance.san_managers.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SanManagerModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

if __name__ == '__main__':
    unittest.main()
