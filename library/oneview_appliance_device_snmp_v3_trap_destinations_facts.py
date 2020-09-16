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
module: oneview_appliance_device_snmp_v3_trap_destinations_facts
short_description: Retrieve the facts about the OneView appliance SNMPv3 trap forwarding destinations.
description:
    - The appliance has the ability to forward events received from monitored or managed server hardware
      to the specified destinations as SNMPv3 traps.
      This module retrives the facts about the appliance SNMPv3 trap forwarding destinations.
version_added: "2.5"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the appliance SNMPv3 trap forwarding destinations.
  oneview_appliance_device_snmp_v3_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_trap_destinations

- name: Gather paginated, filtered and sorted facts about SNMPv3 trap forwarding destinations
  oneview_appliance_device_snmp_v3_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
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
    api_version: 800
    id: "19dc6a96-bd04-4724-819b-32bc660fcefc"
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

from ansible.module_utils.oneview import OneViewModuleBase


class ApplianceDeviceSnmpV3TrapDestinationsFactsModule(OneViewModuleBase):
    argument_spec = dict(
        id=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3TrapDestinationsFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        client = self.oneview_client.appliance_device_snmp_v3_trap_destinations
        ansible_facts = {}

        if self.module.params.get('id'):
            ansible_facts['appliance_device_snmp_v3_trap_destinations'] = self._get_by_id(self.module.params['id'])
        else:
            ansible_facts['appliance_device_snmp_v3_trap_destinations'] = client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _get_by_id(self, id):
        return self.oneview_client.appliance_device_snmp_v3_trap_destinations.get_by_id(id)


def main():
    ApplianceDeviceSnmpV3TrapDestinationsFactsModule().run()


if __name__ == '__main__':
    main()
