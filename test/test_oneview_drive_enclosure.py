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
from oneview_drive_enclosure import DriveEnclosureModule, DRIVE_ENCLOSURE_NAME_REQUIRED, DRIVE_ENCLOSURE_NOT_FOUND

from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

FAKE_MSG_ERROR = 'Fake message error'

DRIVE_ENCLOSURE_URI = '/rest/drive-enclosures/SN123101'

DICT_DEFAULT_DRIVE_ENCLOSURE = {
    'manufacturer': 'HPE',
    'model': 'Synergy D3940 Storage Module',
    'name': '0000A66102, bay 1',
    'powerState': 'On',
    'productName': 'Storage Enclosure 500143803110129D',
    'refreshState': 'NotRefreshing',
    'serialNumber': 'SN123101',
    'state': 'Monitored',
    'stateReason': None,
    'status': 'OK',
    'temperature': 11,
    'type': 'drive-enclosure',
    'uidState': 'Off',
    'uri': DRIVE_ENCLOSURE_URI,
    'wwid': '500143803110129D'
}

YAML_DRIVE_ENCLOSURE_POWER_STATE = """
    config: "{{ config }}"
    state: power_state_set
    data:
        name: '0000A66102, bay 1'
        powerState: 'Off'
"""

YAML_DRIVE_ENCLOSURE_UID_STATE = """
    config: "{{ config_file_path }}"
    state: uid_state_set
    data:
        name: '0000A66102, bay 1'
        uidState: 'On'
"""

YAML_DRIVE_ENCLOSURE_HARD_RESET_STATE = """
    config: "{{ config_file_path }}"
    state: hard_reset_state_set
    data:
        name: '0000A66102, bay 1'
"""

YAML_DRIVE_ENCLOSURE_REFRESH_STATE = """
    config: "{{ config_file_path }}"
    state: refresh_state_set
    data:
        name: '0000A66102, bay 1'
        refreshState: 'RefreshPending'
"""

YAML_WITHOUT_NAME = """
    config: "{{ config }}"
    state: power_state_set
    data:
        powerState: 'Off'
"""


class DriveEnclosureClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class DriveEnclosureSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_raise_exception_when_name_not_defined(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_WITHOUT_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=DRIVE_ENCLOSURE_NAME_REQUIRED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_raise_exception_when_resource_not_found(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = []
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=DRIVE_ENCLOSURE_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_power_off(self, mock_ansible_module, mock_from_json_file):
        mock_return_patch = {'name': 'mock return'}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        mock_ov_instance.drive_enclosures.patch.return_value = mock_return_patch
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ov_instance.drive_enclosures.patch.assert_called_once_with(
            DRIVE_ENCLOSURE_URI, operation='replace', path='/powerState', value='Off')

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=mock_return_patch)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_not_power_off_when_already_off(self, mock_ansible_module, mock_from_json_file):
        drive_enclosure = DICT_DEFAULT_DRIVE_ENCLOSURE.copy()
        drive_enclosure['powerState'] = 'Off'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [drive_enclosure]
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_POWER_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=drive_enclosure)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_turn_uid_on(self, mock_ansible_module, mock_from_json_file):
        mock_return_patch = {'name': 'mock return'}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        mock_ov_instance.drive_enclosures.patch.return_value = mock_return_patch
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_UID_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ov_instance.drive_enclosures.patch.assert_called_once_with(
            DRIVE_ENCLOSURE_URI, operation='replace', path='/uidState', value='On')

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=mock_return_patch)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_not_turn_uid_off_when_already_on(self, mock_ansible_module, mock_from_json_file):
        drive_enclosure = DICT_DEFAULT_DRIVE_ENCLOSURE.copy()
        drive_enclosure['uidState'] = 'On'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [drive_enclosure]
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_UID_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=drive_enclosure)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_request_hard_reset(self, mock_ansible_module, mock_from_json_file):
        mock_return_patch = {'name': 'mock return'}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        mock_ov_instance.drive_enclosures.patch.return_value = mock_return_patch
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_HARD_RESET_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ov_instance.drive_enclosures.patch.assert_called_once_with(
            DRIVE_ENCLOSURE_URI, operation='replace', path='/hardResetState', value='Reset')

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=mock_return_patch)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure.AnsibleModule')
    def test_should_refresh(self, mock_ansible_module, mock_from_json_file):
        mock_return_refresh = {'name': 'mock return'}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        mock_ov_instance.drive_enclosures.refresh_state.return_value = mock_return_refresh
        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DRIVE_ENCLOSURE_REFRESH_STATE)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureModule().run()

        mock_ov_instance.drive_enclosures.refresh_state.assert_called_once_with(
            DRIVE_ENCLOSURE_URI, {'refreshState': 'RefreshPending'})

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=mock_return_refresh)
        )


if __name__ == '__main__':
    unittest.main()
