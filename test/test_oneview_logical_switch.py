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
from oneview_logical_switch import LogicalSwitchModule
from oneview_logical_switch import LOGICAL_SWITCH_CREATED, LOGICAL_SWITCH_DELETED, LOGICAL_SWITCH_ALREADY_EXIST, \
    LOGICAL_SWITCH_ALREADY_ABSENT, LOGICAL_SWITCH_REFRESHED, LOGICAL_SWITCH_NOT_FOUND
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SWITCH_NAME = 'Test Logical Switch'

LOGICAL_SWITCH_FROM_ONEVIEW = dict(
    name=DEFAULT_SWITCH_NAME,
    uri='/rest/logical-switches/f0d7ad37-2053-46ac-bb11-4ebdd079bb66'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(logicalSwitch=dict(name='OneView-Enclosure',
                                 logicalSwitchGroupUri="/rest/logical-switch-groups/dce11b79-6fce-48af-84fb-a315b9644",
                                 switchCredentialConfiguration=[]),  # assume it contains the switches configuration
              logicalSwitchCredentials=[]) # assume it contains the switches credentials
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(logicalSwitch=dict(name='OneView-Enclosure'))
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(logicalSwitch=dict(name='OneView-Enclosure'))
)


class EnclosurePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_create_new_logical_switch(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = []
        mock_ov_instance.logical_switches.create.return_value = LOGICAL_SWITCH_FROM_ONEVIEW

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_SWITCH_CREATED,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_not_create_when_logical_switch_already_exist(self, mock_ansible_module,
                                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_SWITCH_ALREADY_EXIST,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW)
        )


class LogicalSwitchAbsentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_delete_logical_switch(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_SWITCH_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_do_nothing_when_logical_switch_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_SWITCH_ALREADY_ABSENT
        )


class LogicalSwitchRefreshedStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_refresh_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        mock_ov_instance.logical_switches.refresh.return_value = LOGICAL_SWITCH_FROM_ONEVIEW

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW),
            msg=LOGICAL_SWITCH_REFRESHED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_do_nothing_when_logical_switch_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalSwitchModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_SWITCH_NOT_FOUND
        )


class LogicalSwitchErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = []
        mock_ov_instance.logical_switches.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalSwitchModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        mock_ov_instance.logical_switches.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalSwitchModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_switch.AnsibleModule')
    def test_should_fail_when_refresh_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_switches.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        mock_ov_instance.logical_switches.refresh.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalSwitchModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

if __name__ == '__main__':
    unittest.main()
