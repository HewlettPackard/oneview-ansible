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
module: oneview_logical_enclosure
short_description: Manage OneView Logical Enclosure resources.
description:
    - Provides an interface to manage Logical Enclosure resources. Can create, update, update firmware, perform dump,
      update configuration script, reapply configuration, update from group, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Enclosure resource.
              C(present) ensures data properties are compliant with OneView. You can rename the enclosure providing
              an attribute C(newName).
              C(firmware_updated) updates the firmware for the Logical Enclosure.
              C(script_updated) updates the Logical Enclosure configuration script.
              C(dumped) generates a support dump for the Logical Enclosure.
              C(reconfigured) reconfigures all enclosures associated with a logical enclosure.
              C(updated_from_group) makes the logical enclosure consistent with the enclosure group.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'firmware_updated', 'script_updated', 'dumped', 'reconfigured', 'updated_from_group',
                  'absent']
        required: true
    data:
        description:
            - List with Logical Enclosure properties and its associated states.
        required: true
notes:
    - "The C(absent) state and the creation of a Logical Enclosure done through the C(present) state are available only
       on HPE Synergy."

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Logical Enclosure (available only on HPE Synergy)
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: present
    data:
        enclosureUris:
          - "/rest/enclosures/0000000000A66101"
        enclosureGroupUri: "/rest/enclosure-groups/9fafc382-bbef-4a94-a9d1-05f77042f3ac"
        name: "Encl1"
  ignore_errors: true
  delegate_to: localhost

- name: Update the firmware for the Logical Enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: firmware_updated
    data:
        name: "Encl1"
        firmware:
            firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
            firmwareUpdateOn: "EnclosureOnly"
            forceInstallFirmware: "false"
  delegate_to: localhost

# This play is compatible with Synergy Enclosures
- name: Update the firmware for the Logical Enclosure with the logical-interconnect validation set as true
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: firmware_updated
    data:
        name: "Encl1"
        firmware:
            firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
            firmwareUpdateOn: "EnclosureOnly"
            forceInstallFirmware: "false"
            validateIfLIFirmwareUpdateIsNonDisruptive: "true"
            logicalInterconnectUpdateMode: "Orchestrated"
            updateFirmwareOnUnmanagedInterconnect: "true"
  delegate_to: localhost

- name: Update the Logical Enclosure configuration script
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: script_updated
    data:
        name: "Encl1"
        configurationScript: "# script (updated)"
  delegate_to: localhost

- name: Generates a support dump for the Logical Enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: dumped
    data:
        name: "Encl1"
        dump:
          errorCode: "MyDump16"
          encrypt: "true"
          excludeApplianceDump: "false"
  delegate_to: localhost
- debug: var=generated_dump_uri

- name: Reconfigure all enclosures associated with logical enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: reconfigured
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Makes the logical enclosure consistent with the enclosure group
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: updated_from_group
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Update the Logical Enclosure changing the name attribute
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: present
    data:
        name: "Encl1"
        newName: "Encl1 (renamed)"
  delegate_to: localhost

- name: Delete a Logical Enclosure (available only on HPE Synergy)
  oneview_logical_enclosure:
      config: "{{ config_file_name }}"
      state: absent
      data:
          name: 'Encl1'
  delegate_to: localhost
'''

RETURN = '''
logical_enclosure:
    description: Has the facts about the OneView Logical Enclosure.
    returned: On states 'present', 'firmware_updated', 'reconfigured', 'updated_from_group', and 'absent'. Can be null.
    type: dict

configuration_script:
    description: Has the facts about the Logical Enclosure configuration script.
    returned: On state 'script_updated'. Can be null.
    type: dict

generated_dump_uri:
    description: Has the facts about the Logical Enclosure generated support dump URI.
    returned: On state 'dumped'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound, ResourceComparator


