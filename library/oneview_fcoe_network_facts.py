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
module: oneview_fcoe_network_facts
short_description: Retrieve the facts about one or more of the OneView FCoE Networks
description:
    - Retrieve the facts about one or more of the FCoE Networks from OneView.
version_added: "2.4"
requirements:
    - hpOneView >= 5.0.0
author:
    - Felipe Bulsoni (@fgbulsoni)
    - Thiago Miotto (@tmiotto)
    - Adriane Cardozo (@adriane-cardozo)
options:
    name:
      description:
        - FCoE Network name.
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all FCoE Networks
  oneview_fcoe_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost

- debug: var=fcoe_networks

- name: Gather paginated, filtered and sorted facts about FCoE Networks
  oneview_fcoe_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'vlanId=2'
  delegate_to: localhost

- debug: var=fcoe_networks

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: Test FCoE Network Facts
  delegate_to: localhost

- debug: var=fcoe_networks
'''

RETURN = '''
fcoe_networks:
    description: Has all the OneView facts about the FCoE Networks.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class FcoeNetworkFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(type='str'),
            params=dict(type='dict'),
        )

        super(FcoeNetworkFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.fcoe_networks)

    def execute_module(self):

        if self.module.params['name']:
            fcoe_networks = self.resource_client.get_by('name', self.module.params['name'])
        else:
            fcoe_networks = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(fcoe_networks=fcoe_networks))


def main():
    FcoeNetworkFactsModule().run()


if __name__ == '__main__':
    main()
