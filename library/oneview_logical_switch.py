#!/usr/bin/python

###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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

from ansible.module_utils.basic import *
from copy import deepcopy
try:
    from hpOneView.oneview_client import OneViewClient

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False


DOCUMENTATION = '''
---
module: oneview_logical_switch
short_description: Manage OneView Logical Switch resources.
description:
    - Provides an interface to manage Logical Switch resources. Can create, update, delete, or refresh.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Logical Switch resource.
              'present' creates a Logical Switch, if it doesn't exist. To update the Logical Switch, use the 'updated'
              state instead.
              'updated' ensures the Logical Switch is updated. Currently OneView only supports updating the credentials
              and name of the Logical Switch. To change the name of the Logical Switch, a 'newName' in the data must be
              provided. The update operation is non-idempotent.
              'absent' removes the resource from OneView, if it exists.
              'refreshed' reclaims the top-of-rack switches in the logical switch. This operation is non-idempotent.
        choices: ['present', 'updated', 'absent', 'refreshed']
    data:
      description:
        - List with the Logical Switches properties. You can choose set the Logical Switch Group by
          logicalSwitchGroupName or logicalSwitchGroupUri.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
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

LOGICAL_SWITCH_CREATED = 'Logical Switch created successfully.'
LOGICAL_SWITCH_UPDATED = 'Logical Switch updated successfully.'
LOGICAL_SWITCH_DELETED = 'Logical Switch deleted successfully.'
LOGICAL_SWITCH_ALREADY_EXIST = 'Logical Switch already exists.'
LOGICAL_SWITCH_ALREADY_ABSENT = 'Nothing to do.'
LOGICAL_SWITCH_REFRESHED = 'Logical Switch refreshed.'
LOGICAL_SWITCH_NOT_FOUND = 'Logical Switch not found.'
LOGICAL_SWITCH_GROUP_NOT_FOUND = 'Logical Switch Group not found.'
LOGICAL_SWITCH_NEW_NAME_INVALID = 'Rename failed: the new name provided is being used by another Logical Switch.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class LogicalSwitchModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'updated', 'absent', 'refreshed']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = deepcopy(self.module.params['data'])

        try:
            if state == 'present':
                self.__present(data)
            elif state == 'updated':
                self.__update(data)
            elif state == 'absent':
                self.__absent(data)
            elif state == 'refreshed':
                self.__refresh(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data)
        self.__replace_group_name_by_uri(data)

        if not resource:
            self.__create(data)
        else:
            self.module.exit_json(changed=False, msg=LOGICAL_SWITCH_ALREADY_EXIST,
                                  ansible_facts=dict(logical_switch=resource))

    def __create(self, data):
        created_resource = self.oneview_client.logical_switches.create(data)

        self.module.exit_json(changed=True,
                              msg=LOGICAL_SWITCH_CREATED,
                              ansible_facts=dict(logical_switch=created_resource))

    def __update(self, data):
        resource = self.__get_by_name(data)

        if resource:
            data['logicalSwitch']['uri'] = resource['uri']

            if 'logicalSwitchGroupUri' not in data['logicalSwitch']:
                data['logicalSwitch']['logicalSwitchGroupUri'] = resource['logicalSwitchGroupUri']
            if 'switchCredentialConfiguration' not in data['logicalSwitch']:
                data['logicalSwitch']['switchCredentialConfiguration'] = resource['switchCredentialConfiguration']

            if 'newName' in data['logicalSwitch']:
                if self.__get_by_new_name(data):
                    self.module.exit_json(changed=False, msg=LOGICAL_SWITCH_NEW_NAME_INVALID)
                data['logicalSwitch']['name'] = data['logicalSwitch'].pop('newName')

            self.__replace_group_name_by_uri(data)
            created_resource = self.oneview_client.logical_switches.update(data)

            self.module.exit_json(changed=True,
                                  msg=LOGICAL_SWITCH_UPDATED,
                                  ansible_facts=dict(logical_switch=created_resource))
        else:
            raise Exception(LOGICAL_SWITCH_NOT_FOUND)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.logical_switches.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=LOGICAL_SWITCH_DELETED)
        else:
            self.module.exit_json(changed=False, msg=LOGICAL_SWITCH_ALREADY_ABSENT)

    def __refresh(self, data):
        resource = self.__get_by_name(data)

        if resource:
            logical_switch = self.oneview_client.logical_switches.refresh(resource['uri'])
            self.module.exit_json(changed=True,
                                  msg=LOGICAL_SWITCH_REFRESHED,
                                  ansible_facts=dict(logical_switch=logical_switch))
        else:
            raise Exception(LOGICAL_SWITCH_NOT_FOUND)

    def __get_by_name(self, data):
        if 'logicalSwitch' not in data:
            return None

        result = self.oneview_client.logical_switches.get_by('name', data['logicalSwitch']['name'])
        return result[0] if result else None

    def __get_by_new_name(self, data):
        result = self.oneview_client.logical_switches.get_by('name', data['logicalSwitch']['newName'])
        return result[0] if result else None

    def __replace_group_name_by_uri(self, data):
        if 'logicalSwitch' in data and 'logicalSwitchGroupName' in data['logicalSwitch']:
            group_name = data['logicalSwitch']['logicalSwitchGroupName']
            logical_switch_group = self.oneview_client.logical_switch_groups.get_by('name', group_name)

            if logical_switch_group:
                data['logicalSwitch'].pop('logicalSwitchGroupName')
                data['logicalSwitch']['logicalSwitchGroupUri'] = logical_switch_group[0]['uri']
            else:
                raise Exception(LOGICAL_SWITCH_GROUP_NOT_FOUND)


def main():
    LogicalSwitchModule().run()


if __name__ == '__main__':
    main()
