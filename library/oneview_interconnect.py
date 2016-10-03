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
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_interconnect
short_description: Manage the OneView Interconnect resources.
description:
    - Provides an interface to manage the Interconnect power state and the UID light state. Can change the power state,
      UID light state, perform device reset, reset port protection, and update the interconnect ports.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Interconnect resource.
              'powered_on' turns the power on.
              'powered_off' turns the power off.
              'uid_on' turns the UID light on.
              'uid_off' turns the UID light off.
              'device_reset' perform a device reset.
              'update_ports' updates the interconnect ports.
              'reset_port_protection' triggers a reset of port protection.
        choices: [
            'powered_on',
            'powered_off',
            'uid_on',
            'uid_off',
            'device_reset',
            'update_ports',
            'reset_port_protection'
        ]
    name:
      description:
        - Interconnect name
      required: false
    ip:
      description:
        - Interconnect IP add
      required: false
    ports:
      description:
        - List with ports to update. This option should be used together with 'update_ports' state.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Turn the power off for Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'powered_off'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'On' for interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'Off' for interconnect that matches the ip 172.18.1.114
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    ip: '172.18.1.114'
'''

RETURN = '''
interconnect:
    description: Has the facts about the OneView Interconnect.
    returned: Always. Can be null.
    type: complex
'''

MISSING_KEY_MSG = "You must provide the interconnect name or the interconnect ip address"
INTERCONNECT_WAS_NOT_FOUND = "The Interconnect was not found."


class InterconnectModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=[
                'powered_on',
                'powered_off',
                'uid_on',
                'uid_off',
                'device_reset',
                'update_ports',
                'reset_port_protection'
            ]
        ),
        name=dict(required=False, type='str'),
        ip=dict(required=False, type='str'),
        ports=dict(required=False, type='list')
    )

    states = dict(
        powered_on=dict(path='/powerState', value='On'),
        powered_off=dict(path='/powerState', value='Off'),
        uid_on=dict(path='/uidState', value='On'),
        uid_off=dict(path='/uidState', value='Off'),
        device_reset=dict(path='/deviceResetState', value='Reset'),
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            interconnect = self.__get_interconnect()
            state_name = self.module.params['state']

            if state_name == 'update_ports':
                changed, resource = self.update_ports(interconnect)
            elif state_name == 'reset_port_protection':
                changed, resource = self.reset_port_protection(interconnect)
            else:
                state = self.states[state_name]

                if state_name == 'device_reset':
                    changed, resource = self.device_reset(state, interconnect)
                else:
                    changed, resource = self.change_state(state, interconnect)

            self.module.exit_json(
                changed=changed,
                ansible_facts=dict(interconnect=resource)
            )
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_interconnect(self):
        interconnect_ip = self.module.params['ip']
        interconnect_name = self.module.params['name']

        if interconnect_ip:
            interconnects = self.oneview_client.interconnects.get_by('interconnectIP', interconnect_ip) or []
        elif interconnect_name:
            interconnects = self.oneview_client.interconnects.get_by('name', interconnect_name) or []
        else:
            raise Exception(MISSING_KEY_MSG)

        if not interconnects:
            raise Exception(INTERCONNECT_WAS_NOT_FOUND)

        return interconnects[0]

    def change_state(self, state, resource):
        changed = False

        property_name = state['path'][1:]

        if resource[property_name] != state['value']:
            resource = self.execute_operation(resource, state['path'], state['value'])
            changed = True

        return changed, resource

    def device_reset(self, state, resource):
        updated_resource = self.execute_operation(resource, state['path'], state['value'])
        return True, updated_resource

    def execute_operation(self, resource, path, value, operation="replace"):

        return self.oneview_client.interconnects.patch(
            id_or_uri=resource["uri"],
            operation=operation,
            path=path,
            value=value
        )

    def update_ports(self, resource):
        ports = self.module.params['ports']

        if not ports:
            return False, resource

        updated_resource = self.oneview_client.interconnects.update_ports(
            id_or_uri=resource["uri"],
            ports=ports
        )

        return True, updated_resource

    def reset_port_protection(self, resource):
        updated_resource = self.oneview_client.interconnects.reset_port_protection(id_or_uri=resource['uri'])
        return True, updated_resource


def main():
    InterconnectModule().run()


if __name__ == '__main__':
    main()
