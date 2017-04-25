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
module: oneview_event_facts
short_description: Retrieve the facts about one or more of the OneView Events.
description:
    - Retrieve the facts about one or more of the Events from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    "Felipe Bulsoni (@fgbulsoni)"
options:
    name:
      description:
        - Event name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Events
  oneview_event_facts:
    config: "{{ config_file_path }}"

- debug: var=events

- name: Gather paginated, filtered and sorted facts about Events
  oneview_event_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'description:descending'
      filter: 'eventTypeID=hp.justATest'
- debug: var=events

'''

RETURN = '''
events:
    description: Has all the OneView facts about the Events.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class EventFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(EventFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        events = self.oneview_client.events.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(events=events))


def main():
    EventFactsModule().run()


if __name__ == '__main__':
    main()
