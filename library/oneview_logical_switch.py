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
module: oneview_logical_switch
short_description: Manage OneView Logical Switch resources.
description:
    - Provides an interface to manage Logical Switch resources. Can create, update, delete, or refresh.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Switch resource.
              C(present) creates a Logical Switch, if it doesn't exist. To update the Logical Switch, use the C(updated)
              state instead.
              C(updated) ensures the Logical Switch is updated. Currently OneView only supports updating the credentials
              and name of the Logical Switch. To change the name of the Logical Switch, a C(newName) in the data must be
              provided. The update operation is non-idempotent.
              C(absent) removes the resource from OneView, if it exists.
              C(refreshed) reclaims the top-of-rack switches in the logical switch. This operation is non-idempotent.
        choices: ['present', 'updated', 'absent', 'refreshed']
        required: true
    data:
      description:
        - List with the Logical Switches properties. You can choose set the Logical Switch Group by
          C(logicalSwitchGroupName) or C(logicalSwitchGroupUri).
      required: true

notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Logical Switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: present
    data:
      logicalSwitch:
        name: 'Test Logical Switch'
        # You can choose set the Logical Switch Group by logicalSwitchGroupName or logicalSwitchGroupUri
        logicalSwitchGroupName: 'Group Nexus 55xx'                                                   # option 1
        # logicalSwitchGroupUri: '/rest/logical-switch-groups/dce11b79-6fce-48af-84fb-a315b9644571'  # option 2
        switchCredentialConfiguration:
          - snmpV1Configuration:  # Switch 1
              communityString: 'public'
            logicalSwitchManagementHost: '172.18.16.1'
            snmpVersion: 'SNMPv1'
            snmpPort: 161
          - snmpV1Configuration:  # Switch 2
              communityString: 'public'
            logicalSwitchManagementHost: '172.18.16.2'
            snmpVersion: 'SNMPv1'
            snmpPort: 161
      logicalSwitchCredentials:
        - connectionProperties:  # Switch 1
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_1'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_1'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'
        - connectionProperties:  # Switch 2
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_2'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_2'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'

- name: Update the Logical Switch name and credentials
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: updated
    data:
      logicalSwitch:
        name: 'Test Logical Switch'
        newName: 'Test Logical Switch - Renamed'
      logicalSwitchCredentials:
        - connectionProperties:  # Switch 1
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_1'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_1'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'
        - connectionProperties:  # Switch 2
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_2'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_2'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'

- name: Reclaim the top-of-rack switches in the logical switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: refreshed
    data:
      logicalSwitch:
        name: 'Test Logical Switch'

- name: Delete a Logical Switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: absent
    data:
      logicalSwitch:
        name: 'Test Logical Switch'
'''

RETURN = '''
logical_switch:
    description: Has the facts about the OneView Logical Switch.
    returned: On the states 'present', 'updated', and 'refreshed'. Can be null.
    type: complex
'''

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewException, HPOneViewResourceNotFound


class LogicalSwitchModule(OneViewModuleBase):
    MSG_CREATED = 'Logical Switch created successfully.'
    MSG_UPDATED = 'Logical Switch updated successfully.'
    MSG_DELETED = 'Logical Switch deleted successfully.'
    MSG_ALREADY_EXIST = 'Logical Switch already exists.'
    MSG_ALREADY_ABSENT = 'Nothing to do.'
    MSG_REFRESHED = 'Logical Switch refreshed.'
    MSG_LOGICAL_SWITCH_NOT_FOUND = 'Logical Switch not found.'
    MSG_LOGICAL_SWITCH_GROUP_NOT_FOUND = 'Logical Switch Group not found.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'updated', 'absent', 'refreshed']
            ),
            data=dict(required=True, type='dict')
        )
        super(LogicalSwitchModule, self).__init__(additional_arg_spec=argument_spec,
                                                  validate_etag_support=True)

        self.resource_client = self.oneview_client.logical_switches

    def execute_module(self):
        data = deepcopy(self.module.params['data'])
        resource = self.__get_by_name(data)

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present(data, resource)
        elif self.state == 'absent':
            return self.resource_absent(resource)
        elif self.state == 'updated':
            changed, msg, ansible_facts = self.__update(data, resource)
        elif self.state == 'refreshed':
            changed, msg, ansible_facts = self.__refresh(data, resource)

        return dict(changed=changed, msg=msg, ansible_facts=ansible_facts)

    def __present(self, data, resource):
        self.__replace_group_name_by_uri(data)
        resource = self.__get_by_name(data)

        if not resource:
            created_resource = self.oneview_client.logical_switches.create(data)
            return True, self.MSG_CREATED, dict(logical_switch=created_resource)
        else:
            return False, self.MSG_ALREADY_EXIST, dict(logical_switch=resource)

    def __update(self, data, resource):
        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_LOGICAL_SWITCH_NOT_FOUND)
        else:
            data['logicalSwitch']['uri'] = resource['uri']

            if 'logicalSwitchGroupUri' not in data['logicalSwitch']:
                data['logicalSwitch']['logicalSwitchGroupUri'] = resource['logicalSwitchGroupUri']
            if 'switchCredentialConfiguration' not in data['logicalSwitch']:
                data['logicalSwitch']['switchCredentialConfiguration'] = resource['switchCredentialConfiguration']

            if 'newName' in data['logicalSwitch']:
                data['logicalSwitch']['name'] = data['logicalSwitch'].pop('newName')

            self.__replace_group_name_by_uri(data)
            created_resource = self.oneview_client.logical_switches.update(data)
            return True, self.MSG_UPDATED, dict(logical_switch=created_resource)

    def __refresh(self, data, resource):
        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_LOGICAL_SWITCH_NOT_FOUND)
        else:
            logical_switch = self.oneview_client.logical_switches.refresh(resource['uri'])
            return True, self.MSG_REFRESHED, dict(logical_switch=logical_switch)

    def __get_by_name(self, data):
        if 'logicalSwitch' not in data:
            return None

        result = self.oneview_client.logical_switches.get_by('name', data['logicalSwitch']['name'])
        return result[0] if result else None

    def __replace_group_name_by_uri(self, data):
        if 'logicalSwitch' in data and 'logicalSwitchGroupName' in data['logicalSwitch']:
            group_name = data['logicalSwitch']['logicalSwitchGroupName']
            logical_switch_group = self.oneview_client.logical_switch_groups.get_by('name', group_name)

            if logical_switch_group:
                data['logicalSwitch'].pop('logicalSwitchGroupName')
                data['logicalSwitch']['logicalSwitchGroupUri'] = logical_switch_group[0]['uri']
            else:
                raise HPOneViewResourceNotFound(self.MSG_LOGICAL_SWITCH_GROUP_NOT_FOUND)


def main():
    LogicalSwitchModule().run()


if __name__ == '__main__':
    main()
