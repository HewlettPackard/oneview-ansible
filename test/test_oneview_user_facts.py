#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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

import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import UserFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    userName=None,
    role=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    userName="Test User"
)

PARAMS_GET_ROLE = dict(
    config='config.json',
    role='Infrastructure administrator',
    userName=None
)

PARAMS_GET_USERROLE = dict(
    config='config.json',
    userName="testUser",
    options=["getUserRoles"]
)

PRESENT_USERS = [{
    "name": "Test User",
    "uri": "/rest/user/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

ROLE_USERS = [
    {
        "userName": "testUser1"
    },
    {
        "userName": "testUser2"
    }
]

USER_ROLE = [{
    "roleName": "Infrastructure adminstrator"
}]


@pytest.mark.resource(TestUserFactsModule='users')
class TestUserFactsModule(OneViewBaseTest):
    def test_should_get_all_users(self):
        self.resource.get_all.return_value = PRESENT_USERS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        UserFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(users=PRESENT_USERS)
        )

    def test_should_get_user_by_name(self):
        self.resource.data = PRESENT_USERS
        self.resource.get_by_userName.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        UserFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(users=PRESENT_USERS)
        )

    def test_should_get_role(self):
        self.resource.get_user_by_role.return_value = ROLE_USERS
        self.mock_ansible_module.params = PARAMS_GET_ROLE

        UserFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(role=ROLE_USERS)
        )

    def test_should_get_role_associated_with_username(self):
        self.resource.data = PRESENT_USERS
        self.resource.get_by_userName.return_value = self.resource
        self.resource.get_role_associated_with_userName.return_value = USER_ROLE
        self.mock_ansible_module.params = PARAMS_GET_USERROLE

        UserFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(users=PRESENT_USERS, user_roles=USER_ROLE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
