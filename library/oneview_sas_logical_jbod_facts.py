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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_sas_logical_jbod_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical JBODs.
description:
    - Retrieve facts about one or more of the SAS Logical JBODs from OneView.
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
        - Name of SAS Logical JBODs.
      required: false
    options:
      description:
        - "List with options to gather additional facts about SAS Logical JBODs and related resources.
          Options allowed: drives."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical JBODs
    oneview_sas_logical_jbod_facts:
    config: "{{ config_path }}"

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
    type: complex

sas_logical_jbod_drives:
    description: Has all the OneView facts about the list of drives allocated to a SAS logical JBOD.
    returned: Always, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasLogicalJbodFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
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

            if self.module.params['name']:
                name = self.module.params['name']
                sas_logical_jbods = self.oneview_client.sas_logical_jbods.get_by('name', name)

                if self.module.params.get('options') and sas_logical_jbods:
                    ansible_facts = self.__gather_optional_facts(self.module.params['options'], sas_logical_jbods[0])
            else:
                params = self.module.params.get('params') or {}
                sas_logical_jbods = self.oneview_client.sas_logical_jbods.get_all(**params)

            ansible_facts['sas_logical_jbods'] = sas_logical_jbods

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_optional_facts(self, options, sas_logical_jbod):
        options = transform_list_to_dict(options)
        ansible_facts = {}
        sas_logical_jbods_client = self.oneview_client.sas_logical_jbods

        if options.get('drives'):
            ansible_facts['sas_logical_jbod_drives'] = sas_logical_jbods_client.get_drives(sas_logical_jbod['uri'])

        return ansible_facts


def main():
    SasLogicalJbodFactsModule().run()


if __name__ == '__main__':
    main()
