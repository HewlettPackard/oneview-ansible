#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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
from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_server_hardware_type
short_description: Manage OneView Server Hardware Type resources.
description:
    - "Provides an interface to manage Server Hardware Type resources. Can update, remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Server Hardware Type resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Server Hardware Type properties and its associated states.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Update the Server Hardware Type description
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
      name: 'DL380p Gen8 1'
      description: "New Description"
  delegate_to: localhost

- name: Rename the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
        name: 'DL380p Gen8 1'
        newName: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost

- name: Delete the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: absent
    data:
        name: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost
'''

RETURN = '''
server_hardware_type:
    description: Has the OneView facts about the Server Hardware Type.
    returned: On state 'present'. Can be null.
    type: complex
'''

SERVER_HARDWARE_TYPE_UPDATED = 'Server Hardware Type updated successfully.'
SERVER_HARDWARE_TYPE_ALREADY_UPDATED = 'Server Hardware Type is already present.'
SERVER_HARDWARE_TYPE_DELETED = 'Server Hardware Type deleted successfully.'
SERVER_HARDWARE_TYPE_ALREADY_ABSENT = 'Server Hardware Type is already absent.'
SERVER_HARDWARE_TYPE_NOT_FOUND = 'Server Hardware Type was not found for this operation.'


class ServerHardwareTypeModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            resource = (self.oneview_client.server_hardware_types.get_by("name", data['name']) or [None])[0]

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __present(self, data, resource):
        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        if not resource:
            raise Exception(SERVER_HARDWARE_TYPE_NOT_FOUND)

        different = resource.get('name') != data.get('name')
        different |= resource.get('description') != data.get('description')

        if different:
            # update resource
            changed = True
            resource = self.oneview_client.server_hardware_types.update(data, resource['uri'])
            msg = SERVER_HARDWARE_TYPE_UPDATED
        else:
            msg = SERVER_HARDWARE_TYPE_ALREADY_UPDATED

        return changed, msg, dict(server_hardware_type=resource)

    def __absent(self, resource):
        if resource:
            self.oneview_client.server_hardware_types.delete(resource)
            return True, SERVER_HARDWARE_TYPE_DELETED, {}
        else:
            return False, SERVER_HARDWARE_TYPE_ALREADY_ABSENT, {}


def main():
    ServerHardwareTypeModule().run()


if __name__ == '__main__':
    main()
