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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_fc_network
short_description: Manage OneView Fibre Channel Network resources.
description:
    - Provides an interface to manage Fibre Channel Network resources. Can create, update, and delete.
version_added: "2.4"
requirements:
    - "hpeOneView >= 5.4.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the Fibre Channel Network resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Fibre Channel Network properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Fibre Channel Network
  oneview_fc_network:
    config: "{{ config }}"
    state: present
    validate_etag: False
    data:
      name: "{{ item }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
      bandwidth:
        maximumBandwidth: 2000
        typicalBandwidth: 1000
  delegate_to: localhost
  register: fc_network_1
  with_items:
    - "{{ network_name }}"
    - "{{ network_name }} (1)"
    - "{{ network_name }} (2)"

- name: Do nothing with the Fibre Channel Network when no changes are provided
  oneview_fc_network:
    config: "{{ config }}"
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
      bandwidth:
        maximumBandwidth: 2000
        typicalBandwidth: 1000
  delegate_to: localhost

- name: Update the Fibre Channel Network changing the attribute autoLoginRedistribution to True
  oneview_fc_network:
    config: "{{ config }}"
    state: present
    data:
      name: "{{ network_name }}"
      autoLoginRedistribution: False
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      bandwidth:
        maximumBandwidth: 3000
        typicalBandwidth: 2000
  delegate_to: localhost

- name: Delete the Fibre Channel Network
  oneview_fc_network:
    config: "{{ config }}"
    state: absent
    data:
      name: "{{ network_name }}"
  delegate_to: localhost
  register: deleted

- name: Do nothing when Fibre Channel Network is absent
  oneview_fc_network:
    config: "{{ config }}"
    state: absent
    data:
      name: "{{ network_name }}"
  delegate_to: localhost
  register: deleted

- debug: var=fc_network_1.results[1].ansible_facts.fc_network.uri

# This feature is available only from OneView 5.20
- name: Delete Fibre Channel Networks in bulk
  oneview_fc_network:
    config: "{{ config }}"
    state: absent
    data:
      networkUris:
        - "{{ fc_network_1.results[1].ansible_facts.fc_network.uri }}"
        - "{{ fc_network_1.results[2].ansible_facts.fc_network.uri }}"
  delegate_to: localhost
  when: currentVersion >= '1600'
'''

RETURN = '''
fc_network:
    description: Has the facts about the managed OneView FC Network.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, compare


class FcNetworkModule(OneViewModule):
    MSG_CREATED = 'FC Network created successfully.'
    MSG_UPDATED = 'FC Network updated successfully.'
    MSG_DELETED = 'FC Network deleted successfully.'
    BULK_MSG_DELETED = 'FC Networks deleted successfully.'
    MSG_ALREADY_PRESENT = 'FC Network is already present.'
    MSG_ALREADY_ABSENT = 'FC Network is already absent.'
    RESOURCE_FACT_NAME = 'fc_network'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super(FcNetworkModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                              validate_etag_support=True)

        self.set_resource_object(self.oneview_client.fc_networks)
        self.connection_templates = self.oneview_client.connection_templates

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        if self.state == 'present':
            return self._present()
        elif self.state == 'absent':
            if self.data.get('networkUris'):
                changed, msg, ansible_facts = self.__bulk_absent()
            elif not self.module.check_mode:
                return self.resource_absent()
            else:
                return self.check_resource_absent()

        return dict(changed=changed, msg=msg, ansible_facts=ansible_facts)

    def _present(self):
        scope_uris = self.data.pop('scopeUris', None)
        bandwidth = self.data.pop('bandwidth', None)
        if not self.module.check_mode:
            result = self.resource_present(self.RESOURCE_FACT_NAME)
        else:
            result = self.check_resource_present(self.RESOURCE_FACT_NAME)

        if bandwidth is not None:
            if self.__update_connection_template(bandwidth)[0]:
                if not result['changed']:
                    result['changed'] = True
                    result['msg'] = self.MSG_UPDATED

        if scope_uris is not None:
            if not self.module.check_mode:
                result = self.resource_scopes_set(result, 'fc_network', scope_uris)
            else:
                result = self.check_resource_scopes_set(result, 'fc_network', scope_uris)

        return result

    def __bulk_absent(self):
        networkUris = self.data['networkUris']

        if networkUris is not None:
            self.resource_client.delete_bulk(self.data)
            changed = True
            msg = self.BULK_MSG_DELETED

        return changed, msg, dict(fc_network_bulk_delete=None)

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


def main():
    FcNetworkModule().run()


if __name__ == '__main__':
    main()
