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
module: oneview_logical_interconnect_group_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnect Groups.
description:
    - Retrieve facts about one or more of the Logical Interconnect Groups from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Logical Interconnect Group name.
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_interconnect_groups

- name: Gather paginated, filtered and sorted facts about Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=LIGName'

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=logical_interconnect_groups
'''

RETURN = '''
logical_interconnect_groups:
    description: Has all the OneView facts about the Logical Interconnect Groups.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class LogicalInterconnectGroupFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )

        super(LogicalInterconnectGroupFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        if self.module.params.get('name'):
            ligs = self.oneview_client.logical_interconnect_groups.get_by('name', self.module.params['name'])
        else:
            ligs = self.oneview_client.logical_interconnect_groups.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(logical_interconnect_groups=ligs))


def main():
    LogicalInterconnectGroupFactsModule().run()


if __name__ == '__main__':
    main()
