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
module: oneview_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Interconnects.
description:
    - Retrieve facts about one or more of the Interconnects from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Interconnect name
      required: false
    gather_name_servers:
      description:
        - If true facts about the name servers will also be gathered.
      required: false
      default: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: "{{ interconnect_name }}"

- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: "{{ interconnect_name }}"
    gather_name_servers: true
'''

RETURN = '''
interconnects:
    description: The list of interconnects.
    returned: always, but can be null
    type: list
name_servers:
    description: The named servers for an interconnect.
    returned: When the gather_name_servers is true
    type: list
'''


class InterconnectFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        gather_name_servers=dict(required=False, type='bool', default=False)
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            interconnect_name = self.module.params['name']
            facts = dict()

            if interconnect_name:
                interconnects = self.oneview_client.interconnects.get_by('name', interconnect_name)
                facts['interconnects'] = interconnects

                if interconnects and self.module.params['gather_name_servers']:
                    interconnect_uri = interconnects[0]['uri']
                    name_servers = self.oneview_client.interconnects.get_name_servers(interconnect_uri)
                    facts['name_servers'] = name_servers
            else:
                facts['interconnects'] = self.oneview_client.interconnects.get_all()

            self.module.exit_json(
                changed=False,
                ansible_facts=facts
            )
        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    InterconnectFactsModule().run()


if __name__ == '__main__':
    main()
