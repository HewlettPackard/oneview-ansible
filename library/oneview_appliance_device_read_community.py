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
module: oneview_appliance_device_read_community
short_description: Manage the Appliance Device Read Community string.
description:
    - Provides an interface to manage the Appliance Device Read Community string. It can only update it.
      This results in an update of the community string on all servers being managed/monitored by this OneView instance.
      The supported characters for community string are aA-zA, 0-9, !, ", #, $, %, ', &, (, ), *, +, -, ., /, @, `, {, |, }.
version_added: "2.5"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
options:
    state:
        description:
          - Indicates the desired state for the Appliance Device Read Community.
            C(present) ensures data properties are compliant with OneView.
        choices: ['present']
    data:
        description:
            - List with the Appliance Device Read Community.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the Appliance Device Read Community is present with Community String 'public'
  oneview_appliance_device_read_community:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      communityString: 'public'
  delegate_to: localhost

- debug:
    var: appliance_device_read_community
'''

RETURN = '''
appliance_device_read_community:
    description: Has all the OneView facts about the OneView Appliance Device Read Community.
    returned: Always.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class ApplianceDeviceReadCommunityModule(OneViewModuleBase):
    MSG_UPDATED = 'Appliance Device Read Community updated successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Device Read Community is already sets correctly.'
    RESOURCE_FACT_NAME = 'appliance_device_read_community'

    argument_spec = dict(
        data=dict(required=True, type='dict'),
        state=dict(
            required=True,
            choices=['present']))

    def __init__(self):
        super(ApplianceDeviceReadCommunityModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.appliance_device_read_community

    def execute_module(self):
        resource = self.resource_client.get()
        return self.resource_present(resource, self.RESOURCE_FACT_NAME)


def main():
    ApplianceDeviceReadCommunityModule().run()


if __name__ == '__main__':
    main()
