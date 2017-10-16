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
---
module: oneview_sas_logical_jbod_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical JBODs.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the SAS Logical JBODs from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of SAS Logical JBODs.
      required: false
    options:
      description:
        - "List with options to gather additional facts about SAS Logical JBODs and related resources.
          Options allowed: C(drives)."
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical JBODs
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"

- debug: var=sas_logical_jbods

- name: Gather paginated, filtered and sorted facts about SAS Logical JBODs
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "state='Configured'"

- debug: var=sas_logical_jbods

- name: Gather facts about a SAS Logical JBOD by name
  oneview_sas_logical_jbod_facts:
    config: "{{ config_path }}"
    name: "Name of the SAS Logical JBOD"

- debug: var=sas_logical_jbods

- name: Gather facts about a SAS Logical JBOD by name, with the list of drives allocated
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"
    name: "{{ sas_logical_jbod_name }}"
    options:
      - drives

- debug: var=sas_logical_jbods
- debug: var=sas_logical_jbod_drives
'''

RETURN = '''
sas_logical_jbods:
    description: Has all the OneView facts about the SAS Logical JBODs.
    returned: Always, but can be null.
    type: dict

sas_logical_jbod_drives:
    description: Has all the OneView facts about the list of drives allocated to a SAS logical JBOD.
    returned: Always, but can be null.
    type: dict
'''


from ansible.module_utils.oneview import OneViewModuleBase


class SasLogicalJbodFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(SasLogicalJbodFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        ansible_facts = {}

        if self.module.params['name']:
            name = self.module.params['name']
            sas_logical_jbods = self.oneview_client.sas_logical_jbods.get_by('name', name)

            if self.module.params.get('options') and sas_logical_jbods:
                ansible_facts = self.__gather_optional_facts(self.module.params['options'], sas_logical_jbods[0])
        else:
            sas_logical_jbods = self.oneview_client.sas_logical_jbods.get_all(**self.facts_params)

        ansible_facts['sas_logical_jbods'] = sas_logical_jbods

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options, sas_logical_jbod):
        ansible_facts = {}
        sas_logical_jbods_client = self.oneview_client.sas_logical_jbods

        if self.options.get('drives'):
            ansible_facts['sas_logical_jbod_drives'] = sas_logical_jbods_client.get_drives(sas_logical_jbod['uri'])

        return ansible_facts


def main():
    SasLogicalJbodFactsModule().run()


if __name__ == '__main__':
    main()
