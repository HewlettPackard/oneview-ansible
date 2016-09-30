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
try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_datacenter
short_description: Manage OneView Data Center resources.
description:
    - "Provides an interface to manage Data Center resources. Can add, update, remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Data Center resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Data Center properties and its associated states.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
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
    type: complex
'''

DATACENTER_ADDED = 'Data Center added successfully.'
DATACENTER_UPDATED = 'Data Center updated successfully.'
DATACENTER_ALREADY_UPDATED = 'Data Center is already present.'
DATACENTER_REMOVED = 'Data Center removed successfully.'
DATACENTER_ALREADY_ABSENT = 'Data Center is already absent.'
RACK_NOT_FOUND = 'Rack was not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class DatacenterModule(object):
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
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            resource = (self.oneview_client.datacenters.get_by("name", data['name']) or [None])[0]

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
        msg = ''

        if "newName" in data:
            data["name"] = data.pop("newName")

        self.__replace_name_by_uris(data)

        if not resource:
            resource = self.oneview_client.datacenters.add(data)

            changed = True
            msg = DATACENTER_ADDED
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                changed = True
                resource = self.oneview_client.datacenters.update(merged_data)
                msg = DATACENTER_UPDATED
            else:
                msg = DATACENTER_ALREADY_UPDATED

        return changed, msg, dict(datacenter=resource)

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
            raise Exception(RACK_NOT_FOUND)

    def __absent(self, resource):
        if resource:
            self.oneview_client.datacenters.remove(resource)
            return True, DATACENTER_REMOVED, {}
        else:
            return False, DATACENTER_ALREADY_ABSENT, {}


def main():
    DatacenterModule().run()


if __name__ == '__main__':
    main()
