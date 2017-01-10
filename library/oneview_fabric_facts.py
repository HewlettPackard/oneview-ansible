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

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_fabric_facts
short_description: Retrieve the facts about one or more of the OneView Fabrics.
description:
    - Retrieve the facts about one or more of the Fabrics from OneView.
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
        - Fabric name.
      required: false
    options:
      description:
            - "List with options to gather additional facts about an Fabrics and related resources.
          Options allowed: reservedVlanRange."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather paginated, filtered and sorted facts about Fabrics
  oneview_fabric_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=DefaultFabric'

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics

- name: Gather facts about a Fabric by name with options
  oneview_fabric_facts:
    config: "{{ config }}"
    name: DefaultFabric
    options:
      - reservedVlanRange          # optional

- debug: var=fabrics
'''

RETURN = '''
fabrics:
    description: Has all the OneView facts about the Fabrics.
    returned: Always, but can be null.
    type: complex
fabric_reserved_vlan_range:
    description: Has all the OneView facts about the reserved VLAN range
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class FabricFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            ansible_facts = {}
            name = self.module.params['name']
            if name:
                fabrics = self.oneview_client.fabrics.get_by('name', name)

                if self.module.params.get('options') and fabrics:
                    ansible_facts = self.__gather_optional_facts(self.module.params['options'], fabrics[0])
            else:
                params = self.module.params.get('params') or {}

                fabrics = self.oneview_client.fabrics.get_all(**params)

            ansible_facts['fabrics'] = fabrics

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(ansible_facts))

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __gather_optional_facts(self, options, fabric):
        options = transform_list_to_dict(options)

        fabric_client = self.oneview_client.fabrics
        ansible_facts = {}

        if options.get('reservedVlanRange'):
            ansible_facts['fabric_reserved_vlan_range'] = fabric_client.get_reserved_vlan_range(fabric['uri'])

        return ansible_facts


def main():
    FabricFactsModule().run()


if __name__ == '__main__':
    main()
