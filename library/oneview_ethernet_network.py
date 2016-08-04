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
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
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

- name: Create Ethernet networks in bulk
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      vlanIdRange: '1-10,15,17'
      purpose: General
      namePrefix: TestNetwork
      smartLink: false
      privateNetwork: false
      bandwidth:
        maximumBandwidth: 10000
        typicalBandwidth: 2000
'''

ETHERNET_NETWORK_CREATED = 'Ethernet Network created successfully.'
ETHERNET_NETWORK_UPDATED = 'Ethernet Network updated successfully.'
ETHERNET_NETWORK_DELETED = 'Ethernet Network deleted successfully.'
ETHERNET_NETWORK_ALREADY_EXIST = 'Ethernet Network already exists.'
ETHERNET_NETWORK_ALREADY_ABSENT = 'Nothing to do.'
ETHERNET_NETWORKS_CREATED = 'Ethernet Networks created successfully.'
MISSING_ETHERNET_NETWORKS_CREATED = 'Some missing Ethernet Networks were created successfully.'
ETHERNET_NETWORKS_ALREADY_EXIST = 'The specified Ethernet Networks already exist.'


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
                if data.get('vlanIdRange'):
                    self.__bulk_present(data)
                else:
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

    def __bulk_present(self, data):
        existent_enets = self.oneview_client.ethernet_networks.get_range(data['namePrefix'], data['vlanIdRange'])
        vlan_id_range = data['vlanIdRange']

        if not existent_enets:
            new_ethernet_networks = self.oneview_client.ethernet_networks.create_bulk(data)
            self.module.exit_json(changed=True, msg=ETHERNET_NETWORKS_CREATED,
                                  ansible_facts=dict(oneview_enet_bulk=new_ethernet_networks))
        else:
            vlan_ids = self.oneview_client.ethernet_networks.dissociate_values_or_ranges(vlan_id_range)
            for net in existent_enets[:]:
                vlan_ids.remove(net['vlanId'])

            if len(vlan_ids) == 0:
                self.module.exit_json(changed=False, msg=ETHERNET_NETWORKS_ALREADY_EXIST,
                                      ansible_facts=dict(oneview_enet_bulk=existent_enets))
            else:
                if len(vlan_ids) == 1:
                    data['vlanIdRange'] = '{0}-{1}'.format(vlan_ids[0], vlan_ids[0])
                else:
                    data['vlanIdRange'] = ','.join(map(str, vlan_ids))

                self.oneview_client.ethernet_networks.create_bulk(data)
                enets = self.oneview_client.ethernet_networks.get_range(data['namePrefix'], vlan_id_range)
                self.module.exit_json(changed=True, msg=MISSING_ETHERNET_NETWORKS_CREATED,
                                      ansible_facts=dict(oneview_enet_bulk=enets))

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
