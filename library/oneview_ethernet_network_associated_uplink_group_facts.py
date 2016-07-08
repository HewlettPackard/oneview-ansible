#!/usr/bin/python

###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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

from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_ethernet_network_associated_uplink_group_facts
short_description: Gather facts about the uplink sets which are using an Ethernet network.
description:
    - Retrieve a list of uplink port group URIs for the Ethernet network with specified name.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Ethernet Network name.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Gather facts about the uplink sets which are using an Ethernet network named 'Test Ethernet Network'
  oneview_ethernet_network_associated_uplink_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Ethernet Network"

- debug: var=enet_associated_uplink_groups
'''

RETURN = '''
enet_associated_uplink_groups:
    description: Has all the uplink port group URIs which are using an ethernet network.
    returned: always, but can be null
    type: complex
'''

ENET_NOT_FOUND = 'Ethernet Network not found.'


class EthernetNetworkAssociatedUplinkGroupFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=True, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            enet_name = self.module.params['name']
            if enet_name:
                self.__get_associated_uplink_groups(enet_name)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_associated_uplink_groups(self, enet_name):
        ethernet_network = self.__get_by_name(enet_name)

        if ethernet_network:
            associated_uplink_groups = self.oneview_client.ethernet_networks.get_associated_uplink_groups(
                ethernet_network['uri'])
            self.module.exit_json(changed=False,
                                  ansible_facts=dict(enet_associated_uplink_groups=associated_uplink_groups))
        else:
            self.module.exit_json(changed=False,
                                  ansible_facts=dict(enet_associated_uplink_groups=None),
                                  msg=ENET_NOT_FOUND)

    def __get_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None


def main():
    EthernetNetworkAssociatedUplinkGroupFactsModule().run()


if __name__ == '__main__':
    main()
