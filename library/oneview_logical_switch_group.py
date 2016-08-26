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
from hpOneView.common import resource_compare

DOCUMENTATION = '''
---
module: oneview_logical_switch_group
short_description: Manage OneView Logical Switch Group resources.
description:
    - "Provides an interface to manage Logical Switch Group resources. Can add, update, remove."
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
            - Indicates the desired state for the Logical Switch Group resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Logical Switch Group properties and its associated states
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Create a Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        type: "logical-switch-group"
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

- name: Update the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        type: "logical-switch-group"
        name: "OneView Test Logical Switch Group"
        newName: "Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  permittedSwitchTypeUri: '{{ switch_type_uri }}'
  delegate_to: localhost

- name: Delete the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Test Logical Switch Group'
  delegate_to: localhost
'''

RETURN = '''
logical_switch_group:
    description: Has the OneView facts about the Logical Switch Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

LOGICAL_SWITCH_GROUP_CREATED = 'Logical Switch Group created successfully.'
LOGICAL_SWITCH_GROUP_UPDATED = 'Logical Switch Group updated successfully.'
LOGICAL_SWITCH_GROUP_ALREADY_UPDATED = 'Logical Switch Group is already present.'
LOGICAL_SWITCH_GROUP_DELETED = 'Logical Switch Group deleted successfully.'
LOGICAL_SWITCH_GROUP_ALREADY_ABSENT = 'Logical Switch Group is already absent.'
SWITCH_TYPE_NOT_FOUND = 'Switch type was not found.'


class LogicalSwitchGroupModule(object):
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

            resource = (self.oneview_client.logical_switch_groups.get_by("name", data['name']) or [None])[0]

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
            resource = self.oneview_client.logical_switch_groups.create(data)
            changed = True
            msg = LOGICAL_SWITCH_GROUP_CREATED
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                changed = True
                resource = self.oneview_client.logical_switch_groups.update(merged_data)
                msg = LOGICAL_SWITCH_GROUP_UPDATED
            else:
                msg = LOGICAL_SWITCH_GROUP_ALREADY_UPDATED

        return changed, msg, dict(logical_switch_group=resource)

    def __replace_name_by_uris(self, resource):
        switch_map_template = resource.get('switchMapTemplate')

        if switch_map_template:
            switch_map_entry_templates = switch_map_template.get('switchMapEntryTemplates')
            if switch_map_entry_templates:
                for value in switch_map_entry_templates:
                    permitted_switch_type_name = value.pop('permittedSwitchTypeName', None)
                    if permitted_switch_type_name:
                        value['permittedSwitchTypeUri'] = self.__get_switch_by_name(permitted_switch_type_name)['uri']

    def __get_switch_by_name(self, name):
        switch_type = self.oneview_client.switch_types.get_by('name', name)
        if switch_type:
            return switch_type[0]
        else:
            raise Exception(SWITCH_TYPE_NOT_FOUND)

    def __absent(self, resource):
        if resource:
            self.oneview_client.logical_switch_groups.delete(resource)
            return True, LOGICAL_SWITCH_GROUP_DELETED, {}
        else:
            return False, LOGICAL_SWITCH_GROUP_ALREADY_ABSENT, {}


def main():
    LogicalSwitchGroupModule().run()


if __name__ == '__main__':
    main()
