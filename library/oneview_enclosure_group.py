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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_enclosure_group
short_description: Manage OneView Enclosure Group resources.
description:
    - Provides an interface to manage Enclosure Group resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Enclosure Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with Enclosure Group properties.
      required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that Enclosure Group is present using the default configuration
  oneview_enclosure_group:
    config: "{{ config_file_name }}"
    state: present
    data:
        name: "Enclosure Group 1"
        stackingMode: "Enclosure"
        interconnectBayMappings:
            - interconnectBay: 1
            - interconnectBay: 2
            - interconnectBay: 3
            - interconnectBay: 4
            - interconnectBay: 5
            - interconnectBay: 6
            - interconnectBay: 7
            - interconnectBay: 8
  delegate_to: localhost

- name: Update the Enclosure Group changing the name attribute
  oneview_enclosure_group:
        config: "{{ config_file_name }}"
        state: present
        data:
            name: "Enclosure Group 1"
            newName: "Enclosure Group 1 (renamed)"
  delegate_to: localhost

- name: Ensure that Enclosure Group is absent
  oneview_enclosure_group:
    config: "{{ config_file_name }}"
    state: absent
    data:
      name: "Enclosure Group 1 (renamed)"
  delegate_to: localhost
'''

RETURN = '''
enclosure_group:
    description: Has the facts about the Enclosure Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class EnclosureGroupModule(OneViewModuleBase):
    MSG_CREATED = 'Enclosure Group created successfully.'
    MSG_UPDATED = 'Enclosure Group updated successfully.'
    MSG_DELETED = 'Enclosure Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'Enclosure Group is already present.'
    MSG_ALREADY_ABSENT = 'Enclosure Group is already absent.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(EnclosureGroupModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.enclosure_groups

    def execute_module(self):
        resource = self.get_by_name(self.data.get('name'))

        if self.state == 'present':
            if resource and "configurationScript" in self.data:
                if self.data['configurationScript'] == self.resource_client.get_script(resource["uri"]):
                    del self.data['configurationScript']

            return self.resource_present(resource, 'enclosure_group')
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    EnclosureGroupModule().run()


if __name__ == '__main__':
    main()
