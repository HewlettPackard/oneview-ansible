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
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, dict_merge, compare
from copy import deepcopy


class RackModule(OneViewModuleBase):
    MSG_CREATED = 'Rack added successfully.'
    MSG_UPDATED = 'Rack updated successfully.'
    MSG_DELETED = 'Rack removed successfully.'
    MSG_ALREADY_PRESENT = 'Rack is already present.'
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
        if self.state == 'present':
            changed, msg, ansible_facts = self.__present()
        elif self.state == 'absent':
            changed, msg, ansible_facts = self.__absent()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self):
      self.current_resource = self.resource_client.get_by_name(self.data['name'])
      if not self.current_resource:
        response = self.__add(self.data)
      else:
        response = self.__update()

    def __add(self, data):
        self.current_resource = self.resource_client.add(self.data)
        return True, self.MSG_ADDED, dict(oneview_rack=self.current_resource.data)
    
    def __mergeRackMounts(self):
      resource_copy = deepcopy(self.current_resource.data)
      data_copy = deepcopy(self.data)
        for resource_rackMount in resource_copy['rackMounts']:
          for data_rackMount in data_copy['rackMounts']:
            if resource_rackMount['mountUri'] != data_rackMount['mountUri'] or 
                resource_rackMount['topUSlot'] != data_rackMount['topUSlot']:
              data_copy['rackMounts'].append(resource_rackMount)
            else:
              data_rackMount.update(resource_rackMount)
        return data_copy

    def __update(self):
      if "newName" in self.data:
        self.data["name"] = self.data.pop("newName")

      data_copy = self.__mergeRackMounts() 
      merged_data = dict_merge(data_copy, resource_copy)
      if not compare(self.current_resource.data, merged_data):
        self.current_resource.update(merged_data)
        return True, self.MSG_UPDATED, dict(hypervisor_cluster_profile=self.current_resource.data)
      else:
        return False, self.MSG_ALREADY_PRESENT, dict(hypervisor_cluster_profile=self.current_resource.data)

    def __absent(self):
        if self.current_resource:
            changed = True
            msg = self.MSG_DELETED
            self.current_resource.delete(**self.params)
        else:
            changed = False
            msg = self.MSG_ALREADY_ABSENT
        return changed, msg, dict(oneview_rack=None)

def main():
    RackModule().run()


if __name__ == '__main__':
    main()
