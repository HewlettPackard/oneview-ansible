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


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_switch
short_description: Provides an interface to remove ToR Switch resources.
description:
    - Provides an interface to remove Top of Rack(ToR) Switch resources.
      The switch resource will be removed if it is in an unmanaged state.
      If the switch resource is associated with a Logical Switch, its removal is treated as a hardware removal only.
      A reference to the switch is mantained, and the resource is marked as 'Absent'.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Switch resource.
              C(present) will update the switch scopes, if they differ from what is declared.
              C(absent) will remove the resource from OneView, if it exists.
              C(ports_updated) will update the switch ports.
        choices: ['present','absent', 'ports_updated']
    name:
      description:
        - Switch name.
      required: true

notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Delete the Switch
  oneview_switch:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    name: "172.18.16.2"
'''

RETURN = ''' # '''

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleResourceNotFound


class SwitchModule(OneViewModuleBase):
    MSG_DELETED = 'Switch deleted successfully.'
    MSG_ALREADY_ABSENT = 'Switch is already absent.'
    MSG_ALREADY_PRESENT = 'Switch is already present.'
    MSG_PORTS_UPDATED = "Switch ports updated successfully."
    MSG_NOT_FOUND = 'Switch not found.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent', 'ports_updated']
            ),
            data=dict(required=False, type='dict'),
            name=dict(required=True, type='str'),
        )
        super(SwitchModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.switches

    def execute_module(self):
        resource = self.get_by_name(self.module.params.get('name'))

        if self.state == 'absent':
            return self.resource_absent(resource)

        if not resource:
            raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)
        else:
            if self.state == 'present':
                return self.__present(resource)
            elif self.state == 'ports_updated':
                return self.__update_ports(resource)

    def __present(self, resource):
        scope_uris = self.data.pop('scopeUris', None)
        result = dict(
            msg=self.MSG_ALREADY_PRESENT,
            changed=False,
            ansible_facts={'switch': resource}
        )
        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'switch', scope_uris)
        return result

    def __update_ports(self, resource):
        self.resource_client.update_ports(id_or_uri=resource["uri"], ports=self.data.get('ports'))
        return dict(changed=True, msg=self.MSG_PORTS_UPDATED)


def main():
    SwitchModule().run()


if __name__ == '__main__':
    main()
