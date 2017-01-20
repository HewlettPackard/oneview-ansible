#!/usr/bin/python
# -*- coding: utf-8 -*-
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

try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound
    from hpOneView.exceptions import HPOneViewValueError

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_server_hardware
short_description: Manage OneView Server Hardware resources.
description:
    - "Provides an interface to manage Server Hardware resources."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Server Hardware resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
              'power_state_set' will set the power state of the Server Hardware.
              'refresh_state_set will set the refresh state of the Server Hardware.
              'ilo_firmware_version_updated' will update the iLO firmware version of the Server Hardware.
              'ilo_state_reset' will reset the iLO state.
              'uid_state_on' will set on the UID state, if necessary.
              'uid_state_off' will set on the UID state, if necessary.
              'environmental_configuration_set' will set the environmental configuration of the Server Hardware.
        choices: ['present', 'absent', 'power_state_set', 'refresh_state_set', 'ilo_firmware_version_updated',
                  'ilo_state_reset','uid_state_on', 'uid_state_off', environmental_configuration_set]
        required: true
    data:
        description:
            - List with Server Hardware properties and its associated states.
        required: true
    validate_etag:
        description:
            - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
              for the resource matches the ETag provided in the data.
        default: true
        choices: ['true', 'false']
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Add a Server Hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: present
    data:
         hostname : "172.18.6.15"
         username : "username"
         password : "password"
         force : false
         licensingIntent: "OneView"
         configurationState: "Managed"
  delegate_to: localhost

- name: Power Off the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: power_state_set
    data:
        name : "172.18.6.15"
        powerStateData:
            powerState: "Off"
            powerControl: "MomentaryPress"
  delegate_to: localhost

- name: Refresh the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: refresh_state_set
    data:
        name : "172.18.6.15"
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Update the Server Hardware iLO firmware version
  oneview_server_hardware:
    config: "{{ config }}"
    state: ilo_firmware_version_updated
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the calibrated max power of a server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: environmental_configuration_set
    data:
        name : "172.18.6.15"
        environmentalConfigurationData:
            calibratedMaxPower: 2500
  delegate_to: localhost

- name: Remove the server hardware by its IP
  oneview_server_hardware:
    config: "{{ config }}"
    state: absent
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the server UID state off
  oneview_server_hardware:
    config: "{{ config }}"
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
    type: complex
