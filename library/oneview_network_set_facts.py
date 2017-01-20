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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_network_set_facts
short_description: Retrieve facts about the OneView Network Sets.
description:
    - Retrieve facts about the Network Sets from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
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
        - Network Set name.
      required: false
    options:
      description:
        - "List with options to gather facts about Network Set.
          Option allowed: withoutEthernet
          The option 'withoutEthernet' retrieves the list of network_sets excluding Ethernet networks."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Network Sets
  oneview_network_set_facts:
    config: '{{ config_path }}'

- debug: var=network_sets

- name: Gather paginated, filtered, and sorted facts about Network Sets
  oneview_network_set_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: name='netset001'

- debug: var=network_sets

- name: Gather facts about all Network Sets, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    options:
        - withoutEthernet

- debug: var=network_sets


- name: Gather facts about a Network Set by name
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'

- debug: var=network_sets


- name: Gather facts about a Network Set by name, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'
    options:
        - withoutEthernet

- debug: var=network_sets
'''

RETURN = '''
network_sets:
    description: Has all the OneView facts about the Network Sets.
    returned: Always, but can be empty.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class NetworkSetFactsModule(object):
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
            options = self.__get_options()
            network_sets = None

            if self.module.params.get('name'):
                network_sets = self.__get_network_set_by_name(options)
            else:
                network_sets = self.__get_all_network_sets(options)

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(network_sets=network_sets))

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_all_network_sets(self, options):
        if 'withoutEthernet' in options:
            return self.oneview_client.network_sets.get_all_without_ethernet()
        else:
            params = self.module.params.get('params') or {}
            return self.oneview_client.network_sets.get_all(**params)

    def __get_network_set_by_name(self, options):
        name = self.module.params['name']
        if 'withoutEthernet' in options:
            filter_by_name = "\"'name'='{}'\"".format(name)
            return self.oneview_client.network_sets.get_all_without_ethernet(filter=filter_by_name)
        else:
            return self.oneview_client.network_sets.get_by('name', name)

    def __get_options(self):
        if self.module.params.get('options'):
            return transform_list_to_dict(self.module.params['options'])
        else:
            return {}


def main():
    NetworkSetFactsModule().run()


if __name__ == '__main__':
    main()
