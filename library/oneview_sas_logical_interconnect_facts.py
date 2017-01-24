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
module: oneview_sas_logical_interconnect_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical Interconnects.
description:
    - Retrieve facts about one or more of the OneView SAS Logical Interconnects.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
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
        - SAS Logical Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about SAS Logical Interconnect.
          Options allowed:
          'firmware' get the installed firmware for a SAS Logical Interconnect.
        - These options are valid just when a 'name' is provided. Otherwise it will be ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "status='OK'"
- debug: var=sas_logical_interconnects

- name: Gather facts about a SAS Logical Interconnect by name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather facts about an installed firmware for a SAS Logical Interconnect that matches the specified name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
    options:
      - firmware
  delegate_to: localhost
- debug: var=sas_logical_interconnect_firmware
'''

RETURN = '''
sas_logical_interconnects:
    description: The list of SAS Logical Interconnects.
    returned: Always, but can be null.
    type: list

sas_logical_interconnect_firmware:
    description: The installed firmware for a SAS Logical Interconnect.
    returned: When requested, but can be null.
    type: complex
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasLogicalInterconnectFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            oneview_client = OneViewClient.from_environment_variables()
        else:
            oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.resource_client = oneview_client.sas_logical_interconnects

    def run(self):
        try:
            name = self.module.params["name"]

            ansible_facts = {}

            if name:
                sas_logical_interconnects = self.__get_by_name(name)

                if sas_logical_interconnects:
                    options = self.module.params.get("options")

                    if options:
                        options_facts = self.__gather_option_facts(options, sas_logical_interconnects[0])
                        ansible_facts.update(options_facts)
            else:
                params = self.module.params.get('params') or {}
                sas_logical_interconnects = self.resource_client.get_all(**params)

            ansible_facts['sas_logical_interconnects'] = sas_logical_interconnects

            self.module.exit_json(changed=False, ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_by_name(self, name):
        sas_logical_interconnects = self.resource_client.get_by("name", name)

        return sas_logical_interconnects

    def __gather_option_facts(self, options, resource):
        ansible_facts = {}

        options = transform_list_to_dict(options)

        if options.get('firmware'):
            ansible_facts['sas_logical_interconnect_firmware'] = self.resource_client.get_firmware(resource['uri'])

        return ansible_facts


def main():
    SasLogicalInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
