#!/usr/bin/python
# -*- coding: utf-8 -*-
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

DOCUMENTATION = """
---
module: oneview_sas_logical_interconnect
short_description: Manage OneView SAS Logical Interconnect resources.
description:
    - Provides an interface to manage SAS Logical Interconnect resources.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the SAS Logical Interconnect resource.
              'compliant' brings the list of SAS Logical Interconnect back to a consistent state.
              'configuration_updated' asynchronously applies or re-applies the SAS Logical Interconnect configuration
              to all managed interconnects.
              'firmware_updated' installs firmware to a SAS Logical Interconnect.
              'drive_enclosure_replaced' replacement operation of a drive enclosure.
              * All of them are non-idempotent.
        choices: ['compliant', 'drive_enclosure_replaced', 'configuration_updated', 'firmware_updated']
    data:
      description:
        - List with the options.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
"""

EXAMPLES = """
- name: Update the configuration on the SAS Logical Interconnect
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: configuration_updated
    data:
      name: "SAS Logical Interconnect name"
  delegate_to: localhost

- name: Install a firmware to the SAS Logical Interconnect, running the stage operation to upload the firmware
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
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
    config: "{{ config }}"
    state: drive_enclosure_replaced
    data:
      name: "SAS Logical Interconnect name"
      replace_drive_enclosure:
        oldSerialNumber: "S46016710000J4524YPT"
        newSerialNumber: "S46016710001J4524YPT"
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its names
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: compliant
    data:
      logicalInterconnectNames: ["SAS Logical Interconnect name 1", "SAS Logical Interconnect name 2"]
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its URIs
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: compliant
    data:
      logicalInterconnectUris: [
        '/rest/sas-logical-interconnects/16b2990f-944a-449a-a78f-004d8b4e6824',
        '/rest/sas-logical-interconnects/c800b2e4-92bb-44fa-8a46-f71d40737fa5']
  delegate_to: localhost
"""

RETURN = """
sas_logical_interconnect:
    description: Has the OneView facts about the SAS Logical Interconnect.
    returned: On states 'drive_enclosure_replaced', 'configuration_updated', but can be null.
    type: complex

li_firmware:
    description: Has the OneView facts about the updated Firmware.
    returned: On 'firmware_updated' state, but can be null.
    type: complex
"""

SAS_LOGICAL_INTERCONNECT_CONSISTENT = 'SAS Logical Interconnect returned to a consistent state.'
SAS_LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED = 'Configuration on the SAS Logical Interconnect updated successfully.'
SAS_LOGICAL_INTERCONNECT_FIRMWARE_UPDATED = 'Firmware updated successfully.'
SAS_LOGICAL_INTERCONNECT_DRIVE_ENCLOSURE_REPLACED = 'Drive enclosure replaced successfully.'
SAS_LOGICAL_INTERCONNECT_NOT_FOUND = 'SAS Logical Interconnect not found.'
SAS_LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED = 'No options provided.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasLogicalInterconnectModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['compliant', 'drive_enclosure_replaced', 'configuration_updated', 'firmware_updated']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            changed, msg, ansible_facts = False, '', {}

            if state == 'compliant':
                changed, msg, ansible_facts = self.__compliance(data)
            else:

                resource = self.__get_log_interconnect_by_name(data['name'])

                if not resource:
                    raise Exception(SAS_LOGICAL_INTERCONNECT_NOT_FOUND)

                uri = resource['uri']

                if state == 'configuration_updated':
                    changed, msg, ansible_facts = self.__update_configuration(uri)
                elif state == 'firmware_updated':
                    changed, msg, ansible_facts = self.__update_firmware(uri, data)
                elif state == 'drive_enclosure_replaced':
                    changed, msg, ansible_facts = self.__replace_drive_enclosure(uri, data)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __compliance(self, data):

        uris = data.get('logicalInterconnectUris')

        if not uris:
            if 'logicalInterconnectNames' not in data:
                raise Exception(SAS_LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED)

            uris = self.__resolve_log_interconnect_names(data['logicalInterconnectNames'])

        self.oneview_client.sas_logical_interconnects.update_compliance_all(uris)
        return True, SAS_LOGICAL_INTERCONNECT_CONSISTENT, {}

    def __get_log_interconnect_by_name(self, name):
        resource = self.oneview_client.sas_logical_interconnects.get_by("name", name)
        if resource:
            return resource[0]
        else:
            return None

    def __resolve_log_interconnect_names(self, interconnectNames):
        uris = []
        for name in interconnectNames:
            li = self.__get_log_interconnect_by_name(name)
            if not li:
                raise Exception(SAS_LOGICAL_INTERCONNECT_NOT_FOUND)
            uris.append(li['uri'])

        return uris

    def __update_firmware(self, uri, data):
        options = data['firmware'].copy()
        if 'sppName' in options:
            options['sppUri'] = '/rest/firmware-drivers/' + options.pop('sppName')

        firmware = self.oneview_client.sas_logical_interconnects.update_firmware(options, uri)

        return True, SAS_LOGICAL_INTERCONNECT_FIRMWARE_UPDATED, dict(li_firmware=firmware)

    def __update_configuration(self, uri):
        result = self.oneview_client.sas_logical_interconnects.update_configuration(uri)

        return True, SAS_LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED, dict(sas_logical_interconnect=result)

    def __replace_drive_enclosure(self, uri, data):
        result = self.oneview_client.sas_logical_interconnects.replace_drive_enclosure(
            data['replace_drive_enclosure'],
            uri)

        return True, SAS_LOGICAL_INTERCONNECT_DRIVE_ENCLOSURE_REPLACED, dict(sas_logical_interconnect=result)


def main():
    SasLogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
