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
- name: Gather facts about all Scopes
  oneview_scope_facts:
    config: "{{ config }}"
  delegate_to: localhost
- name: Create a User
  oneview_user:
    config: "{{ config }}"
    state: present
    data:
      userName: "{{ user_name }}"
      password: "myPass1234"
      emailAddress: "{{ email }}"
      enabled: true
      fullName: "testUser101"
      mobilePhone: '555-2121'
      officePhone: '555-1212'
      permissions:
        - roleName: "Read only"
          scopeUri: "/rest/scopes/6cf6d4da-1b5e-4322-9dff-6ef545ad700f"
        - roleName: "Infrastructure administrator"
          scopeUri: "/rest/scopes/c7cab507-b49a-422d-9765-aff784112092"
  delegate_to: localhost
  register: user_1
- name: Do nothing with the User when no changes are provided
  oneview_user:
    config: "{{ config }}"
    state: present
    data:
      userName: "{{ user_name }}"
      emailAddress: "{{ email }}"
      enabled: true
      fullName: "testUser101"
      mobilePhone: '555-2121'
      officePhone: '555-1212'
      permissions:
        - roleName: "Read only"
          scopeUri: "/rest/scopes/6cf6d4da-1b5e-4322-9dff-6ef545ad700f"
        - roleName: "Infrastructure administrator"
          scopeUri: "/rest/scopes/c7cab507-b49a-422d-9765-aff784112092"
  delegate_to: localhost
  register: user_1
  delegate_to: localhost
- name: Update the User changing the attribute enabled to False
  oneview_user:
    config: "{{ config }}"
    state: present
    data:
      userName: "{{ user_name }}"
      enabled: false
  delegate_to: localhost
- name: Adds multiple new local users to the appliance
  oneview_user:
    config: "{{ config }}"
    state: add_multiple_users
    data:
      users_list:
        - userName: "{{ user_name }}1"
          password: "myPass1234"
          emailAddress: "{{ email }}"
          enabled: true
          fullName: "testUser101"
          mobilePhone: '555-2121'
          officePhone: '555-1212'
          permissions:
            - roleName: "Read only"
            - roleName: "Infrastructure administrator"
        - userName: "{{ user_name }}2"
          password: "myPass1234"
          emailAddress: "{{ email }}"
          enabled: true
          fullName: "testUser101"
          mobilePhone: '555-2121'
          officePhone: '555-1212'
          permissions:
            - roleName: "Read only"
            - roleName: "Infrastructure administrator"
  delegate_to: localhost
- debug: var=user
- name: Validates the existence of a user with the given user name
  oneview_user:
    config: "{{ config }}"
    state: validate_user_name
    data:
      userName: "testUser"
  delegate_to: localhost
- debug: var=user
- name: Checks for the existence of a user with the specified full name
  oneview_user:
    config: "{{ config }}"
    state: validate_full_name
    data:
      fullName: "testUser101"
  delegate_to: localhost
- debug: var=user
- name: Add role to existing username
  oneview_user:
    config: "{{ config }}"
    state: add_role_to_username
    data:
      userName: "testUser"
      role_list:
        - roleName: "Backup administrator"
        - roleName: "Scope administrator"
  delegate_to: localhost
- debug: var=user
- name: Update role to existing username
  oneview_user:
    config: "{{ config }}"
    state: update_role_to_username
    data:
      userName: "testUser"
      role_list:
        - roleName: "Infrastructure administrator"
        - roleName: "Read only"
  delegate_to: localhost
- debug: var=user
- name: remove role from existing username
  oneview_user:
    config: "{{ config }}"
    state: remove_role_from_username
    data:
      userName: "testUser"
      roleName: "Read only"
  delegate_to: localhost
- debug: var=user
- name: Delete single user
  oneview_user:
    config: "{{ config }}"
    state: absent
    data:
      userName: "testUser"
  delegate_to: localhost
- debug: var=user
- name: Delete multiple users
  oneview_user:
    config: "{{ config }}"
    state: delete_multiple_users
    data:
      users_list:
        - "testUser1"
        - "testUser2"
  delegate_to: localhost
