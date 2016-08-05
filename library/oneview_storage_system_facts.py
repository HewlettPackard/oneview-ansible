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
module: oneview_storage_system_facts
short_description: Retrieve facts about the OneView Storage Systems.
description:
    - Retrieve facts about the Storage Systems from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    ip_hostname:
      description:
        - Storage System IP or hostname.
      required: false
    name:
      description:
        - Storage System name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=oneview_storage_system


- name: Gather facts about a Storage System by IP
  oneview_storage_system_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=oneview_storage_system


- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=oneview_storage_system
'''

RETURN = '''
oneview_storage_system:
    description: Has all the OneView facts about the Storage Systems.
    returned: always, but can be null
    type: complex
'''


class StorageSystemFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        },
        "ip_hostname": {
            "required": False,
            "type": 'str'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if self.module.params.get('ip_hostname'):
                storage_system = self.oneview_client.storage_systems.get_by_ip_hostname(
                    self.module.params.get('ip_hostname'))
            elif self.module.params.get('name'):
                storage_system = self.oneview_client.storage_systems.get_by_name(self.module.params['name'])
            else:
                storage_system = self.oneview_client.storage_systems.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(oneview_storage_system=storage_system))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    StorageSystemFactsModule().run()


if __name__ == '__main__':
    main()
