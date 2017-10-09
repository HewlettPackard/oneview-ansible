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
module: oneview_storage_pool_facts
short_description: Retrieve facts about one or more Storage Pools.
description:
    - Retrieve facts about one or more of the Storage Pools from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Storage Pool name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Storage Pools.
          Options allowed:
          C(reachableStoragePools) gets the list of reachable Storage pools based on the network param.
          If the network param is not specified it gets all of them."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_pools

- name: Gather paginated, filtered and sorted facts about Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_pools

- name: Gather facts about a Storage Pool by name
  oneview_storage_pool_facts:
    config: "{{ config }}"
    name: "CPG_FC-AO"
  delegate_to: localhost

- debug: var=storage_pools

- name: Gather facts about the reachable Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
    options:
        - reachableStoragePools
    params:
        sort: 'name:ascending'
        filter: status='OK'
        networks:
            - /rest/network/123456A
            - /rest/network/123456B
  delegate_to: localhost

- debug: var=storage_pools_reachable_storage_pools
'''

RETURN = '''
storage_pools:
    description: Has all the OneView facts about the Storage Pools.
    returned: Always, but can be null.
    type: dict

storage_pools_reachable_storage_pools:
    description: Has all the OneView facts about the Reachable Storage Pools.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class StoragePoolFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
            options=dict(required=False, type='list')
        )
        super(StoragePoolFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_pools

    def execute_module(self):
        facts = {}
        networks = self.facts_params.pop('networks', None)
        if self.module.params.get('name'):
            storage_pool = self.oneview_client.storage_pools.get_by('name', self.module.params['name'])
        else:
            storage_pool = self.oneview_client.storage_pools.get_all(**self.facts_params)

        if networks:
            self.facts_params['networks'] = networks

        facts['storage_pools'] = storage_pool
        self.__get_options(facts)
        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, facts):
        if self.options:
            if self.options.get('reachableStoragePools'):
                query_params = self.module.params.get('params', {})
                facts['storage_pools_reachable_storage_pools'] = \
                    self.resource_client.get_reachable_storage_pools(**query_params)


def main():
    StoragePoolFactsModule().run()


if __name__ == '__main__':
    main()
