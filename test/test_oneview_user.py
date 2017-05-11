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

from oneview_module_loader import UserModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_PARAMS = dict(
    userName='testUser',
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
              password='False')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(userName=DEFAULT_PARAMS['userName'])
)


class UserModuleSpec(unittest.TestCase, OneViewBaseTestCase):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, UserModule)
        self.resource = self.mock_ov_client.users

    def test_should_create_new_user(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_PARAMS

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_CREATED,
            ansible_facts=dict(user=DEFAULT_PARAMS)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = DEFAULT_PARAMS

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UserModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(user=DEFAULT_PARAMS)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_PARAMS.copy()

        self.resource.get_by.return_value = DEFAULT_PARAMS
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_UPDATED,
            ansible_facts=dict(user=data_merged)
        )

    def test_should_remove_user(self):
        self.resource.get_by.return_value = [DEFAULT_PARAMS]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_DELETED
        )

    def test_should_do_nothing_when_user_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UserModule.MSG_ALREADY_ABSENT
        )

    def test_set_password_to_a_user(self):
        self.mock_ansible_module.params = PARAMS_FOR_SET_PASSWORD

        UserModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UserModule.MSG_PASSWORD_UPDATED,
        )


if __name__ == '__main__':
    unittest.main()
