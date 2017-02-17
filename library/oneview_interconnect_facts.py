#!/usr/bin/python

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
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.common import extract_id_from_uri

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Interconnects.
description:
    - Retrieve facts about one or more of the Interconnects from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          'start': The first item to return, using 0-based indexing.
          'count': The number of resources to return.
          'filter': A general filter/query string to narrow the list of items returned.
          'sort': The sort order of the returned data set."
      required: false
    name:
      description:
        - Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Interconnect.
          Options allowed:
          'nameServers' gets the named servers for an interconnect.
          'statistics' gets the statistics from an interconnect.
          'portStatistics' gets the statistics for the specified port name on an interconnect.
          'subPortStatistics' gets the subport statistics on an interconnect.
          'ports' gets all interconnect ports.
          'port' gets a specific interconnect port."
        - "To gather additional facts it is required inform the Interconnect name. Otherwise, these options will be
          ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"

- debug: var=interconnects

- name: Gather paginated, filtered and sorted facts about Interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "enclosureName='0000A66101'"

- debug: var=interconnects

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'

- debug: var=interconnects


- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - nameServers

- debug: var=interconnects
- debug: var=interconnect_name_servers

- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - statistics

- debug: var=interconnects
- debug: var=interconnect_statistics

- name: Gather facts about statistics for the Port named 'd3' of the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - portStatistics: 'd3'

- debug: var=interconnects
- debug: var=interconnect_port_statistics

- name: Gather facts about statistics for the sub Port number '1' of the Interconnect named 'Enc2, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: 'Enc2, interconnect 2'
    options:
        - subPortStatistics:
            portName: 'd4'
            subportNumber: 1

- debug: var=interconnects
- debug: var=interconnect_subport_statistics

- name: Gather facts about all the Interconnect ports
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - ports

- debug: var=interconnects
- debug: var=interconnect_ports

- name: Gather facts about an Interconnect port
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - port: d1

- debug: var=interconnects
- debug: var=interconnect_port
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
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class InterconnectFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

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
            interconnect_name = self.module.params['name']
            facts = dict()

            if interconnect_name:
                interconnects = self.oneview_client.interconnects.get_by('name', interconnect_name)
                facts['interconnects'] = interconnects

                if interconnects and self.module.params.get('options'):
                    self.__get_options(interconnects, facts)

            else:
                params = self.module.params.get('params') or {}

                facts['interconnects'] = self.oneview_client.interconnects.get_all(**params)

            self.module.exit_json(
                changed=False,
                ansible_facts=facts
            )
        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_options(self, interconnects, facts):

        options = transform_list_to_dict(self.module.params['options'])

        interconnect_uri = interconnects[0]['uri']

        if options.get('nameServers'):
            name_servers = self.oneview_client.interconnects.get_name_servers(interconnect_uri)
            facts['interconnect_name_servers'] = name_servers

        if options.get('statistics'):
            facts['interconnect_statistics'] = self.oneview_client.interconnects.get_statistics(interconnect_uri)

        if options.get('portStatistics'):
            port_name = options['portStatistics']
            port_statistics = self.oneview_client.interconnects.get_statistics(interconnect_uri, port_name)
            facts['interconnect_port_statistics'] = port_statistics

        if options.get('subPortStatistics'):
            facts['interconnect_subport_statistics'] = None
            sub_options = options['subPortStatistics']
            if type(sub_options) is dict and sub_options.get('portName') and sub_options.get('subportNumber'):
                facts['interconnect_subport_statistics'] = self.oneview_client.interconnects.get_subport_statistics(
                    interconnect_uri, sub_options['portName'], sub_options['subportNumber'])

        if options.get('ports'):
            ports = self.oneview_client.interconnects.get_ports(interconnect_uri)
            facts['interconnect_ports'] = ports

        if options.get('port'):
            port_name = options.get('port')
            port_id = "{}:{}".format(extract_id_from_uri(interconnect_uri), port_name)
            port = self.oneview_client.interconnects.get_port(interconnect_uri, port_id)
            facts['interconnect_port'] = port


def main():
    InterconnectFactsModule().run()


if __name__ == '__main__':
    main()
