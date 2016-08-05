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
module: oneview_server_hardware_facts
short_description: Retrieve facts about the OneView Server Hardwares.
description:
    - Retrieve facts about the Server Hardware from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Server Hardware name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Server Hardwares
  oneview_server_hardware_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=oneview_server_hardware


- name: Gather facts about a Server Hardware by name
  oneview_server_hardware_facts:
    config: "{{ config }}"
    name: "172.18.6.15"
  delegate_to: localhost

- debug: var=oneview_server_hardware
'''

RETURN = '''
oneview_server_hardware:
    description: Has all the OneView facts about the Server Hardware.
    returned: always, but can be null
    type: complex
'''


class ServerHardwareFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:

            if self.module.params.get('name'):
                server_hardware = self.oneview_client.server_hardware.get_by("name", self.module.params['name'])
            else:
                server_hardware = self.oneview_client.server_hardware.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(oneview_server_hardware=server_hardware))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    ServerHardwareFactsModule().run()


if __name__ == '__main__':
    main()
