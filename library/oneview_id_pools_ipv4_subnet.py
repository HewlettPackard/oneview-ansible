#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.6.0"
author: "Yuvarani Chidambaram(@yuvirani)"
options:
    state:
        description:
            - Indicates the desired state for the ID pools IPV4 Subnet resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(allocate) will allocate set of ID's from IPv4 subnet
              C(collect) will collect the allocated IDs'
        choices: ['present', 'absent', 'allocate', 'collect']
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

from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError


class IdPoolsIpv4SubnetModule(OneViewModule):
    MSG_CREATED = 'ID pools IPV4 Subnet created successfully.'
    MSG_UPDATED = 'ID pools IPV4 Subnet updated successfully.'
    MSG_DELETED = 'ID pools IPV4 Subnet deleted successfully.'
    MSG_ALREADY_PRESENT = 'ID pools IPV4 Subnet is already present.'
    MSG_ALREADY_ABSENT = 'ID pools IPV4 Subnet is already absent.'
    MSG_VALUE_ERROR = "The name or the uri attrbiutes must be specfied"
    MSG_ALLOCATE = 'IDs found and have been allocated'
    MSG_NO_ALLOCATE = 'No ids found for allocation'
    MSG_COLLECT = 'Collected the ids allocated'
    RESOURCE_FACT_NAME = 'id_pools_ipv4_subnet'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(required=True,
                                       choices=['present', 'absent', 'allocate', 'collect']))

        super(IdPoolsIpv4SubnetModule, self).__init__(additional_arg_spec=additional_arg_spec,
                                                      validate_etag_support=True)

        self.set_resource_object(self.oneview_client.id_pools_ipv4_subnets)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        if self.data.get('uri'):
            resource = self.resource_client.get(self.data.get('uri'))
        elif self.data.get('name'):
            query = self.resource_client.get_all(filter="name='{}'".format(self.data.get('name')))
            resource = query[0] if query and query[0].get('name') == self.data['name'] else None
        else:
            raise OneViewModuleValueError(self.MSG_VALUE_ERROR)

        self.data['type'] = self.data.get('type', 'Subnet')

        if self.state == 'present':
            return self.resource_present(RESOURCE_FACT_NAME)
        elif self.state == 'allocate':
            changed, msg, ipv4_subnet = self.__allocator(resource)
            return dict(changed=changed, msg=msg, ansible_facts=dict(id_pools_ipv4_subnet=ipv4_subnet))
        elif self.state == 'collector':
            changed, msg, ipv4_subnet = self.__collector(resource)
            return dict(changed=changed, msg=msg, ansible_facts=dict(id_pools_ipv4_subnet=ipv4_subnet))
        elif self.state == 'absent':
            return self.resource_absent()

    def __allocator(self, resource):
        try:
            subnet_id = resource['allocatorUri'].split('/')[-2]
            allocate = self.resource_client.allocate({'count': self.data['count']}, subnet_id)
            return True, self.MSG_ALLOCATE, allocate
        except:
            raise OneViewModuleValueError(self.MSG_NO_ALLOCATE)

    def __collector(self, resource):
        subnet_id = resource['allocatorUri'].split('/')[-2]
        collect = self.resource_client.collect({'idList': self.data['idList']}, subnet_id)
        return True, self.MSG_COLLECT, self.data['idList']

def main():
    IdPoolsIpv4SubnetModule().run()


if __name__ == '__main__':
    main()
