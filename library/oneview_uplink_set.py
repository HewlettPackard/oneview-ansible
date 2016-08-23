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
from hpOneView.common import resource_compare

DOCUMENTATION = '''
---
module: oneview_uplink_set
short_description: Manage OneView Uplink Set resources.
description:
    - Provides an interface to manage Uplink Set resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Uplink Set resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with Uplink Set properties
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
    - "To rename an uplink set you must inform a 'newName' in the data argument. The rename is non-idempotent"
'''

EXAMPLES = '''
- name: Ensure that the Uplink Set is present
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Uplink Set'
      status: "OK"
      logicalInterconnectUri: "/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66"
      networkUris: [
         '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4'
         '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
      ]
      fcNetworkUris: []
      fcoeNetworkUris: []
      portConfigInfos: []
      connectionMode: "Auto"
      networkType: "Ethernet"
      manualLoginRedistributionState: "NotSupported"

- name: Rename the Uplink Set from 'Test Uplink Set' to 'Renamed Uplink Set'
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Uplink Set'
      newName: 'Renamed Uplink Set'

- name: Ensure that the Uplink Set is absent
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test Uplink Set'
'''

RETURN = '''
uplink_set:
    description: Has the OneView facts about the Uplink Set.
    returned: on state 'present'. Can be null.
    type: complex
'''

UPLINK_SET_CREATED = 'Uplink Set created successfully.'
UPLINK_SET_UPDATED = 'Uplink Set updated successfully.'
UPLINK_SET_DELETED = 'Uplink Set deleted successfully.'
UPLINK_SET_ALREADY_EXIST = 'Uplink Set already exists.'
UPLINK_SET_ALREADY_ABSENT = 'Nothing to do.'
UPLINK_SET_NOT_EXIST = 'Rename failed: Uplink Set not found.'
UPLINK_SET_NEW_NAME_INVALID = 'Rename failed: the new name is being used by another Uplink Set.'


class UplinkSetModule(object):
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
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            if state == 'present':
                changed, message, resource = self.__present(data)
                self.module.exit_json(changed=changed, msg=message, ansible_facts=dict(uplink_set=resource))
            elif state == 'absent':
                changed, message = self.__absent(data)
                self.module.exit_json(changed=changed, msg=message)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __absent(self, data):
        resource = self.__get_by_name(data['name'])

        if resource:
            self.oneview_client.uplink_sets.delete(resource)
            return True, UPLINK_SET_DELETED
        else:
            return False, UPLINK_SET_ALREADY_ABSENT

    def __present(self, data):
        resource = self.__get_by_name(data['name'])

        if data.get('newName'):
            return self.__rename(data, resource)
        else:
            if not resource:
                return self.__create(data)
            else:
                return self.__update(data, resource)

    def __rename(self, data, resource):
        resource_new_name = self.__get_by_name(data.get('newName'))
        if not resource:
            self.module.exit_json(changed=False, msg=UPLINK_SET_NOT_EXIST)
        elif resource_new_name:
            self.module.exit_json(changed=False, msg=UPLINK_SET_NEW_NAME_INVALID)
        else:
            data["name"] = data.pop("newName")
            return self.__update(data, resource)

    def __create(self, data):
        new_uplink_set = self.oneview_client.uplink_sets.create(data)
        return True, UPLINK_SET_CREATED, new_uplink_set

    def __update(self, new_data, existent_resource):
        resource_to_update = existent_resource.copy()
        resource_to_update.update(new_data)

        if resource_compare(existent_resource, resource_to_update):
            return False, UPLINK_SET_ALREADY_EXIST, existent_resource

        else:
            updated_uplink = self.oneview_client.uplink_sets.update(resource_to_update)
            return True, UPLINK_SET_UPDATED, updated_uplink

    def __get_by_name(self, name):
        result = self.oneview_client.uplink_sets.get_by('name', name)
        return result[0] if result else None


def main():
    UplinkSetModule().run()


if __name__ == '__main__':
    main()
