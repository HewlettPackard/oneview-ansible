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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_rack_facts
short_description: Retrieve facts about Rack resources.
description:
    - Gets a list of rack resources. Filter by name can be used to get a specific Rack. If a name is specified, it
      is  allowed to retrieve information about the device topology.
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
        - Rack name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'deviceTopology'."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Racks
  oneview_rack_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=racks

- name: Gather paginated, filtered and sorted facts about Racks
  oneview_rack_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "depth=1000"

- name: Gather facts about a Rack by name
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
  delegate_to: localhost

- debug: var=racks


- name: Gather facts about the topology information for the rack
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
    options:
      - deviceTopology
  delegate_to: localhost

- debug: var=racks
- debug: var=rack_device_topology
'''

RETURN = '''
racks:
    description: Has all the OneView facts about the Racks.
    returned: Always, but can be null.
    type: complex

rack_device_topology:
    description: Retrieves the topology information for the rack resource.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class RackFactsModule(object):
    argument_spec = {
        "config": {
            "required": False,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        },
        "options": {
            "required": False,
            "type": 'list'
        },
        "params": {
            "required": False,
            "type": 'dict'
        }
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
            client = self.oneview_client.racks

            facts = {}

            if self.module.params.get('name'):
                storage_volume_template = client.get_by('name', self.module.params['name'])

                options = self.module.params.get('options')
                if options and 'deviceTopology' in options and len(storage_volume_template) > 0:
                    facts['rack_device_topology'] = client.get_device_topology(storage_volume_template[0]['uri'])
            else:
                params = self.module.params.get('params') or {}
                storage_volume_template = client.get_all(**params)

            facts['racks'] = storage_volume_template

            self.module.exit_json(changed=False,
                                  ansible_facts=facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    RackFactsModule().run()


if __name__ == '__main__':
    main()
