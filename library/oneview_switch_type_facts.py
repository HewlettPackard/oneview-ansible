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
module: oneview_switch_type_facts
short_description: Retrieve facts about the OneView Switch Types.
description:
    - Retrieve facts about the Switch Types from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Name of the Switch Type.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Switch Types
  oneview_switch_type_facts:
    config: "{{ config_path }}"

- debug: var=switch_types


- name: Gather facts about a Switch Type by name
  oneview_switch_type_facts:
    config: "{{ config_path }}"
    name: "Name of the Switch Type"

- debug: var=switch_types
'''

RETURN = '''
switch_types:
    switch_types: Has all the OneView facts about the Switch Types.
    returned: always, but can be null
    type: complex
'''


class SwitchTypeFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if self.module.params.get('name'):
                switch_types = self.oneview_client.switch_types.get_by('name', self.module.params.get('name'))
            else:
                switch_types = self.oneview_client.switch_types.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(switch_types=switch_types))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    SwitchTypeFactsModule().run()


if __name__ == '__main__':
    main()
