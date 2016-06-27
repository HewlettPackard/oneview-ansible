#!/usr/bin/python

###
# Copyright (2016) Hewlett Packard Enterprise Development LP 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
###

from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_logical_interconnect_group_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnect Groups.
description:
    - Retrieve facts about one or more of the Logical Interconnect Groups from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Logical Interconnect Group name.
      required: false
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=logical_interconnect_groups
'''

RETURN = '''
ligs:
    description: Has all the OneView facts about the Logical Interconnect Groups.
    returned: always, but can be null
    type: complex
'''


class LogicalInterconnectGroupFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if self.module.params['name']:
                self.__get_by_name(self.module.params['name'])
            else:
                self.__get_all()

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        logical_interconnect_groups = self.oneview_client.logical_interconnect_groups.get_by('name', name)

        self.module.exit_json(changed=False,
                              ansible_facts=dict(logical_interconnect_groups=logical_interconnect_groups))

    def __get_all(self):
        logical_interconnect_groups = self.oneview_client.logical_interconnect_groups.get_all()

        self.module.exit_json(changed=False,
                              ansible_facts=dict(logical_interconnect_groups=logical_interconnect_groups))


def main():
    LogicalInterconnectGroupFactsModule().run()


if __name__ == '__main__':
    main()
