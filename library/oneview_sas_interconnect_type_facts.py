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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_sas_interconnect_type_facts
short_description: Retrieve facts about the OneView SAS Interconnect Types.
description:
    - Retrieve facts about the SAS Interconnect Types from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
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
        - Name of the SAS Interconnect Type.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Gather facts about all SAS Interconnect Types
  oneview_sas_interconnect_type_facts:
    config: "{{ config_path }}"

- debug: var=sas_interconnect_types

- name: Gather paginated, filtered and sorted facts about SAS Interconnect Types
  oneview_sas_interconnect_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "enclosureType='SY12000'"

- debug: var=sas_interconnect_types

- name: Gather facts about a SAS Interconnect Type by name
  oneview_sas_interconnect_type_facts:
    config: "{{ config_path }}"
    name: "SAS Interconnect Type Name"

- debug: var=sas_interconnect_types
'''

RETURN = '''
sas_interconnect_types:
    description: Has all the OneView facts about the SAS Interconnect Types.
    returned: Always, but can be null.
    type: complex
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasInterconnectTypeFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
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
            if self.module.params.get('name'):
                types = self.oneview_client.sas_interconnect_types.get_by('name', self.module.params.get('name'))
            else:
                params = self.module.params.get('params') or {}
                types = self.oneview_client.sas_interconnect_types.get_all(**params)

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(sas_interconnect_types=types))

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    SasInterconnectTypeFactsModule().run()


if __name__ == '__main__':
    main()
