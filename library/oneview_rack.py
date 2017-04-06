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
module: oneview_rack
short_description: Manage OneView Racks resources.
description:
    - Provides an interface to manage Rack resources. Can create, update, and delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Rack resource.
              C(present) will ensure data properties are compliant with OneView. To change the name of the Rack,
               a I(newName) in the data must be provided.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the Rack properties.
      required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that a Rack is present using the default configuration
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'

- name: Add rack with custom size and a single mounted enclosure at slot 20
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack101'
      depth: 1500
      height: 2500
      width: 1200
      rackMounts:
        - mountUri: "/rest/enclosures/39SGH102X6J2"
          topUSlot: 20
          uHeight: 10

- name: Rename the Rack to 'Rack101'
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'
      newName: 'Rack101'

- name: Ensure that Rack is absent
  oneview_rack:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Rack Name'
'''

RETURN = '''
rack:
    description: Has the facts about the OneView Racks.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class RackModule(OneViewModuleBase):
    MSG_CREATED = 'Rack added successfully.'
    MSG_UPDATED = 'Rack updated successfully.'
    MSG_DELETED = 'Rack removed successfully.'
    MSG_ALREADY_EXIST = 'Rack already exists.'
    MSG_ALREADY_ABSENT = 'Rack is already absent.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(RackModule, self).__init__(additional_arg_spec=self.argument_spec,
                                         validate_etag_support=True)
        self.resource_client = self.oneview_client.racks

    def execute_module(self):

        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            return self.resource_present(resource, "rack", 'add')
        elif self.state == 'absent':
            return self.resource_absent(resource, "remove")


def main():
    RackModule().run()


if __name__ == '__main__':
    main()
