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
module: oneview_enclosure_script_facts
short_description: Retrieve facts about the script of one enclosure.
description:
    - Retrieve facts about the script of one Enclosure from OneView.
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
        - Enclosure name.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about the script of the enclosure named 'Test-Enclosure'
  oneview_enclosure_script_facts:
    config: "{{ config_file_path }}"
    name: "Enclosure-Name"

- debug: var=enclosure_script
'''

RETURN = '''
enclosure_script:
    description: Has all the OneView facts about the script of one enclosure.
    returned: always, but can be null
    type: complex
'''

ENCLOSURE_NOT_FOUND = 'Enclosure was not found.'


class EnclosureScriptFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=True, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            enclosure = self.__get_by_name(self.module.params['name'])
            if enclosure:
                script = self.oneview_client.enclosures.get_script(enclosure['uri'])
                self.module.exit_json(changed=False,
                                      ansible_facts=dict(enclosure_script=script))
            else:
                self.module.exit_json(changed=False,
                                      ansible_facts=dict(enclosure_env_config=None),
                                      msg=ENCLOSURE_NOT_FOUND)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        result = self.oneview_client.enclosures.get_by('name', name)
        return result[0] if result else None


def main():
    EnclosureScriptFactsModule().run()


if __name__ == '__main__':
    main()
