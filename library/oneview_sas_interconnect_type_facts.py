#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_sas_interconnect_type_facts
short_description: Retrieve facts about the OneView SAS Interconnect Types.
description:
    - Retrieve facts about the SAS Interconnect Types from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the SAS Interconnect Type.
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
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
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class SasInterconnectTypeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(SasInterconnectTypeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        if self.module.params.get('name'):
            types = self.oneview_client.sas_interconnect_types.get_by('name', self.module.params.get('name'))
        else:
            types = self.oneview_client.sas_interconnect_types.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(sas_interconnect_types=types))


def main():
    SasInterconnectTypeFactsModule().run()


if __name__ == '__main__':
    main()
