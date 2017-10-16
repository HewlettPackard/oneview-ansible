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
module: image_streamer_deployment_plan
short_description: Manage Image Streamer Deployment Plan resources.
description:
    - "Provides an interface to manage Image Streamer Deployment Plans. Can create, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Deployment Plan resource.
              C(present) will ensure data properties are compliant with Synergy Image Streamer.
              C(absent) will remove the resource from Synergy Image Streamer, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Deployment Plan properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      description: "Description of this Deployment Plan"
      name: 'Demo Deployment Plan'
      hpProvided: 'false'
      oeBuildPlanName: "Demo Build Plan"
  delegate_to: localhost

- name: Update the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Deployment Plan'
      newName:  'Demo Deployment Plan (changed)'
      description: "New description"
  delegate_to: localhost

- name: Remove the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo Deployment Plan'
  delegate_to: localhost
'''

RETURN = '''
deployment_plan:
    description: Has the facts about the Image Streamer Deployment Plan.
    returned: On state 'present', but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class DeploymentPlanModule(OneViewModuleBase):
    MSG_CREATED = 'Deployment Plan created successfully.'
    MSG_UPDATED = 'Deployment Plan updated successfully.'
    MSG_ALREADY_PRESENT = 'Deployment Plan is already present.'
    MSG_DELETED = 'Deployment Plan deleted successfully.'
    MSG_ALREADY_ABSENT = 'Deployment Plan is already absent.'
    MSG_BUILD_PLAN_WAS_NOT_FOUND = 'OS Build Plan was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(DeploymentPlanModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.deployment_plans

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])
        result = {}

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            result = self.resource_present(resource, 'deployment_plan')
        elif self.state == 'absent':
            result = self.resource_absent(resource)

        return result

    def __replace_name_by_uris(self, data):
        build_plan_name = data.pop('oeBuildPlanName', None)
        if build_plan_name:
            data['oeBuildPlanURI'] = self.__get_build_plan_by_name(build_plan_name)['uri']

    def __get_build_plan_by_name(self, name):
        build_plan = self.i3s_client.build_plans.get_by('name', name)
        if build_plan:
            return build_plan[0]
        else:
            raise HPOneViewResourceNotFound(self.MSG_BUILD_PLAN_WAS_NOT_FOUND)


def main():
    DeploymentPlanModule().run()


if __name__ == '__main__':
    main()