class LogicalEnclosureModule(OneViewModuleBase):
    MSG_UPDATED = 'Logical Enclosure updated successfully.'
    MSG_ALREADY_PRESENT = 'Logical Enclosure is already present.'
    MSG_REQUIRED = "An existing Logical Enclosure is required."
    MSG_UPDATED_FROM_GROUP = 'Logical Enclosure updated from group successfully.'
    MSG_FIRMWARE_UPDATED = 'Logical Enclosure firmware updated.'
    MSG_CONFIGURATION_SCRIPT_UPDATED = 'Logical Enclosure configuration script updated.'
    MSG_DUMP_GENERATED = 'Logical Enclosure support dump generated.'
    MSG_RECONFIGURED = 'Logical Enclosure configuration reapplied.'
    MSG_DELETED = 'Logical Enclosure deleted'
    MSG_ALREADY_ABSENT = 'Logical Enclosure absent'
    MSG_CREATED = 'Logical Enclosure created'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'firmware_updated', 'script_updated',
                     'dumped', 'reconfigured', 'updated_from_group', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(LogicalEnclosureModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        logical_enclosure = self.oneview_client.logical_enclosures.get_by_name(self.data['name'])

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present(self.data, logical_enclosure)
        elif self.state == 'absent':
            changed, msg, ansible_facts = self.__absent(logical_enclosure)
        else:
            if not logical_enclosure:
                raise HPOneViewResourceNotFound(self.MSG_REQUIRED)

            if self.state == 'firmware_updated':
                changed, msg, ansible_facts = self.__update_firmware(self.data, logical_enclosure)
            elif self.state == 'script_updated':
                changed, msg, ansible_facts = self.__update_script(self.data, logical_enclosure)
            elif self.state == 'dumped':
                changed, msg, ansible_facts = self.__support_dump(self.data, logical_enclosure)
            elif self.state == 'reconfigured':
                changed, msg, ansible_facts = self.__reconfigure(logical_enclosure)
            elif self.state == 'updated_from_group':
                changed, msg, ansible_facts = self.__update_from_group(logical_enclosure)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self, data, logical_enclosure):
        if logical_enclosure:
            response = self.__update(data, logical_enclosure)
        else:
            response = self.__create(data)
        return response

    def __create(self, data):
        new_logical_enclosure = self.oneview_client.logical_enclosures.create(data)
        return True, self.MSG_CREATED, dict(logical_enclosure=new_logical_enclosure)

    def __absent(self, logical_enclosure):
        if logical_enclosure:
            changed = True
            msg = self.MSG_DELETED
            self.oneview_client.logical_enclosures.delete(logical_enclosure)
        else:
            changed = False
            msg = self.MSG_ALREADY_ABSENT
        return changed, msg, dict(logical_enclosure=None)

    def __update(self, new_data, existent_resource):
        if "newName" in new_data:
            new_data["name"] = new_data["newName"]
            del new_data["newName"]

        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if not ResourceComparator.compare(existent_resource, merged_data):
            existent_resource = self.oneview_client.logical_enclosures.update(merged_data)
            return True, self.MSG_UPDATED, dict(logical_enclosure=existent_resource)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(logical_enclosure=existent_resource)

    def __update_script(self, data, logical_enclosure):
        script = data.pop("configurationScript")

        self.oneview_client.logical_enclosures.update_script(logical_enclosure['uri'], script)
        return True, self.MSG_CONFIGURATION_SCRIPT_UPDATED, dict(configuration_script=script)

    def __update_firmware(self, data, logical_enclosure):
        logical_enclosure = self.oneview_client.logical_enclosures.patch(logical_enclosure['uri'],
                                                                         operation="replace",
                                                                         path="/firmware",
                                                                         value=data['firmware'])

        return True, self.MSG_FIRMWARE_UPDATED, dict(logical_enclosure=logical_enclosure)

    def __support_dump(self, data, logical_enclosure):
        generated_dump_uri = self.oneview_client.logical_enclosures.generate_support_dump(
            data['dump'],
            logical_enclosure['uri'])

        return True, self.MSG_DUMP_GENERATED, dict(generated_dump_uri=generated_dump_uri)

    def __reconfigure(self, logical_enclosure):
        logical_enclosure = self.oneview_client.logical_enclosures.update_configuration(logical_enclosure['uri'])

        return True, self.MSG_RECONFIGURED, dict(logical_enclosure=logical_enclosure)

    def __update_from_group(self, logical_enclosure):
        logical_enclosure = self.oneview_client.logical_enclosures.update_from_group(logical_enclosure['uri'])

        return True, self.MSG_UPDATED_FROM_GROUP, dict(logical_enclosure=logical_enclosure)


def main():
    LogicalEnclosureModule().run()


if __name__ == '__main__':
    main()
