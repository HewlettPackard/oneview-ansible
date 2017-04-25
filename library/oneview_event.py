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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_event
short_description: Manage OneView Events.
description:
    - Provides an interface to manage Events. Can only create.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the Event.
              C(present) will ensure data properties are compliant with OneView
        choices: ['present']
    data:
        description:
            - List with the Event properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the Event is present using a test type id
  oneview_event:
    config: "{{ config_file_path }}"
    state: present
    data:
      description: "This is a very simple test event"
      eventTypeID: "hp.justATest"
      eventDetails: [{
                      eventItemName: "ipv4Address",
                      eventItemValue: "198.51.100.5",
                      isThisVarbindData: "false",
                      varBindOrderIndex: -1
                      }]
'''

RETURN = '''
event:
    description: Has the facts about the OneView Events.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class EventModule(OneViewModuleBase):
    MSG_CREATED = 'Event created successfully.'
    RESOURCE_FACT_NAME = 'event'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super(EventModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                          validate_etag_support=True)

        self.resource_client = self.oneview_client.events

    def resource_present(self, resource, fact_name):
        """
        Implementation of the present state for the OneView resource 'Event'.
        It creates the resource. This operation is not idempotent as there is
        no way to query for a resource other than its uri.

        Args:
            resource (dict):
                Resource to create.
            fact_name (str):
                Name of the fact returned to the Ansible.

        Returns:
            A dictionary with the expected arguments for the event
        """
        changed = False
        resource = self.resource_client.create(self.data)
        msg = self.MSG_CREATED
        changed = True

        return dict(
            msg=msg,
            changed=changed,
            ansible_facts={fact_name: resource}
        )

    def execute_module(self):
        resource = None

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)


def main():
    EventModule().run()


if __name__ == '__main__':
    main()
