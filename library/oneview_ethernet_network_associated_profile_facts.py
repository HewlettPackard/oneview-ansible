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
module: oneview_ethernet_network_associated_profile_facts
short_description: Retrieve the facts about the profiles which are using an Ethernet network.
description:
    - Retrieve the facts about the profiles which are using an Ethernet network.
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
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about profiles which are using an Ethernet network named 'Test-Ethernet-Network'
  oneview_ethernet_network_associated_profile_facts:
    config: "{{ config_file_path }}"
    name: "Test-Ethernet-Network"

- debug: var=oneview_enet_associated_profiles
'''

RETURN = '''
oneview_enet_associated_profiles:
    description:  List of profile URIs for the Ethernet network.
    returned: always, but can be null
    type: complex
'''


ETHERNET_NETWORK_NOT_FOUND = 'Ethernet Network not found.'


class EthernetNetworkAssociatedProfileModule(object):

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
            ethernet_network_name = self.module.params['name']
            if ethernet_network_name:
                self.__get_ethernet_network_associated_profiles(ethernet_network_name)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_ethernet_network_associated_profiles(self, name):
        ethernet_network = self.__get_ethernet_network_by_name(name)

        if ethernet_network:
            env_config = self.oneview_client.ethernet_networks.get_associated_profiles(ethernet_network['uri'])
            self.module.exit_json(changed=False,
                                  ansible_facts=dict(oneview_enet_associated_profiles=env_config))
        else:
            self.module.exit_json(changed=False,
                                  ansible_facts=dict(oneview_enet_associated_profiles=None),
                                  msg=ETHERNET_NETWORK_NOT_FOUND)

    def __get_ethernet_network_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None


def main():
    EthernetNetworkAssociatedProfileModule().run()


if __name__ == '__main__':
    main()
