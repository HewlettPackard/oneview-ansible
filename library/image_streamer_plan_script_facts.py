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
module: image_streamer_plan_script_facts
short_description: Retrieve facts about the Image Streamer Plan Scripts.
description:
    - Retrieve facts about one or more of the Image Streamer Plan Script.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Plan Script name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather paginated, filtered and sorted facts about Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: planType=capture
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather facts about a Plan Script by name
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    name: "Demo Plan Script"
  delegate_to: localhost
- debug: var=plan_scripts
'''

RETURN = '''
plan_scripts:
    description: The list of Plan Scripts.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.oneview import OneViewModuleBase


class PlanScriptFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(PlanScriptFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        ansible_facts = {}

        if name:
            plan_scripts = self.i3s_client.plan_scripts.get_by("name", name)
        else:
            plan_scripts = self.i3s_client.plan_scripts.get_all(**self.facts_params)

        ansible_facts['plan_scripts'] = plan_scripts

        if self.options:
            ansible_facts.update(self._get_options_facts(plan_scripts))

        return dict(changed=False, ansible_facts=ansible_facts)

    def _get_options_facts(self, plan_script):
        options_facts = {}

        if self.options.get("getUseby"):
            options_facts["use_by"] = self.i3s_client.plan_scirpts.get_useby_and_readonly(plan_script[0]["uri"])

        return options_facts

def main():
    PlanScriptFactsModule().run()


if __name__ == '__main__':
    main()
