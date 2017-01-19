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
    from hpOneView.exceptions import HPOneViewValueError

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: image_streamer_plan_script
short_description: Manage the Image Streamer Plan Script resources.
description:
    - "Provides an interface to manage the Image Streamer Plan Script. Can create, update, and remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
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
            - Indicates the desired state for the Plan Script resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
              'differences_retrieved' will retrieve the modified contents of the Plan Script as per
              the selected attributes.
        choices: ['present', 'absent', 'differences_retrieved']
        required: true
    data:
        description:
            - List with Plan Script properties and its associated states.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
    type: complex

plan_script_differences:
    description: Has the facts about the modified contents of the Plan Script as per the selected attributes.
    returned: On state 'differences_retrieved'.
    type: complex
'''

PLAN_SCRIPT_CREATED = 'Plan Script created successfully.'
PLAN_SCRIPT_UPDATED = 'Plan Script updated successfully.'
PLAN_SCRIPT_ALREADY_UPDATED = 'Plan Script is already present.'
PLAN_SCRIPT_DELETED = 'Plan Script deleted successfully.'
PLAN_SCRIPT_ALREADY_ABSENT = 'Plan Script is already absent.'
PLAN_SCRIPT_DIFFERENCES_RETRIEVED = 'Plan Script differences retrieved successfully.'
PLAN_SCRIPT_CONTENT_ATTRIBUTE_MANDATORY = 'Missing mandatory attribute: data.content.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class PlanScriptModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'differences_retrieved']
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

            resource = (self.i3s_client.plan_scripts.get_by("name", data['name']) or [None])[0]

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)
            elif state == 'differences_retrieved':
                changed, msg, ansible_facts = self.__retrieve_differences(data, resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, resource):
        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        if not resource:
            resource = self.i3s_client.plan_scripts.create(data)
            msg = PLAN_SCRIPT_CREATED
            changed = True
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                resource = self.i3s_client.plan_scripts.update(merged_data)
                changed = True
                msg = PLAN_SCRIPT_UPDATED
            else:
                msg = PLAN_SCRIPT_ALREADY_UPDATED

        return changed, msg, dict(plan_script=resource)

    def __absent(self, resource):
        if resource:
            self.i3s_client.plan_scripts.delete(resource)
            return True, PLAN_SCRIPT_DELETED, {}
        else:
            return False, PLAN_SCRIPT_ALREADY_ABSENT, {}

    def __retrieve_differences(self, data, resource):
        if 'content' not in data:
            raise HPOneViewValueError(PLAN_SCRIPT_CONTENT_ATTRIBUTE_MANDATORY)

        differences = self.i3s_client.plan_scripts.retrieve_differences(resource['uri'], data['content'])
        return False, PLAN_SCRIPT_DIFFERENCES_RETRIEVED, dict(plan_script_differences=differences)


def main():
    PlanScriptModule().run()


if __name__ == '__main__':
    main()
