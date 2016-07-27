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
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_firmware_driver
short_description: Provides an interface to remove Firmware Drivers resources.
description:
    - Provides an interface to remove Firmware Drivers resources.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Firmware Driver.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['absent']
    name:
      description:
        - Firmware driver name.
      required: True
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"
'''

FIRMWARE_DRIVER_DELETED = 'Firmware driver deleted successfully.'
FIRMWARE_DRIVER_ALREADY_ABSENT = 'Nothing to do.'


class FirmwareDriverModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['absent']
        ),
        name=dict(required=True, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.firmware_drivers

    def run(self):
        try:
            name = self.module.params["name"]
            resource = self.__get_by_name(name)

            if resource:
                self.resource_client.delete(resource)
                self.module.exit_json(changed=True, msg=FIRMWARE_DRIVER_DELETED)
            else:
                self.module.exit_json(changed=False, msg=FIRMWARE_DRIVER_ALREADY_ABSENT)
        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        result = self.resource_client.get_by('name', name) or [None]
        return result[0]


def main():
    FirmwareDriverModule().run()


if __name__ == '__main__':
    main()
