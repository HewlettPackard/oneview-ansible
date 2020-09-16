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
module: oneview_fabric_facts
short_description: Retrieve the facts about one or more of the OneView Fabrics.
description:
    - Retrieve the facts about one or more of the Fabrics from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Fabric name.
      required: false
    options:
      description:
            - "List with options to gather additional facts about an Fabrics and related resources.
          Options allowed: C(reservedVlanRange)."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather paginated, filtered and sorted facts about Fabrics
  oneview_fabric_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=DefaultFabric'

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics

- name: Gather facts about a Fabric by name with options
  oneview_fabric_facts:
    config: "{{ config }}"
    name: DefaultFabric
    options:
      - reservedVlanRange          # optional

- debug: var=fabrics
'''

RETURN = '''
fabrics:
    description: Has all the OneView facts about the Fabrics.
    returned: Always, but can be null.
    type: dict
fabric_reserved_vlan_range:
    description: Has all the OneView facts about the reserved VLAN range
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class FabricFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(FabricFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.fabrics

    def execute_module(self):
        ansible_facts = {}
        name = self.module.params['name']
        if name:
            fabrics = self.oneview_client.fabrics.get_by('name', name)

            if self.options and fabrics:
                ansible_facts = self.__gather_optional_facts(fabrics[0])
        else:
            fabrics = self.oneview_client.fabrics.get_all(**self.facts_params)

        ansible_facts['fabrics'] = fabrics

        return dict(changed=False, ansible_facts=dict(ansible_facts))

    def __gather_optional_facts(self, fabric):
        ansible_facts = {}

        if self.options.get('reservedVlanRange'):
            ansible_facts['fabric_reserved_vlan_range'] = self.resource_client.get_reserved_vlan_range(fabric['uri'])

        return ansible_facts


def main():
    FabricFactsModule().run()


if __name__ == '__main__':
    main()
