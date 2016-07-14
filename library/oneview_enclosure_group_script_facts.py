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
module: oneview_enclosure_group_script_facts
short_description: Retrieve the configuration script associated to an OneView Enclosure Group.
description:
    - Retrieve the configuration script associated to an OneView Enclosure Group.
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
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Get Enclosure Group Script by Enclosure Group name
  oneview_enclosure_group_script_facts:
    config: "{{ config }}"
    name: "Enclosure Group (For Demo)"
  delegate_to: localhost

- debug: var=enclosure_group
'''

RETURN = '''
oneview_enclosure_group_script_facts:
    description: Gets the Enclosure Group script by Enclosure Group name.
    returned: always, but can be null
    type: complex
'''


class EnclosureGroupScriptFactsModule(object):
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
            enclosure_group = self.oneview_client.enclosure_groups.get_by('name', self.module.params['name'])
            script = ''

            if len(enclosure_group) > 0:
                script = self.oneview_client.enclosure_groups.get_script(enclosure_group[0]['uri'])

            self.module.exit_json(changed=False, ansible_facts=dict(enclosure_group_script=script))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    EnclosureGroupScriptFactsModule().run()


if __name__ == '__main__':
    main()
