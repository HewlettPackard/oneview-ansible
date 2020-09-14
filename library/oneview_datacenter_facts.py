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
module: oneview_datacenter_facts
short_description: Retrieve facts about the OneView Data Centers.
description:
    - Retrieve facts about the OneView Data Centers.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Data Center name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'visualContent'."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=datacenters

- name: Gather paginated, filtered and sorted facts about Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'state=Unmanaged'
- debug: var=datacenters

- name: Gather facts about a Data Center by name
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
  delegate_to: localhost
- debug: var=datacenters

- name: Gather facts about the Data Center Visual Content
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
    options:
      - visualContent
  delegate_to: localhost
- debug: var=datacenters
- debug: var=datacenter_visual_content
'''

RETURN = '''
datacenters:
    description: Has all the OneView facts about the Data Centers.
    returned: Always, but can be null.
    type: dict

datacenter_visual_content:
    description: Has facts about the Data Center Visual Content.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class DatacenterFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(DatacenterFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        client = self.oneview_client.datacenters
        ansible_facts = {}

        if self.module.params.get('name'):
            datacenters = client.get_by('name', self.module.params['name'])

            if self.options and 'visualContent' in self.options:
                if datacenters:
                    ansible_facts['datacenter_visual_content'] = client.get_visual_content(datacenters[0]['uri'])
                else:
                    ansible_facts['datacenter_visual_content'] = None

            ansible_facts['datacenters'] = datacenters
        else:
            ansible_facts['datacenters'] = client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=ansible_facts)


def main():
    DatacenterFactsModule().run()


if __name__ == '__main__':
    main()
