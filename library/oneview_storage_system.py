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
- name: Add a Storage System with one managed pool (before API500)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
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
    api_version: 600
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

- name: Remove the storage system by its IP (before API500)
  oneview_storage_system:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
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
    api_version: 600
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

from ansible.module_utils.oneview import OneViewModuleBase, OneViewModuleValueError, compare


class StorageSystemModule(OneViewModuleBase):
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

        self.resource_client = self.oneview_client.storage_systems

    def execute_module(self):
        if self.oneview_client.api_version < 500:
            resource = self.__get_resource_hostname('ip_hostname', 'newIp_hostname')
        else:
            resource = self.__get_resource_hostname('hostname', 'newHostname')

        if self.state == 'present':
            return self.__present(resource)
        elif self.state == 'absent':
            return self.resource_absent(resource, 'remove')

    def __present(self, resource):
        changed = False
        msg = ''

        if not resource:
            if 'credentials' not in self.data:
                raise OneViewModuleValueError(self.MSG_CREDENTIALS_MANDATORY)
            if self.oneview_client.api_version < 500:
                resource = self.oneview_client.storage_systems.add(self.data['credentials'])
            else:
                options = self.data['credentials'].copy()
                options['family'] = self.data.get('family', None)
                options['hostname'] = self.data.get('hostname', None)
                resource = self.oneview_client.storage_systems.add(options)

            changed = True
            msg = self.MSG_ADDED

        merged_data = resource.copy()
        merged_data.update(self.data)

        # remove password, it cannot be used in comparison
        if 'credentials' in merged_data and 'password' in merged_data['credentials']:
            del merged_data['credentials']['password']

        if not compare(resource, merged_data):
            # update the resource
            resource = self.oneview_client.storage_systems.update(merged_data)
            if not changed:
                changed = True
                msg = self.MSG_UPDATED
        else:
            msg = self.MSG_ALREADY_PRESENT

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(storage_system=resource))

    def __get_resource_hostname(self, hostname_key, new_hostname_key):
        hostname = self.data.get(hostname_key, None)
        if 'credentials' in self.data and hostname is None:
            hostname = self.data['credentials'].get(hostname_key, None)
        if hostname:
            get_method = getattr(self.oneview_client.storage_systems, "get_by_{}".format(hostname_key))
            resource = get_method(hostname)
            if self.data['credentials'].get(new_hostname_key):
                self.data['credentials'][hostname_key] = self.data['credentials'].pop(new_hostname_key)
            elif self.data.get(new_hostname_key):
                self.data[hostname_key] = self.data.pop(new_hostname_key)
            return resource
        elif self.data.get('name'):
            return self.oneview_client.storage_systems.get_by_name(self.data['name'])
        else:
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELDS_MISSING)


def main():
    StorageSystemModule().run()


if __name__ == '__main__':
    main()
