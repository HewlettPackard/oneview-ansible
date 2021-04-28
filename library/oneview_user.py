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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_user
short_description: Manage OneView Users.
description:
    - Provides an interface to manage Users. Can create, update, and delete.
version_added: "2.3"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the User.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(set_password) will set a user password to the value specified. This operation is non-idempotent.
        choices: ['present', 'absent', 'set_password']
    data:
        description:
            - List with the User properties.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the User is present using the default configuration
  oneview_user:
    config: "{{ config_file_path }}"
    state: present
    data:
      userName: testUser
      password: pass1234
      emailAddress: testUser@example.com
      enabled: true
      fullName: testUser101
    delegate_to: localhost

- name: Ensure that the User is present with enabled 'false'
  oneview_user:
    config: "{{ config_file_path }}"
    state: present
    data:
      userName: testUser
      enabled: false
    delegate_to: localhost

- name: Ensure that the User is absent
  oneview_user:
    config: "{{ config_file_path }}"
    state: absent
    data:
      userName: testUser
    delegate_to: localhost

- name: Set the password of specified user
  oneview_user:
    config: "{{ config_file_path }}"
    state: set_password
    data:
      userName: testUser
      password: newPass1234
    delegate_to: localhost
'''

RETURN = '''
user:
    description: Has the facts about the OneView Users.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleException, compare
from hpeOneView.exceptions import HPEOneViewException


class UserModule(OneViewModule):
    MSG_CREATED = 'User created successfully.'
    MSG_MULTIPLE_USER_CREATED = 'Created multiple users successfully.'
    MSG_UPDATED = 'User updated successfully.'
    MSG_DELETED = 'User deleted successfully.'
    MSG_MULTIPLE_USER_DELETED = 'Specified users are deleted successfully'
    MSG_ALREADY_PRESENT = 'User is already present.'
    MSG_ALREADY_ABSENT = 'User is already absent.'
    MSG_ADDED_ROLE = 'Added role to existing username successfully.'
    MSG_UPDATED_ROLE = 'Updated role to existing username successfully.'
    MSG_DELETED_ROLE = 'Removed role to existing username successfully.'
    MSG_VALIDATED_USERNAME = 'Validated username successfully.'
    MSG_VALIDATED_FULLNAME = 'Validated fullname successfully.'
    MSG_PASSWORD_UPDATED = "User password set successfully."
    RESOURCE_FACT_NAME = 'users'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent', 'add_multiple_users', 'add_role_to_username', 'update_role_to_username',
                                                'validate_full_name', 'validate_user_name', 'delete_multiple_users', 'remove_role_from_username',
                                                'set_password']))

        super(UserModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                         validate_etag_support=True)

        self.resource_client = self.oneview_client.users

    def execute_module(self):
        if self.state == 'present':
            try:
                self.current_resource = self.resource_client.get_by_userName(self.data['userName'])
            except HPEOneViewException:
                self.current_resource = None
            return self.__present(self.current_resource)
        elif self.state == 'absent':
            try:
                self.current_resource = self.resource_client.get_by_userName(self.data['userName'])
            except HPEOneViewException:
                self.current_resource = None
            return self.resource_absent()
        elif self.state == 'delete_multiple_users':
            self.resource_client.delete_multiple_user(self.data['users_list'])
            return dict(changed=True, msg=self.MSG_MULTIPLE_USER_DELETED, ansible_facts=dict(user=True))
        elif self.state == 'add_multiple_users':
            resource = self.resource_client.create_multiple_user(self.data['users_list']).data
            return dict(changed=True, msg=self.MSG_MULTIPLE_USER_CREATED, ansible_facts=dict(user=resource))
        elif self.state == 'add_role_to_username':
            resource = self.resource_client.add_role_to_userName(self.data['userName'], self.data['role_list']).data
            return dict(changed=True, msg=self.MSG_ADDED_ROLE, ansible_facts=dict(user=resource))
        elif self.state == 'update_role_to_username':
            resource = self.resource_client.update_role_to_userName(self.data['userName'], self.data['role_list'])
            return dict(changed=True, msg=self.MSG_UPDATED_ROLE, ansible_facts=dict(user=resource))
        elif self.state == 'remove_role_from_username':
            resource = self.resource_client.remove_role_from_username(self.data['userName'], self.data['roleName'])
            return dict(changed=True, msg=self.MSG_DELETED_ROLE, ansible_facts=dict(user=resource))
        elif self.state == 'validate_user_name':
            resource = self.resource_client.validate_user_name(self.data['userName']).data
            return dict(changed=True, msg=self.MSG_VALIDATED_USERNAME, ansible_facts=dict(user=resource))
        elif self.state == 'validate_full_name':
            resource = self.resource_client.validate_full_name(self.data['fullName']).data
            return dict(changed=True, msg=self.MSG_VALIDATED_FULLNAME, ansible_facts=dict(user=resource))
        elif self.state == 'set_password':
            resource = self.resource_client.change_password(self.data)
            return dict(changed=True, msg=self.MSG_PASSWORD_UPDATED, ansible_facts=dict(user=resource))

    def __present(self, resource):

        changed = False
        msg = ''
        if not resource:
            resource = self.resource_client.create(self.data)
            msg = self.MSG_CREATED
            changed = True
        else:
            merged_data = resource.data.copy()
            merged_data.update(self.data)

            # remove password, it cannot be used in comparison
            if 'password' in merged_data:
                del merged_data['password']

            if compare(resource.data, merged_data):
                msg = self.MSG_ALREADY_PRESENT
            else:
                resource = self.resource_client.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(user=resource.data))


def main():
    UserModule().run()


if __name__ == '__main__':
    main()
