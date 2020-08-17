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
module: oneview_certificates_server_facts
short_description: Retrieve the facts about one or more of the OneView Server Certificates
description:
    - Retrieve the facts about one or more of the Server Certificates from OneView.
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - hpeOneView >= 5.2.0
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    alias_name:
      description:
        - Server Certificate aliasname.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about a Server Certificate by remote address
  oneview_certificates_server_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    remote: "172.18.13.11"
  delegate_to: localhost

- debug: var=remote_certificate['certificateDetails'][0]['base64Data']

- name: Gather facts about a Server Certificate by alias_name
  oneview_certificates_server_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    aliasName: "172.18.13.11"
  delegate_to: localhost

- debug: var=certificate
'''

RETURN = '''
certificate_server:
    description: Has all the OneView facts about the Server Certificates.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class CertificatesServerFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            remote=dict(required=False, type='str'),
            aliasName=dict(required=False, type='str'),
        )

        super(CertificatesServerFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.certificates_server

    def execute_module(self):
        ansible_facts = {}

        if self.module.params.get('aliasName'):
            aliasname = self.module.params['aliasName']
            certificates_server = self.resource_client.get_by_alias_name(aliasname)
            ansible_facts['certificates_server'] = certificates_server.data if certificates_server else None

        elif self.module.params.get('remote'):
            remote_address = self.module.params['remote']
            remote_cert = self.resource_client.get_remote(remote_address)
            ansible_facts['remote_certificate'] = remote_cert.data

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    CertificatesServerFactsModule().run()


if __name__ == '__main__':
    main()
