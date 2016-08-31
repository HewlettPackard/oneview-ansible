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
from hpOneView.oneview_client import OneViewClient
from hpOneView.common import resource_compare

DOCUMENTATION = '''
---
module: oneview_power_device
short_description: Manage OneView Power Device resources.
description:
    - "Provides an interface to manage Power delivery devices resources. Can add, update, remove, change power state,
       change UID state and refresh state."
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Power Device resource.
              'present' will ensure data properties are compliant to OneView.
              'discovered' will add an iPDU to the OneView.
              'absent' will remove the resource from OneView, if it exists.
              'power_state_set' will set the power state of the Power Device.
              'refresh_state_set will set the refresh state of the Power Device.
              'uid_state_set will set the UId state of the Power Device.
        choices: ['present', 'discovered', 'absent', 'power_state_set', 'refresh_state_set', 'uid_state_set']
        required: true
    data:
        description:
            - List with Power Device properties and its associated states
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
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

POWER_DEVICE_ADDED = 'Power Device added successfully.'
POWER_DEVICE_ALREADY_PRESENT = 'Power Device is already present.'
POWER_DEVICE_DELETED = 'Power Device deleted successfully.'
POWER_DEVICE_UPDATED = 'Power Device updated successfully.'
POWER_DEVICE_ALREADY_ABSENT = 'Power Device is already absent.'
POWER_DEVICE_NEW_NAME_ALERADY_EXISTS = 'Power Device with new name already exists.'
POWER_DEVICE_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: data.name"
POWER_DEVICE_POWER_STATE_UPDATED = 'Power Device power state changed successfully.'
POWER_DEVICE_REFRESH_STATE_UPDATED = 'Power Device refresh state changed successfully.'
POWER_DEVICE_UID_STATE_UPDATED = 'Power Device uid state changed successfully.'
POWER_DEVICE_NOT_FOUND = 'Power Device was not found for this operation.'


class PowerDeviceModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'power_state_set', 'refresh_state_set', 'uid_state_set', 'discovered']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            if state == 'discovered':
                changed, msg, ansible_facts = self.__discover(data)
            else:
                resource = self.__get_resource(data)

                if state == 'present':
                    changed, msg, ansible_facts = self.__present(data, resource)
                elif state == 'absent':
                    changed, msg, ansible_facts = self.__absent(resource)
                elif state == 'power_state_set':
                    changed, msg, ansible_facts = self.__set_power_state(data, resource)
                elif state == 'refresh_state_set':
                    changed, msg, ansible_facts = self.__set_refresh_state(data, resource)
                elif state == 'uid_state_set':
                    changed, msg, ansible_facts = self.__set_uid_state(data, resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __get_resource(self, data):

        if not data.get('name'):
            raise Exception(POWER_DEVICE_MANDATORY_FIELD_MISSING)

        resource = (self.oneview_client.power_devices.get_by("name", data['name']) or [None])[0]
        return resource

    def __present(self, data, resource):

        changed = False

        self.__check_rename(data, resource)

        if not resource:
            resource = self.oneview_client.power_devices.add(data)
            changed = True
            msg = POWER_DEVICE_ADDED
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                # update resource
                changed = True
                resource = self.oneview_client.power_devices.update(merged_data)
                msg = POWER_DEVICE_UPDATED
            else:
                msg = POWER_DEVICE_ALREADY_PRESENT

        return changed, msg, dict(power_device=resource)

    def __check_rename(self, data, resource):

        if "newName" not in data:
            return

        resource_new_name = self.__get_resource({'name': data['newName']})

        if not resource:
            self.module.exit_json(changed=False, msg=POWER_DEVICE_NOT_FOUND)
        elif resource_new_name:
            self.module.exit_json(changed=False, msg=POWER_DEVICE_NEW_NAME_ALERADY_EXISTS)

        data["name"] = data.pop("newName")

    def __absent(self, resource):
        if resource:
            self.oneview_client.power_devices.remove(resource)
            return True, POWER_DEVICE_DELETED, {}
        else:
            return False, POWER_DEVICE_ALREADY_ABSENT, {}

    def __discover(self, data):

        resource = self.oneview_client.power_devices.add_ipdu(data)
        msg = POWER_DEVICE_ADDED

        return True, msg, dict(power_device=resource)

    def __set_power_state(self, data, resource):
        if not resource:
            raise Exception(POWER_DEVICE_NOT_FOUND)

        resource = self.oneview_client.power_devices.update_power_state(resource['uri'], data['powerStateData'])

        return True, POWER_DEVICE_POWER_STATE_UPDATED, dict(power_device=resource)

    def __set_uid_state(self, data, resource):
        if not resource:
            raise Exception(POWER_DEVICE_NOT_FOUND)

        resource = self.oneview_client.power_devices.update_uid_state(resource['uri'], data['uidStateData'])

        return True, POWER_DEVICE_UID_STATE_UPDATED, dict(power_device=resource)

    def __set_refresh_state(self, data, resource):
        if not resource:
            raise Exception(POWER_DEVICE_NOT_FOUND)

        resource = self.oneview_client.power_devices.update_refresh_state(resource['uri'], data['refreshStateData'])

        return True, POWER_DEVICE_REFRESH_STATE_UPDATED, dict(power_device=resource)


def main():
    PowerDeviceModule().run()


if __name__ == '__main__':
    main()
