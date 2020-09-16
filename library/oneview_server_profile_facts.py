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
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_server_profile_facts
short_description: Retrieve facts about the OneView Server Profiles.
description:
    - Retrieve facts about the Server Profile from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Server Profile name.
    uri:
      description:
        - Server Profile uri.
    options:
      description:
        - "List with options to gather additional facts about Server Profile related resources.
          Options allowed: C(schema), C(compliancePreview), C(profilePorts), C(messages), C(transformation),
          C(available_networks), C(available_servers), C(available_storage_system), C(available_storage_systems),
          C(available_targets), C(newProfileTemplate),"
        - "To gather facts about C(compliancePreview), C(messages), C(newProfileTemplate) and C(transformation)
           a Server Profile name is required. Otherwise, these options will be ignored."
notes:
    - The option C(newProfileTemplate), C(available_servers) is only available till API version 1200.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Server Profiles
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  delegate_to: localhost

- debug: var=server_profiles

- name: Gather paginated, filtered and sorted facts about Server Profiles
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about a Server Profile by name
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    name: WebServer-1
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about a Server Profile by uri
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    uri: /rest/server-profiles/e23d9fa4-f926-4447-b971-90116ca3e61e
  delegate_to: localhost

- debug: var=server_profiles

- name: Gather facts about available servers and bays for a given enclosure group and server hardware type
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    options:
      - availableTargets:
          enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
          serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
  delegate_to: localhost

- debug: var=server_profile_available_targets


- name: Gather all facts about a Server Profile
  oneview_server_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    name : "Encl1, bay 1"
    options:
        - schema
        - compliancePreview
        - newProfileTemplate
        - profilePorts:
           enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
           serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - messages
        - transformation:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableNetworks:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableServers
        - availableStorageSystem:
            storageSystemId: "{{storage_system_id}}"
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableStorageSystems:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableTargets

  delegate_to: localhost

- debug: var=server_profiles
- debug: var=server_profile_schema
- debug: var=server_profile_compliance_preview
- debug: var=server_profile_new_profile_template
- debug: var=server_profile_profile_ports
- debug: var=server_profile_messages
- debug: var=server_profile_transformation
- debug: var=server_profile_available_networks
- debug: var=server_profile_available_servers
- debug: var=server_profile_available_storage_system
- debug: var=server_profile_available_storage_systems
- debug: var=server_profile_available_targets
'''

RETURN = '''
server_profiles:
    description: Has all the OneView facts about the Server Profiles.
    returned: Always, but can be null.
    type: dict

server_profile_schema:
    description: Has the facts about the Server Profile schema.
    returned: When requested, but can be null.
    type: dict

server_profile_compliance_preview:
    description:
        Has all the facts about the manual and automatic updates required to make the server profile compliant
        with its template.
    returned: When requested, but can be null.
    type: dict

server_profile_new_profile_template:
    description:
        Has the facts derived from a server profile, which can be used to generate a server profile template.
    returned: When requested, but can be null.
    type: dict

server_profile_profile_ports:
    description: Has the facts about the port model associated with the profile.
    returned: When requested, but can be null.
    type: dict

server_profile_messages:
    description: Has the facts about the profile status messages associated with the profile.
    returned: When requested, but can be null.
    type: dict

server_profile_transformation:
    description:
        Has the facts about the transformation of an existing profile by supplying a new server hardware type
        and/or enclosure group.
    returned: When requested, but can be null.
    type: dict

server_profile_available_networks:
    description:
        Has all the facts about the list of Ethernet networks, Fibre Channel networks and network sets that
        are available to the server profile along with their respective ports.
    returned: When requested, but can be null.
    type: dict

server_profile_available_servers:
    description: Has the facts about the list of available servers.
    returned: When requested, but can be null.
    type: dict

server_profile_available_storage_system:
    description:
        Has the facts about a specific storage system and its associated volumes that are available to
        the server profile.
    returned: When requested, but can be null.
    type: dict

server_profile_available_storage_systems:
    description:
        Has the facts about the list of the storage systems and their associated volumes that are available to
        the server profile.
    returned: When requested, but can be null.
    type: dict

server_profile_available_targets:
    description:
        Has the facts about the target servers and empty device bays that are available for assignment to
        the server profile.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class ServerProfileFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(type='str'),
        uri=dict(type='str'),
        options=dict(type='list'),
        params=dict(type='dict')
    )

    def __init__(self):
        super(ServerProfileFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.server_profiles)

    def execute_module(self):
        ansible_facts = {}
        server_profiles = []

        if self.current_resource:
            server_profiles = [self.current_resource.data]
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            server_profiles = self.resource_client.get_all(**self.facts_params)

        if self.options:
            ansible_facts = self.__gather_option_facts()

        ansible_facts["server_profiles"] = server_profiles

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def __gather_option_facts(self):
        facts = {}

        if self.current_resource:
            if self.options.get('messages'):  # Supported only for API version <= 500
                facts['server_profile_messages'] = self.current_resource.get_messages()

            if self.options.get('transformation'):
                transform_options = self.__get_sub_options(self.options['transformation'])
                facts['server_profile_transformation'] = self.current_resource.get_transformation(**transform_options)

            if self.options.get('compliancePreview'):
                facts['server_profile_compliance_preview'] = self.current_resource.get_compliance_preview()

            if self.options.get('newProfileTemplate'):
                facts['server_profile_new_profile_template'] = self.current_resource.get_new_profile_template()

        if self.options.get('schema'):
            facts['server_profile_schema'] = self.resource_client.get_schema()

        if self.options.get('profilePorts'):
            ports_options = self.__get_sub_options(self.options['profilePorts'])
            facts['server_profile_profile_ports'] = self.resource_client.get_profile_ports(**ports_options)

        if self.options.get('availableNetworks'):
            enets_options = self.__get_sub_options(self.options['availableNetworks'])
            facts['server_profile_available_networks'] = self.resource_client.get_available_networks(**enets_options)

        if self.options.get('availableServers'):  # Supported only for API version <= 1200
            servers_options = self.__get_sub_options(self.options['availableServers'])
            facts['server_profile_available_servers'] = self.resource_client.get_available_servers(**servers_options)

        if self.options.get('availableStorageSystem'):  # Supported only for API version <= 500
            storage_options = self.__get_sub_options(self.options['availableStorageSystem'])
            facts['server_profile_available_storage_system'] = self.resource_client.get_available_storage_system(**storage_options)

        if self.options.get('availableStorageSystems'):  # Supported only for API version <= 500
            storage_options = self.__get_sub_options(self.options['availableStorageSystems'])
            facts['server_profile_available_storage_systems'] = self.resource_client.get_available_storage_systems(**storage_options)

        if self.options.get('availableTargets'):
            target_options = self.__get_sub_options(self.options['availableTargets'])
            facts['server_profile_available_targets'] = self.resource_client.get_available_targets(**target_options)

        return facts

    def __get_sub_options(self, option):
        return option if isinstance(option, dict) else {}


def main():
    ServerProfileFactsModule().run()


if __name__ == '__main__':
    main()
