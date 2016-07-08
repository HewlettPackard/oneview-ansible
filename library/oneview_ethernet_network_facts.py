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
module: oneview_ethernet_network_facts
short_description: Retrieve facts about one or more of the OneView Ethernet Networks.
description:
    - Retrieve facts about one or more of the Ethernet Networks from OneView.
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
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Gather facts about all Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    name: Ethernet network name

- debug: var=ethernet_networks
'''

RETURN = '''
ethernet_networks:
    description: Has all the OneView facts about the Ethernet Networks.
    returned: always, but can be null
    type: complex
'''


class EthernetNetworkFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            enet_name = self.module.params['name']
            if enet_name:
                self.__get_by_name(enet_name)
            else:
                self.__get_all()

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        ethernet_networks = self.oneview_client.ethernet_networks.get_by('name', name)

        self.module.exit_json(changed=False,
                              ansible_facts=dict(ethernet_networks=ethernet_networks))

    def __get_all(self):
        ethernet_networks = self.oneview_client.ethernet_networks.get_all()

        self.module.exit_json(changed=False,
                              ansible_facts=dict(ethernet_networks=ethernet_networks))


def main():
    EthernetNetworkFactsModule().run()


if __name__ == '__main__':
    main()
