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
module: oneview_fcoe_network
short_description: Manage OneView FCoE Network resources.
description:
    - Provides an interface to manage FCoE Network resources. Can create, update, or delete.
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
            - Indicates the desired state for the FCoE Network resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with FCoE Network properties
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Ensure that FCoE Network is present using the default configuration
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test FCoE Network'
      vlanId: '201'

- name: Ensure that FCoE Network is absent
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FCoE Network'
'''

RETURN = '''
fcoe_network:
    description: Has the facts about the OneView FCoE Networks.
    returned: on state 'present'. Can be null.
    type: complex
'''

FCOE_NETWORK_CREATED = 'FCoE Network created successfully.'
FCOE_NETWORK_UPDATED = 'FCoE Network updated successfully.'
FCOE_NETWORK_DELETED = 'FCoE Network deleted successfully.'
FCOE_NETWORK_ALREADY_EXIST = 'FCoE Network already exists.'
FCOE_NETWORK_ALREADY_ABSENT = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class FcoeNetworkModule(object):
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
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data)

        if "newName" in data:
            data["name"] = data["newName"]
            del data["newName"]

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.fcoe_networks.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=FCOE_NETWORK_DELETED)
        else:
            self.module.exit_json(changed=False, msg=FCOE_NETWORK_ALREADY_ABSENT)

    def __create(self, data):
        new_fcoe_network = self.oneview_client.fcoe_networks.create(data)

        self.module.exit_json(changed=True,
                              msg=FCOE_NETWORK_CREATED,
                              ansible_facts=dict(fcoe_network=new_fcoe_network))

    def __update(self, new_data, existent_resource):
        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if resource_compare(existent_resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=FCOE_NETWORK_ALREADY_EXIST,
                                  ansible_facts=dict(fcoe_network=existent_resource))

        else:
            updated_fcoe_network = self.oneview_client.fcoe_networks.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=FCOE_NETWORK_UPDATED,
                                  ansible_facts=dict(fcoe_network=updated_fcoe_network))

    def __get_by_name(self, data):
        result = self.oneview_client.fcoe_networks.get_by('name', data['name'])
        return result[0] if result else None


def main():
    FcoeNetworkModule().run()


if __name__ == '__main__':
    main()
