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
module: oneview_server_hardware_type_facts
short_description: Retrieve facts about Server Hardware Types of the OneView.
description:
    - Retrieve facts about Server Hardware Types of the OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Server Hardware Type name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=server_hardware_types

- name: Gather paginated, filtered and sorted facts about Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: name:ascending
      filter: formFactor='HalfHeight'
  delegate_to: localhost
- debug: msg="{{server_hardware_types | map(attribute='name') | list }}"

- name: Gather facts about a Server Hardware Type by name
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    name: "BL460c Gen8 1"
  delegate_to: localhost
- debug: var=server_hardware_types
'''

RETURN = '''
server_hardware_types:
    description: Has all the OneView facts about the Server Hardware Types.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class ServerHardwareTypeFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )
        super(ServerHardwareTypeFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        name = self.module.params.get('name')

        if name:
            server_hardware_types = self.oneview_client.server_hardware_types.get_by('name', name)
        else:
            server_hardware_types = self.oneview_client.server_hardware_types.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(server_hardware_types=server_hardware_types))


def main():
    ServerHardwareTypeFactsModule().run()


if __name__ == '__main__':
    main()
