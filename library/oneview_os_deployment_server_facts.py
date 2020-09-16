#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2017) Hewlett Packard Enterprise Development LP
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
module: oneview_os_deployment_server_facts
short_description: Retrieve facts about one or more OS Deployment Servers.
description:
    - Retrieve facts about one or more of the OS Deployment Servers from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 3.1.1"
author: "Camila Balestrin (@balestrinc)"
options:
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(filter): A general filter/query string to narrow the list of items returned.
          C(sort): The sort order of the returned data set.
          C(query): A general query string to narrow the list of resources returned.
          C(fields): Specifies which fields should be returned in the result set.
          C(view): Return a specific subset of the attributes of the resource or collection, by
          specifying the name of a predefined view."
      required: false
    name:
      description:
        - OS Deployment Server name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an OS Deployment Server and related resources.
          Options allowed: C(networks), C(appliances), and C(appliance)."
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all OS Deployment Servers
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: "OS Deployment Server-Name"
  delegate_to: localhost

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name with options
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: 'Test-OS Deployment Server'
    options:
      - networks                    # optional
      - appliances                  # optional
      - appliance: 'Appliance name' # optional
  delegate_to: localhost

- debug: var=os_deployment_servers
- debug: var=os_deployment_server_networks
- debug: var=os_deployment_server_appliances
- debug: var=os_deployment_server_appliance
'''

RETURN = '''
os_deployment_servers:
    description: Has all the OneView facts about the OS Deployment Servers.
    returned: Always, but can be null.
    type: dict

os_deployment_server_networks:
    description: Has all the OneView facts about the OneView networks.
    returned: When requested, but can be null.
    type: dict

os_deployment_server_appliances:
    description: Has all the OneView facts about all the Image Streamer resources.
    returned: When requested, but can be null.
    type: dict

os_deployment_server_appliance:
    description: Has the facts about the particular Image Streamer resource.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class OsDeploymentServerFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(OsDeploymentServerFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        ansible_facts = {}

        if self.module.params.get('name'):
            os_deployment_servers = self.oneview_client.os_deployment_servers.get_by('name',
                                                                                     self.module.params['name'])
        else:
            os_deployment_servers = self.oneview_client.os_deployment_servers.get_all(**self.facts_params)

        if self.options:
            ansible_facts = self.__gather_optional_facts(self.options)

        ansible_facts['os_deployment_servers'] = os_deployment_servers

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options):

        facts = {}

        if options.get('networks'):
            facts['os_deployment_server_networks'] = self.oneview_client.os_deployment_servers.get_networks()
        if options.get('appliances'):
            facts['os_deployment_server_appliances'] = self.oneview_client.os_deployment_servers.get_appliances()
        if options.get('appliance'):
            facts['os_deployment_server_appliance'] = self.oneview_client.os_deployment_servers.get_appliance_by_name(
                options.get('appliance'))

        return facts


def main():
    OsDeploymentServerFactsModule().run()


if __name__ == '__main__':
    main()
