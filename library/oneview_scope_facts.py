#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_scope_facts
short_description: Retrieve facts about one or more of the OneView Scopes.
description:
    - Retrieve facts about one or more of the Scopes from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Name of the scope.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           c(start): The first item to return, using 0-based indexing.
           c(count): The number of resources to return.
           c(query): A general query string to narrow the list of resources returned.
           c(sort): The sort order of the returned data set.
           c(view): Returns a specific subset of the attributes of the resource or collection, by specifying the name
           of a predefined view."
      required: false
notes:
    - This resource is available for API version 300 or later.
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all Scopes
  oneview_scope_facts:
    config: "{{ config_path }}"

- debug: var=scopes

- name: Gather paginated, filtered and sorted facts about Scopes
  oneview_scope_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      query: name eq 'SampleScope'
  delegate_to: localhost

- debug: var=scopes

- name: Gather facts about a Scope by name
  oneview_scope_facts:
    config: "{{ config_path }}"
    name: "Name of the Scope"

- debug: var=scopes
'''

RETURN = '''
scopes:
    description: Has all the OneView facts about the Scopes.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class ScopeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ScopeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.scopes

    def execute_module(self):
        name = self.module.params.get('name')
        if name:
            scope = self.oneview_client.scopes.get_by_name(name)
            scopes = [scope] if scope else []
        else:
            scopes = self.oneview_client.scopes.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(scopes=scopes))


def main():
    ScopeFactsModule().run()


if __name__ == '__main__':
    main()
