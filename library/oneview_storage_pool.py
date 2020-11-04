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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_storage_pool
short_description: Manage OneView Storage Pool resources.
description:
    - "Provides an interface to manage Storage Pool resources. Can add and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Storage Pool resource.
              C(present) will ensure data properties are compliant with OneView.
              From API500 onwards it is only possible to update its state.
              C(absent) will remove the resource from OneView, if it exists.
              From API500 onwards absent state is immutable.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage Pool properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Storage Pool (prior to API500)
  oneview_storage_pool:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 300
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: "FST_CPG2"
  delegate_to: localhost
- name: Delete the Storage Pool (prior to API500)
  oneview_storage_pool:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 300
    state: absent
    data:
       poolName: "FST_CPG2"
  delegate_to: localhost
- name: Ensure the storage pool 'FST_CPG2' is managed by the appliance (API500 onwards)
  oneview_storage_pool:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: FST_CPG2
       isManaged: True
  delegate_to: localhost
- name: Ensure the storage pool 'FST_CPG2' is unmanaged (API500 onwards)
  oneview_storage_pool:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: FST_CPG2
       isManaged: False
  delegate_to: localhost
'''

RETURN = '''
storage_pool:
    description: Has the OneView facts about the Storage Pool.
    returned: On 'present' state, but can be null.
    type: dict
'''


from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError, OneViewModuleResourceNotFound, compare


class StoragePoolModule(OneViewModule):
    MSG_CREATED = 'Storage Pool added successfully.'
    MSG_ALREADY_PRESENT = 'Storage Pool is already present.'
    MSG_UPDATED = 'Storage Pool was updated.'
    MSG_DELETED = 'Storage Pool deleted successfully.'
    MSG_ALREADY_ABSENT = 'Storage Pool is already absent.'
    MSG_MANDATORY_FIELD_MISSING = "Mandatory field was not informed:" \
                                  " data.poolName (prior to API500) or data.name (API500 onwards)"
    MSG_RESOURCE_NOT_FOUND = "The resource was not found. It is not possible to add it in API500 onwards." \
                             "The addition of Storage Pools can only be performed once through the Storage Systems."
    MSG_RESOURCE_FOUND = "The resource was found. It is not possible to remove it in API500 onwards." \
                         "The addition of Storage Pools can only be performed once through the Storage Systems."

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent']
            ),
            data=dict(required=True, type='dict')
        )

        super(StoragePoolModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.storage_pools)

    def execute_module(self):

        if not self.data.get("poolName") and not self.data.get("name"):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING)

        if self.data.get("poolName"):
            self.current_resource = self.resource_client.get_by_name(self.data.get("poolName"))

        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.__absent()

    def __present(self):
        changed = False
        msg = self.MSG_ALREADY_PRESENT

        if not self.current_resource:
            if self.oneview_client.api_version >= 500:
                raise OneViewModuleResourceNotFound(self.MSG_RESOURCE_NOT_FOUND)
            else:
                self.current_resource = self.resource_client.add(self.data)
                changed = True
                msg = self.MSG_CREATED
        else:
            merged_data = self.current_resource.data.copy()
            merged_data.update(self.data)

            if compare(self.current_resource.data, merged_data):
                changed = False
                msg = self.MSG_ALREADY_PRESENT
            else:
                self.current_resource.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED

        return dict(changed=changed, msg=msg, ansible_facts=dict(storage_pool=self.current_resource.data))

    def __absent(self):
        if self.oneview_client.api_version >= 500:
            if self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_RESOURCE_FOUND)
            else:
                return dict(changed=False, msg=self.MSG_ALREADY_ABSENT, ansible_facts=dict(storage_pool=None))
        else:
            return self.resource_absent('remove')


def main():
    StoragePoolModule().run()


if __name__ == '__main__':
    main()
