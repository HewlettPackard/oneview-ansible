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


ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_server_hardware_type
short_description: Manage OneView Server Hardware Type resources.
description:
    - "Provides an interface to manage Server Hardware Type resources. Can update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Server Hardware Type resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Server Hardware Type properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Update the Server Hardware Type description
  oneview_server_hardware_type:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'DL380p Gen8 1'
      description: "New Description"
  delegate_to: localhost

- name: Rename the Server Hardware Type
  oneview_server_hardware_type:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'DL380p Gen8 1'
      newName: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost

- name: Delete the Server Hardware Type
  oneview_server_hardware_type:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost
'''

RETURN = '''
server_hardware_type:
    description: Has the OneView facts about the Server Hardware Type.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class ServerHardwareTypeModule(OneViewModule):
    MSG_UPDATED = 'Server Hardware Type updated successfully.'
    MSG_ALREADY_PRESENT = 'Server Hardware Type is already present.'
    MSG_DELETED = 'Server Hardware Type deleted successfully.'
    MSG_ALREADY_ABSENT = 'Server Hardware Type is already absent.'
    MSG_RESOURCE_NOT_FOUND = 'Server Hardware Type was not found for this operation.'

    argument_spec = dict(
        state=dict(required=True, choices=['present', 'absent']),
        data=dict(required=True, type='dict'))

    def __init__(self):

        super(ServerHardwareTypeModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                       validate_etag_support=True)
        self.set_resource_object(self.oneview_client.server_hardware_types)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.__absent()

    def __present(self):
        changed, msg = False, self.MSG_ALREADY_PRESENT

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_RESOURCE_NOT_FOUND)

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        different = self.current_resource.data.get('name') != self.data.get('name')
        different |= self.current_resource.data.get('description') != self.data.get('description')

        if different:
            self.current_resource.update(self.data)
            changed = True
            msg = self.MSG_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(server_hardware_type=self.current_resource.data))

    def __absent(self):
        if self.current_resource:
            self.current_resource.delete()
            return dict(changed=True, msg=self.MSG_DELETED)

        return dict(changed=False, msg=self.MSG_ALREADY_ABSENT)


def main():
    ServerHardwareTypeModule().run()


if __name__ == '__main__':
    main()
