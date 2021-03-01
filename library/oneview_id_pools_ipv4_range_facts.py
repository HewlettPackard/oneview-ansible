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
module: oneview_id_pools_ipv4_range_facts
short_description: Retrieve the facts about one or more of the OneView ID Pools IPV4 Ranges.
description:
    - Retrieve the facts about one or more of the ID Pools IPV4 Ranges from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 4.0.0"
author:
    "Thiago Miotto (@tmiotto)"
options:
    name:
      description:
        - ID Pools IPV4 Range name.
      required: false
    uri:
      description:
        - ID Pools IPV4 Range ID or URI.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an IPv4 Range and related resources.
          Options allowed:
          C(allocatedFragments) gets all fragments that have been allocated in range.
          C(freeFragments) gets all free fragments in an IPv4 range."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all ID Pools IPV4 Ranges
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config_file_path }}"
- debug: var=id_pools_ipv4_ranges

- name: Gather all facts about a Server Profile
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config_file_path }}"
    options:
        - schema
-  debug: var=id_pools_ipv4_ranges

- name: Gather paginated, filtered and sorted facts about ID Pools IPV4 Ranges
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'name:descending'
- debug: var=id_pools_ipv4_ranges

- name: Gather facts about a ID Pools IPV4 Range by name
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config_file_path }}"
    name: IPV4Range_01

- debug: var=id_pools_ipv4_ranges

- name: Gather facts about the 3 first ID Pools IPV4 Range free fragments
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config_file_path }}"
    options:
      - freeFragments
    name: IPV4Range_01
    params:
      count: 3
      start: 0

- name: Gather facts about all the ID Pools IPV4 Range allocated fragments
  oneview_id_pools_ipv4_range_facts:
    config: "{{ config_file_path }}"
    options:
      - allocatedFragments
    name: IPV4Range_01
    params:
      count: -1
      start: 0

- debug: var=id_pools_ipv4_range_allocated_fragments
'''

RETURN = '''
id_pools_ipv4_ranges:
    description: Has all the OneView facts about the ID Pools IPV4 Ranges.
    returned: Always, but can be null.
    type: dict

id_pools_ipv4_ranges_free_fragments:
    description: Has all the OneView facts about the ID Pools IPV4 Range Free fragments.
    returned: Always, but can be null.
    type: dict

id_pools_ipv4_ranges_allocated_fragments:
    description: Has all the OneView facts about the ID Pools IPV4 Range allocated fragments.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class IdPoolsIpv4RangeFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            uri=dict(required=False, type='str'),
            subnetUri=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict')
        )
        super(IdPoolsIpv4RangeFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.id_pools_ipv4_ranges

    def execute_module(self):
        facts = {}
        id_pools_ipv4_ranges = []
        is_specific_resource = True
        if self.module.params.get('uri'):
            id_pools_ipv4_ranges = self.resource_client.get_by_uri(self.module.params['uri']).data
        elif self.module.params.get('subnetUri'):
            subnet = self.oneview_client.id_pools_ipv4_subnets.get(self.module.params.get('subnetUri'))
            if self.module.params.get('name'):
                for range_uri in subnet['rangeUris']:
                    maybe_resource = self.resource_client.get_by_uri(range_uri).data
                    if maybe_resource['name'] == self.module.params.get('name'):
                        id_pools_ipv4_ranges = maybe_resource
                        break
            else:
                is_specific_resource = False
                for range_uri in subnet['rangeUris']:
                    id_pools_ipv4_ranges.append(self.resource_client.get_by_uri(range_uri).data)
        else:
            is_specific_resource = False
            subnets = self.oneview_client.id_pools_ipv4_subnets.get_all()
            for subnet in subnets:
                for range_uri in subnet['rangeUris']:
                    range_data = self.resource_client.get_by_uri(range_uri).data
                    id_pools_ipv4_ranges.append(range_data)

        self.__get_options(facts, id_pools_ipv4_ranges, is_specific_resource)

        facts['id_pools_ipv4_ranges'] = [id_pools_ipv4_ranges] if is_specific_resource else id_pools_ipv4_ranges

        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, facts, id_pools_ipv4_range, is_specific_resource):
        if self.options and is_specific_resource:
            range_uri = id_pools_ipv4_range['uri']
            query_params = self.module.params.get('params')
            # query_params may be None, even if 'params' is not declared, this 'if' is needed
            if query_params is None:
                query_params = {}
            if self.options.get('allocatedFragments'):
                facts['id_pools_ipv4_ranges_allocated_fragments'] = \
                    self.oneview_client.id_pools_ipv4_ranges.get_allocated_fragments(range_uri, **query_params)
            if self.options.get('freeFragments'):
                facts['id_pools_ipv4_ranges_free_fragments'] = \
                    self.oneview_client.id_pools_ipv4_ranges.get_free_fragments(range_uri, **query_params)
        elif self.options and not(is_specific_resource):
            if self.options.get('schema'):
                facts['id_pools_ipv4_ranges_schema'] = \
                    self.oneview_client.id_pools_ipv4_ranges.get_schema()


def main():
    IdPoolsIpv4RangeFactsModule().run()


if __name__ == '__main__':
    main()
