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
module: oneview_logical_enclosure_facts
short_description: Retrieve facts about one or more of the OneView Logical Enclosures.
description:
    - Retrieve facts about one or more of the Logical Enclosures from OneView.
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
        - Logical Enclosure name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=oneview_logical_enclosure

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=oneview_logical_enclosure
'''

RETURN = '''
oneview_logical_enclosure_facts:
    description: Has all the OneView facts about the Logical Enclosures.
    returned: always, but can be null
    type: complex
'''


class LogicalEnclosureFactsModule(object):
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
            if self.module.params.get('name'):
                logical_enclosure = self.oneview_client.logical_enclosures.get_by('name', self.module.params['name'])
            else:
                logical_enclosure = self.oneview_client.logical_enclosures.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(onveview_logical_enclosure=logical_enclosure))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    LogicalEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
