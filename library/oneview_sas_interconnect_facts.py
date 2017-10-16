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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: oneview_sas_interconnect_facts
short_description: Retrieve facts about the OneView SAS Interconnects.
description:
    - Retrieve facts about the OneView SAS Interconnects.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - SAS Interconnect name.
      required: false
notes:
    - This resource is only available on HPE Synergy
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"

- name: Gather paginated, filtered and sorted facts about SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "softResetState='Normal'"

- name: Gather facts about a SAS Interconnect by name
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    name: "0000A66103, interconnect 1"
'''

RETURN = '''
sas_interconnects:
    description: The list of SAS Interconnects.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.oneview import OneViewModuleBase


class SasInterconnectFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(SasInterconnectFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.sas_interconnects

    def execute_module(self):
        facts = dict()
        name = self.module.params["name"]

        if name:
            facts['sas_interconnects'] = self.resource_client.get_by('name', name)
        else:
            facts['sas_interconnects'] = self.resource_client.get_all(**self.facts_params)

        return dict(ansible_facts=facts)


def main():
    SasInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
