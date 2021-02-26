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
module: oneview_appliance_ssh_access_facts
short_description: Retrieve the facts about the OneView appliance SSH access configuration.
description:
    - Retrieve the facts about the OneView appliance SSH access configuration.
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.6.0"
author:
    "Shanmugam M (@SHANDCRUZ)"
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the Appliance SSH Access
  oneview_appliance_ssh_access_facts:
    config: "{{ config file path}}"
  delegate_to: localhost

- debug: var=appliance_ssh_access
'''

RETURN = '''
appliance_ssh_access:
    description: Has all the OneView facts about the Appliance SSH access.
    returned: Always.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class ApplianceSshAccessFactsModule(OneViewModule):
    def __init__(self):
        super(ApplianceSshAccessFactsModule, self).__init__(additional_arg_spec=dict())
        self.set_resource_object(self.oneview_client.appliance_ssh_access)

    def execute_module(self):
        appliance_ssh_access = self.resource_client.get_all()
        appliance_ssh_access = appliance_ssh_access.data
        return dict(changed=False,
                    ansible_facts=dict(appliance_ssh_access=appliance_ssh_access))


def main():
    ApplianceSshAccessFactsModule().run()


if __name__ == '__main__':
    main()
