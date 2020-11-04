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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_server_profile_template_facts
short_description: Retrieve facts about the Server Profile Templates from OneView.
description:
    - Retrieve facts about the Server Profile Templates from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Server Profile Template name.
    uri:
      description:
        - Server Profile Template uri.
    options:
      description:
        - "List with options to gather additional facts about Server Profile Template resources.
          Options allowed: C(new_profile), C(transformation) and C(available_networks)."
notes:
    - The option C(transformation) is only available for API version 300 or later.
    - The option C(available_networks) is only available for API version 600 or later.
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"

- debug: var=server_profile_templates

- name: Gather paginated, filtered and sorted facts about Server Profile Templates
  oneview_server_profile_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
      scope_uris: /rest/scopes/af62ae65-06b2-4aaf-94d3-6a92562888cf
  delegate_to: localhost

- debug: var=server_profile_templates

- name: Gather facts about a Server Profile Template by name
  oneview_server_profile_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    name: "ProfileTemplate101"

- name: Gather facts about a Server Profile by uri
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    uri: /rest/server-profile-templates/c0868397-eff6-49ed-8151-4338702792d3
  delegate_to: localhost

- name: Gather facts about a template and a profile with the configuration based on this template
  oneview_server_profile_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    name: "ProfileTemplate101"
    options:
      - new_profile

- name: Gather facts about available networks.
  oneview_server_profile_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    options:
      - available_networks:
          serverHardwareTypeUri: "/rest/server-hardware-types/253F1D49-0FEE-4DCD-B14C-B26234E9D414"
          enclosureGroupUri: "/rest/enclosure-groups/293e8efe-c6b1-4783-bf88-2d35a8e49071"
  delegate_to: localhost

'''

RETURN = '''
server_profile_templates:
    description: Has all the OneView facts about the Server Profile Templates.
    returned: Always, but can be null.
    type: dict

new_profile:
    description: A profile object with the configuration based on this template.
    returned: When requested, but can be null.
    type: dict

server_profile_template_available_networks:
    description: Has all the facts about the list of Ethernet networks, Fibre Channel networks and network sets that
      are available to the server profile along with their respective ports.
    returned: When requested, but can be null.
    type: dict

'''
from ansible.module_utils.oneview import OneViewModule


class ServerProfileTemplateFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(type='str'),
        options=dict(type='list'),
        params=dict(type='dict'),
        uri=dict(type='str')
    )

    def __init__(self):
        super(ServerProfileTemplateFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

        self.set_resource_object(self.oneview_client.server_profile_templates)

    def execute_module(self):
        name = self.module.params.get("name")
        uri = self.module.params.get("uri")

        if name or uri:
            facts = self.__get_options(name, uri)
        elif self.options and self.options.get("available_networks"):
            network_params = self.options["available_networks"]
            facts = {"server_profile_template_available_networks": self.resource_client.get_available_networks(**network_params)}
        else:
            facts = self.__get_all()

        return dict(changed=False, ansible_facts=facts)

    def __get_options(self, name, uri):
        if not self.current_resource:
            return dict(server_profile_templates=[])

        facts = dict(server_profile_templates=[self.current_resource.data])

        if self.options:
            if "new_profile" in self.options:
                facts["new_profile"] = self.current_resource.get_new_profile()

            if "transformation" in self.options:
                tranformation_data = self.options.get('transformation')
                facts["transformation"] = self.current_resource.get_transformation(**tranformation_data)

        return facts

    def __get_all(self):
        templates = self.resource_client.get_all(**self.facts_params)
        return dict(server_profile_templates=templates)


def main():
    ServerProfileTemplateFactsModule().run()


if __name__ == '__main__':
    main()
