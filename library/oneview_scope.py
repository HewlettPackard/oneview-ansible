#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
module: oneview_scope
short_description: Manage OneView Scope resources.
description:
    - Provides an interface to manage scopes. Can create, update, or delete scopes, and modify the scope membership by
      adding or removing resource assignments.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Scope resource.
              C(present) ensures data properties are compliant with OneView.
              C(absent) removes the resource from OneView, if it exists.
              C(resource_assignments_updated) modifies scope membership by adding or removing resource assignments.
              This operation is non-idempotent.
        choices: ['present', 'absent', 'resource_assignments_updated']
    data:
        description:
            - List with the Scopes properties.
        required: true
notes:
    - This resource is available for API version 300 or later.
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a scope
  oneview_scope:
    config: '{{ config }}'
    state: present
    data:
      name: 'SampleScope'
  delegate_to: localhost

- name: Update the scope
  oneview_scope:
    config: '{{ config }}'
    state: present
    data:
      name: 'SampleScope'
      newName: 'SampleScopeRenamed'
  delegate_to: localhost

- name: Delete the Scope
  oneview_scope:
    config: '{{ config }}'
    state: absent
    data:
      name: 'SampleScopeRenamed'
  delegate_to: localhost

- name: Update the scope resource assignments, adding a resource
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        addedResourceUris: '{{ fc_network_1.uri }}'
  delegate_to: localhost

- name: Update the scope resource assignments, removing two resources
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        removedResourceUris:
            - '{{ fc_network_1.uri }}'
            - '{{ fc_network_2.uri }}'
  delegate_to: localhost
'''

RETURN = '''
scope:
    description: Has the facts about the Scope.
    returned: On state 'present' and 'resource_assignments_updated', but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class ScopeModule(OneViewModule):
    MSG_CREATED = 'Scope created successfully.'
    MSG_UPDATED = 'Scope updated successfully.'
    MSG_DELETED = 'Scope deleted successfully.'
    MSG_ALREADY_PRESENT = 'Scope is already present.'
    MSG_ALREADY_ABSENT = 'Scope is already absent.'
    MSG_RESOURCE_ASSIGNMENTS_UPDATED = 'Scope Resource Assignments updated successfully.'
    MSG_RESOURCE_ASSIGNMENTS_NOT_UPDATED = 'Scope Resource Assignments were not updated'
    MSG_RESOURCE_NOT_FOUND = 'Scope not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'resource_assignments_updated']
        ),
        data=dict(required=True, type='dict'),
    )

    def __init__(self):

        super(ScopeModule, self).__init__(additional_arg_spec=self.argument_spec,
                                          validate_etag_support=True)

        self.set_resource_object(self.oneview_client.scopes)

    def execute_module(self):
        if self.state == 'present':
            return self.resource_present('scope')
        elif self.state == 'absent':
            return self.resource_absent()
        elif self.state == 'resource_assignments_updated':
            return self.__update_resource_assignments()

    def __update_resource_assignments(self):
        # returns None if scope doesn't exist
        if not self.current_resource:
            return dict(failed=True,
                        msg=self.MSG_RESOURCE_NOT_FOUND)

        add_resources = self.data.get('resourceAssignments').get('addedResourceUris') is not None
        remove_resources = self.data.get('resourceAssignments').get('removedResourceUris') is not None
        updated_name = self.data.get('resourceAssignments').get('name') is not None
        updated_description = self.data.get('resourceAssignments').get('description') is not None
        if add_resources:
            self.current_resource.patch(operation='add',
                                        path='/addedResourceUris/-',
                                        value=self.data.get('resourceAssignments').get('addedResourceUris'))
        if remove_resources:
            self.current_resource.patch(operation='replace',
                                        path='/removedResourceUris',
                                        value=self.data.get('resourceAssignments').get('removedResourceUris'))
        if updated_name:
            self.current_resource.patch(operation='replace',
                                        path='/name',
                                        value=self.data.get('resourceAssignments').get('name'))
        if updated_description:
            self.current_resource.patch(operation='replace',
                                        path='/description',
                                        value=self.data.get('resourceAssignments').get('description'))
        if not add_resources and not remove_resources and not updated_name and not updated_description:
            return dict(changed=False,
                        msg=self.MSG_RESOURCE_ASSIGNMENTS_NOT_UPDATED,
                        ansible_facts=dict(scope=self.current_resource.data))

        return dict(changed=True,
                    msg=self.MSG_RESOURCE_ASSIGNMENTS_UPDATED,
                    ansible_facts=dict(scope=self.current_resource.data))


def main():
    ScopeModule().run()


if __name__ == '__main__':
    main()
