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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_certificates_server
short_description: Manage OneView Server Certificate resources.
description:
    - Provides an interface to manage Server Certificate resources. Can create, update, and delete.
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - "hpOneView >= 5.1.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the Server Certificate resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Server Certificate properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Server Certificate
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'

- name: Update the Server Certificate name to 'vcenter Renamed'
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      name: 'vcenter renamed'
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'

- name: Ensure that the Hypervisor Manager is absent
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    name: "172.18.13.11"
    data:
      alias_name: 'vcenter'
'''

RETURN = '''
certificate_server:
    description: Has the facts about the managed OneView Hypervisor Manager.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError


class CertificatesServerModule(OneViewModule):
    MSG_CREATED = 'Server Certificate created successfully.'
    MSG_UPDATED = 'Server Certificate updated successfully.'
    MSG_DELETED = 'Server Certificate deleted successfully.'
    MSG_ALREADY_PRESENT = 'Server Certificate is already present.'
    MSG_ALREADY_ABSENT = 'Server Certificate is already absent.'
    MSG_VALUE_ERROR = 'The aliasName or remote server name must be specified'
    RESOURCE_FACT_NAME = 'certificate_server'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   name=dict(required=False, type='str'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super(CertificatesServerModule, self).__init__(additional_arg_spec=additional_arg_spec, validate_etag_support=True)
        self.__set_current_resource(self.oneview_client.certificates_server)

    def execute_module(self):
        if self.state == 'present':
            return self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent()

    def __set_current_resource(self, resource_client, aliasname=None):
        self.resource_client = resource_client

        if self.data['certificateDetails'][0].get('aliasName'):
            aliasname = self.data['certificateDetails'][0]['aliasName']
        elif self.module.params.get('name'):
            aliasname = self.module.params['name']
        else:
            raise OneViewModuleValueError(self.MSG_VALUE_ERROR)

        try:
            self.current_resource =  self.resource_client
            self.current_resource.data = self.resource_client.get_by_aliasName(aliasname)
        except Exception as e:
            cert_not_found_message = "No matching certificate found for the specified alias"
            if cert_not_found_message in e.msg:
                self.current_resource = None
            else:
                raise Exception(e.msg)


def main():
    CertificatesServerModule().run()


if __name__ == '__main__':
    main()
