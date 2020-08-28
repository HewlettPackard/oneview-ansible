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
module: oneview_storage_system
short_description: Manage OneView Storage System resources.
description:
    - Provides an interface to manage Storage System resources. Can add, update and remove.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
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
- name: Add a Storage System with one managed pool (before API500)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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

- name: Add a StoreServ Storage System with one managed pool (API500 onwards)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      credentials:
          username: '{{ storage_system_username }}'
          password: '{{ storage_system_password }}'
      hostname: '{{ storage_system_ip }}'
      family: StoreServ
      deviceSpecificAttributes:
          managedDomain: TestDomain
          managedPools:
              - domain: TestDomain
                type: StoragePoolV2
                name: CPG_FC-AO
                deviceType: FC

  delegate_to: localhost

- name: Update the Storage System adding one port using name as key
  oneview_storage_system:
    state: present
    data:
      credentials:
        username: '{{ storage_system_username }}'
        password: '{{ storage_system_password }}'
    name: '{{ storage_system_name }}'
    family: StoreServ
    hostname: '{{ storage_system_ip }}'
    ports:
      - expectedNetworkUri: '/rest/fc-networks/9141498a-9616-4512-b683-a8848be039c3'
        name: 0:1:2
        mode: Managed

  delegate_to: localhost

- name: Remove the storage system by its IP (before API500)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
        credentials:
            ip_hostname: 172.18.11.12
  delegate_to: localhost

- name: Remove the storage system by its IP (API500 onwards)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
        credentials:
            hostname: 172.18.11.12
  delegate_to: localhost
'''

RETURN = '''
storage_system:
    description: Has the OneView facts about the Storage System.
    returned: On state 'present'. Can be null.
    type: dict
'''

import collections
from copy import deepcopy
from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError, compare, dict_merge


class StorageSystemModule(OneViewModule):
    MSG_ADDED = 'Storage System added successfully.'
    MSG_UPDATED = 'Storage System updated successfully.'
    MSG_ALREADY_PRESENT = 'Storage System is already present.'
    MSG_DELETED = 'Storage System deleted successfully.'
    MSG_ALREADY_ABSENT = 'Storage System is already absent.'
    MSG_MANDATORY_FIELDS_MISSING = "At least one mandatory field must be provided: name or credentials.hostname" \
                                   "(credentials.ip_hostname if API version lower than 500 )."
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
        self.set_resource_object(self.oneview_client.storage_systems)

    def execute_module(self):
        if self.oneview_client.api_version < 500:
            self.__get_resource_hostname('ip_hostname', 'newIp_hostname')
        else:
            self.__get_resource_hostname('hostname', 'newHostname')

        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent('remove')

    def __present(self):
        changed = False
        msg = ''

        if not self.current_resource:
            if 'credentials' not in self.data:
                raise OneViewModuleValueError(self.MSG_CREDENTIALS_MANDATORY)

            if self.oneview_client.api_version < 500:
                self.current_resource = self.resource_client.add(self.data['credentials'])
            else:
                options = self.data['credentials'].copy()
                options['family'] = self.data.get('family', None)
                options['hostname'] = self.data.get('hostname', None)
                self.current_resource = self.resource_client.add(options)

            changed = True
            msg = self.MSG_ADDED

        else:
            resource = deepcopy(self.current_resource.data)
            data = self.data.copy()
            merged_data = dict_merge(resource, data)
            temp_list = []
            merged_data_copy = deepcopy(merged_data)
            if merged_data_copy.get('deviceSpecificAttributes') and merged_data_copy.get('deviceSpecificAttributes').get('discoveredPools') and \
                    merged_data_copy.get('deviceSpecificAttributes').get('managedPools'):
                for discoveredPool in merged_data_copy['deviceSpecificAttributes']['discoveredPools']:
                    for managedPool in merged_data['deviceSpecificAttributes']['managedPools']:
                        if discoveredPool['name'] == managedPool['name']:
                            temp_list.append(discoveredPool)
                            merged_data['deviceSpecificAttributes']['discoveredPools'].remove(discoveredPool)
                merged_data['deviceSpecificAttributes']['managedPools'] = temp_list

            # remove password, it cannot be used in comparison
            if 'credentials' in merged_data and 'password' in merged_data['credentials']:
                del merged_data['credentials']['password']

            if not compare(self.current_resource.data, merged_data):
                # update the resource
                self.current_resource.update(merged_data)
                # if not changed:
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(storage_system=self.current_resource.data))

    def __get_resource_hostname(self, hostname_key, new_hostname_key):
        hostname = self.data.get(hostname_key, None)
        if 'credentials' in self.data and hostname is None:
            hostname = self.data['credentials'].get(hostname_key, None)

        if hostname:
            get_method = getattr(self.oneview_client.storage_systems, "get_by_{}".format(hostname_key))
            self.current_resource = get_method(hostname)

            if self.data['credentials'].get(new_hostname_key):
                self.data['credentials'][hostname_key] = self.data['credentials'].pop(new_hostname_key)
            elif self.data.get(new_hostname_key):
                self.data[hostname_key] = self.data.pop(new_hostname_key)

        if not hostname and not self.data.get("name"):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELDS_MISSING)


def main():
    StorageSystemModule().run()


if __name__ == '__main__':
    main()
