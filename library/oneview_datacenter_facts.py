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
module: oneview_datacenters_facts
short_description: Retrieve facts about Data Centers of the OneView.
description:
    - Retrieve facts about Data Centers of the OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Data Center name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'visualContent'"
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=datacenters


- name: Gather facts about a Data Center by name
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
  delegate_to: localhost

- debug: var=datacenters


- name: Gather facts about the Data Center Visual Content
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
    options:
      - visualContent
  delegate_to: localhost

- debug: var=datacenters
- debug: var=datacenter_visual_content
'''

RETURN = '''
datacenters:
    description: Has all the OneView facts about the Data Centers.
    returned: Always, but can be null.
    type: complex

datacenter_visual_content:
    description: Has facts about the Data Center Visual Content.
    returned: When requested, but can be null.
    type: complex
'''


class DatacenterFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        },
        "options": {
            "required": False,
            "type": 'list'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            client = self.oneview_client.datacenters
            ansible_facts = {}

            if self.module.params.get('name'):
                datacenters = client.get_by('name', self.module.params['name'])

                if self.module.params.get('options') and 'visualContent' in self.module.params['options']:
                    if datacenters:
                        ansible_facts['datacenter_visual_content'] = client.get_visual_content(datacenters[0]['uri'])
                    else:
                        ansible_facts['datacenter_visual_content'] = None

                ansible_facts['datacenters'] = datacenters
            else:
                ansible_facts['datacenters'] = client.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    DatacenterFactsModule().run()


if __name__ == '__main__':
    main()
