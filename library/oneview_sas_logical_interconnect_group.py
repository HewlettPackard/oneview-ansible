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
module: oneview_sas_logical_interconnect_group
short_description: Manage OneView SAS Logical Interconnect Group resources.
description:
    - Provides an interface to manage SAS Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the SAS Logical Interconnect Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the SAS Logical Interconnect Group properties.
      required: true
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the SAS Logical Interconnect Group is present
  oneview_sas_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: "Test SAS Logical Interconnect Group"
      state: "Active"
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "1"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeName: "Synergy 12Gb SAS Connection Module"
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "4"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeName: "Synergy 12Gb SAS Connection Module"
      enclosureType: "SY12000"
      enclosureIndexes: [1]
      interconnectBaySet: "1"

- name: Ensure that the SAS Logical Interconnect Group is present with name 'Test'
  oneview_sas_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: 'New SAS Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the SAS Logical Interconnect Group is absent
  oneview_sas_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
      name: 'New SAS Logical Interconnect Group'
'''

RETURN = '''
sas_logical_interconnect_group:
    description: Has the facts about the OneView SAS Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class SasLogicalInterconnectGroupModule(OneViewModule):
    MSG_CREATED = 'SAS Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'SAS Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'SAS Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'SAS Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'SAS Logical Interconnect Group is already absent.'
    RESOURCE_FACT_NAME = 'sas_logical_interconnect_group'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(SasLogicalInterconnectGroupModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                                validate_etag_support=True)

        self.set_resource_object(self.oneview_client.sas_logical_interconnect_groups)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent()
    def __present(self):
        scope_uris = self.data.pop('scopeUris', None)

        self.__replace_name_by_uris()
        result = self.resource_present(self.RESOURCE_FACT_NAME)

        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'sas_logical_interconnect_group', scope_uris)

        return result

    def __replace_name_by_uris(self):
        map_template = self.data.get('interconnectMapTemplate')

        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name).get('uri')

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.sas_interconnect_types.get_by('name', name)
        if i_type:
            return i_type[0]
        else:
            raise OneViewModuleResourceNotFound(self.MSG_INTERCONNECT_TYPE_NOT_FOUND)


def main():
    SasLogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
