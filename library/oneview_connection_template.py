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
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_connection_template
short_description: Manage the OneView Connection Template resources.
description:
    - "Provides an interface to manage the Connection Template resources. Can update."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Connection Template resource.
              C('present') will ensure data properties are compliant with OneView.
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
    config: "{{ config }}"
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
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import (OneViewModuleBase,
                                  HPOneViewValueError,
                                  HPOneViewResourceNotFound,
                                  ResourceComparator)


class ConnectionTemplateModule(OneViewModuleBase):
    MSG_UPDATED = 'Connection Template updated successfully.'
    MSG_NOT_FOUND = 'Connection Template was not found.'
    MSG_ALREADY_PRESENT = 'Connection Template is already updated.'
    MSG_MANDATORY_FIELD_MISSING = 'Mandatory field was not informed: data.name'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present']
            ),
            data=dict(required=True, type='dict')
        )
        super(ConnectionTemplateModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.connection_templates

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        if not self.data.get('name'):
            raise HPOneViewValueError(self.MSG_MANDATORY_FIELD_MISSING)

        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present(self.data, resource)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self, data, resource):
        changed = False
        msg = ''

        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)
        else:
            if 'newName' in data:
                data['name'] = data.pop('newName')

            merged_data = resource.copy()
            merged_data.update(data)

            if not ResourceComparator.compare(resource, merged_data):
                resource = self.resource_client.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return changed, msg, dict(connection_template=resource)


def main():
    ConnectionTemplateModule().run()


if __name__ == '__main__':
    main()
