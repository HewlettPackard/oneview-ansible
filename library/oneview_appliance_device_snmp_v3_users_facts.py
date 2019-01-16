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
module: oneview_appliance_device_snmp_v3_users_facts
short_description: Retrieve the facts about the OneView appliance SNMPv3 users.
description:
    - SNMPv3 user will be used for sending the SNMPv3 trap to the associated destinations.
      One user can be assigned to multiple destinations.
      This module retrives the facts about the appliance SNMPv3 users.
version_added: "2.7"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the appliance SNMPv3 users.
  oneview_appliance_device_snmp_v3_users_facts:
    config: "{{ config }}"

- debug:
    var: appliance_device_snmp_v3_users

- name: Gather paginated, filtered and sorted facts about SNMPv3 users
  oneview_appliance_device_snmp_v3_users_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "securityLevel='Authentication and privacy'"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users

- name: Gather facts about a SNMPv3 user by ID
  oneview_appliance_device_snmp_v3_users_facts:
    config: "{{ config }}"
    id: "2af33d0c-dc1f-4b5f-ba3e-e4a0b1acb899"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users
'''

RETURN = '''
appliance_device_snmp_v3_users:
    description: Has all the OneView facts about the OneView appliance SNMPv3 users.
    returned: Always.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class ApplianceDeviceSnmpV3UsersFactsModule(OneViewModuleBase):
    argument_spec = dict(
        id=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3UsersFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        client = self.oneview_client.appliance_device_snmp_v3_users
        ansible_facts = {}

        if self.module.params.get('id'):
            ansible_facts['appliance_device_snmp_v3_users'] = self._get_by_id(self.module.params['id'])
        else:
            ansible_facts['appliance_device_snmp_v3_users'] = client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _get_by_id(self, id):
        return self.oneview_client.appliance_device_snmp_v3_users.get_by_id(id)


def main():
    ApplianceDeviceSnmpV3UsersFactsModule().run()


if __name__ == '__main__':
    main()
