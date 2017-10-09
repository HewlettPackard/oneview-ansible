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
module: oneview_fcoe_network_facts
short_description: Retrieve the facts about one or more of the OneView FCoE Networks.
description:
    - Retrieve the facts about one or more of the FCoE Networks from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - FCoE Network name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fcoe_networks

- name: Gather paginated, filtered and sorted facts about FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'vlanId=2'

- debug: var=fcoe_networks

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"
    name: "Test FCoE Network Facts"

- debug: var=fcoe_networks
'''

RETURN = '''
fcoe_networks:
    description: Has all the OneView facts about the FCoE Networks.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class FcoeNetworkFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(FcoeNetworkFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        if self.module.params['name']:
            fcoe_networks = self.oneview_client.fcoe_networks.get_by('name', self.module.params['name'])
        else:
            fcoe_networks = self.oneview_client.fcoe_networks.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(fcoe_networks=fcoe_networks))


def main():
    FcoeNetworkFactsModule().run()


if __name__ == '__main__':
    main()
