#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
module: oneview_sas_logical_interconnect
short_description: Manage OneView SAS Logical Interconnect resources.
description:
    - "Provides an interface to manage SAS Logical Interconnect resources."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the SAS Logical Interconnect resources.
              C(compliant) brings the list of SAS Logical Interconnect back to a consistent state.
              C(configuration_updated) asynchronously applies or re-applies the SAS Logical Interconnect configuration
              to all managed interconnects.
              C(firmware_updated) installs firmware to a SAS Logical Interconnect.
              C(drive_enclosure_replaced) replacement operation of a drive enclosure.
              * All of them are non-idempotent.
        choices: ['compliant', 'drive_enclosure_replaced', 'configuration_updated', 'firmware_updated']
        required: true
    data:
      description:
        - List with SAS Logical Interconnect properties and its associated states.
      required: true

notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
'''


EXAMPLES = '''
- name: Update the configuration on the SAS Logical Interconnect
  oneview_sas_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: configuration_updated
    data:
      name: "SAS Logical Interconnect name"
  delegate_to: localhost

- name: Install a firmware to the SAS Logical Interconnect, running the stage operation to upload the firmware
  oneview_sas_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: firmware_updated
    data:
      name: "SAS Logical Interconnect name"
      firmware:
        command: Stage
        sppName: "firmware_driver_name"
        # Can be either the firmware name with "sppName" or the uri with "sppUri", e.g.:
        # sppUri: '/rest/firmware-drivers/<filename>'
  delegate_to: localhost

- name: Replace drive enclosure
  oneview_sas_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: drive_enclosure_replaced
    data:
      name: "SAS Logical Interconnect name"
      replace_drive_enclosure:
        oldSerialNumber: "S46016710000J4524YPT"
        newSerialNumber: "S46016710001J4524YPT"
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its names
  oneview_sas_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: compliant
    data:
      logicalInterconnectNames: ["SAS Logical Interconnect name 1", "SAS Logical Interconnect name 2"]
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its URIs
  oneview_sas_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: compliant
    data:
      logicalInterconnectUris: [
        '/rest/sas-logical-interconnects/16b2990f-944a-449a-a78f-004d8b4e6824',
        '/rest/sas-logical-interconnects/c800b2e4-92bb-44fa-8a46-f71d40737fa5']
  delegate_to: localhost
'''

RETURN = '''
sas_logical_interconnect:
    description: Has the OneView facts about the SAS Logical Interconnect.
    returned: On states 'drive_enclosure_replaced', 'configuration_updated', but can be null.
    type: dict

li_firmware:
    description: Has the OneView facts about the updated Firmware.
    returned: On 'firmware_updated' state, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError


class SasLogicalInterconnectModule(OneViewModule):
    MSG_CONSISTENT = 'SAS Logical Interconnect returned to a consistent state.'
    MSG_CONFIGURATION_UPDATED = 'Configuration on the SAS Logical Interconnect updated successfully.'
    MSG_FIRMWARE_UPDATED = 'Firmware updated successfully.'
    MSG_DRIVE_ENCLOSURE_REPLACED = 'Drive enclosure replaced successfully.'
    MSG_NOT_FOUND = 'SAS Logical Interconnect not found.'
    MSG_NO_OPTIONS_PROVIDED = 'No options provided.'

    def __init__(self):
        additional_arg_spec = dict(
            data=dict(required=True, type='dict'),
            state=dict(
                required=True,
                choices=['compliant', 'drive_enclosure_replaced', 'configuration_updated', 'firmware_updated']
            )
        )

        super(SasLogicalInterconnectModule, self).__init__(additional_arg_spec=additional_arg_spec)

        self.set_resource_object(self.oneview_client.sas_logical_interconnects)

    def execute_module(self):
        if self.state == 'compliant':
            changed, msg, ansible_facts = self.__compliance()

        else:
            if not self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

            if self.state == 'configuration_updated':
                changed, msg, ansible_facts = self.__update_configuration()
            elif self.state == 'firmware_updated':
                changed, msg, ansible_facts = self.__update_firmware()
            elif self.state == 'drive_enclosure_replaced':
                changed, msg, ansible_facts = self.__replace_drive_enclosure()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __compliance(self):
        uris = self.data.get('logicalInterconnectUris')
        if not uris:
            if 'logicalInterconnectNames' not in self.data:
                raise OneViewModuleValueError(self.MSG_NO_OPTIONS_PROVIDED)

            uris = self.__resolve_log_interconnect_names(self.data['logicalInterconnectNames'])

        self.resource_client.update_compliance_all(uris)
        return True, self.MSG_CONSISTENT, {}

    def __resolve_log_interconnect_names(self, interconnectNames):
        uris = []
        for name in interconnectNames:
            li = self.get_by_name(name)
            if not li:
                raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)
            uris.append(li['uri'])

        return uris

    def __update_firmware(self):
        options = self.data['firmware'].copy()
        if 'sppName' in options:
            options['sppUri'] = '/rest/firmware-drivers/' + options.pop('sppName')

        firmware = self.current_resource.update_firmware(options)

        return True, self.MSG_FIRMWARE_UPDATED, dict(li_firmware=firmware)

    def __update_configuration(self):
        result = self.current_resource.update_configuration()

        return True, self.MSG_CONFIGURATION_UPDATED, dict(sas_logical_interconnect=result)

    def __replace_drive_enclosure(self):
        result = self.current_resource.replace_drive_enclosure(
            self.data['replace_drive_enclosure'])

        return True, self.MSG_DRIVE_ENCLOSURE_REPLACED, dict(sas_logical_interconnect=result)


def main():
    SasLogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
