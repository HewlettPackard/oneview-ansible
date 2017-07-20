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
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    name:
      description:
        - Firmware driver name.
      required: False
    data:
      description:
          - List with the Firmware Driver properties.
      required: False
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create the Firmware Driver using names to find the baseline and hotfix firmwares.
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: present
    data:
      customBaselineName: "Service Pack for ProLiant - Custom"
      baselineName: "Service Pack for ProLiant"
      hotfixNames: ['hotfix 1', 'hotfix 2']

- name: Create the Firmware Driver using URIs to find the baseline and hotfix firmwares.
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: present
    data:
      customBaselineName: "Service Pack for ProLiant - Custom"
      baselineUri: "/rest/firmware-driver/SPP1"
      hotfixUris: ['/rest/firmware-driver/hotfix1', '/rest/firmware-driver/hotfix2']

- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import (OneViewModuleBase, HPOneViewException)


class FirmwareDriverModule(OneViewModuleBase):
    MSG_CREATED = 'Firmware driver created successfully.'
    MSG_UPDATED = 'Firmware driver updated successfully.'
    MSG_ALREADY_PRESENT = 'Firmware driver is already present.'
    MSG_DELETED = 'Firmware driver deleted successfully.'
    MSG_ALREADY_ABSENT = 'Firmware driver is already absent.'
    RESOURCE_FACT_NAME = 'firmware_driver'

    def __init__(self):
        argument_spec = dict(state=dict(required=True, choices=['absent', 'present']),
                             name=dict(required=False, type='str'),
                             data=dict(required=False, type='dict'))

        super(FirmwareDriverModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.firmware_drivers

    def execute_module(self):
        data = self.data or {}
        # Checks for the name and data['customBaselineName'] params for a name attribute to the Firmware Driver.
        if not data.get('customBaselineName') and not self.module.params.get('name'):
            msg = 'A "name" parameter or a "customBaselineName" field inside the "data" parameter'
            msg += 'is required for this operation.'
            raise HPOneViewException(msg)

        if data and data.get('customBaselineName'):
            fw_name = data['customBaselineName']
        elif self.module.params.get('name'):
            fw_name = self.module.params['name']

        resource = self.get_by_name(fw_name)

        if self.state == 'present':
            changed, msg, firmware_driver = self.__present(resource)
            return dict(changed=changed, msg=msg, ansible_facts=firmware_driver)
        elif self.state == 'absent':
            return self.resource_absent(resource)

    def __present(self, resource):
        if not resource:
            data = self.__parse_data()
            resource = self.oneview_client.firmware_drivers.create(data)
            return True, self.MSG_CREATED, dict(firmware_driver=resource)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(firmware_driver=resource)

    def __parse_data(self):
        data = self.data.copy()
        # Allow usage of baselineName instead of baselineUri
        if data and data.get('baselineName'):
            baseline_name = data.pop('baselineName', "")
            spp = self.get_by_name(baseline_name)
            if spp:
                data['baselineUri'] = spp['uri']
            else:
                raise HPOneViewException('Baseline SPP named "%s" not found in OneView Appliance.' % baseline_name)

        # Allow usage of hotfixNames instead of hotfixUris
        if data and data.get('hotfixNames'):
            hotfix_names = data.pop('hotfixNames', [])
            data['hotfixUris'] = data.get('hotfixUris') or []
            for hotfix_name in hotfix_names:
                hotfix = self.get_by_name(hotfix_name)
                if hotfix:
                    data['hotfixUris'].append(hotfix['uri'])
                else:
                    raise HPOneViewException('Hotfix named "%s" not found in OneView Appliance.' % hotfix_name)
        return data


def main():
    FirmwareDriverModule().run()


if __name__ == '__main__':
    main()
