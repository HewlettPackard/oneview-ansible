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
module: oneview_server_hardware
short_description: Manage OneView Server Hardware resources.
description:
    - "Provides an interface to manage Server Hardware resources."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.5.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Server Hardware resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(power_state_set) will set the power state of the Server Hardware.
              C(refresh_state_set) will set the refresh state of the Server Hardware.
              C(ilo_firmware_version_updated) will update the iLO firmware version of the Server Hardware.
              C(ilo_state_reset) will reset the iLO state.
              C(uid_state_on) will set on the UID state, if necessary.
              C(uid_state_off) will set off the UID state, if necessary.
              C(environmental_configuration_set) will set the environmental configuration of the Server Hardware.
              C(multiple_servers_added) will add multiple rack-mount servers.
        choices: ['present', 'absent', 'power_state_set', 'refresh_state_set', 'ilo_firmware_version_updated',
                  'ilo_state_reset','uid_state_on', 'uid_state_off', 'environmental_configuration_set',
                  'multiple_servers_added']
        required: true
    data:
        description:
            - List with Server Hardware properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Add a Server Hardware
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
         hostname : "172.18.6.15"
         username : "username"
         password : "password"
         force : false
         licensingIntent: "OneView"
         configurationState: "Managed"
  delegate_to: localhost

- name: Ensure that the Server Hardware is present and is inserted in the desired scopes
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
         name : "172.18.6.15"
         scopeUris:
           - '/rest/scopes/00SC123456'
           - '/rest/scopes/01SC123456'
  delegate_to: localhost

- name: Add multiple rack-mount servers
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: multiple_servers_added
    data:
        mpHostsAndRanges :
          - '172.18.6.15'
        username : 'username'
        password : 'password'
        initialScopeUris:
          - "/rest/scopes/01SC123456"
        licensingIntent: "OneView"
        configurationState: "Managed"
  delegate_to: localhost

- name: Power Off the server hardware
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: power_state_set
    data:
        name : "172.18.6.15"
        powerStateData:
            powerState: "Off"
            powerControl: "MomentaryPress"
  delegate_to: localhost

- name: Refresh the server hardware
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: refresh_state_set
    data:
        name : "172.18.6.15"
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Update the Server Hardware iLO firmware version
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: ilo_firmware_version_updated
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the calibrated max power of a server hardware
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: environmental_configuration_set
    data:
        name : "172.18.6.15"
        environmentalConfigurationData:
            calibratedMaxPower: 2500
  delegate_to: localhost

- name: Remove the server hardware by its IP
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the server UID state off
  oneview_server_hardware:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: uid_state_off
    data:
        name : '0000A66102, bay 12'
  delegate_to: localhost
'''

RETURN = '''
server_hardware:
    description: Has the OneView facts about the Server Hardware.
    returned: On states 'present', 'power_state_set', 'refresh_state_set', and 'ilo_firmware_version_updated'.
              Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleResourceNotFound, OneViewModuleValueError


