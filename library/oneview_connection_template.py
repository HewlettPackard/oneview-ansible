#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
module: oneview_connection_template
short_description: Manage the OneView Connection Template resources.
description:
    - "Provides an interface to manage the Connection Template resources. Can update."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Connection Template resource.
              C(present) will ensure data properties are compliant with OneView.
        choices: ['present']
        required: true
    data:
        description:
            - List with Connection Template properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Update the Connection Template
  oneview_connection_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
        name: 'name1304244267-1467656930023'
        type : "connection-template"
        bandwidth :
            maximumBandwidth : 10000
            typicalBandwidth : 2000
        newName : "CT-23"
  delegate_to: localhost
'''

RETURN = '''
connection_template:
    description: Has the OneView facts about the Connection Template.
    returned: On 'present' state, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import (OneViewModule, OneViewModuleValueError,
                                          OneViewModuleResourceNotFound, compare)


class ConnectionTemplateModule(OneViewModule):
    MSG_UPDATED = 'Connection Template updated successfully.'
    MSG_NOT_FOUND = 'Connection Template was not found.'
    MSG_ALREADY_PRESENT = 'Connection Template is already updated.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present']
            ),
            data=dict(required=True, type='dict')
        )
        super(ConnectionTemplateModule, self).__init__(additional_arg_spec=argument_spec)

        self.set_resource_object(self.oneview_client.connection_templates)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        if self.state == 'present':
            changed, msg = self.__present()
            ansible_facts = dict(connection_template=self.current_resource.data)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self):
        changed = False
        msg = ''

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)
        else:
            if 'newName' in self.data:
                self.data['name'] = self.data.pop('newName')

            changed, msg = self._update_resource()

        return changed, msg


def main():
    ConnectionTemplateModule().run()


if __name__ == '__main__':
    main()
