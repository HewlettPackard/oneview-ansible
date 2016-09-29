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
module: oneview_firmware_bundle
short_description: Upload OneView Firmware Bundle resources.
description:
    - Upload an SPP ISO image file or a hotfix file to the appliance.
notes:
   - "This module is non-idempotent"
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Firmware Driver resource.
              'present' will ensure that the firmware bundle is at OneView.
        choices: ['present']
    file_path:
      description:
        - The full path of a local file to be loaded.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Ensure that the Firmware Driver is present
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm"

'''

RETURN = '''
firmware_bundle:
    description: Has the facts about the OneView Firmware Bundle.
    returned: Always. Can be null.
    type: complex
'''

FIRMWARE_BUNDLE_UPLOADED = 'Firmware Bundle uploaded sucessfully.'


class FirmwareBundleModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(required=True, choices=['present']),
        file_path=dict(required=True, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        file_path = self.module.params['file_path']

        try:
            new_firmware = self.oneview_client.firmware_bundles.upload(file_path)
            self.module.exit_json(changed=True,
                                  msg=FIRMWARE_BUNDLE_UPLOADED,
                                  ansible_facts=dict(firmware_bundle=new_firmware))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    FirmwareBundleModule().run()


if __name__ == '__main__':
    main()