class ServerHardwareModule(OneViewModuleBase):
    MSG_ADDED = 'Server Hardware added successfully.'
    MSG_ALREADY_PRESENT = 'Server Hardware is already present.'
    MSG_POWER_STATE_UPDATED = 'Server Hardware power state changed successfully.'
    MSG_REFRESH_STATE_UPDATED = 'Server Hardware refresh state changed successfully.'
    MSG_ILO_FIRMWARE_VERSION_UPDATED = 'Server Hardware iLO firmware version updated successfully.'
    MSG_ENV_CONFIG_UPDATED = 'Server Hardware calibrated max power updated successfully.'
    MSG_SERVER_HARDWARE_NOT_FOUND = 'The provided Server Hardware was not found.'
    MSG_UID_STATE_CHANGED = 'Server Hardware UID state changed successfully.'
    MSG_ILO_STATE_RESET = 'Server Hardware iLO state changed successfully.'
    MSG_NOTHING_TO_DO = 'Nothing to do.'
    MSG_DELETED = 'Server Hardware deleted successfully.'
    MSG_ALREADY_ABSENT = 'Server Hardware is already absent.'
    MSG_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: {0}"
    MSG_MULTIPLE_RACK_MOUNT_SERVERS_ADDED = "Servers added successfully."

    patch_success_message = dict(
        ilo_state_reset=MSG_ILO_STATE_RESET,
        uid_state_on=MSG_UID_STATE_CHANGED,
        uid_state_off=MSG_UID_STATE_CHANGED
    )

    patch_params = dict(
        ilo_state_reset=dict(operation='replace', path='/mpState', value='Reset'),
        uid_state_on=dict(operation='replace', path='/uidState', value='On'),
        uid_state_off=dict(operation='replace', path='/uidState', value='Off')
    )

    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'power_state_set',
                'refresh_state_set',
                'ilo_firmware_version_updated',
                'ilo_state_reset',
                'uid_state_on',
                'uid_state_off',
                'environmental_configuration_set',
                'multiple_servers_added'
            ]
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):

        super(ServerHardwareModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                   validate_etag_support=True)

        self.resource_client = self.oneview_client.server_hardware

    def execute_module(self):

        if self.state == 'present':
            return self.__present()
        elif self.state == 'multiple_servers_added':
            changed, msg, ansible_facts = self.__add_multiple_rack_mount_servers()
        else:
            if not self.data.get('name'):
                raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.name"))

            resource = self.__get_server_hardware(self.data['name'])

            if self.state == 'absent':
                return self.resource_absent(resource, method='remove')
            else:
                if not resource:
                    raise OneViewModuleResourceNotFound(self.MSG_SERVER_HARDWARE_NOT_FOUND)

                if self.state == 'power_state_set':
                    changed, msg, ansible_facts = self.__set_power_state(resource)
                elif self.state == 'refresh_state_set':
                    changed, msg, ansible_facts = self.__set_refresh_state(resource)
                elif self.state == 'ilo_firmware_version_updated':
                    changed, msg, ansible_facts = self.__update_mp_firmware_version(resource)
                elif self.state == 'environmental_configuration_set':
                    changed, msg, ansible_facts = self.__set_environmental_configuration(resource)
                else:
                    changed, msg, ansible_facts = self.__patch(resource)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __get_server_hardware(self, name):
        return (self.oneview_client.server_hardware.get_by("name", name) or [None])[0]

    def __present(self):

        if not self.data.get('hostname'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.hostname"))

        resource = self.__get_server_hardware(self.data['hostname'])

        scope_uris = self.data.pop('scopeUris', None)

        result = dict()

        if not resource:
            resource = self.oneview_client.server_hardware.add(self.data)
            result = dict(
                changed=True,
                msg=self.MSG_ADDED,
                ansible_facts={'server_hardware': resource}
            )
        else:
            result = dict(
                changed=False,
                msg=self.MSG_ALREADY_PRESENT,
                ansible_facts={'server_hardware': resource}
            )

        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'server_hardware', scope_uris)

        return result

    def __set_power_state(self, resource):
        resource = self.oneview_client.server_hardware.update_power_state(self.data['powerStateData'], resource['uri'])
        return True, self.MSG_POWER_STATE_UPDATED, dict(server_hardware=resource)

    def __set_environmental_configuration(self, resource):
        resource = self.oneview_client.server_hardware.update_environmental_configuration(
            self.data['environmentalConfigurationData'],
            resource['uri'])

        return True, self.MSG_ENV_CONFIG_UPDATED, dict(server_hardware=resource)

    def __set_refresh_state(self, resource):
        resource = self.oneview_client.server_hardware.refresh_state(self.data['refreshStateData'], resource['uri'])
        return True, self.MSG_REFRESH_STATE_UPDATED, dict(server_hardware=resource)

    def __update_mp_firmware_version(self, resource):
        resource = self.oneview_client.server_hardware.update_mp_firware_version(resource['uri'])
        return True, self.MSG_ILO_FIRMWARE_VERSION_UPDATED, dict(server_hardware=resource)

    def __patch(self, resource):
        state_name = self.state
        message = self.MSG_NOTHING_TO_DO
        changed = False

        state = self.patch_params[state_name].copy()
        property_name = state['path'][1:]
        property_value_changed = resource.get(property_name) != state['value']

        if state_name == 'ilo_state_reset' or property_value_changed:
            resource = self.oneview_client.server_hardware.patch(id_or_uri=resource['uri'], **state)
            changed, message = True, self.patch_success_message[state_name]

        return changed, message, dict(server_hardware=resource)

    def __add_multiple_rack_mount_servers(self):
        resource = self.oneview_client.server_hardware.add_multiple_servers(self.data)
        return True, self.MSG_MULTIPLE_RACK_MOUNT_SERVERS_ADDED, {"server_hardware": resource}


def main():
    ServerHardwareModule().run()


if __name__ == '__main__':
    main()
