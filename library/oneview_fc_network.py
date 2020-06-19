#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
    - "hpOneView >= 5.0.0"
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
- name: Ensure that the Fibre Channel Network is present using the default configuration
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'New FC Network'

- name: Ensure that the Fibre Channel Network is present with fabricType 'DirectAttach'
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'New FC Network'
      fabricType: 'DirectAttach'

# This feature is available only till OneView 3.10
- name: Ensure that the Fibre Channel Network is present and is inserted in the desired scopes
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 500
    state: present
    data:
      name: 'New FC Network'
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'

- name: Ensure that the Fibre Channel Network is absent
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'New FC Network'
'''

RETURN = '''
fc_network:
    description: Has the facts about the managed OneView FC Network.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule
from ansible.module_utils.oneview_check_mode import OneViewModuleCheckMode


class FcNetworkModule(OneViewModule, OneViewModuleCheckMode):
    MSG_CREATED = 'FC Network created successfully.'
    MSG_UPDATED = 'FC Network updated successfully.'
    MSG_DELETED = 'FC Network deleted successfully.'
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

    def execute_module(self):
        if self.state == 'present':
            return self._present()
        else:
            return self.resource_absent()

    def _present(self):
        scope_uris = self.data.pop('scopeUris', None)
        if not self.module.check_mode:
            result = self.resource_present(self.RESOURCE_FACT_NAME)
        else:
            result = self.check_resource_present(self.RESOURCE_FACT_NAME)
        if scope_uris is not None:
            if not self.module.check_mode:
                result = self.resource_scopes_set(result, 'fc_network', scope_uris)
            else:
                result = self.check_resource_scopes_set(result, 'fc_network', scope_uris)
        return result


def main():
    FcNetworkModule().run()


if __name__ == '__main__':
    main()
