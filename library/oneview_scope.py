#!/usr/bin/python
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
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_scope
short_description: Manage OneView Scope resources.
description:
    - Provides an interface to manage scopes. Can create, update, or delete scopes, and modify the scope membership by
      adding or removing resource assignments.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Scope resource.
              'present' ensures data properties are compliant with OneView.
              'absent' removes the resource from OneView, if it exists.
              'resource_assignments_updated' modifies scope membership by adding or removing resource assignments. This
              operation is non-idempotent.
        choices: ['present', 'absent', 'resource_assignments_updated']
    data:
        description:
            - List with the Scopes properties.
        required: true
    validate_etag:
        description:
            - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
              for the resource matches the ETag provided in the data.
        default: true
        choices: ['true', 'false']
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is available for API version 300 or later.
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

- name: Update the scope resource assignments, adding two resources
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        addedResourceUris:
          - '{{ fc_network_1.uri }}'
          - '{{ fc_network_2.uri }}'
  delegate_to: localhost

- name: Update the scope resource assignments, adding one resource and removing another previously added
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        addedResourceUris:
          - '{{ fc_network_3.uri }}'
        removedResourceUris:
          - '{{ fc_network_1.uri }}'
  delegate_to: localhost
'''

RETURN = '''
scope:
    description: Has the facts about the Scope.
    returned: On state 'present' and 'resource_assignments_updated', but can be null.
    type: complex
'''

SCOPE_CREATED = 'Scope created successfully.'
SCOPE_UPDATED = 'Scope updated successfully.'
SCOPE_DELETED = 'Scope deleted successfully.'
SCOPE_ALREADY_EXIST = 'Scope already exists.'
SCOPE_ALREADY_ABSENT = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'
SCOPE_RESOURCE_ASSIGNMENTS_UPDATED = 'Scope Resource Assignments updated successfully.'
SCOPE_NOT_FOUND = 'Scope not found.'


class ScopeModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'resource_assignments_updated']
        ),
        data=dict(required=True, type='dict'),
        validate_etag=dict(
            required=False,
            type='bool',
            default=True)
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data'].copy()

        try:
            if not self.module.params.get('validate_etag'):
                self.oneview_client.connection.disable_etag_validation()

            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)
            elif state == 'resource_assignments_updated':
                self.__update_resource_assignments(data)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data)

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.scopes.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=SCOPE_DELETED)
        else:
            self.module.exit_json(changed=False, msg=SCOPE_ALREADY_ABSENT)

    def __create(self, data):
        scope_created = self.oneview_client.scopes.create(data)

        self.module.exit_json(changed=True,
                              msg=SCOPE_CREATED,
                              ansible_facts=dict(scope=scope_created))

    def __update(self, data, resource):
        if 'newName' in data:
            data['name'] = data.pop('newName')

        merged_data = resource.copy()
        merged_data.update(data)

        if resource_compare(resource, merged_data):
            self.module.exit_json(changed=False,
                                  msg=SCOPE_ALREADY_EXIST,
                                  ansible_facts=dict(scope=resource))

        else:
            scope_updated = self.oneview_client.scopes.update(merged_data)
            self.module.exit_json(changed=True,
                                  msg=SCOPE_UPDATED,
                                  ansible_facts=dict(scope=scope_updated))

    def __update_resource_assignments(self, data):
        resource = self.__get_by_name(data)

        if not resource:
            raise HPOneViewResourceNotFound(SCOPE_NOT_FOUND)
        else:
            scope = self.oneview_client.scopes.update_resource_assignments(resource['uri'],
                                                                           data.get('resourceAssignments'))
            self.module.exit_json(changed=True,
                                  msg=SCOPE_RESOURCE_ASSIGNMENTS_UPDATED,
                                  ansible_facts=dict(scope=scope))

    def __get_by_name(self, data):
        return self.oneview_client.scopes.get_by_name(data['name'])


def main():
    ScopeModule().run()


if __name__ == '__main__':
    main()
