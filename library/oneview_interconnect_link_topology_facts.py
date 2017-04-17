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
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_interconnect_link_topology_facts
short_description: Retrieve facts about the OneView Interconnect Link Topologies.
description:
    - Retrieve facts about the Interconnect Link Topologies from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the Interconnect Link Topology.
      required: false
notes:
    - This resource is only available on HPE Synergy.
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Interconnect Link Topologies
  oneview_interconnect_link_topology_facts:
    config: "{{ config_path }}"

- debug: var=interconnect_link_topologies

- name: Gather paginated, filtered and sorted facts about Interconnect Link Topologies
  oneview_interconnect_link_topology_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='name1900571853-1483553596802'"

- debug: var=interconnect_link_topologies

- name: Gather facts about an Interconnect Link Topology by name
  oneview_interconnect_link_topology_facts:
    config: "{{ config_path }}"
    name: "Name of the Interconnect Link Topologies"

- debug: var=interconnect_link_topologies
'''

RETURN = '''
interconnect_link_topologies:
    description: Has all the OneView facts about the Interconnect Link Topologies.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class InterconnectLinkTopologyFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(InterconnectLinkTopologyFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        name = self.module.params.get('name')
        if name:
            interconnect_link_topologies = self.oneview_client.interconnect_link_topologies.get_by('name', name)
        else:
            interconnect_link_topologies = self.oneview_client.interconnect_link_topologies.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(interconnect_link_topologies=interconnect_link_topologies))


def main():
    InterconnectLinkTopologyFactsModule().run()


if __name__ == '__main__':
    main()
