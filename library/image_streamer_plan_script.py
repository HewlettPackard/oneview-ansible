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
module: image_streamer_plan_script
short_description: Manage the Image Streamer Plan Script resources.
description:
    - "Provides an interface to manage the Image Streamer Plan Script. Can create, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Plan Script resource.
              C(present) will ensure data properties are compliant with Synergy Image Streamer.
              C(absent) will remove the resource from Synergy Image Streamer, if it exists.
              C(differences_retrieved) will retrieve the modified contents of the Plan Script as per
              the selected attributes.
        choices: ['present', 'absent', 'differences_retrieved']
        required: true
    data:
        description:
            - List with Plan Script properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: present
    data:
      description: "Description of this plan script"
      name: 'Demo Plan Script'
      hpProvided: False
      planType: "deploy"
      content: 'echo "test script"'
  delegate_to: localhost

- name: Update the Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Plan Script'
      newName:  'Demo Plan Script new name'
      description: "New description"
      content: 'echo "test script changed"'
  delegate_to: localhost

- name: Retrieve the Plan Script content differences
  image_streamer_plan_script:
    config: "{{ config }}"
    state: differences_retrieved
    data:
      name: 'Demo Plan Script'
      content: 'echo "test script changed 2"'
  delegate_to: localhost
- debug: var=plan_script_differences

- name: Remove the Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo Plan Script'
  delegate_to: localhost
'''

RETURN = '''
plan_script:
    description: Has the facts about the Image Streamer Plan Script.
    returned: On state 'present', but can be null.
    type: dict

plan_script_differences:
    description: Has the facts about the modified contents of the Plan Script as per the selected attributes.
    returned: On state 'differences_retrieved'.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewValueError


class PlanScriptModule(OneViewModuleBase):
    MSG_CREATED = 'Plan Script created successfully.'
    MSG_UPDATED = 'Plan Script updated successfully.'
    MSG_ALREADY_PRESENT = 'Plan Script is already present.'
    MSG_DELETED = 'Plan Script deleted successfully.'
    MSG_ALREADY_ABSENT = 'Plan Script is already absent.'
    MSG_DIFFERENCES_RETRIEVED = 'Plan Script differences retrieved successfully.'
    MSG_CONTENT_ATTRIBUTE_MANDATORY = 'Missing mandatory attribute: data.content.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'differences_retrieved']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(PlanScriptModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.plan_scripts

    def execute_module(self):

        resource = self.get_by_name(self.data['name'])
        result = {}

        if self.state == 'present':
            result = self.resource_present(resource, 'plan_script')
        elif self.state == 'absent':
            result = self.resource_absent(resource)
        elif self.state == 'differences_retrieved':
            result = self.__retrieve_differences(self.data, resource)

        return result

    def __retrieve_differences(self, data, resource):
        if 'content' not in data:
            raise HPOneViewValueError(self.MSG_CONTENT_ATTRIBUTE_MANDATORY)

        differences = self.i3s_client.plan_scripts.retrieve_differences(resource['uri'], data['content'])
        return dict(changed=False,
                    msg=self.MSG_DIFFERENCES_RETRIEVED,
                    ansible_facts=dict(plan_script_differences=differences))


def main():
    PlanScriptModule().run()


if __name__ == '__main__':
    main()
