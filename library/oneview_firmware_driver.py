#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
module: oneview_firmware_driver
short_description: Provides an interface to remove Firmware Driver resources.
version_added: "2.4"
description:
    - Provides an interface to remove Firmware Driver resources.
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.6.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
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
      required: True
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create the Firmware Driver
  oneview_firmware_driver:
    config: "{{ config }}"
    state: present
    data:
      customBaselineName: "{{ firmware_name }}"
      baselineName: "{{ baseline_firmware_name }}"
      hotfixNames: "{{ hotfix_firmware_list }}"
  delegate_to: localhost

- name: Create the Firmware Driver if already present
  oneview_firmware_driver:
    config: "{{ config }}"
    state: present
    data:
      customBaselineName: "{{ firmware_name }}"
      baselineName: "{{ baseline_firmware_name }}"
      hotfixNames: "{{ hotfix_firmware_list }}"
  delegate_to: localhost

- name: Delete the Firmware Driver
  oneview_firmware_driver:
    config: "{{ config }}"
    state: absent
    name: "{{ firmware_name }}"
  delegate_to: localhost

- name: Do nothing when Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config }}"
    state: absent
    name: "{{ firmware_name }}"
  delegate_to: localhost
'''

RETURN = '''
firmware_drivers:
    description: Has the facts about the OneView firmware driver.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleException
from copy import deepcopy


class FirmwareDriverModule(OneViewModule):
    MSG_CREATED = 'Firmware driver created successfully.'
    MSG_ALREADY_PRESENT = 'Firmware driver is already present.'
    MSG_DELETED = 'Firmware driver deleted successfully.'
    MSG_ALREADY_ABSENT = 'Firmware driver is already absent.'
    RESOURCE_FACT_NAME = 'firmware_drivers'

    def __init__(self):
        argument_spec = dict(state=dict(required=True, choices=['absent', 'present']),
                             name=dict(required=False, type='str'),
                             data=dict(required=False, type='dict'))

        super(FirmwareDriverModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.firmware_drivers)

    def execute_module(self):
        data = deepcopy(self.data) or {}
        # Checks for the name and data['customBaselineName'] params for a name attribute to the Firmware Driver.
        if not data.get('customBaselineName') and not self.module.params.get('name'):
            msg = "A 'name' parameter or a 'customBaselineName' field inside the 'data' parameter "
            msg += "is required for this operation."
            raise OneViewModuleException(msg)

        # name parameter takes priority over customBaselineName
        if data.get('customBaselineName') and not self.module.params.get('name'):
            self.current_resource = self.resource_client.get_by_name(data['customBaselineName'])

        if self.state == 'present':
            changed, msg, firmware_driver = self.__present(data)
            return dict(changed=changed, msg=msg, ansible_facts=firmware_driver)
        elif self.state == 'absent':
            return self.resource_absent()

    def __present(self, data):
        if not self.current_resource:
            data = self.__parse_data()
            self.current_resource = self.resource_client.create(data)
            return True, self.MSG_CREATED, dict(firmware_driver=self.current_resource.data)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(firmware_driver=self.current_resource.data)

    def __parse_data(self):
        data = deepcopy(self.data)
        # Allow usage of baselineName instead of baselineUri
        if data.get('baselineName'):
            baseline_name = data.pop('baselineName', "")
            spp = self.resource_client.get_by_name(baseline_name)
            if spp:
                data['baselineUri'] = spp.data['uri']
            else:
                raise OneViewModuleException("Baseline SPP named '{}' not found in OneView Appliance.".format(baseline_name))

        # Allow usage of hotfixNames instead of hotfixUris
        if data and data.get('hotfixNames'):
            hotfix_names = data.pop('hotfixNames', [])
            data['hotfixUris'] = data.get('hotfixUris', [])
            for hotfix_name in hotfix_names:
                hotfix = self.resource_client.get_by_name(hotfix_name)
                if hotfix:
                    data['hotfixUris'].append(hotfix.data['uri'])
                else:
                    raise OneViewModuleException("Hotfix named '{}' not found in OneView Appliance.".format(hotfix_name))
        return data


def main():
    FirmwareDriverModule().run()


if __name__ == '__main__':
    main()
