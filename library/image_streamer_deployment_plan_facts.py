#!/usr/bin/python
# -*- coding: utf-8 -*-
###
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: image_streamer_deployment_plan_facts
short_description: Retrieve facts about the Image Streamer Deployment Plans.
description:
    - Retrieve facts about one or more of the Image Streamer Deployment Plans.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Deployment Plan name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Deployment Plans
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather paginated, filtered and sorted facts about Deployment Plans
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=active
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather facts about a Deployment Plan by name
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "Demo Deployment Plan"
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather facts about Server Profiles and Server Profile Templates that are using Deployment Plan
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "Demo Deployment Plan"
    options: "usedby"
  delegate_to: localhost
- debug: var=deployment_plans

- name: Get the OS deployment plan details from OneView for a deployment plan
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "Demo Deployment Plan"
    options: "osdp"
  delegate_to: localhost
- debug: var=deployment_plans
'''

RETURN = '''
deployment_plans:
    description: The list of Deployment Plans.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.oneview import OneViewModule


class DeploymentPlanFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(DeploymentPlanFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")
        options = self.module.params.get("options")
        ansible_facts = {}
        if name:
            ansible_facts['deployment_plans'] = self.i3s_client.deployment_plans.get_by("name", name)
            if ansible_facts['deployment_plans'] and options == 'usedby':
                deployment_plan = ansible_facts['deployment_plans'][0]
                environmental_configuration = self.i3s_client.deployment_plans.get_usedby(deployment_plan['uri'])
                ansible_facts['deployment_plans'][0]['deployment_plan_usedby'] = environmental_configuration
            elif ansible_facts['deployment_plans'] and options == 'osdp':
                deployment_plan = ansible_facts['deployment_plans'][0]
                environmental_configuration = self.i3s_client.deployment_plans.get_osdp(deployment_plan['uri'])
                ansible_facts['deployment_plans'][0]['deployment_plan_osdp'] = environmental_configuration
        else:
            ansible_facts['deployment_plans'] = self.i3s_client.deployment_plans.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    DeploymentPlanFactsModule().run()


if __name__ == '__main__':
    main()
