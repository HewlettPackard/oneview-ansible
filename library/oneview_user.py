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
    - "python >= 2.7.9"
    - "hpeOneView >= 3.2.0"
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

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleException, compare
from hpeOneView.exceptions import HPEOneViewException


class UserModule(OneViewModuleBase):
    MSG_CREATED = 'User created successfully.'
    MSG_UPDATED = 'User updated successfully.'
    MSG_DELETED = 'User deleted successfully.'
    MSG_ALREADY_PRESENT = 'User is already present.'
    MSG_ALREADY_ABSENT = 'User is already absent.'
    MSG_PASSWORD_UPDATED = "User password set successfully."
    RESOURCE_FACT_NAME = 'user'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent', 'set_password']))

        super(UserModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                         validate_etag_support=True)

        self.resource_client = self.oneview_client.users

    def execute_module(self):
        # Allows usage of 'name' or 'userName' instead of enforcing 'userName'.
        # 'name' takes precedence over 'userName' if used.
        if self.data.get("name") is not None:
            self.data["userName"] = self.data.pop("name")
        try:
            resource = self.resource_client.get_by('name', self.data['userName'])
        except HPEOneViewException:
            resource = None

        if self.state == 'present':
            return self.__present(resource)
        elif self.state == 'absent':
            return self.resource_absent(resource)
        elif self.state == 'set_password':
            return self.__set_password(resource)

    def __present(self, resource):

        changed = False
        msg = ''
        if not resource:
            resource = self.oneview_client.users.create(self.data)
            msg = self.MSG_CREATED
            changed = True
        else:
            merged_data = resource.copy()
            merged_data.update(self.data)

            # remove password, it cannot be used in comparison
            if 'password' in merged_data:
                del merged_data['password']

            if compare(resource, merged_data):
                msg = self.MSG_ALREADY_PRESENT
            else:
                resource = self.resource_client.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(user=resource))

    def __set_password(self, resource):

        if not resource:
            raise OneViewModuleException('The specified user does not exist.')
        if 'password' not in self.data:
            raise OneViewModuleException('This state requires a password to be declared.')
        resource = self.resource_client.update(self.data)
        return dict(changed=True, msg=self.MSG_PASSWORD_UPDATED, ansible_facts=dict(user=resource))


def main():
    UserModule().run()


if __name__ == '__main__':
    main()
