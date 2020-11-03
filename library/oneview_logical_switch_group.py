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
module: oneview_logical_switch_group
short_description: Manage OneView Logical Switch Group resources.
description:
    - "Provides an interface to manage Logical Switch Group resources. Can add, update, remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Switch Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Logical Switch Group properties and its associated states.
        required: true
notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Logical Switch Group
  oneview_logical_switch_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  # You can choose either permittedSwitchTypeName or permittedSwitchTypeUri to inform the Switch Type
                  permittedSwitchTypeName: 'Cisco Nexus 50xx'
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Update the Logical Switch Group and make sure it is present in the desired scopes
  oneview_logical_switch_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        newName: "Test Logical Switch Group"
        scopeUris:
          - '/rest/scopes/00SC123456'
          - '/rest/scopes/01SC123456'
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Delete the Logical Switch Group
  oneview_logical_switch_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
        name: 'Test Logical Switch Group'
  delegate_to: localhost
'''

RETURN = '''
logical_switch_group:
    description: Has the OneView facts about the Logical Switch Group.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class LogicalSwitchGroupModule(OneViewModule):
    MSG_CREATED = 'Logical Switch Group created successfully.'
    MSG_UPDATED = 'Logical Switch Group updated successfully.'
    MSG_ALREADY_PRESENT = 'Logical Switch Group is already present.'
    MSG_DELETED = 'Logical Switch Group deleted successfully.'
    MSG_ALREADY_ABSENT = 'Logical Switch Group is already absent.'
    MSG_SWITCH_TYPE_NOT_FOUND = 'Switch type was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(LogicalSwitchGroupModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                       validate_etag_support=True)

        self.set_resource_object(self.oneview_client.logical_switch_groups)

    def execute_module(self):
        if self.state == 'present':
            self.__replace_name_by_uris()
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent()

    def __present(self):
        scope_uris = self.data.pop('scopeUris', None)
        result = self.resource_present('logical_switch_group')
        if scope_uris:
            result = self.resource_scopes_set(result, 'logical_switch_group', scope_uris)
        return result

    def __replace_name_by_uris(self):
        switch_map_template = self.data.get('switchMapTemplate')

        if switch_map_template:
            switch_map_entry_templates = switch_map_template.get('switchMapEntryTemplates')
            if switch_map_entry_templates:
                for value in switch_map_entry_templates:
                    permitted_switch_type_name = value.pop('permittedSwitchTypeName', None)
                    if permitted_switch_type_name:
                        value['permittedSwitchTypeUri'] = self.__get_switch_by_name(permitted_switch_type_name).data['uri']

    def __get_switch_by_name(self, name):
        switch_type = self.oneview_client.switch_types.get_by_name(name)
        if switch_type:
            return switch_type
        else:
            raise OneViewModuleResourceNotFound(self.MSG_SWITCH_TYPE_NOT_FOUND)


def main():
    LogicalSwitchGroupModule().run()


if __name__ == '__main__':
    main()
