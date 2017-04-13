#!/usr/bin/python

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
module: oneview_fabric
short_description: Manage OneView Fabric resources.
description:
    - Provides an interface for managing fabrics in OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Andressa Cruz (@asserdna)"
options:
    name:
      description:
        - Fabric name.
      required: false
    data:
      description:
        - List with Fabrics properties.
      required: true
notes:
    - "This module is only available on HPE Synergy."
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Update the range of the fabric
  oneview_fabric:
    config: '{{ config }}'
    state: reserved_vlan_range_updated
    data:
      name: '{{ name }}'
      reservedVlanRangeParameters:
        start: '300'
        length: '62'
'''

RETURN = '''
fabric:
    description: Has all the OneView facts about the Fabrics.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound, ResourceComparator


class FabricModule(OneViewModuleBase):
    MSG_NOT_FOUND = "Informed Fabric was not found."
    MSG_ALREADY_PRESENT = "No change found"

    def __init__(self):
        argument_spec = dict(
            state=dict(required=True,
                       choices=['reserved_vlan_range_updated']),
            data=dict(required=True, type='dict')
        )
        super(FabricModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.fabrics

    def execute_module(self):
        if self.state == 'reserved_vlan_range_updated':
            return self.__reserved_vlan_range_updated()

    def __reserved_vlan_range_updated(self):
        resource = self.get_by_name(self.data['name'])
        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)
        resource_vlan_range = resource.get('reservedVlanRange')
        merged_data = resource_vlan_range.copy()
        merged_data.update(self.data['reservedVlanRangeParameters'])

        if ResourceComparator.compare(resource_vlan_range, merged_data):
            return dict(changed=False, msg=self.MSG_ALREADY_PRESENT, ansible_facts=dict(fabric=resource))
        else:
            return self.__update_vlan_range(self.data, resource)

    def __update_vlan_range(self, data, resource):
        fabric_updated = self.oneview_client.fabrics.update_reserved_vlan_range(
            resource["uri"],
            data["reservedVlanRangeParameters"])
        return dict(changed=True, ansible_facts=dict(fabric=fabric_updated))


def main():
    FabricModule().run()


if __name__ == '__main__':
    main()
