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
module: oneview_datacenters_facts
short_description: Retrieve facts about the OneView Data Centers.
description:
    - Retrieve facts about the OneView Data Centers.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
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
        - Data Center name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'visualContent'."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=datacenters

- name: Gather paginated, filtered and sorted facts about Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
    params:
      - start: 0
      - count: 3
      - sort: 'name:descending'
      - filter: 'state=Unmanaged'

- debug: var=datacenters

- name: Gather facts about a Data Center by name
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
  delegate_to: localhost

- debug: var=datacenters


- name: Gather facts about the Data Center Visual Content
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
    options:
      - visualContent
  delegate_to: localhost

- debug: var=datacenters
- debug: var=datacenter_visual_content
'''

RETURN = '''
datacenters:
    description: Has all the OneView facts about the Data Centers.
    returned: Always, but can be null.
    type: complex

datacenter_visual_content:
    description: Has facts about the Data Center Visual Content.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class DatacenterFactsModule(object):
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
            "type": 'list'
        },
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
            client = self.oneview_client.datacenters
            ansible_facts = {}

            if self.module.params.get('name'):
                datacenters = client.get_by('name', self.module.params['name'])

                if self.module.params.get('options') and 'visualContent' in self.module.params['options']:
                    if datacenters:
                        ansible_facts['datacenter_visual_content'] = client.get_visual_content(datacenters[0]['uri'])
                    else:
                        ansible_facts['datacenter_visual_content'] = None

                ansible_facts['datacenters'] = datacenters
            else:
                params = self.module.params.get('params')
                get_all_params = transform_list_to_dict(params) if params else {}
                ansible_facts['datacenters'] = client.get_all(**get_all_params)

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    DatacenterFactsModule().run()


if __name__ == '__main__':
    main()
