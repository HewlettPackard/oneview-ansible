#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_label_facts
short_description: Retrieve the facts about one or more of the OneView Labels.
description:
    - Retrieve the facts about one or more of the Labels from OneView.
version_added: "2.4"
requirements:
    - hpeOneView >= 5.4.0
author:
    - Asis Bagga (@asisbagga)
options:
    name:
      description:
        - Label name.
      type: str
    resourceUri:
      description:
        - Uri of the resource which labels are associated with.
      type: str

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Labels
  oneview_label_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
  delegate_to: localhost

- debug: var=labels

- name: Gather paginated, filtered and sorted facts about Labels
  oneview_label_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: ''
- debug: var=labels

- name: Gather facts about a Label by name
  oneview_label_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    name: "{{ labels[0]['name'] }}"
  delegate_to: localhost

- debug: var=labels

- name: Gather facts about a Label by Resource
  oneview_label_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    resourceUri: "/rest/enclosures/0000000000A66102"
  delegate_to: localhost

- debug: var=labels
'''

RETURN = '''
labels:
    description: Has all the OneView facts about the Labels.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class LabelFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            resourceUri=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )
        super(LabelFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.labels

    def execute_module(self):
        if self.module.params['name']:
            labels = self.resource_client.get_by('name', self.module.params['name'])
        elif self.module.params.get('resourceUri'):
            labels = self.oneview_client.labels.get_by_resource(self.module.params['resourceUri']).data
        else:
            labels = self.resource_client.get_all(**self.facts_params)
        return dict(changed=False, ansible_facts=dict(labels=labels))


def main():
    LabelFactsModule().run()


if __name__ == '__main__':
    main()
