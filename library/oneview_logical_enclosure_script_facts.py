#!/usr/bin/python
# -*- coding: utf-8 -*-
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
module: oneview_logical_enclosure_script_facts
short_description: Retrieve the configuration script associated to an OneView Logical Enclosure.
description:
    - Retrieve the configuration script associated to an OneView Logical Enclosure.
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
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Get Logical Enclosure Script by Logical Enclosure name
  oneview_logical_enclosure_script_facts:
    config: "{{ config }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=oneview_logical_enclosure
'''

RETURN = '''
oneview_logical_enclosure_script_facts:
    description: Gets the Logical Enclosure script by Logical Enclosure name.
    returned: always, but can be null
    type: complex
'''


class LogicalEnclosureScriptFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'},
        "name": {
            "required": True,
            "type": 'str'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            logical_enclosure = self.oneview_client.logical_enclosures.get_by_name(self.module.params['name'])
            script = ''

            if logical_enclosure:
                script = self.oneview_client.logical_enclosures.get_script(logical_enclosure['uri'])

            self.module.exit_json(changed=False, ansible_facts=dict(oneview_logical_enclosure_script=script))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    LogicalEnclosureScriptFactsModule().run()


if __name__ == '__main__':
    main()
