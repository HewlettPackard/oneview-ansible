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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_appliance_device_snmp_v3_trap_destinations
short_description: Manage the Appliance Device SNMPv3 Trap Destinations.
description:
    - Provides an interface to manage the Appliance Device SNMPv3 Trap Destinations.
version_added: "2.5"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.6.0"
author:
    "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
      description:
        - Indicates the desired state for the Appliance Device SNMPv3 Trap Destinations.
          C(present) will ensure data properties are compliant with OneView.
          C(absent) will remove the resource from OneView, if it exists.
      choices: ['present', 'absent']
    name:
      description:
        - Appliance Device snmpv3 trap destination address.
      required: True
    data:
      description:
            - List with the SNMPv3 Trap Destinations properties
      required: True
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the SNMPv3 Trap Destination is present
  oneview_appliance_device_snmp_v3_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: present
    name: 10.0.0.1
    data:
        destinationAddress: "10.0.0.1"
        port: 162
        userName: "test1"
  delegate_to: localhost

- name: Update the userId of specified SNMPv3 Trap Destination
  oneview_appliance_device_snmp_v3_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: present
    name: 10.0.0.1
    data:
      destinationAddress: "10.0.0.1"
      userId: "3953867c-5283-4059-a9ae-33487f901e85"
  delegate_to: localhost

- name: Ensure that the SNMPv3 Trap Destination is absent
  oneview_appliance_device_snmp_v3_trap_destinations:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: absent
    name: 10.0.0.1
  delegate_to: localhost
'''

RETURN = '''
oneview_appliance_device_snmp_v3_trap_destinations:
    description: Has all the OneView facts about the OneView appliance SNMPv3 Trap Destination.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleException, OneViewModuleValueError, OneViewModuleResourceNotFound


class ApplianceDeviceSnmpV3TrapDestinationsModule(OneViewModule):
    MSG_CREATED = 'Appliance Device SNMPv3 Trap Destination created successfully.'
    MSG_UPDATED = 'Appliance Device SNMPv3 Trap Destination updated successfully.'
    MSG_DELETED = 'Appliance Device SNMPv3 Trap Destination deleted successfully.'
    MSG_USER_NOT_FOUND = 'Appliance Device SNMPv3 User not found.'
    MSG_ALREADY_PRESENT = 'Appliance Device SNMPv3 Trap Destination is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Device SNMPv3 Trap Destination is already absent.'
    MSG_API_VERSION_ERROR = 'This module requires at least OneView 4.0 (API >= 600)'
    RESOURCE_FACT_NAME = 'appliance_device_snmp_v3_trap_destinations'

    argument_spec = dict(
        data=dict(required=False, type='dict'),
        name=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent'])
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3TrapDestinationsModule, self).__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.appliance_device_snmp_v3_trap_destinations)

    def execute_module(self):
        if self.oneview_client.api_version < 600:
            raise OneViewModuleValueError(self.MSG_API_VERSION_ERROR)

        self.__replace_snmpv3_username_by_userid()

        if self.state == 'present':
            return self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent()

    def __replace_snmpv3_username_by_userid(self):
        if self.data and self.data.get('userName'):
            username = self.data.pop('userName', None)

            result = self.oneview_client.appliance_device_snmp_v3_users.get_by('userName', username)
            if result:
                self.data['userId'] = result[0]['id']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_USER_NOT_FOUND)


def main():
    ApplianceDeviceSnmpV3TrapDestinationsModule().run()


if __name__ == '__main__':
    main()
