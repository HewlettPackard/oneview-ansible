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
module: oneview_id_pools_ipv4_subnet_facts
short_description: Retrieve the facts about one or more of the OneView ID Pools IPV4 Subnets.
description:
    - Retrieve the facts about one or more of the ID Pools IPV4 Subnets from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 2.0.1"
author:
    "Thiago Miotto (@tmiotto)"
options:
    name:
      description:
        - ID Pools IPV4 Subnet name.
      required: false
    uri:
      description:
        - ID Pools IPV4 Subnet ID or URI.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all ID Pools IPV4 Subnets
  oneview_id_pools_ipv4_subnet_facts:
    config: "{{ config_file_path }}"

- debug: var=id_pools_ipv4_subnets

- name: Gather paginated, filtered and sorted facts about ID Pools IPV4 Subnets
  oneview_id_pools_ipv4_subnet_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'name:descending'
- debug: var=id_pools_ipv4_subnets

- name: Gather facts about a ID Pools IPV4 Subnet by name
  oneview_id_pools_ipv4_subnet_facts:
    config: "{{ config_file_path }}"
    name: IPV4Subnet_01

- debug: var=id_pools_ipv4_subnets
'''

RETURN = '''
id_pools_ipv4_subnets:
    description: Has all the OneView facts about the ID Pools IPV4 Subnets.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class IdPoolsIpv4SubnetFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            uri=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )
        super(IdPoolsIpv4SubnetFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.id_pools_ipv4_subnets

    def execute_module(self):
        if self.module.params.get('name'):
            query = self.resource_client.get_all(filter="name='{}'".format(self.module.params['name']))
            id_pools_ipv4_subnets = [query[0]] if query and query[0].get('name') == self.module.params['name'] else None
        elif self.module.params.get('uri'):
            id_pools_ipv4_subnets = [self.resource_client.get(self.module.params['uri'])]
        else:
            id_pools_ipv4_subnets = self.oneview_client.id_pools_ipv4_subnets.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(id_pools_ipv4_subnets=id_pools_ipv4_subnets))


def main():
    IdPoolsIpv4SubnetFactsModule().run()


if __name__ == '__main__':
    main()
