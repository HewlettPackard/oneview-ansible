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
module: oneview_uplink_set_facts
short_description: Retrieve facts about one or more of the OneView Uplink Sets.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the Uplink Sets from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Uplink Set name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Uplink Sets
  oneview_uplink_set_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600

- debug: var=uplink_sets

- name: Gather paginated, filtered and sorted facts about Uplink Sets
  oneview_uplink_set_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "logicalInterconnectUri='/rest/logical-interconnects/4a49ca0d-3782-4c11-b93e-79d8f90c5487'"

- debug: var=uplink_sets

- name: Gather facts about a Uplink Set by name
  oneview_uplink_set_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    name: logical lnterconnect group name

- debug: var=uplink_sets
'''

RETURN = '''
uplink_sets:
    description: Has all the OneView facts about the Uplink Sets.
    returned: Always, but can be null.
    type: dict
'''
from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleResourceNotFound


class UplinkSetFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(UplinkSetFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        if self.module.params['name']:
            resources = self.oneview_client.uplink_sets.get_by('name', self.module.params['name'])
        else:
            resources = self.oneview_client.uplink_sets.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(uplink_sets=resources))


def main():
    UplinkSetFactsModule().run()


if __name__ == '__main__':
    main()
