#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_logical_switch_facts
short_description: Retrieve the facts about one or more of the OneView Logical Switches.
description:
    - Retrieve the facts about one or more of the Logical Switches from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Logical Switch name.
      required: false
notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Switches
  oneview_logical_switch_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
- debug: var=logical_switches

- name: Gather paginated, filtered and sorted facts about Logical Switches
  oneview_logical_switch_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_switches

- name: Gather facts about a Logical Switch by name
  oneview_logical_switch_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    name: 'Name of the Logical Switch'

- debug: var=logical_switches
'''

RETURN = '''
logical_switches:
    description: Has all the OneView facts about the Logical Switches.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class LogicalSwitchFactsModule(OneViewModuleBase):

    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )

        super(LogicalSwitchFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        name = self.module.params.get('name')
        if name:
            logical_switches = self.oneview_client.logical_switches.get_by('name', name)
        else:
            logical_switches = self.oneview_client.logical_switches.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(logical_switches=logical_switches))


def main():
    LogicalSwitchFactsModule().run()


if __name__ == '__main__':
    main()
