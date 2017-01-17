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
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: image_streamer_deployment_plan
short_description: Manage Image Streamer Deployment Plan resources.
description:
    - "Provides an interface to manage Image Streamer Deployment Plans. Can create, update, and remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Deployment Plan resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Deployment Plan properties and its associated states.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
    type: complex
'''

DEPLOYMENT_PLAN_CREATED = 'Deployment Plan created successfully.'
DEPLOYMENT_PLAN_UPDATED = 'Deployment Plan updated successfully.'
DEPLOYMENT_PLAN_ALREADY_UPDATED = 'Deployment Plan is already present.'
DEPLOYMENT_PLAN_DELETED = 'Deployment Plan deleted successfully.'
DEPLOYMENT_PLAN_ALREADY_ABSENT = 'Deployment Plan is already absent.'
I3S_BUILD_PLAN_WAS_NOT_FOUND = 'OS Build Plan was not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class DeploymentPlanModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
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

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            resource = (self.i3s_client.deployment_plans.get_by("name", data['name']) or [None])[0]

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, resource):
        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        self.__replace_name_by_uris(data)

        if not resource:
            resource = self.i3s_client.deployment_plans.create(data)
            msg = DEPLOYMENT_PLAN_CREATED
            changed = True
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                resource = self.i3s_client.deployment_plans.update(merged_data)
                changed = True
                msg = DEPLOYMENT_PLAN_UPDATED
            else:
                msg = DEPLOYMENT_PLAN_ALREADY_UPDATED

        return changed, msg, dict(deployment_plan=resource)

    def __absent(self, resource):
        if resource:
            self.i3s_client.deployment_plans.delete(resource)
            return True, DEPLOYMENT_PLAN_DELETED, {}
        else:
            return False, DEPLOYMENT_PLAN_ALREADY_ABSENT, {}

    def __replace_name_by_uris(self, data):
        build_plan_name = data.pop('oeBuildPlanName', None)
        if build_plan_name:
            data['oeBuildPlanURI'] = self.__get_build_plan_by_name(build_plan_name)['uri']

    def __get_build_plan_by_name(self, name):
        build_plan = self.i3s_client.build_plans.get_by('name', name)
        if build_plan:
            return build_plan[0]
        else:
            raise HPOneViewResourceNotFound(I3S_BUILD_PLAN_WAS_NOT_FOUND)


def main():
    DeploymentPlanModule().run()


if __name__ == '__main__':
    main()
