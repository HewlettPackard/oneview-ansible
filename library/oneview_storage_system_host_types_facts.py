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
module: oneview_storage_system_host_types_facts
short_description: Retrieve facts about Host Types of the OneView Storage Systems.
description:
    - Retrieve facts about Host Types of the OneView Storage Systems.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Gather facts about Storage System - Host Types
  oneview_storage_system_host_types_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=oneview_storage_host_types
'''

RETURN = '''
oneview_storage_system_host_types:
    description: Has all the OneView facts about the Storage Systems - Host Types.
    returned: always, but can be null
    type: complex
'''


class StorageSystemHostTypesFactsModule(object):
    argument_spec = {
        "config": {
            "required": True,
            "type": 'str'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:

            host_types = self.oneview_client.storage_systems.get_host_types()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(oneview_storage_host_types=host_types))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    StorageSystemHostTypesFactsModule().run()


if __name__ == '__main__':
    main()
