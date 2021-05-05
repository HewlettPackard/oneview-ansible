#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
module: oneview_logical_interconnect_group
short_description: Manage OneView Logical Interconnect Group resources.
description:
    - Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.9"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Interconnect Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Logical Interconnect Group properties.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalDownlinkUri: ~
            logicalLocation:
                locationEntries:
                    - relativeValue: "1"
                      type: "Bay"
                    - relativeValue: 1
                      type: "Enclosure"
            permittedInterconnectTypeName: 'HP VC Flex-10/10D Module'
            # Alternatively you can inform permittedInterconnectTypeUri
# Below Task is available only till OneView 3.10
- name: Ensure that the Logical Interconnect Group has the specified scopes
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'

- name: Ensure that the Logical Interconnect Group is present with uplinkSets
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets:
        - name: 'e23 uplink set'
          mode: 'Auto'
          networkType: 'Ethernet'
          networkNames:
            - 'TestNetwork_1'
          networkUris:
            - '/rest/ethernet-networks/b2be27ec-ae31-41cb-9f92-ff6da5905abc'
          logicalPortConfigInfos:
            - desiredSpeed: 'Auto'
              logicalLocation:
                  locationEntries:
                    - relativeValue: 1
                      type: "Bay"
                    - relativeValue: 23
                      type: "Port"
                    - relativeValue: 1
                      type: "Enclosure"

- name: Ensure that the Logical Interconnect Group is present with name 'Test'
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'New Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the Logical Interconnect Group is absent
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'New Logical Interconnect Group'
'''

RETURN = '''
logical_interconnect_group:
    description: Has the facts about the OneView Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, compare, dict_merge, LIGMerger, sort_by_uplink_set_location
from copy import deepcopy

class LogicalInterconnectGroupModule(OneViewModule):
    MSG_CREATED = 'Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'Logical Interconnect Group is already absent.'
    MSG_INTERCONNECT_TYPE_NOT_FOUND = 'Interconnect Type was not found.'
    MSG_NETWORK_NOT_FOUND = 'Given Network was not found.'
    MSG_NETWORK_SET_NOT_FOUND = 'Network Set was not found.'

    RESOURCE_FACT_NAME = 'logical_interconnect_group'

    def __init__(self):
        argument_spec = dict(
            state=dict(required=True, choices=['present', 'absent']),
            data=dict(required=True, type='dict')
        )

        super(LogicalInterconnectGroupModule, self).__init__(additional_arg_spec=argument_spec,
                                                             validate_etag_support=True)
        self.set_resource_object(self.oneview_client.logical_interconnect_groups)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent()

    def __present(self):
        changed = False
        scope_uris = self.data.pop('scopeUris', None)

        self.__replace_name_by_uris()

        if 'uplinkSets' in self.data:
            self.__replace_uplinkset_network_uris()

        if self.current_resource:
            changed, msg = self.__update()
        else:
            changed, msg = self.__create()

        result = dict(
            msg=msg,
            changed=changed,
            ansible_facts=dict(logical_interconnect_group=self.current_resource.data)
        )

        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'logical_interconnect_group', scope_uris)

        return result

    def __create(self):
        self.current_resource = self.resource_client.create(self.data)
        return True, self.MSG_CREATED

    def __update(self):
        changed = False
        current_data = self.current_resource.data.copy()

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        # escaping logicalDownlinkUri from current_data while comparing
        map_template = current_data.get('interconnectMapTemplate')
        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    value.pop('logicalDownlinkUri', None)

        merged_data = LIGMerger().merge_data(current_data, self.data)

        current_data_copy = current_data.copy()
        merged_data_copy = deepcopy(merged_data)
        current_data_localid = current_data_copy.pop('logicalPortConfigInfos', None)
        merged_data_localid = merged_data_copy.pop('logicalPortConfigInfos', None)
        result = True
        if current_data_localid and merged_data_localid:
            result = sort_by_uplink_set_location(current_data_localid, merged_data_localid)
        elif current_data_localid or merged_data_localid:
            result = False
        if compare(current_data_copy, merged_data_copy) and result:
            msg = self.MSG_ALREADY_PRESENT
        else:
            self.current_resource.update(merged_data)
            changed = True
            msg = self.MSG_UPDATED
        return changed, msg

    def __replace_name_by_uris(self):
        if self.data.get('internalNetworkNames'):
            self.__replace_internal_network_names_by_uris()

        map_template = self.data.get('interconnectMapTemplate')
        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name)

    # replace internalNetworkNames with internalNetworkUris
    def __replace_internal_network_names_by_uris(self):
        internalNetworkUris = self.data.get('internalNetworkUris', [])
        internalNetworkNames = self.data.pop('internalNetworkNames', None)
        if internalNetworkNames:
            int_networkUris = [self.__get_network_uri(x, 'Ethernet') for x in internalNetworkNames]
            internalNetworkUris.extend(int_networkUris)
        self.data['internalNetworkUris'] = internalNetworkUris

    # retrieves and replaces network/network-set name with uri in LIG uplinksets
    def __replace_uplinkset_network_uris(self):
        for uplinkSet in self.data['uplinkSets']:
            networkNames = uplinkSet.pop('networkNames', None)
            networkSetNames = uplinkSet.pop('networkSetNames', None)
            network_type = uplinkSet.get('networkType', '')

            if networkNames and not uplinkSet.get('networkUris'):
                uplinkSet['networkUris'] = []
            if networkNames:
                networkUris = [self.__get_network_uri(x, network_type) for x in networkNames]
                uplinkSet['networkUris'].extend(networkUris)
            if networkSetNames and not uplinkSet.get('networkSetUris'):
                uplinkSet['networkSetUris'] = []
            if networkSetNames:
                networkSetUris = [self.__get_network_set(x) for x in networkSetNames]
                uplinkSet['networkSetUris'].extend(networkSetUris)

    def __get_network_uri(self, name, network_type):
        if network_type == 'Ethernet':
            network_name = self.oneview_client.ethernet_networks.get_by_name(name)
        else:
            network_name = self.oneview_client.fc_networks.get_by_name(name)

        if network_name:
            return network_name.data['uri']
        else:
            raise OneViewModuleResourceNotFound(self.MSG_NETWORK_NOT_FOUND)

    def __get_network_set(self, name):
        network_set = self.oneview_client.network_sets.get_by_name(name)
        if network_set:
            return network_set.data['uri']
        else:
            raise OneViewModuleResourceNotFound(self.MSG_NETWORK_SET_NOT_FOUND)

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.interconnect_types.get_by_name(name)
        if i_type:
            return i_type.data['uri']
        else:
            raise OneViewModuleResourceNotFound(self.MSG_INTERCONNECT_TYPE_NOT_FOUND)


def main():
    LogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
