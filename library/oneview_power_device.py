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
module: oneview_power_device
short_description: Manage OneView Power Device resources.
description:
    - "Provides an interface to manage Power delivery devices resources. Can add, update, remove, change power state,
       change UID state and refresh state."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Power Device resource.
              C(present) will ensure data properties are compliant with OneView.
              C(discovered) will add an iPDU to the OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(power_state_set) will set the power state of the Power Device.
              C(refresh_state_set) will set the refresh state of the Power Device.
              C(uid_state_set) will set the UID state of the Power Device.
        choices: ['present', 'discovered', 'absent', 'power_state_set', 'refresh_state_set', 'uid_state_set']
        required: true
    data:
        description:
            - List with Power Device properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Add a Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: present
    data:
        name: 'Power Device Name'
        ratedCapacity: 40
  delegate_to: localhost

- name: Add an iPDU
  oneview_power_device:
    config: "{{ config }}"
    state: discovered
    data:
         hostname : '{{ power_device_hostname }}'
         username : '{{ power_device_username }}'
         password : '{{ power_device_password }}'
         force : false
  delegate_to: localhost

- name: Power off the Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: power_state_set
    data:
        name: 'Power Device Name'
        powerStateData:
            powerState: "Off"
  delegate_to: localhost

- name: Refresh the Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: refresh_state_set
    data:
        name: 'Power Device Name'
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Set UID light state of the Power Device on
  oneview_power_device:
    config: "{{ config }}"
    state: uid_state_set
    data:
        name: 'Power Device Name'
        uidStateData:
            uidState: "On"
  delegate_to: localhost

- name: Remove the Power Device by its name
  oneview_power_device:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Power Device Name'
  delegate_to: localhost
'''

RETURN = '''
power_device:
    description: Has the OneView facts about the Power Device.
    returned: On states 'present', 'discovered', 'power_state_set', 'refresh_state_set', 'uid_state_set'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewValueError, HPOneViewResourceNotFound


class PowerDeviceModule(OneViewModuleBase):
    MSG_CREATED = 'Power Device added successfully.'
    MSG_IPDU_ADDED = 'iPDU added successfully.'
    MSG_ALREADY_EXIST = 'Power Device is already present.'
    MSG_DELETED = 'Power Device deleted successfully.'
    MSG_UPDATED = 'Power Device updated successfully.'
    MSG_ALREADY_ABSENT = 'Power Device is already absent.'
    MSG_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: data.name"
    MSG_POWER_STATE_UPDATED = 'Power Device power state changed successfully.'
    MSG_REFRESH_STATE_UPDATED = 'Power Device refresh state changed successfully.'
    MSG_UID_STATE_UPDATED = 'Power Device UID state changed successfully.'
    MSG_NOT_FOUND = 'Power Device was not found for this operation.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'power_state_set', 'refresh_state_set', 'uid_state_set', 'discovered']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(PowerDeviceModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                validate_etag_support=True)
        self.resource_client = self.oneview_client.power_devices

    def execute_module(self):

        changed, msg, ansible_facts = False, '', {}

        if self.state == 'discovered':
            changed, msg, ansible_facts = self.__discover(self.data)
        else:

            if not self.data.get('name'):
                raise HPOneViewValueError(self.MSG_MANDATORY_FIELD_MISSING)

            resource = self.get_by_name(self.data['name'])

            if self.state == 'present':
                return self.resource_present(resource, 'power_device', 'add')
            elif self.state == 'absent':
                return self.resource_absent(resource, 'remove')
            elif self.state == 'power_state_set':
                changed, msg, ansible_facts = self.__set_power_state(self.data, resource)
            elif self.state == 'refresh_state_set':
                changed, msg, ansible_facts = self.__set_refresh_state(self.data, resource)
            elif self.state == 'uid_state_set':
                changed, msg, ansible_facts = self.__set_uid_state(self.data, resource)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __discover(self, data):
        resource = self.oneview_client.power_devices.add_ipdu(data)

        return True, self.MSG_IPDU_ADDED, dict(power_device=resource)

    def __check_resource(self, resource):
        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)

    def __set_power_state(self, data, resource):
        self.__check_resource(resource)

        resource = self.oneview_client.power_devices.update_power_state(resource['uri'], data['powerStateData'])

        return True, self.MSG_POWER_STATE_UPDATED, dict(power_device=resource)

    def __set_uid_state(self, data, resource):
        self.__check_resource(resource)

        resource = self.oneview_client.power_devices.update_uid_state(resource['uri'], data['uidStateData'])

        return True, self.MSG_UID_STATE_UPDATED, dict(power_device=resource)

    def __set_refresh_state(self, data, resource):
        self.__check_resource(resource)

        resource = self.oneview_client.power_devices.update_refresh_state(resource['uri'], data['refreshStateData'])

        return True, self.MSG_REFRESH_STATE_UPDATED, dict(power_device=resource)


def main():
    PowerDeviceModule().run()


if __name__ == '__main__':
    main()
