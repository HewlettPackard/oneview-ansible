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
module: oneview_storage_system
short_description: Manage OneView Storage System resources.
description:
    - Provides an interface to manage Storage System resources. Can add, update and remove.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Storage System resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage System properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Storage System with one managed pool
  oneview_storage_system:
    config: "{{ config }}"
    state: present
    data:
        credentials:
            ip_hostname: '{{ storage_system_ip_hostname }}'
            username: '{{ storage_system_username }}'
            password: '{{ storage_system_password }}'
        managedDomain: TestDomain
        managedPools:
          - domain: TestDomain
            type: StoragePoolV2
            name: CPG_FC-AO
            deviceType: FC

  delegate_to: localhost

- name: Remove the storage system by its IP
  oneview_storage_system:
    config: "{{ config }}"
    state: absent
    data:
        credentials:
            ip_hostname: 172.18.11.12
  delegate_to: localhost
'''

RETURN = '''
storage_system:
    description: Has the OneView facts about the Storage System.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewValueError, ResourceComparator


class StorageSystemModule(OneViewModuleBase):
    MSG_ADDED = 'Storage System added successfully.'
    MSG_UPDATED = 'Storage System updated successfully.'
    MSG_ALREADY_UPDATED = 'Storage System is already updated.'
    MSG_DELETED = 'Storage System deleted successfully.'
    MSG_ALREADY_ABSENT = 'Storage System is already absent.'
    MSG_MANDATORY_FIELDS_MISSING = 'At least one mandatory field must be provided: name or credentials.ip_hostname.'
    MSG_CREDENTIALS_MANDATORY = "The attribute 'credentials' is mandatory for Storage System creation."

    def __init__(self):

        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent']
            ),
            data=dict(required=True, type='dict')
        )
        super(StorageSystemModule, self).__init__(additional_arg_spec=argument_spec,
                                                  validate_etag_support=True)

        self.resource_client = self.oneview_client.storage_systems

    def execute_module(self):
        resource = self.__get_resource()

        if self.state == 'present':
            return self.__present(resource)
        elif self.state == 'absent':
            return self.resource_absent(resource, 'remove')

    def __present(self, resource):

        changed = False
        msg = ''

        if not resource:
            if 'credentials' not in self.data:
                raise HPOneViewValueError(self.MSG_CREDENTIALS_MANDATORY)
            resource = self.oneview_client.storage_systems.add(self.data['credentials'])
            changed = True
            msg = self.MSG_ADDED

        merged_data = resource.copy()
        merged_data.update(self.data)

        if 'credentials' in merged_data and 'password' in merged_data['credentials']:
            # remove password, it cannot be used in comparison
            del merged_data['credentials']['password']

        if not ResourceComparator.compare(resource, merged_data):
            # update the resource
            resource = self.oneview_client.storage_systems.update(merged_data)
            if not changed:
                changed = True
                msg = self.MSG_UPDATED
        else:
            msg = self.MSG_ALREADY_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(storage_system=resource))

    def __get_resource(self):
        if 'credentials' in self.data and self.data['credentials'].get('ip_hostname'):
            resource = self.oneview_client.storage_systems.get_by_ip_hostname(self.data['credentials']['ip_hostname'])

            if self.data['credentials'].get('newIp_hostname'):
                self.data['credentials']['ip_hostname'] = self.data['credentials'].pop('newIp_hostname')

            return resource
        elif self.data.get('name'):
            return self.oneview_client.storage_systems.get_by_name(self.data['name'])
        else:
            raise HPOneViewValueError(self.MSG_MANDATORY_FIELDS_MISSING)


def main():
    StorageSystemModule().run()


if __name__ == '__main__':
    main()
