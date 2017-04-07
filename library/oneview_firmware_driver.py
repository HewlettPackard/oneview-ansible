#!/usr/bin/python

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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_firmware_driver
short_description: Provides an interface to remove Firmware Driver resources.
version_added: "2.3"
description:
    - Provides an interface to remove Firmware Driver resources.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Firmware Driver.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['absent']
    name:
      description:
        - Firmware driver name.
      required: True
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class FirmwareDriverModule(OneViewModuleBase):
    MSG_DELETED = 'Firmware driver deleted successfully.'
    MSG_ALREADY_ABSENT = 'Nothing to do.'

    def __init__(self):
        argument_spec = dict(state=dict(required=True, choices=['absent']),
                             name=dict(required=True, type='str'))

        super(FirmwareDriverModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.firmware_drivers

    def execute_module(self):
        resource = self.get_by_name(self.module.params.get("name"))
        return self.resource_absent(resource)


def main():
    FirmwareDriverModule().run()


if __name__ == '__main__':
    main()
