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
module: oneview_datacenter
short_description: Manage OneView Data Center resources.
description:
    - "Provides an interface to manage Data Center resources. Can add, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Data Center resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Data Center properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Add a Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        width: 5000
        depth: 6000
        contents:
            # You can choose either resourceName or resourceUri to inform the Rack
            - resourceName: '{{ datacenter_content_rack_name }}' # option 1
              resourceUri: ''                                    # option 2
              x: 1000
              y: 1000
  delegate_to: localhost

- name: Update the Data Center with specified properties (no racks)
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        coolingCapacity: '5'
        costPerKilowattHour: '0.10'
        currency: USD
        deratingType: NaJp
        deratingPercentage: '20.0'
        defaultPowerLineVoltage: '220'
        coolingMultiplier: '1.5'
        width: 4000
        depth: 5000
        contents: ~

  delegate_to: localhost

- name: Rename the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        newName: "My Datacenter"
  delegate_to: localhost

- name: Remove the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: absent
    data:
        name: 'My Datacenter'
  delegate_to: localhost
'''

RETURN = '''
datacenter:
    description: Has the OneView facts about the Data Center.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleResourceNotFound


class DatacenterModule(OneViewModuleBase):
    MSG_CREATED = 'Data Center added successfully.'
    MSG_UPDATED = 'Data Center updated successfully.'
    MSG_ALREADY_PRESENT = 'Data Center is already present.'
    MSG_DELETED = 'Data Center removed successfully.'
    MSG_ALREADY_ABSENT = 'Data Center is already absent.'
    MSG_RACK_NOT_FOUND = 'Rack was not found.'
    RESOURCE_FACT_NAME = 'datacenter'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(DatacenterModule, self).__init__(additional_arg_spec=self.argument_spec,
                                               validate_etag_support=True)
        self.resource_client = self.oneview_client.datacenters

    def execute_module(self):

        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            return self.resource_present(resource, self.RESOURCE_FACT_NAME, 'add')
        elif self.state == 'absent':
            return self.resource_absent(resource, 'remove')

    def __replace_name_by_uris(self, resource):
        contents = resource.get('contents')

        if contents:
            for content in contents:
                resource_name = content.pop('resourceName', None)
                if resource_name:
                    content['resourceUri'] = self.__get_rack_by_name(resource_name)['uri']

    def __get_rack_by_name(self, name):
        racks = self.oneview_client.racks.get_by('name', name)
        if racks:
            return racks[0]
        else:
            raise OneViewModuleResourceNotFound(self.MSG_RACK_NOT_FOUND)


def main():
    DatacenterModule().run()


if __name__ == '__main__':
    main()