- debug: var=user
- name: Create a User for automation
  oneview_user:
    config: "{{ config }}"
    state: present
    data:
      userName: "{{ user_name }}"
      password: "myPass1234"
      emailAddress: "{{ email }}"
      enabled: true
      fullName: "testUser101"
      mobilePhone: '555-2121'
      officePhone: '555-1212'
      permissions:
        - roleName: "Read only"
        - roleName: "Infrastructure administrator"
  delegate_to: localhost
  register: user_1
'''

RETURN = '''
user:
    description: Has the facts about the OneView Users.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, compare


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
    MSG_USERNAME_MISSING = 'userName field is missing.'
    MSG_USERNAME_DOES_NOT_EXIT = 'userName doesn\'t exist.'
    MSG_ROLELIST_MISSING = 'role_list field is missing.'
    MSG_PASSWORD_MISSING =  'either oldPassword or newPassword field is missing.'
    MSG_ROLENAME_MISSING = 'roleName field is missing.'

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
        if self.data.get('userName'):
            self.current_resource = self.resource_client.get_by_userName(self.data['userName'])
            if self.state == 'present':
                return self.__present(self.current_resource)

            elif self.state == 'absent':
                return self.resource_absent()

            if self.current_resource:
                if self.data.get('role_list'):
                    if self.state == 'add_role_to_username':
                        resource = self.resource_client.add_role_to_userName(self.data['userName'], self.data['role_list']).data
                        return dict(changed=True, msg=self.MSG_ADDED_ROLE, ansible_facts=dict(user=resource))
                    elif self.state == 'update_role_to_username':
                        resource = self.resource_client.update_role_to_userName(self.data['userName'], self.data['role_list'])
                        return dict(changed=True, msg=self.MSG_UPDATED_ROLE, ansible_facts=dict(user=resource))

                elif self.state == 'remove_role_from_username':
                    if self.data.get('roleName'):
                        resource = self.resource_client.remove_role_from_username(self.data['userName'], self.data['roleName'])
                        return dict(changed=True, msg=self.MSG_DELETED_ROLE, ansible_facts=dict(user=resource))
                    else:
                        return dict(failed=True, msg=self.MSG_ROLENAME_MISSING)

                elif self.state == 'validate_user_name':
                    resource = self.resource_client.validate_user_name(self.data['userName']).data
                    return dict(changed=True, msg=self.MSG_VALIDATED_USERNAME, ansible_facts=dict(user=resource))

                elif self.state == 'set_password':
                    if self.data.get('oldPassword') and self.data.get('newPassword'):
                        resource = self.resource_client.change_password(self.data)
                        return dict(changed=True, msg=self.MSG_PASSWORD_UPDATED, ansible_facts=dict(user=resource))
                    else:
                        return dict(failed=True, msg=self.MSG_PASSWORD_MISSING)
                else:
                    return dict(failed=True, msg=self.MSG_ROLELIST_MISSING)
            else:
                return dict(failed=True, msg=self.MSG_USERNAME_DOES_NOT_EXIT)

        elif not self.data.get('userName') and (self.data.get('users_list') or self.data.get('fullName')):
            if self.state == 'delete_multiple_users':
                self.resource_client.delete_multiple_user(self.data['users_list'])
                return dict(changed=True, msg=self.MSG_MULTIPLE_USER_DELETED, ansible_facts=dict(user=True))

            elif self.state == 'add_multiple_users':
                resource = self.resource_client.create_multiple_user(self.data['users_list']).data
                return dict(changed=True, msg=self.MSG_MULTIPLE_USER_CREATED, ansible_facts=dict(user=resource))

            elif self.state == 'validate_full_name':
                resource = self.resource_client.validate_full_name(self.data['fullName']).data
                return dict(changed=True, msg=self.MSG_VALIDATED_FULLNAME, ansible_facts=dict(user=resource))

        else:
            return dict(failed=True, msg=self.MSG_USERNAME_MISSING)

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
