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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
module: oneview_switch_facts
short_description: Retrieve facts about the OneView Switches.
description:
    - Retrieve facts about the OneView Switches.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Switch name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Switch.
          Options allowed:
          C(environmentalConfiguration) gets the environmental configuration for a switch."
      required: false

notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all switches
  oneview_switch_facts:
    config: "{{ config }}"

- name: Gather paginated facts about switches
  oneview_switch_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3

- debug: var=switches

- name: Gather facts about the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"

- name: Gather facts about the environmental configuration for the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"
  options:
    - environmentalConfiguration
'''

RETURN = '''
switches:
    description: The list of switches.
    returned: Always, but can be null.
    type: list

switch_environmental_configuration:
    description: The environmental configuration for a switch.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class SwitchFactsModule(OneViewModuleBase):

    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )

        super(SwitchFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.switches

    def execute_module(self):
        facts = dict()
        name = self.module.params["name"]
        if name:
            facts['switches'] = self.resource_client.get_by('name', name)

            if facts['switches'] and 'environmentalConfiguration' in self.options:
                uri = facts['switches'][0]['uri']
                environmental_configuration = self.resource_client.get_environmental_configuration(id_or_uri=uri)
                facts['switch_environmental_configuration'] = environmental_configuration
        else:
            facts['switches'] = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=facts)


def main():
    SwitchFactsModule().run()


if __name__ == '__main__':
    main()
