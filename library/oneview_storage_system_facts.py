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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_storage_system_facts
short_description: Retrieve facts about the OneView Storage Systems.
description:
    - Retrieve facts about the Storage Systems from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    ip_hostname:
      description:
        - Storage System IP or hostname.
      required: false
    name:
      description:
        - Storage System name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Storage System and related resources.
          Options allowed:
          C(hostTypes) gets the list of supported host types.
          C(storagePools) gets a list of storage pools belonging to the specified storage system."
        - "To gather facts about C(storagePools) it is required to inform either the argument C(name) or C(ip_hostname).
          Otherwise, this option will be ignored."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather paginated, filtered and sorted facts about Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: managedDomain=TestDomain

- debug: var=storage_systems

- name: Gather facts about a Storage System by IP
  oneview_storage_system_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_systems


- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System and all options
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
    options:
        - hostTypes
        - storagePools
  delegate_to: localhost

- debug: var=storage_systems
- debug: var=storage_system_host_types
- debug: var=storage_system_pools

'''

RETURN = '''
storage_systems:
    description: Has all the OneView facts about the Storage Systems.
    returned: Always, but can be null.
    type: complex

storage_system_host_types:
    description: Has all the OneView facts about the supported host types.
    returned: When requested, but can be null.
    type: complex

storage_system_pools:
    description: Has all the OneView facts about the Storage Systems - Storage Pools.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class StorageSystemFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            ip_hostname=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )

        super(StorageSystemFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_systems

    def execute_module(self):
        facts = {}
        is_specific_storage_system = True
        if self.module.params.get('ip_hostname'):
            storage_systems = self.oneview_client.storage_systems.get_by_ip_hostname(
                self.module.params.get('ip_hostname'))
        elif self.module.params.get('name'):
            storage_systems = self.oneview_client.storage_systems.get_by_name(self.module.params['name'])
        else:
            storage_systems = self.oneview_client.storage_systems.get_all(**self.facts_params)
            is_specific_storage_system = False

        self.__get_options(facts, storage_systems, is_specific_storage_system)

        facts['storage_systems'] = storage_systems

        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, facts, storage_system, is_specific_storage_system):

        if self.options:
            if self.options.get('hostTypes'):
                facts['storage_system_host_types'] = self.oneview_client.storage_systems.get_host_types()

            if storage_system and is_specific_storage_system:
                storage_uri = storage_system['uri']
                if self.options.get('storagePools'):
                    facts['storage_system_pools'] = self.oneview_client.storage_systems.get_storage_pools(storage_uri)


def main():
    StorageSystemFactsModule().run()


if __name__ == '__main__':
    main()
