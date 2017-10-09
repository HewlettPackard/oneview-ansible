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
---
module: oneview_logical_enclosure_facts
short_description: Retrieve facts about one or more of the OneView Logical Enclosures.
description:
    - Retrieve facts about one or more of the Logical Enclosures from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Logical Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Logical Enclosure and related resources.
          Options allowed: script."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather paginated, filtered and sorted facts about Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name with options
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
    options:
      - script
  delegate_to: localhost

- debug: var=logical_enclosures
- debug: var=logical_enclosure_script
'''

RETURN = '''
logical_enclosures:
    description: Has all the OneView facts about the Logical Enclosures.
    returned: Always, but can be null.
    type: dict

logical_enclosure_script:
    description: Has the facts about the script of a Logical Enclosure.
    returned: When required, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class LogicalEnclosureFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(LogicalEnclosureFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        ansible_facts = {}

        if self.module.params.get('name'):
            logical_enclosures = self.oneview_client.logical_enclosures.get_by('name', self.module.params['name'])

            if self.options and logical_enclosures:
                ansible_facts = self.__gather_optional_facts(self.options, logical_enclosures[0])
        else:
            logical_enclosures = self.oneview_client.logical_enclosures.get_all(**self.facts_params)

        ansible_facts['logical_enclosures'] = logical_enclosures

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options, logical_enclosure):

        logical_enclosure_client = self.oneview_client.logical_enclosures
        ansible_facts = {}

        if options.get('script'):
            ansible_facts['logical_enclosure_script'] = logical_enclosure_client.get_script(logical_enclosure['uri'])

        return ansible_facts


def main():
    LogicalEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
