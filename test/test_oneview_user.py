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

from copy import deepcopy
from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import (UserModule,
                                   OneViewModuleException)


FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_PARAMS = dict(
    userName='testUser',
    password='secret',
    emailAddress='testUser@example.com',
    enabled='true',
    fullName='testUser101'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=DEFAULT_PARAMS
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(userName=DEFAULT_PARAMS['userName'],
              enabled=False)
)

PARAMS_FOR_SET_PASSWORD = dict(
    config='config.json',
    state='set_password',
    data=dict(userName=DEFAULT_PARAMS['userName'],
              oldPassword='oldPassword',
              newPassword='newPassword')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(userName=DEFAULT_PARAMS['userName'])
)

PARAMS_DELETE_MULTIPLE_USER = dict(
    config='config.json',
    state='delete_multiple_users',
    data=dict(users_list=['testUser1', 'testUser2'])
)

PARAMS_ADD_MULTIPLE_USER = dict(
    config='config.json',
    state='add_multiple_users',
    data=dict(users_list=["testUser1", "testUser2"])
)

PARAMS_VALIDATE_FULLNAME = dict(
    config='config.json',
    state='validate_full_name',
    data=dict(fullName='Testuser')
)

PARAMS_ADD_ROLE = dict(
    config='config.json',
    state='add_role_to_username',
    data=dict(userName='testUser',
              role_list=['role1', 'role2'])
)

PARAMS_UPDATE_ROLE = dict(
    config='config.json',
    state='update_role_to_username',
    data=dict(userName='testUser',
              role_list=['role1', 'role2'])
)

PARAMS_REMOVE_ROLE = dict(
    config='config.json',
    state='remove_role_from_username',
    data=dict(userName='testUser',
              roleName='role1')
)

PARAMS_VALIDATE_USERNAME = dict(
    config='config.json',
    state='validate_user_name',
    data=dict(userName='Testuser')
)

DEFAULT_ROLE = dict(
    roleName='Infrastructure administrator',
    uri='AAAA-BBBB-CCCCC'
)

PARAMS_MISSING_USERNAME = dict(
    config='config.json',
    state='add_role_to_username',
    data=dict()
)


@pytest.mark.resource(TestUserModule='users')
class TestUserModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_user(self):
        self.resource.get_by_userName.return_value = None
        self.resource.data = DEFAULT_PARAMS
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_CREATED,
            ansible_facts=dict(user=DEFAULT_PARAMS)
        )

    def test_should_not_update_when_data_is_equals(self):
        data_for_comparison = deepcopy(DEFAULT_PARAMS)
        data_for_comparison.pop('password')
        self.resource.data = data_for_comparison
        self.resource.get_by_userName.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UserModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(user=data_for_comparison)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_PARAMS.copy()

        self.resource.data = DEFAULT_PARAMS
        self.resource.get_by_userName.return_value = self.resource
        self.resource.data = data_merged
        self.resource.update.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_UPDATED,
            ansible_facts=dict(user=data_merged)
        )

    def test_should_remove_user(self):
        self.resource.data = DEFAULT_PARAMS
        self.resource.get_by_userName.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_DELETED
        )

    def test_should_do_nothing_when_user_not_exist(self):
        self.resource.get_by_userName.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UserModule.MSG_ALREADY_ABSENT
        )

    def test_set_password_to_a_user(self):

        self.resource.get_by_userName.return_value = self.resource
        self.resource.change_password.return_value = DEFAULT_PARAMS
        self.mock_ansible_module.params = PARAMS_FOR_SET_PASSWORD

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_PASSWORD_UPDATED,
            ansible_facts=dict(user=DEFAULT_PARAMS)
        )

    def test_requires_password_for_set_password(self):

        self.resource.get_by_userName.return_value = self.resource
        data_for_comparison = deepcopy(PARAMS_FOR_SET_PASSWORD)
        data_for_comparison['data'].pop('oldPassword')
        self.mock_ansible_module.params = data_for_comparison

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_PASSWORD_MISSING)

    def test_requires_existing_resource_for_set_password(self):

        self.resource.get_by_userName.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_SET_PASSWORD

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_USERNAME_DOES_NOT_EXIT)

    def test_delete_multiple_user(self):

        self.resource.delete_multiple_user.return_value = True
        self.mock_ansible_module.params = PARAMS_DELETE_MULTIPLE_USER

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_MULTIPLE_USER_DELETED,
            ansible_facts=dict(user=True))

    def test_delete_multiple_user_with_missing_field(self):

        removed_data = deepcopy(PARAMS_DELETE_MULTIPLE_USER)
        removed_data['data'].pop('users_list')
        self.mock_ansible_module.params = removed_data

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_USERLIST_MISSING)

    def test_add_multiple_users(self):

        data1 = deepcopy(DEFAULT_PARAMS)
        data2 = deepcopy(DEFAULT_PARAMS)
        self.resource.data = [data1, data2]
        self.resource.create_multiple_user.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_ADD_MULTIPLE_USER

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_MULTIPLE_USER_CREATED,
            ansible_facts=dict(user=[data1, data2]))

    def test_validate_full_name(self):

        self.resource.data = True
        self.resource.validate_full_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_VALIDATE_FULLNAME

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_VALIDATED_FULLNAME,
            ansible_facts=dict(user=True))

    def test_validate_full_name_with_missing_field(self):

        removed_data = deepcopy(PARAMS_VALIDATE_FULLNAME)
        removed_data['data'].pop('fullName')
        self.mock_ansible_module.params = removed_data

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_FULLNAME_MISSING)

    def test_add_role_to_username(self):

        self.resource.get_by_userName.return_value = self.resource
        self.resource.data = DEFAULT_ROLE
        self.resource.add_role_to_userName.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_ADD_ROLE

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_ADDED_ROLE,
            ansible_facts=dict(user=DEFAULT_ROLE)
        )

    def test_update_role_to_userName(self):

        self.resource.get_by_userName.return_value = self.resource
        self.resource.update_role_to_userName.return_value = DEFAULT_ROLE
        self.mock_ansible_module.params = PARAMS_UPDATE_ROLE

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_UPDATED_ROLE,
            ansible_facts=dict(user=DEFAULT_ROLE)
        )

    def test_missing_field_role_list(self):

        removed_data = deepcopy(PARAMS_ADD_ROLE)
        removed_data['data'].pop('role_list')
        self.resource.get_by_userName.return_value = self.resource
        self.mock_ansible_module.params = removed_data

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_ROLELIST_MISSING
        )

    def test_remove_role_from_username(self):

        self.resource.get_by_userName.return_value = self.resource
        self.resource.remove_role_from_username.return_value = True
        self.mock_ansible_module.params = PARAMS_REMOVE_ROLE

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_DELETED_ROLE,
            ansible_facts=dict(user=True)
        )

    def test_missing_field_rolename(self):

        removed_data = deepcopy(PARAMS_REMOVE_ROLE)
        removed_data['data'].pop('roleName')
        self.resource.get_by_userName.return_value = self.resource
        self.mock_ansible_module.params = removed_data

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_ROLENAME_MISSING
        )

    def test_validate_user_name(self):

        self.resource.get_by_userName.return_value = self.resource
        self.resource.data = True
        self.resource.validate_user_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_VALIDATE_USERNAME

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_VALIDATED_USERNAME,
            ansible_facts=dict(user=True)
        )

    def test_missing_filed_username(self):

        self.mock_ansible_module.params = PARAMS_MISSING_USERNAME

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=UserModule.MSG_USERNAME_MISSING
        )


if __name__ == '__main__':
    pytest.main([__file__])
