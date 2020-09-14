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
module: oneview_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Interconnects.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the Interconnects from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Interconnect.
          Options allowed:
          C(nameServers) gets the named servers for an interconnect.
          C(statistics) gets the statistics from an interconnect.
          C(portStatistics) gets the statistics for the specified port name on an interconnect.
          C(subPortStatistics) gets the subport statistics on an interconnect.
          C(ports) gets all interconnect ports.
          C(port) gets a specific interconnect port.
          C(pluggableModuleInformation) gets all the SFP information."
        - "To gather additional facts it is required inform the Interconnect name. Otherwise, these options will be
          ignored."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200

- debug: var=interconnects

- name: Gather paginated, filtered and sorted facts about Interconnects
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "enclosureName='0000A66101'"

- debug: var=interconnects

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'

- debug: var=interconnects


- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - nameServers

- debug: var=interconnects
- debug: var=interconnect_name_servers

- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - statistics

- debug: var=interconnects
- debug: var=interconnect_statistics

- name: Gather facts about statistics for the Port named 'd3' of the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - portStatistics: 'd3'

- debug: var=interconnects
- debug: var=interconnect_port_statistics

- name: Gather facts about statistics for the sub Port number '1' of the Interconnect named 'Enc2, interconnect 2'
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: 'Enc2, interconnect 2'
    options:
        - subPortStatistics:
            portName: 'd4'
            subportNumber: 1

- debug: var=interconnects
- debug: var=interconnect_subport_statistics

- name: Gather facts about all the Interconnect ports
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - ports

- debug: var=interconnects
- debug: var=interconnect_ports

- name: Gather facts about an Interconnect port
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - port: d1

- debug: var=interconnects
- debug: var=interconnect_port

- name: Gather facts about all the SFPs plugged
  oneview_interconnect_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: '0000A66102, interconnect 2'
    options:
        - pluggableModuleInformation

- debug: var=interconnects
- debug: var=interconnect_pluggable_module_information

'''

RETURN = '''
interconnects:
    description: The list of interconnects.
    returned: Always, but can be null.
    type: list

interconnect_name_servers:
    description: The named servers for an interconnect.
    returned: When requested, but can be null.
    type: list

interconnect_statistics:
    description: Has all the OneView facts about the Interconnect Statistics.
    returned: When requested, but can be null.
    type: dict

interconnect_port_statistics:
    description: Statistics for the specified port name on an interconnect.
    returned: When requested, but can be null.
    type: dict

interconnect_subport_statistics:
    description: The subport statistics on an interconnect.
    returned: When requested, but can be null.
    type: dict

interconnect_ports:
    description: All interconnect ports.
    returned: When requested, but can be null.
    type: list

interconnect_port:
    description: The interconnect port.
    returned: When requested, but can be null.
    type: dict

interconnect_pluggable_module_information:
    description: The plugged SFPs information.
    returned: When requested, but can be null.
    type: list
'''

from ansible.module_utils.oneview import OneViewModule
from hpeOneView.resources.resource import extract_id_from_uri


class InterconnectFactsModule(OneViewModule):
    MSG_INTERCONNECT_NOT_FOUND = 'Interconnect not found'

    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(InterconnectFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.interconnects)

    def execute_module(self):
        facts = dict()

        if self.current_resource:
            facts['interconnects'] = [self.current_resource.data]

            if self.module.params.get('options'):
                self.__get_options(facts)
        else:
            facts['interconnects'] = self.resource_client.get_all(**self.facts_params)

        return dict(
            changed=False,
            ansible_facts=facts
        )

    def __get_options(self, facts):
        if self.options.get('nameServers'):
            name_servers = self.current_resource.get_name_servers()
            facts['interconnect_name_servers'] = name_servers

        if self.options.get('statistics'):
            facts['interconnect_statistics'] = self.current_resource.get_statistics()

        if self.options.get('portStatistics'):
            port_name = self.options['portStatistics']
            port_statistics = self.current_resource.get_statistics(port_name)
            facts['interconnect_port_statistics'] = port_statistics

        if self.options.get('subPortStatistics'):
            facts['interconnect_subport_statistics'] = None
            sub_options = self.options['subPortStatistics']
            if isinstance(sub_options, dict) and sub_options.get('portName') and sub_options.get('subportNumber'):
                facts['interconnect_subport_statistics'] = self.current_resource.get_subport_statistics(
                    sub_options['portName'], sub_options['subportNumber'])

        if self.options.get('ports'):
            ports = self.current_resource.get_ports()
            facts['interconnect_ports'] = ports

        if self.options.get('port'):
            port_name = self.options.get('port')
            port_id = "{}:{}".format(extract_id_from_uri(self.current_resource.data['uri']), port_name)
            port = self.current_resource.get_port(port_id)
            facts['interconnect_port'] = port

        if self.options.get('pluggableModuleInformation'):
            sfp_info = self.current_resource.get_pluggable_module_information()
            facts['interconnect_pluggable_module_information'] = sfp_info


def main():
    InterconnectFactsModule().run()


if __name__ == '__main__':
    main()
