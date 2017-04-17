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
module: oneview_logical_interconnect_group
short_description: Manage OneView Logical Interconnect Group resources.
description:
    - Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Interconnect Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Logical Interconnect Group properties.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalDownlinkUri: ~
            logicalLocation:
                locationEntries:
                    - relativeValue: "1"
                      type: "Bay"
                    - relativeValue: 1
                      type: "Enclosure"
            permittedInterconnectTypeName: 'HP VC Flex-10/10D Module'
            # Alternatively you can inform permittedInterconnectTypeUri

- name: Ensure that the Logical Interconnect Group is present with name 'Test'
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the Logical Interconnect Group is absent
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New Logical Interconnect Group'
'''

RETURN = '''
logical_interconnect_group:
    description: Has the facts about the OneView Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class LogicalInterconnectGroupModule(OneViewModuleBase):
    MSG_CREATED = 'Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'Logical Interconnect Group is already absent.'
    MSG_INTERCONNECT_TYPE_NOT_FOUND = 'Interconnect Type was not found.'

    RESOURCE_FACT_NAME = 'logical_interconnect_group'

    def __init__(self):
        argument_spec = dict(
            state=dict(required=True, choices=['present', 'absent']),
            data=dict(required=True, type='dict')
        )

        super(LogicalInterconnectGroupModule, self).__init__(additional_arg_spec=argument_spec,
                                                             validate_etag_support=True)
        self.resource_client = self.oneview_client.logical_interconnect_groups

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)

    def __replace_name_by_uris(self, data):
        map_template = data.get('interconnectMapTemplate')

        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name).get('uri')

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.interconnect_types.get_by('name', name)
        if i_type:
            return i_type[0]
        else:
            raise HPOneViewResourceNotFound(self.MSG_INTERCONNECT_TYPE_NOT_FOUND)


def main():
    LogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
