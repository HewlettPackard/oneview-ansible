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
module: oneview_interconnect_type_facts
short_description: Retrieve facts about one or more of the OneView Interconnect Types.
description:
    - Retrieve facts about one or more of the Interconnect Types from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Interconnect Type name.
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Interconnect Types
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600

- debug: var=interconnect_types

- name: Gather paginated, filtered and sorted facts about Interconnect Types
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "maximumFirmwareVersion='4000.99'"

- debug: var=interconnect_types

- name: Gather facts about an Interconnect Type by name
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    name: HP VC Flex-10 Enet Module

- debug: var=interconnect_types
'''

RETURN = '''
interconnect_types:
    description: Has all the OneView facts about the Interconnect Types.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class InterconnectTypeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(InterconnectTypeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.interconnect_types

    def execute_module(self):

        if self.module.params.get('name'):
            interconnect_types = self.oneview_client.interconnect_types.get_by('name', self.module.params['name'])
        else:
            interconnect_types = self.oneview_client.interconnect_types.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(interconnect_types=interconnect_types))


def main():
    InterconnectTypeFactsModule().run()


if __name__ == '__main__':
    main()
