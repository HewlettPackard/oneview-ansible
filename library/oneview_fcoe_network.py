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
module: oneview_fcoe_network
short_description: Manage OneView FCoE Network resources
description:
    - Provides an interface to manage FCoE Network resources. Can create, update, or delete.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the FCoE Network resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        default: present
        choices: ['present', 'absent']
    data:
        description:
            - List with FCoE Network properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that FCoE Network is present using the default configuration
  oneview_fcoe_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: present
    data:
      name: Test FCoE Network
      vlanId: 201
  delegate_to: localhost
# Below task is supported only with OneView 3.10
- name: Update the FCOE network scopes
  oneview_fcoe_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: New FCoE Network
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'
  delegate_to: localhost

- name: Ensure that FCoE Network is absent
  oneview_fcoe_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: absent
    data:
      name: New FCoE Network
  delegate_to: localhost

- name: Delete FCoE Networks in bulk(works from API1600)
  oneview_fcoe_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1800
    state: absent
    data:
      networkUris:
        -  "/rest/fcoe-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548"
  delegate_to: localhost
'''

RETURN = '''
fcoe_network:
    description: Has the facts about the OneView FCoE Networks.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class FcoeNetworkModule(OneViewModule):
    MSG_CREATED = 'FCoE Network created successfully.'
    MSG_UPDATED = 'FCoE Network updated successfully.'
    MSG_DELETED = 'FCoE Network deleted successfully.'
    MSG_BULK_DELETED = 'FCoE Networks deleted successfully.'
    MSG_ALREADY_PRESENT = 'FCoE Network is already present.'
    MSG_ALREADY_ABSENT = 'FCoE Network is already absent.'
    RESOURCE_FACT_NAME = 'fcoe_network'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(default='present',
                                              choices=['present', 'absent']))

        super(FcoeNetworkModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                                validate_etag_support=True)

        self.set_resource_object(self.oneview_client.fcoe_networks)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            if self.data.get('networkUris'):
                changed, msg, ansible_facts = self.__bulk_absent()
            else:
                return self.resource_absent()

        return dict(changed=changed, msg=msg, ansible_facts=ansible_facts)

    def __present(self):
        scope_uris = self.data.pop('scopeUris', None)
        result = self.resource_present(self.RESOURCE_FACT_NAME)
        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'fcoe_network', scope_uris)
        return result

    def __bulk_absent(self):
        networkUris = self.data['networkUris']

        if networkUris is not None:
            self.resource_client.delete_bulk(self.data)
            changed = True
            msg = self.MSG_BULK_DELETED

        return changed, msg, dict(fcoe_network_bulk_delete=None)


def main():
    FcoeNetworkModule().run()


if __name__ == '__main__':
    main()
