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
from hpOneView.common import transform_list_to_dict

DOCUMENTATION = '''
---
module: oneview_logical_enclosure_facts
short_description: Retrieve facts about one or more of the OneView Logical Enclosures.
description:
    - Retrieve facts about one or more of the Logical Enclosures from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Logical Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Logical Enclosure and related resources.
          Options allowed: script."
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

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name with options
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
    options:
      - script
  delegate_to: localhost

- debug: var=logical_enclosures
- debug: var=logical_enclosure_script
'''

RETURN = '''
logical_enclosures:
    description: Has all the OneView facts about the Logical Enclosures.
    returned: always, but can be null
    type: complex

logical_enclosure_script:
    description: Has the facts about the script of a Logical Enclosure.
    returned: when required, but can be null
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
        },
        "options": {
            "required": False,
            "type": 'list'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            ansible_facts = {}

            if self.module.params.get('name'):
                logical_enclosures = self.oneview_client.logical_enclosures.get_by('name', self.module.params['name'])

                if self.module.params.get('options') and logical_enclosures:
                    ansible_facts = self.__gather_optional_facts(self.module.params['options'], logical_enclosures[0])
            else:
                logical_enclosures = self.oneview_client.logical_enclosures.get_all()

            ansible_facts['logical_enclosures'] = logical_enclosures

            self.module.exit_json(changed=False, ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_optional_facts(self, options, logical_enclosure):
        options = transform_list_to_dict(options)

        logical_enclosure_client = self.oneview_client.logical_enclosures
        ansible_facts = {}

        if options.get('script'):
            ansible_facts['logical_enclosure_script'] = logical_enclosure_client.get_script(logical_enclosure['uri'])

        return ansible_facts


def main():
    LogicalEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
