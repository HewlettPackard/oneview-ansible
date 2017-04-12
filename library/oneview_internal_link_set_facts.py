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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_internal_link_set_facts
short_description: Retrieve facts about the OneView Internal Link Sets.
description:
    - Retrieve facts about the Internal Link Sets from OneView. It is possible get all Internal Link Sets or filter
      by name.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(filter): A general filter/query string to narrow the list of items returned.
          C(sort): The sort order of the returned data set.
          C(query): A general query string to narrow the list of resources returned.
          C(fields): Specifies which fields should be returned in the result set.
          C(view): Return a specific subset of the attributes of the resource or collection, by specifying the name
          of a predefined view."
      required: false
    name:
      description:
        - Name of the Internal Link Set.
      required: false
notes:
    - This resource is available for API version 300 or later
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"

- debug: var=internal_link_sets

- name: Gather paginated and sorted facts about Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:ascending'

- debug: var=internal_link_sets

- name: Gather facts about an Internal Link Set by name
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    name: "Internal Link Set Name"

- debug: var=internal_link_sets
'''

RETURN = '''
internal_link_sets:
    description: Has all the OneView facts about the Internal Link Sets.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class InternalLinkSetFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')

    )

    def __init__(self):
        super(InternalLinkSetFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        name = self.module.params.get('name')
        if name:
            internal_links = self.oneview_client.internal_link_sets.get_by('name', name)
        else:
            internal_links = self.oneview_client.internal_link_sets.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(internal_link_sets=internal_links))


def main():
    InternalLinkSetFactsModule().run()


if __name__ == '__main__':
    main()
