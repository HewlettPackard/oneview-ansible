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
from hpOneView.common import resource_compare
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_storage_system
short_description: Manage OneView Storage System resources.
description:
    - Provides an interface to manage Storage System resources. Can add, update and remove.
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
            - Indicates the desired state for the Storage System resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage System properties and its associated states
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
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

STORAGE_SYSTEM_ADDED = 'Storage System added successfully.'
STORAGE_SYSTEM_UPDATED = 'Storage System updated successfully.'
STORAGE_SYSTEM_ALREADY_UPDATED = 'Storage System is already updated.'
STORAGE_SYSTEM_DELETED = 'Storage System deleted successfully.'
STORAGE_SYSTEM_ALREADY_ABSENT = 'Storage System is already absent.'
STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING = \
    'At least one mandatory field must be provided: name or credentials.ip_hostname.'


class StorageSystemModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
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

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(data)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __present(self, data):
        resource = self.__get_resource(data)
        changed = False
        msg = ''

        if not resource:
            resource = self.oneview_client.storage_systems.add(data['credentials'])
            changed = True
            msg = STORAGE_SYSTEM_ADDED

        merged_data = resource.copy()
        merged_data.update(data)

        if 'credentials' in merged_data and 'password' in merged_data['credentials']:
            # remove password, it cannot be used in comparison
            del merged_data['credentials']['password']

        if not resource_compare(resource, merged_data):
            # update the resource
            resource = self.oneview_client.storage_systems.update(merged_data)
            if not changed:
                changed = True
                msg = STORAGE_SYSTEM_UPDATED
        else:
            msg = STORAGE_SYSTEM_ALREADY_UPDATED

        return changed, msg, dict(oneview_storage_system=resource)

    def __absent(self, data):
        resource = self.__get_resource(data)

        if resource:
            self.oneview_client.storage_systems.remove(resource)
            return True, STORAGE_SYSTEM_DELETED, {}
        else:
            return False, STORAGE_SYSTEM_ALREADY_ABSENT, {}

    def __get_resource(self, data):
        if 'credentials' in data and data['credentials'].get('ip_hostname'):
            resource = self.oneview_client.storage_systems.get_by_ip_hostname(data['credentials']['ip_hostname'])

            if data['credentials'].get('newIp_hostname'):
                data['credentials']['ip_hostname'] = data['credentials'].pop('newIp_hostname')

            return resource
        elif data.get('name'):
            return self.oneview_client.storage_systems.get_by_name(data['name'])
        else:
            raise Exception(STORAGE_SYSTEM_MANDATORY_FIELDS_MISSING)


def main():
    StorageSystemModule().run()


if __name__ == '__main__':
    main()
