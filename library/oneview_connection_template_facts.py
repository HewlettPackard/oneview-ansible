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
module: oneview_connection_template_facts
short_description: Retrieve facts about the OneView Connection Templates.
version_added: "2.3"
description:
    - Retrieve facts about the OneView Connection Templates.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Connection Template name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Connection Template related resources.
           Options allowed: C(defaultConnectionTemplate)."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Connection Templates
  oneview_connection_template_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather paginated, filtered and sorted facts about Connection Templates
  oneview_connection_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=defaultConnectionTemplate'

- debug: var=connection_templates

- name: Gather facts about a Connection Template by name
  oneview_connection_template_facts:
    config: "{{ config }}"
    name: 'connection template name'
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather facts about the Default Connection Template
  oneview_connection_template_facts:
    config: "{{ config }}"
    options:
      - defaultConnectionTemplate
  delegate_to: localhost
- debug: var=default_connection_template
'''

RETURN = '''
connection_templates:
    description: Has all the OneView facts about the Connection Templates.
    returned: Always, except when defaultConnectionTemplate is requested. Can be null.
    type: dict

default_connection_template:
    description: Has the facts about the Default Connection Template.
    returned: When requested, but can be null.
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class ConnectionTemplateFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict')
        )
        super(ConnectionTemplateFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        client = self.oneview_client.connection_templates
        ansible_facts = {}

        if 'defaultConnectionTemplate' in self.options:
            ansible_facts['default_connection_template'] = client.get_default()
        elif self.module.params.get('name'):
            ansible_facts['connection_templates'] = client.get_by('name', self.module.params['name'])
        else:
            ansible_facts['connection_templates'] = client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=ansible_facts)


def main():
    ConnectionTemplateFactsModule().run()


if __name__ == '__main__':
    main()
