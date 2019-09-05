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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_enclosure_group_facts
short_description: Retrieve facts about one or more of the OneView Enclosure Groups.
description:
    - Retrieve facts about one or more of the Enclosure Groups from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Enclosure Group name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Enclosure Group.
          Options allowed:
          C(configuration_script) Gets the configuration script for an Enclosure Group."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather paginated, filtered and sorted facts about Enclosure Groups
  oneview_enclosure_group_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'
      scope_uris: '/rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'

- debug: var=enclosure_groups

- name: Gather facts about an Enclosure Group by name with configuration script
  oneview_enclosure_group_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    name: "Test Enclosure Group Facts"
    options:
      - configuration_script
    delegate_to: localhost

- debug: var=enclosure_groups
- debug: var=enclosure_group_script
'''

RETURN = '''
enclosure_groups:
    description: Has all the OneView facts about the Enclosure Groups.
    returned: Always, but can be null.
    type: dict

enclosure_group_script:
    description: The configuration script for an Enclosure Group.
    returned: When requested, but can be null.
    type: string
'''

from ansible.module_utils.oneview import OneViewModule


class EnclosureGroupFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(EnclosureGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.enclosure_groups)

    def execute_module(self):
        facts = {}
        enclosure_groups = []
        name = self.module.params.get("name")

        if name:
            if self.current_resource:
                enclosure_groups = [self.current_resource.data]
                if "configuration_script" in self.options:
                    facts["enclosure_group_script"] = self.current_resource.get_script()
        else:
            enclosure_groups = self.resource_client.get_all(**self.facts_params)

        facts["enclosure_groups"] = enclosure_groups
        return dict(changed=False, ansible_facts=facts)


def main():
    EnclosureGroupFactsModule().run()


if __name__ == '__main__':
    main()
