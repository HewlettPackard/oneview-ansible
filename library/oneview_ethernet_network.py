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
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_ethernet_network
short_description: Manage OneView Ethernet Network resources.
description:
    - Provides an interface to manage Ethernet Network resources. Can create, update, or delete.
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
            - Indicates the desired state for the Ethernet Network resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
              'default_bandwidth_reset' will reset the network connection template to the default.
        choices: ['present', 'absent', 'default_bandwidth_reset']
    data:
        description:
            - List with Ethernet Network properties.
        required: true
    validate_etag:
        description:
            - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
              for the resource matches the ETag provided in the data.
        default: true
        choices: ['true', 'false']
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Ensure that the Ethernet Network is present using the default configuration
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      vlanId: '201'

- name: Update the Ethernet Network changing bandwidth and purpose
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
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

- name: Reset to the default network connection template
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: default_bandwidth_reset
    data:
      name: 'Test Ethernet Network'
  delegate_to: localhost
'''

RETURN = '''
ethernet_network:
    description: Has the facts about the Ethernet Networks.
    returned: On state 'present'. Can be null.
    type: complex

ethernet_network_bulk:
    description: Has the facts about the Ethernet Networks affected by the bulk insert.
    returned: When 'vlanIdRange' attribute is in data argument. Can be null.
    type: complex

ethernet_network_connection_template:
    description: Has the facts about the Ethernet Network Connection Template.
    returned: On state 'default_bandwidth_reset'. Can be null.
    type: complex
'''

ETHERNET_NETWORK_CREATED = 'Ethernet Network created successfully.'
ETHERNET_NETWORK_UPDATED = 'Ethernet Network updated successfully.'
ETHERNET_NETWORK_DELETED = 'Ethernet Network deleted successfully.'
ETHERNET_NETWORK_ALREADY_EXIST = 'Ethernet Network already exists.'
ETHERNET_NETWORK_ALREADY_ABSENT = 'Ethernet Network is already absent.'
ETHERNET_NETWORKS_CREATED = 'Ethernet Networks created successfully.'
MISSING_ETHERNET_NETWORKS_CREATED = 'Some missing Ethernet Networks were created successfully.'
ETHERNET_NETWORKS_ALREADY_EXIST = 'The specified Ethernet Networks already exist.'
ETHERNET_NETWORK_CONNECTION_TEMPLATE_RESET = 'Ethernet Network connection template was reset to the default.'
ETHERNET_NETWORK_NOT_FOUND = 'Ethernet Network was not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class EthernetNetworkModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'default_bandwidth_reset']
        ),
        data=dict(required=True, type='dict'),
        validate_etag=dict(
            required=False,
            type='bool',
            default=True)
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
        data = self.module.params['data']
        changed, msg, ansible_facts = False, '', {}

        try:
            if not self.module.params.get('validate_etag'):
                self.oneview_client.connection.disable_etag_validation()

            if state == 'present':
                if data.get('vlanIdRange'):
                    changed, msg, ansible_facts = self.__bulk_present(data)
                else:
                    changed, msg, ansible_facts = self.__present(data)
            elif state == 'default_bandwidth_reset':
                changed, msg, ansible_facts = self.__default_bandwidth_reset(data)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(data)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        ethernet_network = self.__get_by_name(data)

        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        bandwidth = data.pop('bandwidth', None)

        if not ethernet_network:
            ethernet_network = self.oneview_client.ethernet_networks.create(data)
            changed = True
            msg = ETHERNET_NETWORK_CREATED
        else:
            merged_data = ethernet_network.copy()
            merged_data.update(data)

            if not resource_compare(ethernet_network, merged_data):
                ethernet_network = self.oneview_client.ethernet_networks.update(merged_data)
                changed = True
                msg = ETHERNET_NETWORK_UPDATED
            else:
                msg = ETHERNET_NETWORK_ALREADY_EXIST

        if bandwidth:
            if self.__update_connection_template(ethernet_network, bandwidth)[0]:
                if not changed:
                    changed = True
                    msg = ETHERNET_NETWORK_UPDATED

        return changed, msg, dict(ethernet_network=ethernet_network)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.ethernet_networks.delete(resource)
            return True, ETHERNET_NETWORK_DELETED, {}
        else:
            return False, ETHERNET_NETWORK_ALREADY_ABSENT, {}

    def __bulk_present(self, data):
        vlan_id_range = data['vlanIdRange']

        ethernet_networks = self.oneview_client.ethernet_networks.get_range(data['namePrefix'], vlan_id_range)

        if not ethernet_networks:
            ethernet_networks = self.oneview_client.ethernet_networks.create_bulk(data)
            changed = True
            msg = ETHERNET_NETWORKS_CREATED

        else:
            vlan_ids = self.oneview_client.ethernet_networks.dissociate_values_or_ranges(vlan_id_range)
            for net in ethernet_networks[:]:
                vlan_ids.remove(net['vlanId'])

            if len(vlan_ids) == 0:
                msg = ETHERNET_NETWORKS_ALREADY_EXIST
                changed = False
            else:
                if len(vlan_ids) == 1:
                    data['vlanIdRange'] = '{0}-{1}'.format(vlan_ids[0], vlan_ids[0])
                else:
                    data['vlanIdRange'] = ','.join(map(str, vlan_ids))

                self.oneview_client.ethernet_networks.create_bulk(data)
                ethernet_networks = self.oneview_client.ethernet_networks.get_range(data['namePrefix'], vlan_id_range)
                changed = True
                msg = MISSING_ETHERNET_NETWORKS_CREATED

        return changed, msg, dict(ethernet_network_bulk=ethernet_networks)

    def __get_by_name(self, data):
        result = self.oneview_client.ethernet_networks.get_by('name', data['name'])
        return result[0] if result else None

    def __update_connection_template(self, ethernet_network, bandwidth):

        if 'connectionTemplateUri' not in ethernet_network:
            return False, None

        connection_template = self.oneview_client.connection_templates.get(ethernet_network['connectionTemplateUri'])

        merged_data = connection_template.copy()
        merged_data.update({'bandwidth': bandwidth})

        if not resource_compare(connection_template, merged_data):
            connection_template = self.oneview_client.connection_templates.update(merged_data)
            return True, connection_template
        else:
            return False, None

    def __default_bandwidth_reset(self, data):
        resource = self.__get_by_name(data)

        if not resource:
            raise HPOneViewResourceNotFound(ETHERNET_NETWORK_NOT_FOUND)

        default_connection_template = self.oneview_client.connection_templates.get_default()

        changed, connection_template = self.__update_connection_template(resource,
                                                                         default_connection_template['bandwidth'])

        return changed, ETHERNET_NETWORK_CONNECTION_TEMPLATE_RESET, dict(
            ethernet_network_connection_template=connection_template)


def main():
    EthernetNetworkModule().run()


if __name__ == '__main__':
    main()
