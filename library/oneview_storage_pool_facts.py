#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
    - "hpeOneView >= 5.0.0"
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost
- debug: var=storage_pools
- name: Gather paginated, filtered and sorted facts about Storage Pools
  oneview_storage_pool_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'
- debug: var=storage_pools
- name: Gather facts about a Storage Pool by name
  oneview_storage_pool_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "CPG_FC-AO"
  delegate_to: localhost
- debug: var=storage_pools
- name: Gather facts about the reachable Storage Pools
  oneview_storage_pool_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    options:
        - reachableStoragePools
    params:
        sort: 'name:ascending'
        filter: status='OK'
        networks:
            - /rest/network/123456A
            - /rest/network/123456B
        scope_exclusions:
            - /rest/storage-pools/5F9CA89B-C632-4F09-BC55-A8AA00DA5C4A
        scope_uris: '/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7'
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

from ansible.module_utils.oneview import OneViewModule


class StoragePoolFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
            options=dict(required=False, type='list')
        )
        super(StoragePoolFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.storage_pools)

    def execute_module(self):
        facts = {}
        pools = []
        if self.module.params['name']:
            pools = self.resource_client.get_by('name', self.module.params['name'])
        else:
            pools = self.resource_client.get_all(**self.facts_params)

        facts['storage_pools'] = pools
        self.__get_options(facts)
        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, facts):
        if self.options:
            if self.options.get('reachableStoragePools'):
                query_params = self.options['reachableStoragePools']
                facts['storage_pools_reachable_storage_pools'] = \
                    self.resource_client.get_reachable_storage_pools(**query_params)


def main():
    StoragePoolFactsModule().run()


if __name__ == '__main__':
    main()
