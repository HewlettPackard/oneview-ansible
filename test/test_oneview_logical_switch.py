#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from copy import deepcopy
from hpe_test_utils import OneViewBaseTestCase
from oneview_module_loader import LogicalSwitchModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SWITCH_NAME = 'Test Logical Switch'

LOGICAL_SWITCH_FROM_ONEVIEW = dict(
    name=DEFAULT_SWITCH_NAME,
    uri='/rest/logical-switches/f0d7ad37-2053-46ac-bb11-4ebdd079bb66',
    logicalSwitchGroupUri='/rest/logical-switch-groups/af370d9a-f2f4-4beb-a1f1-670930d6741d',
    switchCredentialConfiguration=[{'logicalSwitchManagementHost': '172.16.1.1'},
                                   {'logicalSwitchManagementHost': '172.16.1.2'}]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(
        logicalSwitch=dict(
            name=DEFAULT_SWITCH_NAME,
            logicalSwitchGroupName="Logical Switch Group Name",
            switchCredentialConfiguration=[]
        ),  # assume it contains the switches configuration
        logicalSwitchCredentials=[]
    )  # assume this list contains the switches credentials
)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='updated',
    data=dict(
        logicalSwitch=dict(
            name=DEFAULT_SWITCH_NAME,
            newName='Test Logical Switch - Renamed'
        ),
        logicalSwitchCredentials=[]
    )  # assume this list contains the switches credentials
)

PARAMS_FOR_UPDATE_WITH_SWITCHES_AND_GROUPS = dict(
    config='config.json',
    state='updated',
    data=dict(
        logicalSwitch=dict(
            name=DEFAULT_SWITCH_NAME,
            logicalSwitchGroupName='Logical Switch Group Name',
            switchCredentialConfiguration=[
                {'logicalSwitchManagementHost': '172.16.1.3'},
                {'logicalSwitchManagementHost': '172.16.1.4'}
            ]
        ),
        logicalSwitchCredentials=[]
    )  # assume this list contains the switches credentials
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(logicalSwitch=dict(name=DEFAULT_SWITCH_NAME))
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(logicalSwitch=dict(name=DEFAULT_SWITCH_NAME))
)


class LogicalSwitchModuleSpec(unittest.TestCase,
                              OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchModule)
        self.resource = self.mock_ov_client.logical_switches
        self.logical_switch_group_client = self.mock_ov_client.logical_switch_groups

    def test_should_create_new_logical_switch(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.logical_switch_group_client.get_by.return_value = [{'uri': '/rest/logical-switch-groups/aa-bb-cc'}]
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchModule.MSG_CREATED,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW)
        )

    def test_should_not_create_when_logical_switch_already_exist(self):
        self.resource.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        self.logical_switch_group_client.get_by.return_value = [{'uri': '/rest/logical-switch-groups/aa-bb-cc'}]
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalSwitchModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW)
        )

    def test_should_fail_when_group_not_found(self):
        self.resource.get_by.return_value = []
        self.logical_switch_group_client.get_by.return_value = []
        self.resource.create.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LogicalSwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchModule.MSG_LOGICAL_SWITCH_GROUP_NOT_FOUND
        )

    def test_should_update_logical_switch(self):
        self.resource.get_by.side_effect = [[LOGICAL_SWITCH_FROM_ONEVIEW], []]
        self.resource.update.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.logical_switch_group_client.get_by.return_value = [{'uri': '/rest/logical-switch-groups/aa-bb-cc'}]
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchModule.MSG_UPDATED,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW)
        )

    def test_should_not_update_when_logical_switch_not_found(self):
        self.resource.get_by.side_effect = [[], []]
        self.resource.update.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.logical_switch_group_client.get_by.return_value = [{'uri': '/rest/logical-switch-groups/aa-bb-cc'}]
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        LogicalSwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchModule.MSG_LOGICAL_SWITCH_NOT_FOUND
        )

    def test_should_fail_when_group_not_found_for_update(self):
        self.resource.get_by.side_effect = [[LOGICAL_SWITCH_FROM_ONEVIEW], []]
        self.resource.update.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.logical_switch_group_client.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_WITH_SWITCHES_AND_GROUPS

        LogicalSwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchModule.MSG_LOGICAL_SWITCH_GROUP_NOT_FOUND
        )

    def test_should_fail_on_update_when_logical_switch_attribute_missing(self):
        params = deepcopy(PARAMS_FOR_UPDATE_WITH_SWITCHES_AND_GROUPS)
        del params['data']['logicalSwitch']
        self.mock_ansible_module.params = params

        LogicalSwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchModule.MSG_LOGICAL_SWITCH_NOT_FOUND
        )

    def test_should_update_with_current_switches_and_group_when_not_provided(self):
        self.resource.get_by.side_effect = [[LOGICAL_SWITCH_FROM_ONEVIEW], []]
        self.resource.update.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        LogicalSwitchModule().run()

        data_for_update = {
            'logicalSwitch': {
                'name': 'Test Logical Switch - Renamed',
                'uri': '/rest/logical-switches/f0d7ad37-2053-46ac-bb11-4ebdd079bb66',
                'logicalSwitchGroupUri': '/rest/logical-switch-groups/af370d9a-f2f4-4beb-a1f1-670930d6741d',
                'switchCredentialConfiguration': [{'logicalSwitchManagementHost': '172.16.1.1'},
                                                  {'logicalSwitchManagementHost': '172.16.1.2'}],

            },
            'logicalSwitchCredentials': []

        }
        self.resource.update.assert_called_once_with(data_for_update)

    def test_should_update_with_given_switches_and_group_when_provided(self):
        self.resource.get_by.side_effect = [[LOGICAL_SWITCH_FROM_ONEVIEW], []]
        self.resource.update.return_value = LOGICAL_SWITCH_FROM_ONEVIEW
        self.logical_switch_group_client.get_by.return_value = [{'uri': '/rest/logical-switch-groups/aa-bb-cc'}]

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_WITH_SWITCHES_AND_GROUPS

        LogicalSwitchModule().run()

        data_for_update = {
            'logicalSwitch': {
                'name': 'Test Logical Switch',
                'uri': LOGICAL_SWITCH_FROM_ONEVIEW['uri'],
                'logicalSwitchGroupUri': '/rest/logical-switch-groups/aa-bb-cc',
                'switchCredentialConfiguration': [{'logicalSwitchManagementHost': '172.16.1.3'},
                                                  {'logicalSwitchManagementHost': '172.16.1.4'}],

            },
            'logicalSwitchCredentials': []

        }
        self.resource.update.assert_called_once_with(data_for_update)

    def test_should_delete_logical_switch(self):
        self.resource.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchModule.MSG_DELETED
        )

    def test_should_do_nothing_when_logical_switch_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalSwitchModule.MSG_ALREADY_ABSENT
        )

    def test_should_refresh_logical_switch(self):
        self.resource.get_by.return_value = [LOGICAL_SWITCH_FROM_ONEVIEW]
        self.resource.refresh.return_value = LOGICAL_SWITCH_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        LogicalSwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(logical_switch=LOGICAL_SWITCH_FROM_ONEVIEW),
            msg=LogicalSwitchModule.MSG_REFRESHED
        )

    def test_should_fail_when_logical_switch_not_found(self):
        self.resource.get_by.return_value = []
        self.resource.refresh.return_value = LOGICAL_SWITCH_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        LogicalSwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchModule.MSG_LOGICAL_SWITCH_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
