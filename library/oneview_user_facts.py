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
    - "python >= 2.7.9"
    - "hpOneView >= 3.2.0"
author:
    "Felipe Bulsoni (@fgbulsoni)"
options:
    name:
      description:
        - User name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Users
  oneview_user_facts:
    config: "{{ config_file_path }}"

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
    config: "{{ config_file_path }}"
    name: user name

- debug: var=users
'''

RETURN = '''
users:
    description: It has all the OneView facts about the Users.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class UserFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(UserFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        if self.module.params['name']:
            users = self.oneview_client.users.get_by('name', self.module.params['name'])
        else:
            users = self.oneview_client.users.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(users=users))


def main():
    UserFactsModule().run()


if __name__ == '__main__':
    main()
