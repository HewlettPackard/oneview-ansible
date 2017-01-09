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
module: oneview_enclosure_group_facts
short_description: Retrieve facts about one or more of the OneView Enclosure Groups.
description:
    - Retrieve facts about one or more of the Enclosure Groups from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Bruno Souza (@bsouza)"
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
        - Enclosure Group name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Enclosure Group.
          Options allowed:
          'configuration_script' Gets the configuration script for an Enclosure Group."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather paginated, filtered and sorted facts about Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config }}"
    params:
      - start: 0
      - count: 3
      - sort: 'name:descending'
      - filter: 'status=OK'

- debug: var=enclosure_groups

- name: Gather facts about an Enclosure Group by name with configuration script
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
    options:
      - configuration_script
    delegate_to: localhost

- debug: var=enclosure_groups
- debug: var=enclosure_group_script
'''

RETURN = '''
enclosure_groups:
    description: Has all the OneView facts about the Enclosure Groups.
    returned: Always, but can be null.
    type: complex

enclosure_group_script:
    description: The configuration script for an Enclosure Group.
    returned: When requested, but can be null.
    type: string
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class EnclosureGroupFactsModule(object):
    argument_spec = {
        "config": {
            "required": False,
            "type": 'str'},
        "name": {
            "required": False,
            "type": 'str'},
        "options": {
            "required": False,
            "type": "list"
        },
        "params": {
            "required": False,
            "type": "list"
        }}

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
            facts = {}
            name = self.module.params.get('name')

            if name:
                enclosure_groups = self.oneview_client.enclosure_groups.get_by('name', name)
                options = self.module.params.get("options") or []

                if enclosure_groups and "configuration_script" in options:
                    facts["enclosure_group_script"] = self.__get_script(enclosure_groups)
            else:
                params = self.module.params.get('params')
                get_all_params = transform_list_to_dict(params) if params else {}

                enclosure_groups = self.oneview_client.enclosure_groups.get_all(**get_all_params)

            facts["enclosure_groups"] = enclosure_groups
            self.module.exit_json(changed=False, ansible_facts=facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_script(self, enclosure_groups):
        script = None

        if enclosure_groups:
            enclosure_group_uri = enclosure_groups[0]['uri']
            script = self.oneview_client.enclosure_groups.get_script(id_or_uri=enclosure_group_uri)

        return script


def main():
    EnclosureGroupFactsModule().run()


if __name__ == '__main__':
    main()
