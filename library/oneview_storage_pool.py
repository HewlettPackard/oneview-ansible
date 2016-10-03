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

DOCUMENTATION = '''
---
module: oneview_storage_pool
short_description: Manage OneView Storage Pool resources.
description:
    - "Provides an interface to manage Storage Pool resources. Can add and remove."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Storage Pool resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage Pool properties and its associated states
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Create a Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: "FST_CPG2"
  delegate_to: localhost

- name: Delete the Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: absent
    data:
       poolName: "FST_CPG2"
  delegate_to: localhost
'''

RETURN = '''
storage_pool:
    description: Has the OneView facts about the Storage Pool.
    returned: on 'present' state, but can be null
    type: complex
'''

STORAGE_POOL_ADDED = 'Storage Pool added successfully.'
STORAGE_POOL_ALREADY_ADDED = 'Storage Pool is already present.'
STORAGE_POOL_DELETED = 'Storage Pool deleted successfully.'
STORAGE_POOL_ALREADY_ABSENT = 'Storage Pool is already absent.'
STORAGE_POOL_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: data.poolName"


class StoragePoolModule(object):
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

            if not data.get('poolName'):
                raise Exception(STORAGE_POOL_MANDATORY_FIELD_MISSING)

            resource = (self.oneview_client.storage_pools.get_by("name", data['poolName']) or [None])[0]

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __present(self, data, resource):

        changed = False
        msg = ''

        if not resource:
            resource = self.oneview_client.storage_pools.add(data)
            changed = True
            msg = STORAGE_POOL_ADDED
        else:
            msg = STORAGE_POOL_ALREADY_ADDED

        return changed, msg, dict(storage_pool=resource)

    def __absent(self, resource):
        if resource:
            self.oneview_client.storage_pools.remove(resource)
            return True, STORAGE_POOL_DELETED, {}
        else:
            return False, STORAGE_POOL_ALREADY_ABSENT, {}


def main():
    StoragePoolModule().run()


if __name__ == '__main__':
    main()
