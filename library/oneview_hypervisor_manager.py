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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_hypervisor_manager
short_description: Manage OneView Hypervisor Managers resources.
description:
    - Provides an interface to manage Hypervisor Managers resources. Can create, update, and delete.
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - "hpOneView >= 5.1.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the Hypervisor Managers resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Hypervisor Managers properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Hypervisor Manager
  oneview_hypervisor_manager:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: '172.18.13.11'
      displayName: 'vcenter'
      hypervisorType: 'Vmware'
      username: 'dcs'
      password: 'dcs'

- name: Update the Hypervisor Manager display name to 'vcenter Renamed'
  oneview_hypervisor_manager:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: '172.18.13.11'
      displayName: 'vcenter Renamed'
      hypervisorType: 'Vmware'
      username: 'dcs'
      password: 'dcs'

- name: Ensure that the Hypervisor Manager is present with hypervisorType 'Vmware'
  oneview_hypervisor_manager:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: '172.18.13.11'
      hypervisorType: 'Vmware'

- name: Ensure that the Hypervisor Manager is absent
  oneview_hypervisor_manager:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      displayName: 'New hypervisor manager'
'''

RETURN = '''
hypervisor_manager:
    description: Has the facts about the managed OneView Hypervisor Manager.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class HypervisorManagerModule(OneViewModule):
    MSG_CREATED = 'Hypervisor Manager created successfully.'
    MSG_UPDATED = 'Hypervisor Manager updated successfully.'
    MSG_DELETED = 'Hypervisor Manager deleted successfully.'
    MSG_ALREADY_PRESENT = 'Hypervisor Manager is already present.'
    MSG_ALREADY_ABSENT = 'Hypervisor Manager is already absent.'
    RESOURCE_FACT_NAME = 'hypervisor_manager'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super(HypervisorManagerModule, self).__init__(additional_arg_spec=additional_arg_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.hypervisor_managers)

    def execute_module(self):
        if self.state == 'present':
            return self._present()
        elif self.state == 'absent':
            return self.resource_absent()

    def _present(self):
        scope_uris = self.data.pop('scopeUris', None)
        result = self.resource_present(self.RESOURCE_FACT_NAME)

        if scope_uris is not None:
            result = self.resource_scopes_set(result, self.RESOURCE_FACT_NAME, scope_uris)
        return result


def main():
    HypervisorManagerModule().run()


if __name__ == '__main__':
    main()
