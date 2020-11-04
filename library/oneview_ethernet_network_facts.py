#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
module: oneview_ethernet_network_facts
short_description: Retrieve the facts about one or more of the OneView Ethernet Networks.
description:
    - Retrieve the facts about one or more of the Ethernet Networks from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author:
    - "Camila Balestrin (@balestrinc)"
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Ethernet Network name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an Ethernet Network and related resources.
          Options allowed: C(associatedProfiles) and C(associatedUplinkGroups)."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Ethernet Networks
  oneview_ethernet_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200

- debug: var=ethernet_networks

- name: Gather paginated and filtered facts about Ethernet Networks
  oneview_ethernet_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'purpose=General'

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name
  oneview_ethernet_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: Ethernet network name

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name with options
  oneview_ethernet_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    name: "{{ name }}"
    options:
      - associatedProfiles
      - associatedUplinkGroups
  delegate_to: localhost

- debug: var=enet_associated_profiles
- debug: var=enet_associated_uplink_groups
'''

RETURN = '''
ethernet_networks:
    description: Has all the OneView facts about the Ethernet Networks.
    returned: Always, but can be null.
    type: dict

enet_associated_profiles:
    description: Has all the OneView facts about the profiles which are using the Ethernet network.
    returned: When requested, but can be null.
    type: dict

enet_associated_uplink_groups:
    description: Has all the OneView facts about the uplink sets which are using the Ethernet network.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class EthernetNetworkFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(EthernetNetworkFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.ethernet_networks)

    def execute_module(self):
        ansible_facts = {}
        ethernet_networks = []

        if self.module.params['name']:
            if self.current_resource:
                ethernet_networks = self.current_resource.data
                if self.module.params.get('options'):
                    ansible_facts = self.__gather_optional_facts()
        else:
            ethernet_networks = self.resource_client.get_all(**self.facts_params)

        ansible_facts['ethernet_networks'] = ethernet_networks

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self):
        ansible_facts = {}

        if self.options.get('associatedProfiles'):
            ansible_facts['enet_associated_profiles'] = self.__get_associated_profiles()
        if self.options.get('associatedUplinkGroups'):
            ansible_facts['enet_associated_uplink_groups'] = self.__get_associated_uplink_groups()

        return ansible_facts

    def __get_associated_profiles(self):
        associated_profiles = self.current_resource.get_associated_profiles()
        return [self.oneview_client.server_profiles.get_by_uri(x).data for x in associated_profiles]

    def __get_associated_uplink_groups(self):
        uplink_groups = self.current_resource.get_associated_uplink_groups()
        return [self.oneview_client.uplink_sets.get_by_uri(x).data for x in uplink_groups]


def main():
    EthernetNetworkFactsModule().run()


if __name__ == '__main__':
    main()