'''

SERVER_HARDWARE_ADDED = 'Server Hardware added successfully.'
SERVER_HARDWARE_ALREADY_ADDED = 'Server Hardware is already present.'
SERVER_HARDWARE_DELETED = 'Server Hardware deleted successfully.'
SERVER_HARDWARE_ALREADY_ABSENT = 'Server Hardware is already absent.'
SERVER_HARDWARE_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: {0}"
SERVER_HARDWARE_POWER_STATE_UPDATED = 'Server Hardware power state changed successfully.'
SERVER_HARDWARE_REFRESH_STATE_UPDATED = 'Server Hardware refresh state changed successfully.'
SERVER_HARDWARE_ILO_FIRMWARE_VERSION_UPDATED = 'Server Hardware iLO firmware version updated successfully.'
SERVER_HARDWARE_ENV_CONFIG_UPDATED = 'Server Hardware calibrated max power updated successfully.'
SERVER_HARDWARE_NOT_FOUND = 'Server Hardware is required for this operation.'
SERVER_HARDWARE_UID_STATE_CHANGED = 'Server Hardware UID state changed successfully.'
SERVER_HARDWARE_ILO_STATE_RESET = 'Server Hardware iLO state changed successfully.'
NOTHING_TO_DO = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerHardwareModule(object):
    patch_success_message = dict(
        ilo_state_reset=SERVER_HARDWARE_ILO_STATE_RESET,
        uid_state_on=SERVER_HARDWARE_UID_STATE_CHANGED,
        uid_state_off=SERVER_HARDWARE_UID_STATE_CHANGED
    )

    patch_params = dict(
        ilo_state_reset=dict(operation='replace', path='/mpState', value='Reset'),
        uid_state_on=dict(operation='replace', path='/uidState', value='On'),
        uid_state_off=dict(operation='replace', path='/uidState', value='Off')
    )

    argument_spec = dict(
        config=dict(required=False, type='str'),
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
            ]
        ),
        data=dict(required=True, type='dict'),
        validate_etag=dict(
            required=False,
            type='bool',
            default=True)
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']

            if not self.module.params.get('validate_etag'):
                self.oneview_client.connection.disable_etag_validation()

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data)

            else:
                if not data.get('name'):
                    raise HPOneViewValueError(SERVER_HARDWARE_MANDATORY_FIELD_MISSING.format("data.name"))

                resource = self.__get_server_hardware(data['name'])

                if state == 'absent':
                    changed, msg, ansible_facts = self.__absent(resource)
                else:
                    if not resource:
                        raise HPOneViewResourceNotFound(SERVER_HARDWARE_NOT_FOUND)

                    if state == 'power_state_set':
                        changed, msg, ansible_facts = self.__set_power_state(data, resource)
                    elif state == 'refresh_state_set':
                        changed, msg, ansible_facts = self.__set_refresh_state(data, resource)
                    elif state == 'ilo_firmware_version_updated':
                        changed, msg, ansible_facts = self.__update_mp_firmware_version(resource)
                    elif state == 'environmental_configuration_set':
                        changed, msg, ansible_facts = self.__set_environmental_configuration(data, resource)

                    else:
                        changed, msg, ansible_facts = self.__patch(state, resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg=exception.args[0])

    def __get_server_hardware(self, name):
        return (self.oneview_client.server_hardware.get_by("name", name) or [None])[0]

    def __present(self, data):

        if not data.get('hostname'):
            raise HPOneViewValueError(SERVER_HARDWARE_MANDATORY_FIELD_MISSING.format("data.hostname"))

        resource = self.__get_server_hardware(data['hostname'])

        changed = False

        if not resource:
            resource = self.oneview_client.server_hardware.add(data)
            changed = True
            msg = SERVER_HARDWARE_ADDED
        else:
            msg = SERVER_HARDWARE_ALREADY_ADDED

        return changed, msg, dict(server_hardware=resource)

    def __absent(self, resource):
        if resource:
            self.oneview_client.server_hardware.remove(resource)
            return True, SERVER_HARDWARE_DELETED, {}
        else:
            return False, SERVER_HARDWARE_ALREADY_ABSENT, {}

    def __set_power_state(self, data, resource):
        resource = self.oneview_client.server_hardware.update_power_state(data['powerStateData'], resource['uri'])
        return True, SERVER_HARDWARE_POWER_STATE_UPDATED, dict(server_hardware=resource)

    def __set_environmental_configuration(self, data, resource):
        resource = self.oneview_client.server_hardware.update_environmental_configuration(
            data['environmentalConfigurationData'],
            resource['uri'])

        return True, SERVER_HARDWARE_ENV_CONFIG_UPDATED, dict(server_hardware=resource)

    def __set_refresh_state(self, data, resource):
        resource = self.oneview_client.server_hardware.refresh_state(data['refreshStateData'], resource['uri'])
        return True, SERVER_HARDWARE_REFRESH_STATE_UPDATED, dict(server_hardware=resource)

    def __update_mp_firmware_version(self, resource):
        resource = self.oneview_client.server_hardware.update_mp_firware_version(resource['uri'])
        return True, SERVER_HARDWARE_ILO_FIRMWARE_VERSION_UPDATED, dict(server_hardware=resource)

    def __patch(self, state_name, resource):
        message = NOTHING_TO_DO
        changed = False

        state = self.patch_params[state_name].copy()
        property_name = state['path'][1:]

        if state_name == 'ilo_state_reset' or resource[property_name] != state['value']:
            resource = self.oneview_client.server_hardware.patch(id_or_uri=resource['uri'], **state)
            changed, message = True, self.patch_success_message[state_name]

        return changed, message, dict(server_hardware=resource)


def main():
    ServerHardwareModule().run()


if __name__ == '__main__':
    main()
