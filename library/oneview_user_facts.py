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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_user_facts
short_description: Retrieve the facts about one or more of the OneView Users.
description:
    - Retrieve the facts about one or more of the Users from OneView.
version_added: "2.3"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.1.0"
author:
    "Felipe Bulsoni (@fgbulsoni)"
options:
    userName:
      description:
        - User name.
      required: false
    role:
      description:
        - Role name.
      required: false
    options:
      description:
        - "To gather the additonal facts about the roles associated with username.
          Options allowed: C(getUserRoles) retrieves the list of roles associated with username."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Users
  oneview_user_facts:
    config: "{{ config }}"

- debug: var=users

- name: Gather paginated, filtered and sorted facts about Users
  oneview_user_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'emailAddress:descending'
      filter: 'enabled=true'

- debug: var=users

- name: Gather facts about a User by name
  oneview_user_facts:
    config: "{{ config }}"
    userName: "testUser"

- debug: var=users

- name: Gather facts about the users who have permissions that use a specified role
  oneview_user_facts:
    config: "{{ config }}"
    role: "{{ role }}"
  delegate_to: localhost

- debug: var=role

- name: Gather facts about lists of user's roles
  oneview_user_facts:
    config: "{{ config }}"
    userName: "testUser"
    options:
        - getUserRoles
  delegate_to: localhost

- debug: var=users
'''

RETURN = '''
users:
    description: It has all the OneView facts about the Users.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class UserFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            userName=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
            role=dict(required=False, type='str'),
            options=dict(required=False, type='list')
        )

        super(UserFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.users)

    def execute_module(self):

        ansible_facts = {}
        if self.module.params['userName']:
            self.current_resource = self.resource_client.get_by_userName(self.module.params['userName'])
            ansible_facts['users'] = self.current_resource.data
        elif self.module.params['role']:
            ansible_facts['role'] = self.resource_client.get_user_by_role(self.module.params['role'])
        else:
            ansible_facts['users'] = self.resource_client.get_all(**self.facts_params)

        if self.module.params['userName'] and self.options.get('getUserRoles'):
            ansible_facts['user_roles'] = self.resource_client.get_role_associated_with_userName(self.module.params['userName'])

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    UserFactsModule().run()


if __name__ == '__main__':
    main()
