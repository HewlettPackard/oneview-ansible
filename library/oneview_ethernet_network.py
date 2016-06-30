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
module: oneview_ethernet_network
short_description: Manage OneView Ethernet Network resources.
description:
    - Provides an interface to manage Ethernet Network resources. Can create, update, or delete.
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
            - Indicates the desired state for the Ethernet Network resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with Ethernet Network properties
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Ensure that the Ethernet Network is present using the default configuration
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      vlanId: '201'

- name: Ensure that the Logical Interconnect Group is present with name 'Renamed Ethernet Network'
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      newName: 'Renamed Ethernet Network'

- name: Ensure that the Ethernet Network is absent
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New Ethernet Network'
'''

ETHERNET_NETWORK_CREATED = 'Ethernet Network created sucessfully.'
ETHERNET_NETWORK_UPDATED = 'Ethernet Network updated sucessfully.'
ETHERNET_NETWORK_DELETED = 'Ethernet Network deleted sucessfully.'
ETHERNET_NETWORK_ALREADY_EXIST = 'Ethernet Network already exists.'
ETHERNET_NETWORK_ALREADY_ABSENT = 'Nothing to do.'


class EthernetNetworkModule(object):
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
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

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
            self.oneview_client.ethernet_networks.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=ETHERNET_NETWORK_DELETED)
        else:
            self.module.exit_json(changed=False, msg=ETHERNET_NETWORK_ALREADY_ABSENT)

    def __create(self, data):
        new_ethernet_network = self.oneview_client.ethernet_networks.create(data)

        self.module.exit_json(changed=True,
                              msg=ETHERNET_NETWORK_CREATED,
                              ansible_facts=dict(ethernet_network=new_ethernet_network))

    def __update(self, new_data, existent_resource):
        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if resource_compare(existent_resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=ETHERNET_NETWORK_ALREADY_EXIST,
                                  ansible_facts=dict(ethernet_network=existent_resource))

        else:
            updated_ethernet_network = self.oneview_client.ethernet_networks.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=ETHERNET_NETWORK_UPDATED,
                                  ansible_facts=dict(ethernet_network=updated_ethernet_network))

    def __get_by_name(self, data):
        result = self.oneview_client.ethernet_networks.get_by('name', data['name'])
        return result[0] if result else None


def main():
    EthernetNetworkModule().run()


if __name__ == '__main__':
    main()
