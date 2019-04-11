#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_logical_interconnect_group_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnect Groups
description:
    - Retrieve facts about one or more of the Logical Interconnect Groups from OneView
version_added: "2.5"
requirements:
    - python >= 2.7.9
    - hpOneView >= 5.0.0
author:
    - Felipe Bulsoni (@fgbulsoni)
    - Thiago Miotto (@tmiotto)
    - Adriane Cardozo (@adriane-cardozo)
options:
    name:
      description:
        - Logical Interconnect Group name.
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  no_log: true
  delegate_to: localhost

- debug: var=logical_interconnect_groups

- name: Gather paginated, filtered and sorted facts about Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    params:
      start: 0
      count: 3
      sort: name:descending
      filter: name=LIGName
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  no_log: true
  delegate_to: localhost

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by scopeUris
  oneview_logical_interconnect_group_facts:
    params:
      scope_uris: "/rest/scopes/63d1ca81-95b3-41f1-a1ee-f9e1bc2d635f"
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  no_log: true
  delegate_to: localhost

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    name: logical lnterconnect group name
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  no_log: true
  delegate_to: localhost

- debug: var=logical_interconnect_groups
'''

RETURN = '''
logical_interconnect_groups:
    description: Has all the OneView facts about the Logical Interconnect Groups.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class LogicalInterconnectGroupFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            name=dict(type='str'),
            params=dict(type='dict'),
        )

        super(LogicalInterconnectGroupFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.logical_interconnect_groups

    def execute_module(self):
        if self.module.params.get('name'):
            ligs = self.resource_client.get_by('name', self.module.params['name'])
        else:
            ligs = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(logical_interconnect_groups=ligs))


def main():
    LogicalInterconnectGroupFactsModule().run()


if __name__ == '__main__':
    main()
