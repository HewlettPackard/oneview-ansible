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
module: oneview_appliance_device_snmp_v3_users
short_description: Manage the Appliance Device SNMPv3 Users.
description:
    - Provides an interface to manage the Appliance Device SNMPv3 Users.
version_added: "2.7"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.8.0"
author:
    "Gianluca Zecchi (@gzecchi)"
options:
    state:
        description:
          - Indicates the desired state for the Appliance Device SNMPv3 User.
            C(present) ensures data properties are compliant with OneView.
            C(absent) removes the resource from OneView, if it exists.
            C(set_password) will set a user password to the value specified. This operation is non-idempotent.
        choices: ['present', 'absent', 'set_password']
    data:
        description:
            - List with the SNMPv3 Users properties
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the SNMPv3 user is present using the default configuration
  oneview_appliance_device_snmp_v3_users:
    config: "{{ config }}"
    state: present
    data:
        type: "Users"
        userName: "testUser"
        securityLevel: "Authentication"
        authenticationProtocol: "SHA512"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users

- name: Set the password of specified SNMPv3 user
  oneview_appliance_device_snmp_v3_users:
    config: "{{ config }}"
    state: set_password
    data:
      userName: "testUser"
      authenticationPassphrase: "NewPass1234"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users

- name: Ensure that the SNMPv3 user is absent
  oneview_appliance_device_snmp_v3_users:
    config: "{{ config }}"
    state: absent
    data:
        userName: "testUser"
  delegate_to: localhost
'''

RETURN = '''
appliance_device_snmp_v3_users:
    description: Has all the OneView facts about the OneView appliance SNMPv3 users.
    returned: On state 'present' and 'set_password'.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleException, OneViewModuleValueError


class ApplianceDeviceSnmpV3UsersModule(OneViewModuleBase):
    MSG_CREATED = 'Appliance Device SNMPv3 User created successfully.'
    MSG_UPDATED = 'Appliance Device SNMPv3 User updated successfully.'
    MSG_DELETED = 'Appliance Device SNMPv3 User deleted successfully.'
    MSG_USER_NOT_FOUND = 'Appliance Device SNMPv3 User not found.'
    MSG_ALREADY_PRESENT = 'Appliance Device SNMPv3 User is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Device SNMPv3 User is already absent.'
    MSG_VALUE_ERROR = 'The userName or the id attrbiutes must be specfied'
    MSG_API_VERSION_ERROR = 'This module requires at least OneView 4.0 (API >= 600)'
    MSG_PASSWORD_UPDATED = 'User authenticationPassphrase set successfully.'
    RESOURCE_FACT_NAME = 'appliance_device_snmp_v3_users'

    argument_spec = dict(
        data=dict(required=True, type='dict'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'set_password'])
    )

    def __init__(self):
        super(ApplianceDeviceSnmpV3UsersModule, self).__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.appliance_device_snmp_v3_users

    def execute_module(self):
        if self.oneview_client.api_version < 600:
            raise OneViewModuleValueError(self.MSG_API_VERSION_ERROR)

        if self.data.get('id'):
            query = self.resource_client.get_by_id(self.data.get('id'))
            resource = query[0] if query and query[0].get('id') == self.data['id'] else None
        elif self.data.get('userName'):
            query = self.resource_client.get_by('userName', self.data.get('userName'))
            resource = query[0] if query and query[0].get('userName') == self.data['userName'] else None
        else:
            raise OneViewModuleValueError(self.MSG_VALUE_ERROR)

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)
        elif self.state == 'set_password':
            return self.__set_password(resource)

    def __set_password(self, resource):
        if not resource:
            raise OneViewModuleException('The specified user does not exist.')
        if 'authenticationPassphrase' not in self.data:
            raise OneViewModuleException('This state requires an authenticationPassphrase to be declared.')

        data_merged = resource.copy()
        data_merged['authenticationPassphrase'] = self.data['authenticationPassphrase']
        resource = self.resource_client.update(data_merged)

        return dict(changed=True, msg=self.MSG_PASSWORD_UPDATED, ansible_facts=dict(appliance_device_snmp_v3_users=resource))


def main():
    ApplianceDeviceSnmpV3UsersModule().run()


if __name__ == '__main__':
    main()
