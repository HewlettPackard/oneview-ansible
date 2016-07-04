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
module: oneview_enclosure_group_facts
short_description: Retrieve facts about one or more of the OneView Enclosure Groups.
description:
    - Retrieve facts about one or more of the Enclosure Groups from OneView.
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
        - Enclosure Group name.
      required: false
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=enclosure_group

- name: Gather facts about a Enclosure Group by name
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
  delegate_to: localhost

- debug: var=enclosure_group
'''

RETURN = '''
oneview_enclosure_group_facts:
    description: Has all the OneView facts about the Enclosure Groups.
    returned: always, but can be null
    type: complex
'''


class EnclosureGroupFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'},
        "name": {
            "required": False,
            "type": 'str'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if 'name' in self.module.params and self.module.params['name']:
                enclosure_group = self.oneview_client.enclosure_groups.get_by('name', self.module.params['name'])
            else:
                enclosure_group = self.oneview_client.enclosure_groups.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(enclosure_group=enclosure_group))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    EnclosureGroupFactsModule().run()


if __name__ == '__main__':
    main()
