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
module: oneview_firmware_driver_facts
short_description: Retrieve the facts about one or more of the OneView Firmware Drivers.
description:
    - Retrieve the facts about one or more of the Firmware Drivers from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(sort): The sort order of the returned data set."
      required: false
    name:
      description:
        - Firmware driver name.
      required: false
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"

- debug: var=firmware_drivers

- name: Gather paginated, filtered and sorted facts about Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=firmware_drivers
'''

RETURN = '''
firmware_drivers:
    description: Has all the OneView facts about the Firmware Drivers.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class FirmwareDriverFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')

        )
        super(FirmwareDriverFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.firmware_drivers

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            result = self.resource_client.get_by('name', name)
        else:
            result = self.resource_client.get_all(**self.facts_params)

        return dict(
            changed=False,
            ansible_facts=dict(firmware_drivers=result)
        )


def main():
    FirmwareDriverFactsModule().run()


if __name__ == '__main__':
    main()
