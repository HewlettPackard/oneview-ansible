#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
module: oneview_id_pools_ipv4_subnet
short_description: Manage OneView ID pools IPV4 Subnet resources.
description:
    - Provides an interface to manage ID pools IPV4 Subnet resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
author: "Thiago Miotto (@tmiotto)"
options:
    state:
        description:
            - Indicates the desired state for the ID pools IPV4 Subnet resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with ID pools IPV4 Subnet properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that ID pools IPV4 Subnet is present using the default configuration
  oneview_id_pools_ipv4_subnet:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test ID pools IPV4 Subnet'
      vlanId: '201'

- name: Ensure that ID pools IPV4 Subnet is absent
  oneview_id_pools_ipv4_subnet:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'ID pools IPV4 Subnet'
'''

RETURN = '''
id_pools_ipv4_subnet:
    description: Has the facts about the OneView ID pools IPV4 Subnets.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewValueError, ResourceComparator


class IdPoolsIpv4SubnetModule(OneViewModuleBase):
    MSG_CREATED = 'ID pools IPV4 Subnet created successfully.'
    MSG_UPDATED = 'ID pools IPV4 Subnet updated successfully.'
    MSG_DELETED = 'ID pools IPV4 Subnet deleted successfully.'
    MSG_ALREADY_PRESENT = 'ID pools IPV4 Subnet is already present.'
    MSG_ALREADY_ABSENT = 'ID pools IPV4 Subnet is already absent.'
    MSG_VALUE_ERROR = "The name or the uri attrbiutes must be specfied"
    RESOURCE_FACT_NAME = 'id_pools_ipv4_subnet'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super(IdPoolsIpv4SubnetModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                                      validate_etag_support=True)

        self.resource_client = self.oneview_client.id_pools_ipv4_subnets

    def execute_module(self):
        if self.data.get('uri'):
            resource = self.resource_client.get(self.data.get('uri'))
        elif self.data.get('name'):
            query = self.resource_client.get_all(filter="name='{}'".format(self.data.get('name')))
            resource = query[0] if query and query[0].get('name') == self.data['name'] else None
        else:
            raise HPOneViewValueError(self.MSG_VALUE_ERROR)

        self.data['type'] = self.data.get('type', 'Subnet')

        if self.state == 'present':
            return self.resource_present(resource, 'id_pools_ipv4_subnet')
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    IdPoolsIpv4SubnetModule().run()


if __name__ == '__main__':
    main()
