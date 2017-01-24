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
    from hpOneView.extras.comparators import resource_compare
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: image_streamer_build_plan
short_description: Manages Image Stream OS Build Plan resources.
description:
    - "Provides an interface to manage Image Stream OS Build Plans. Can create, update, and remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the OS Build Plan resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with OS Build Plan properties and its associated states.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Create an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "oebuildplan"
      oeBuildPlanType: "deploy"
  delegate_to: localhost

- name: Update the OS Build Plan description and name
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "New description"
      newName: 'OS Build Plan Renamed'
  delegate_to: localhost

- name: Remove an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo OS Build Plan'
  delegate_to: localhost
'''

RETURN = '''
build_plan:
    description: Has the OneView facts about the OS Build Plan.
    returned: On state 'present'.
    type: complex
'''

BUILD_PLAN_CREATED = 'OS Build Plan created successfully.'
BUILD_PLAN_UPDATED = 'OS Build Plan updated successfully.'
BUILD_PLAN_ALREADY_UPDATED = 'OS Build Plan is already present.'
BUILD_PLAN_DELETED = 'OS Build Plan deleted successfully.'
BUILD_PLAN_ALREADY_ABSENT = 'OS Build Plan is already absent.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class BuildPlanModule(object):
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

            resource = (self.i3s_client.build_plans.get_by("name", data.get('name')) or [None])[0]

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)
            else:
                changed, msg, ansible_facts = self.__absent(resource)

            self.module.exit_json(changed=changed, msg=msg, ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, resource):

        changed = False
        msg = BUILD_PLAN_ALREADY_UPDATED

        if "newName" in data:
            data["name"] = data.pop("newName")

        if not resource:
            resource = self.i3s_client.build_plans.create(data)
            msg = BUILD_PLAN_CREATED
            changed = True

        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                resource = self.i3s_client.build_plans.update(merged_data)
                changed = True
                msg = BUILD_PLAN_UPDATED

        return changed, msg, dict(build_plan=resource)

    def __absent(self, resource):
        if resource:
            self.i3s_client.build_plans.delete(resource)
            return True, BUILD_PLAN_DELETED, {}
        else:
            return False, BUILD_PLAN_ALREADY_ABSENT, {}


def main():
    BuildPlanModule().run()


if __name__ == '__main__':
    main()
