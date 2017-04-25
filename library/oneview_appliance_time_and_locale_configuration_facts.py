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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_appliance_time_and_locale_configuration_facts
short_description: Retrieve the facts about the OneView appliance time and locale configuration.
description:
    - Retrieve the facts about the OneView appliance time and locale configuration.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    "Thiago Miotto (@tmiotto)"
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about the Appliance time and locale configuration
  oneview_appliance_time_and_locale_configuration_facts:
    config: "{{ config_file_path }}"

- debug: var=appliance_time_and_locale_configuration
'''

RETURN = '''
appliance_time_and_locale_configuration:
    description: Has all the OneView facts about the Appliance time and locale configuration.
    returned: Always.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class ApplianceTimeAndLocaleConfigurationFactsModule(OneViewModuleBase):
    def __init__(self):
        super(ApplianceTimeAndLocaleConfigurationFactsModule, self).__init__(additional_arg_spec=dict())

    def execute_module(self):
        appliance_time_and_locale_configuration = self.oneview_client.appliance_time_and_locale_configuration.get()
        return dict(changed=False,
                    ansible_facts=dict(appliance_time_and_locale_configuration=appliance_time_and_locale_configuration))


def main():
    ApplianceTimeAndLocaleConfigurationFactsModule().run()


if __name__ == '__main__':
    main()
