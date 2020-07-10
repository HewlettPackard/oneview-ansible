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
module: oneview_ethernet_network
short_description: Manage OneView Ethernet Network resources.
description:
    - Provides an interface to manage Ethernet Network resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Ethernet Network resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(default_bandwidth_reset) will reset the network connection template to the default.
        choices: ['present', 'absent', 'default_bandwidth_reset']
    data:
        description:
            - List with Ethernet Network properties.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the Ethernet Network is present using the default configuration
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: present
    data:
      name: 'Test Ethernet Network'
      vlanId: '201'

- name: Update the Ethernet Network changing bandwidth and purpose
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: present
    data:
      name: 'Test Ethernet Network'
      purpose: Management
      bandwidth:
          maximumBandwidth: 3000
          typicalBandwidth: 2000
  delegate_to: localhost

- name: Ensure that the Ethernet Network is present with name 'Renamed Ethernet Network'
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: present
    data:
      name: 'Test Ethernet Network'
      newName: 'Renamed Ethernet Network'

- name: Ensure that the Ethernet Network is absent
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: absent
    data:
      name: 'New Ethernet Network'

- name: Create Ethernet networks in bulk
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
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

- name: Reset to the default network connection template
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: default_bandwidth_reset
    data:
      name: 'Test Ethernet Network'
  delegate_to: localhost

- name: Update the ethernet network scopes
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: present
    data:
      name: 'Test Ethernet Network'
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'
  delegate_to: localhost

- name: Delete Ethernet Networks in bulk(works from API1600)
  oneview_ethernet_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: absent
    data:
      networkUris:
        -  "/rest/ethernet-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548"
  delegate_to: localhost
'''

RETURN = '''
ethernet_network:
    description: Has the facts about the Ethernet Networks.
    returned: On state 'present'. Can be null.
    type: dict

ethernet_network_bulk:
    description: Has the facts about the Ethernet Networks affected by the bulk insert.
    returned: When 'vlanIdRange' attribute is in data argument. Can be null.
    type: dict

ethernet_network_connection_template:
    description: Has the facts about the Ethernet Network Connection Template.
    returned: On state 'default_bandwidth_reset'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, compare


class EthernetNetworkModule(OneViewModule):
    MSG_CREATED = 'Ethernet Network created successfully.'
    MSG_UPDATED = 'Ethernet Network updated successfully.'
    MSG_DELETED = 'Ethernet Network deleted successfully.'
    MSG_ALREADY_PRESENT = 'Ethernet Network is already present.'
    MSG_ALREADY_ABSENT = 'Ethernet Network is already absent.'

    MSG_BULK_CREATED = 'Ethernet Networks created successfully.'
    MSG_BULK_DELETED = 'Ethernet Networks deleted successfully.'
    MSG_MISSING_BULK_CREATED = 'Some missing Ethernet Networks were created successfully.'
    MSG_BULK_ALREADY_EXIST = 'The specified Ethernet Networks already exist.'
    MSG_CONNECTION_TEMPLATE_RESET = 'Ethernet Network connection template was reset to the default.'
    MSG_ETHERNET_NETWORK_NOT_FOUND = 'Ethernet Network was not found.'

    RESOURCE_FACT_NAME = 'ethernet_network'

    def __init__(self):

        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent', 'default_bandwidth_reset']
            ),
            data=dict(required=True, type='dict'),
        )

        super(EthernetNetworkModule, self).__init__(additional_arg_spec=argument_spec, validate_etag_support=True)

        self.set_resource_object(self.oneview_client.ethernet_networks)
        self.connection_templates = self.oneview_client.connection_templates

    def execute_module(self):

        changed, msg, ansible_facts = False, '', {}

        if self.state == 'present':
            if self.data.get('vlanIdRange'):
                changed, msg, ansible_facts = self.__bulk_present()
            else:
                return self.__present()
        elif self.state == 'absent':
            if self.data.get('networkUris'):
                changed, msg, ansible_facts = self.__bulk_absent()
            else:
                return self.resource_absent()
        elif self.state == 'default_bandwidth_reset':
            changed, msg, ansible_facts = self.__default_bandwidth_reset()

        return dict(changed=changed, msg=msg, ansible_facts=ansible_facts)

    def __present(self):

        bandwidth = self.data.pop('bandwidth', None)
        scope_uris = self.data.pop('scopeUris', None)
        result = self.resource_present(self.RESOURCE_FACT_NAME)

        if bandwidth:
            if self.__update_connection_template(bandwidth)[0]:
                if not result['changed']:
                    result['changed'] = True
                    result['msg'] = self.MSG_UPDATED

        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'ethernet_network', scope_uris)

        return result

    def __bulk_present(self):
        vlan_id_range = self.data['vlanIdRange']

        ethernet_networks = self.resource_client.get_range(self.data['namePrefix'], vlan_id_range)

        if not ethernet_networks:
            ethernet_networks = self.resource_client.create_bulk(self.data)
            changed = True
            msg = self.MSG_BULK_CREATED

        else:
            vlan_ids = self.resource_client.dissociate_values_or_ranges(vlan_id_range)
            for net in ethernet_networks[:]:
                vlan_ids.remove(net['vlanId'])

            if len(vlan_ids) == 0:
                msg = self.MSG_BULK_ALREADY_EXIST
                changed = False
            else:
                if len(vlan_ids) == 1:
                    self.data['vlanIdRange'] = '{0}-{1}'.format(vlan_ids[0], vlan_ids[0])
                else:
                    self.data['vlanIdRange'] = ','.join(map(str, vlan_ids))

                self.resource_client.create_bulk(self.data)
                ethernet_networks = self.resource_client.get_range(self.data['namePrefix'], vlan_id_range)
                changed = True
                msg = self.MSG_MISSING_BULK_CREATED

        return changed, msg, dict(ethernet_network_bulk=ethernet_networks)

    def __bulk_absent(self):
        networkUris = self.data['networkUris']

        if networkUris is not None:
            self.resource_client.delete_bulk(self.data)
            changed = True
            msg = self.MSG_BULK_DELETED

        return changed, msg, dict(ethernet_network_bulk_delete=None)

    def __update_connection_template(self, bandwidth):

        if 'connectionTemplateUri' not in self.current_resource.data:
            return False, None

        connection_template = self.connection_templates.get_by_uri(
            self.current_resource.data['connectionTemplateUri'])

        merged_data = connection_template.data.copy()
        merged_data.update({'bandwidth': bandwidth})

        if not compare(connection_template.data, merged_data):
            connection_template.update(merged_data)
            return True, connection_template.data
        else:
            return False, None

    def __default_bandwidth_reset(self):

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_ETHERNET_NETWORK_NOT_FOUND)

        default_connection_template = self.connection_templates.get_default()

        changed, connection_template_data = self.__update_connection_template(
            default_connection_template['bandwidth'])

        return changed, self.MSG_CONNECTION_TEMPLATE_RESET, dict(
            ethernet_network_connection_template=connection_template_data)


def main():
    EthernetNetworkModule().run()


if __name__ == '__main__':
    main()
