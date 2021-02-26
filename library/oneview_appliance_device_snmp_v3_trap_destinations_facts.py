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
module: oneview_appliance_device_snmp_v3_trap_destinations_facts
short_description: Retrieve the facts about the OneView appliance SNMPv3 trap forwarding destinations.
description:
    - The appliance has the ability to forward events received from monitored or managed server hardware
      to the specified destinations as SNMPv3 traps.
      This module retrives the facts about the appliance SNMPv3 trap forwarding destinations.
version_added: "2.5"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.6.0"
author:
    "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        -  destination address of snmpv3 trap.
      required: false
    uri:
      description:
        - snmpv3 trap uri.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(sort): The sort order of the returned data set."
          C(filter): A general filter to narrow the list of resources returned.
          C(query): A general query string to narrow the list of resources returned.
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about the appliance SNMPv3 trap forwarding destinations.
  oneview_appliance_device_snmp_v3_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_trap_destinations

- name: Gather paginated, filtered and sorted facts about SNMPv3 trap forwarding destinations
  oneview_appliance_device_snmp_v3_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    params:
      start: 0
      count: 3
      sort: 'destinationAddress:descending'
      filter: "port='162'"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_trap_destinations

- name: Gather facts about a Trap Destination by ID
  oneview_appliance_device_snmp_v3_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    name: "1.1.1.1"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_trap_destinations
'''

RETURN = '''
appliance_device_snmp_v3_trap_destinations:
    description: Has all the OneView facts about the OneView appliance SNMPv3 trap forwarding destinations.
    returned: Always.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class ApplianceDeviceSnmpV3TrapDestinationsFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        uri=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3TrapDestinationsFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.appliance_device_snmp_v3_trap_destinations)

    def execute_module(self):
        if self.module.params['name']:
            obj_appliance_device_snmp_v3_trap = self.resource_client.get_by_name(self.module.params['name'])
            appliance_device_snmp_v3_trap_destinations = obj_appliance_device_snmp_v3_trap.data if obj_appliance_device_snmp_v3_trap else None
        elif self.module.params['uri']:
            obj_appliance_device_snmp_v3_trap = self.resource_client.get_by_uri(self.module.params['uri'])
            appliance_device_snmp_v3_trap_destinations = obj_appliance_device_snmp_v3_trap.data if obj_appliance_device_snmp_v3_trap else None
        else:
            appliance_device_snmp_v3_trap_destinations = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=appliance_device_snmp_v3_trap_destinations))


def main():
    ApplianceDeviceSnmpV3TrapDestinationsFactsModule().run()


if __name__ == '__main__':
    main()
