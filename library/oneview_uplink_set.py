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
try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_uplink_set
short_description: Manage OneView Uplink Set resources.
description:
    - Provides an interface to manage Uplink Set resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Uplink Set resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
              The key used to find the resource to perform the operation is a compound key, that consists of
              the name of the uplink set and the URI (or name) of the Logical Interconnect combined. You can choose to
              set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName.
        choices: ['present', 'absent']
    data:
      description:
        - List with Uplink Set properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
      # You can choose set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName
      logicalInterconnectName: "Name of the Logical Interconnect"                                   # option 1
      # logicalInterconnectUri: "/rest/logical-interconnects/461a9cef-beef-4916-8be1-926078ffb948"  # option 2
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
      logicalInterconnectName: "Name of the Logical Interconnect"

- name: Ensure that the Uplink Set is absent
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test Uplink Set'
      logicalInterconnectName: "Name of the Logical Interconnect"
'''

RETURN = '''
uplink_set:
    description: Has the OneView facts about the Uplink Set.
    returned: On state 'present'. Can be null.
    type: complex
'''

UPLINK_SET_KEY_REQUIRED = "Uplink Set Name and Logical Interconnect required."
UPLINK_SET_CREATED = 'Uplink Set created successfully.'
UPLINK_SET_UPDATED = 'Uplink Set updated successfully.'
UPLINK_SET_DELETED = 'Uplink Set deleted successfully.'
UPLINK_SET_ALREADY_EXIST = 'Uplink Set already exists.'
UPLINK_SET_ALREADY_ABSENT = 'Nothing to do.'
UPLINK_SET_LOGICAL_INTERCONNECT_NOT_FOUND = "Logical Interconnect not found."
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class UplinkSetModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data'].copy()

        try:
            self.__validate_key(data)
            self.__replace_logical_interconnect_name_by_uri(data)

            if state == 'present':
                changed, message, resource = self.__present(data)
                self.module.exit_json(changed=changed, msg=message, ansible_facts=dict(uplink_set=resource))
            elif state == 'absent':
                changed, message = self.__absent(data)
                self.module.exit_json(changed=changed, msg=message)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __absent(self, data):
        resource = self.__get_by(data['name'], data['logicalInterconnectUri'])

        if resource:
            self.oneview_client.uplink_sets.delete(resource)
            return True, UPLINK_SET_DELETED
        else:
            return False, UPLINK_SET_ALREADY_ABSENT

    def __present(self, data):
        resource = self.__get_by(data['name'], data['logicalInterconnectUri'])

        if not resource:
            return self.__create(data)
        else:
            return self.__update(data, resource)

    def __create(self, data):
        new_uplink_set = self.oneview_client.uplink_sets.create(data)
        return True, UPLINK_SET_CREATED, new_uplink_set

    def __update(self, data, existent_resource):
        if 'newName' in data:
            data['name'] = data.pop('newName')

        resource_to_update = existent_resource.copy()
        resource_to_update.update(data)

        if resource_compare(existent_resource, resource_to_update):
            return False, UPLINK_SET_ALREADY_EXIST, existent_resource
        else:
            updated_uplink = self.oneview_client.uplink_sets.update(resource_to_update)
            return True, UPLINK_SET_UPDATED, updated_uplink

    def __validate_key(self, data):
        if 'name' not in data:
            raise Exception(UPLINK_SET_KEY_REQUIRED)
        if 'logicalInterconnectUri' not in data and 'logicalInterconnectName' not in data:
            raise Exception(UPLINK_SET_KEY_REQUIRED)

    def __replace_logical_interconnect_name_by_uri(self, data):
        if 'logicalInterconnectName' in data:
            name = data['logicalInterconnectName']
            logical_interconnect = self.oneview_client.logical_interconnects.get_by_name(name)

            if logical_interconnect:
                del data['logicalInterconnectName']
                data['logicalInterconnectUri'] = logical_interconnect['uri']
            else:
                raise Exception(UPLINK_SET_LOGICAL_INTERCONNECT_NOT_FOUND)

    def __get_by(self, name, logical_interconnect_uri):
        uplink_sets = self.oneview_client.uplink_sets.get_by('name', name)
        uplink_sets = [x for x in uplink_sets if x['logicalInterconnectUri'] == logical_interconnect_uri]
        return uplink_sets[0] if uplink_sets else None


def main():
    UplinkSetModule().run()


if __name__ == '__main__':
    main()
