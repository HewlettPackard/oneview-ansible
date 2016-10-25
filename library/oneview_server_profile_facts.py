#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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

from ansible.module_utils.basic import *
try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import transform_list_to_dict

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_server_profile_facts
short_description: Retrieve facts about the OneView Server Profiles.
description:
    - Retrieve facts about the Server Profile from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Server Profile name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Server Profile related resources.
          Options allowed: schema, compliancePreview, profilePorts, messages, transformation, available_networks,
          available_servers, available_storage_system, available_storage_systems, available_targets"
        - "To gather facts about 'compliancePreview', 'messages' and 'transformation' it is required inform the Server
          Profile name. Otherwise, these options will be ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Server Profiles
  oneview_server_profile_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about a Server Profile by name
  oneview_server_profile_facts:
    config: "{{ config }}"
    name: "WebServer-1"
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about available servers and bays for a given enclosure group and server hardware type
  oneview_server_profile_facts:
    config: "{{ config }}"
    options:
      - availableTargets:
          enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
          serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
  delegate_to: localhost

- debug: var=server_profile_available_targets


- name: Gather all facts about a Server Profile
  oneview_server_profile_facts:
   config: "{{ config }}"
   name : "Encl1, bay 1"
   options:
        - schema
        - compliancePreview
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
    type: complex

server_profile_schema:
    description: Has the facts about the Server Profile schema.
    returned: When requested, but can be null.
    type: complex

server_profile_compliance_preview:
    description:
        Has all the facts about the manual and automatic updates required to make the server profile compliant
        with its template.
    returned: When requested, but can be null.
    type: complex

server_profile_profile_ports:
    description: Has the facts about the port model associated.
    returned: When requested, but can be null.
    type: complex

server_profile_messages:
    description: Has the facts about the profile status messages associated with the profile.
    returned: When requested, but can be null.
    type: complex

server_profile_transformation:
    description:
        Has the facts about the transformation of an existing profile by supplying a new server hardware type
        and/or enclosure group.
    returned: When requested, but can be null.
    type: complex

server_profile_available_networks:
    description:
        Has all the facts about the list of Ethernet networks, Fibre Channel networks and network sets that
        are available to the server profile along with their respective ports.
    returned: When requested, but can be null.
    type: complex

server_profile_available_servers:
    description: Has the facts about the list of available servers.
    returned: When requested, but can be null.
    type: complex

server_profile_available_storage_system:
    description:
        Has the facts about a specific storage system and its associated volumes that are available to
        the server profile.
    returned: When requested, but can be null.
    type: complex

server_profile_available_storage_systems:
    description:
        Has the facts about the list of the storage systems and their associated volumes that are available to
        the server profile.
    returned: When requested, but can be null.
    type: complex

server_profile_available_targets:
    description:
        Has the facts about the target servers and empty device bays that are available for assignment to
        the server profile.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerProfileFactsModule(object):
    argument_spec = {
        "config": {"required": False, "type": 'str'},
        "name": {"required": False, "type": 'str'},
        "options": {"required": False, "type": 'list'}
    }

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:

            ansible_facts = {}
            server_profile_uri = None

            if self.module.params.get('name'):
                server_profiles = self.oneview_client.server_profiles.get_by("name", self.module.params['name'])
                if len(server_profiles) > 0:
                    server_profile_uri = server_profiles[0]['uri']
            else:
                server_profiles = self.oneview_client.server_profiles.get_all()

            if self.module.params.get('options'):
                ansible_facts = self.__gather_option_facts(self.module.params['options'], server_profile_uri)

            ansible_facts["server_profiles"] = server_profiles

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_option_facts(self, options, profile_uri):

        options = transform_list_to_dict(options)

        client = self.oneview_client.server_profiles
        facts = {}

        if profile_uri:
            if options.get('messages'):
                facts['server_profile_messages'] = client.get_messages(profile_uri)

            if options.get('transformation'):
                transform_options = self.__get_sub_options(options['transformation'])
                facts['server_profile_transformation'] = client.get_transformation(profile_uri, **transform_options)

            if options.get('compliancePreview'):
                facts['server_profile_compliance_preview'] = client.get_compliance_preview(profile_uri)

        if options.get('schema'):
            facts['server_profile_schema'] = client.get_schema()

        if options.get('profilePorts'):
            ports_options = self.__get_sub_options(options['profilePorts'])
            facts['server_profile_profile_ports'] = client.get_profile_ports(**ports_options)

        if options.get('availableNetworks'):
            enets_options = self.__get_sub_options(options['availableNetworks'])
            facts['server_profile_available_networks'] = client.get_available_networks(**enets_options)

        if options.get('availableServers'):
            servers_options = self.__get_sub_options(options['availableServers'])
            facts['server_profile_available_servers'] = client.get_available_servers(**servers_options)

        if options.get('availableStorageSystem'):
            storage_options = self.__get_sub_options(options['availableStorageSystem'])
            facts['server_profile_available_storage_system'] = client.get_available_storage_system(**storage_options)

        if options.get('availableStorageSystems'):
            storage_options = self.__get_sub_options(options['availableStorageSystems'])
            facts['server_profile_available_storage_systems'] = client.get_available_storage_systems(**storage_options)

        if options.get('availableTargets'):
            target_options = self.__get_sub_options(options['availableTargets'])
            facts['server_profile_available_targets'] = client.get_available_targets(**target_options)

        return facts

    def __get_sub_options(self, option):
        return option if type(option) is dict else {}


def main():
    ServerProfileFactsModule().run()


if __name__ == '__main__':
    main()
