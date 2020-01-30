#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_interconnect
short_description: Manage the OneView Interconnect resources.
version_added: "2.3"
description:
    - Provides an interface to manage Interconnect resources. Can change the power state, UID light state, perform
      device reset, reset port protection, and update the interconnect ports.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Interconnect resource.
              C(powered_on) turns the power on.
              C(powered_off) turns the power off.
              C(uid_on) turns the UID light on.
              C(uid_off) turns the UID light off.
              C(device_reset) perform a device reset.
              C(update_ports) updates the interconnect ports.
              C(reset_port_protection) triggers a reset of port protection.
              C(reconfigured) will reapply the appliance's configuration on the interconnect. This includes running
              the same configuration steps that were performed as part of the interconnect add by the enclosure.
        choices: [
            'powered_on',
            'powered_off',
            'uid_on',
            'uid_off',
            'device_reset',
            'update_ports',
            'reset_port_protection',
            'reconfigured'
        ]
    name:
      description:
        - Interconnect name.
      required: false
    ip:
      description:
        - Interconnect IP address.
      required: false
    ports:
      description:
        - List with ports to update. This option should be used together with C(update_ports) state.
      required: false

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Turn the power off for Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: 'powered_off'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'On' for interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: 'uid_on'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'Off' for interconnect that matches the ip 172.18.1.114
  oneview_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: 'uid_on'
    ip: '172.18.1.114'

- name: Reconfigures the interconnect that matches the ip 172.18.1.114
  oneview_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: 'reconfigured'
    ip: '172.18.1.114'
'''

RETURN = '''
interconnect:
    description: Has the facts about the OneView Interconnect.
    returned: Always. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError)
from hpOneView.resources.resource import extract_id_from_uri


class InterconnectModule(OneViewModule):
    MSG_MISSING_KEY = "You must provide the interconnect name or the interconnect ip address."
    MSG_POWERED_ON = "Interconnect Powered On successfully."
    MSG_ALREADY_POWERED_ON = "Interconnect is already Powered On."
    MSG_POWERED_OFF = "Interconnect Powered Off successfully."
    MSG_ALREADY_POWERED_OFF = "Interconnect is already Powered Off."
    MSG_UID_STATE_ON = "Interconnect UID turned On succesfully."
    MSG_UID_STATE_ALREADY_ON = "Interconnect UID state is already On."
    MSG_UID_STATE_OFF = "Interconnect UID turned Off succesfully."
    MSG_UID_STATE_ALREADY_OFF = "Interconnect UID state is already Off."
    MSG_RESET = 'Interconnect Device Reset successful.'
    MSG_PORTS_UPDATED = 'Interconnect ports updated successfully.'
    MSG_PORTS_ALREADY_UPDATED = 'Interconnect ports already updated.'
    MSG_RESET_PORT_PROTECTION = 'Port protection reset successfully.'
    MSG_RECONFIGURED = 'Interconnect reconfigured successfully.'
    MSG_INTERCONNECT_NOT_FOUND = "The Interconnect was not found."

    states = dict(
        powered_on=dict(path='/powerState', value='On', msg=MSG_POWERED_ON, msg_no_changes=MSG_ALREADY_POWERED_ON),
        powered_off=dict(path='/powerState', value='Off', msg=MSG_POWERED_OFF, msg_no_changes=MSG_ALREADY_POWERED_OFF),
        uid_on=dict(path='/uidState', value='On', msg=MSG_UID_STATE_ON, msg_no_changes=MSG_UID_STATE_ALREADY_ON),
        uid_off=dict(path='/uidState', value='Off', msg=MSG_UID_STATE_OFF, msg_no_changes=MSG_UID_STATE_ALREADY_OFF),
        device_reset=dict(path='/deviceResetState', value='Reset', msg=MSG_RESET, msg_no_changes=None)
    )

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=[
                    'powered_on',
                    'powered_off',
                    'uid_on',
                    'uid_off',
                    'device_reset',
                    'update_ports',
                    'reset_port_protection',
                    'reconfigured'
                ]
            ),
            name=dict(required=False, type='str'),
            ip=dict(required=False, type='str'),
            ports=dict(required=False, type='list')
        )
        super(InterconnectModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.interconnects)

    def execute_module(self):

        self.__find_interconnect()
        state_name = self.module.params['state']

        if state_name == 'update_ports':
            changed, msg, resource = self.update_ports()
        elif state_name == 'reset_port_protection':
            changed, msg, resource = self.reset_port_protection()
        elif state_name == 'reconfigured':
            changed, msg, resource = self.reconfigure()
        else:
            state = self.states[state_name]

            if state_name == 'device_reset':
                changed, msg, resource = self.device_reset(state)
            else:
                changed, msg, resource = self.change_state(state)

        return dict(
            changed=changed,
            msg=msg,
            ansible_facts=dict(interconnect=resource)
        )

    def __find_interconnect(self):
        interconnect_ip = self.module.params['ip']

        if not self.current_resource and interconnect_ip:
            interconnects = self.oneview_client.interconnects.get_by('interconnectIP', interconnect_ip) or []
            if interconnects:
                self.current_resource = self.resource_client.get_by_uri(interconnects[0]["uri"])

        if not interconnect_ip and not self.module.params["name"]:
            raise OneViewModuleValueError(self.MSG_MISSING_KEY)

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_INTERCONNECT_NOT_FOUND)

    def change_state(self, state):
        changed = False

        property_name = state['path'][1:]

        if self.current_resource.data[property_name] != state['value']:
            self.current_resource = self.execute_operation(state['path'], state['value'])
            changed = True
            msg = state['msg']
        else:
            msg = state['msg_no_changes']

        return changed, msg, self.current_resource.data

    def device_reset(self, state):
        updated_resource = self.execute_operation(state['path'], state['value'])
        return True, self.MSG_RESET, updated_resource.data

    def execute_operation(self, path, value, operation="replace"):
        return self.current_resource.patch(
            operation=operation,
            path=path,
            value=value
        )

    def update_ports(self):
        ports = self.module.params['ports']

        if not ports:
            return False, self.MSG_PORTS_ALREADY_UPDATED, self.current_resource.data

        updated_resource = self.current_resource.update_ports(
            ports=ports
        )
        return True, self.MSG_PORTS_UPDATED, updated_resource

    def reset_port_protection(self):
        updated_resource = self.current_resource.reset_port_protection()
        return True, self.MSG_RESET_PORT_PROTECTION, updated_resource

    def reconfigure(self):
        updated_resource = self.current_resource.update_configuration()
        return True, self.MSG_RECONFIGURED, updated_resource


def main():
    InterconnectModule().run()


if __name__ == '__main__':
    main()
