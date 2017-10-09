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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_event
short_description: Manage OneView Events.
description:
    - Provides an interface to manage Events. Can only create.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.2.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the Event.
              C(present) will ensure data properties are compliant with OneView. This operation is non-idempotent.
        choices: ['present']
    data:
        description:
            - List with the Event properties.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the Event is present using a test type id
  oneview_event:
    config: "{{ config_file_path }}"
    state: present
    data:
      description: "This is a very simple test event"
      eventTypeID: "hp.justATest"
      eventDetails:
        - eventItemName: ipv4Address
          eventItemValue: 198.51.100.5
          isThisVarbindData: false
          varBindOrderIndex: -1
'''

RETURN = '''
event:
    description: Has the facts about the OneView Events.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class EventModule(OneViewModuleBase):
    MSG_CREATED = 'Event created successfully.'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super(EventModule, self).__init__(additional_arg_spec=additional_arg_spec)

        self.resource_client = self.oneview_client.events

    def execute_module(self):
        if self.state == 'present':
            resource = self.resource_client.create(self.data)
            return dict(changed=True, msg=self.MSG_CREATED, ansible_facts=dict(event=resource))


def main():
    EventModule().run()


if __name__ == '__main__':
    main()
