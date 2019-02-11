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
module: oneview_appliance_device_snmp_v3_trap_destinations
short_description: Manage the Appliance Device SNMPv3 Trap Destinations.
description:
    - Provides an interface to manage the Appliance Device SNMPv3 Trap Destinations.
version_added: "2.7"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
options:
    state:
        description:
          - Indicates the desired state for the Appliance Device SNMPv3 Trap Destinations.
            C(present) ensures data properties are compliant with OneView.
            C(absent) removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the SNMPv3 Trap Destinations properties
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the SNMPv3 Trap Destination is present
  oneview_appliance_device_snmp_v3_trap_destinations:
    config: "{{ config }}"
    state: present
    data:
        type: "Destination"
        destinationAddress: "10.0.0.1"
        port: 162
        userId: "8e57d829-2f17-4167-ae23-8fb46607c76c"
  delegate_to: localhost

- debug:
    var: oneview_appliance_device_snmp_v3_trap_destinations

- name: Update the userId of specified SNMPv3 Trap Destination
  oneview_appliance_device_snmp_v3_trap_destinations:
    config: "{{ config }}"
    state: present
    data:
      destinationAddress: "10.0.0.1"
      userId: "3953867c-5283-4059-a9ae-33487f901e85"
  delegate_to: localhost

- debug:
    var: oneview_appliance_device_snmp_v3_trap_destinations

- name: Ensure that the SNMPv3 Trap Destination is absent
  oneview_appliance_device_snmp_v3_trap_destinations:
    config: "{{ config }}"
    state: absent
    data:
        destinationAddress: "10.0.0.1"
  delegate_to: localhost
'''

RETURN = '''
oneview_appliance_device_snmp_v3_trap_destinations:
    description: Has all the OneView facts about the OneView appliance SNMPv3 Trap Destination.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleException, OneViewModuleValueError


class ApplianceDeviceSnmpV3TrapDestinationsModule(OneViewModuleBase):
    MSG_CREATED = 'Appliance Device SNMPv3 Trap Destination created successfully.'
    MSG_UPDATED = 'Appliance Device SNMPv3 Trap Destination updated successfully.'
    MSG_DELETED = 'Appliance Device SNMPv3 Trap Destination deleted successfully.'
    MSG_USER_NOT_FOUND = 'Appliance Device SNMPv3 User not found.'
    MSG_ALREADY_PRESENT = 'Appliance Device SNMPv3 Trap Destination is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Device SNMPv3 Trap Destination is already absent.'
    MSG_VALUE_ERROR = 'The destinationAddress or the id attrbiutes must be specfied'
    MSG_API_VERSION_ERROR = 'This module requires at least OneView 4.0 (API >= 600)'
    RESOURCE_FACT_NAME = 'appliance_device_snmp_v3_trap_destinations'

    argument_spec = dict(
        data=dict(required=True, type='dict'),
        state=dict(
            required=True,
            choices=['present', 'absent'])
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3TrapDestinationsModule, self).__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.appliance_device_snmp_v3_trap_destinations

    def execute_module(self):
        if self.oneview_client.api_version < 600:
            raise OneViewModuleValueError(self.MSG_API_VERSION_ERROR)

        if self.data.get('id'):
            query = self.resource_client.get_by_id(self.data.get('id'))
            resource = query[0] if query and query[0].get('id') == self.data['id'] else None
        elif self.data.get('destinationAddress'):
            query = self.resource_client.get_by('destinationAddress', self.data.get('destinationAddress'))
            resource = query[0] if query and query[0].get('destinationAddress') == self.data['destinationAddress'] else None
        else:
            raise OneViewModuleValueError(self.MSG_VALUE_ERROR)

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    ApplianceDeviceSnmpV3TrapDestinationsModule().run()


if __name__ == '__main__':
    main()
