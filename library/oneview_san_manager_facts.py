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

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_san_manager_facts
short_description: Retrieve facts about one or more of the OneView SAN Managers.
description:
    - Retrieve facts about one or more of the SAN Managers from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    provider_display_name:
      description:
        - Provider Display Name.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           'start': The first item to return, using 0-based indexing.
           'count': The number of resources to return.
           'query': A general query string to narrow the list of resources returned.
           'sort': The sort order of the returned data set."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all SAN Managers
    oneview_san_manager_facts:
    config: "{{ config_path }}"

- debug: var=san_managers

- name: Gather paginated, filtered and sorted facts about SAN Managers
  oneview_san_manager_facts:
  config: "{{ config_path }}"
  params:
    start: 0
    count: 3
    sort: name:ascending
    query: isInternal eq false
  delegate_to: localhost

- debug: var=san_managers

- name: Gather facts about a SAN Manager by provider display name
    oneview_san_manager_facts:
    config: "{{ config_path }}"
    provider_display_name: "Brocade Network Advisor"

- debug: var=san_managers
'''

RETURN = '''
san_managers:
    description: Has all the OneView facts about the SAN Managers.
    returned: Always, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SanManagerFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        provider_display_name=dict(required=False, type='str'),
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
            if self.module.params.get('provider_display_name'):
                provider_display_name = self.module.params['provider_display_name']
                san_manager = self.oneview_client.san_managers.get_by_provider_display_name(provider_display_name)
                if san_manager:
                    resources = [san_manager]
                else:
                    resources = []
            else:
                params = self.module.params.get('params') or {}
                resources = self.oneview_client.san_managers.get_all(**params)

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(san_managers=resources))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    SanManagerFactsModule().run()


if __name__ == '__main__':
    main()
