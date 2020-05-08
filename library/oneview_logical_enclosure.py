#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
    - "hpOneView >= 5.0.0"
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: firmware_updated
    data:
        name: "Encl1"
        firmware:
            firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
            firmwareUpdateOn: "EnclosureOnly"
            forceInstallFirmware: "false"
        custom_headers:
            if-Match: '*'
  delegate_to: localhost

# This play is compatible with Synergy Enclosures
- name: Update the firmware for the Logical Enclosure with the logical-interconnect validation set as true
  oneview_logical_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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
        custom_headers:
            if-Match: '*'
  delegate_to: localhost

- name: Update the Logical Enclosure configuration script
  oneview_logical_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: script_updated
    data:
        name: "Encl1"
        configurationScript: "# script (updated)"
  delegate_to: localhost

- name: Generates a support dump for the Logical Enclosure
  oneview_logical_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: reconfigured
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Makes the logical enclosure consistent with the enclosure group
  oneview_logical_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: updated_from_group
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Update the Logical Enclosure changing the name attribute
  oneview_logical_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
        name: "Encl1"
        newName: "Encl1 (renamed)"
  delegate_to: localhost

- name: Delete a Logical Enclosure (available only on HPE Synergy)
  oneview_logical_enclosure:
      hostname: 172.16.101.48
      username: administrator
      password: my_password
      api_version: 1200
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

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, compare


class LogicalEnclosureModule(OneViewModule):
    MSG_UPDATED = 'Logical Enclosure updated successfully.'
    MSG_ALREADY_PRESENT = 'Logical Enclosure is already present.'
    MSG_REQUIRED = "An existing Logical Enclosure is required."
    MSG_UPDATED_FROM_GROUP = 'Logical Enclosure updated from group successfully.'
    MSG_FIRMWARE_UPDATED = 'Logical Enclosure firmware updated.'
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
        self.set_resource_object(self.oneview_client.logical_enclosures)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present()
        elif self.state == 'absent':
            changed, msg, ansible_facts = self.__absent()
        else:
            if not self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_REQUIRED)

            if self.state == 'firmware_updated':
                changed, msg, ansible_facts = self.__update_firmware()
            elif self.state == 'dumped':
                changed, msg, ansible_facts = self.__support_dump()
            elif self.state == 'reconfigured':
                changed, msg, ansible_facts = self.__reconfigure()
            elif self.state == 'updated_from_group':
                changed, msg, ansible_facts = self.__update_from_group()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self):
        if self.current_resource:
            response = self.__update()
        else:
            response = self.__create(self.data)
        return response

    def __create(self, data):
        self.current_resource = self.resource_client.create(data)
        return True, self.MSG_CREATED, dict(logical_enclosure=self.current_resource.data)

    def __absent(self):
        if self.current_resource:
            changed = True
            msg = self.MSG_DELETED
            self.current_resource.delete()
        else:
            changed = False
            msg = self.MSG_ALREADY_ABSENT
        return changed, msg, dict(logical_enclosure=None)

    def __update(self):
        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        merged_data = self.current_resource.data.copy()
        merged_data.update(self.data)

        if not compare(self.current_resource.data, merged_data):
            self.current_resource.update(merged_data)
            return True, self.MSG_UPDATED, dict(logical_enclosure=self.current_resource.data)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(logical_enclosure=self.current_resource.data)

    def __update_firmware(self):
        self.current_resource.patch(operation="replace",
                                    path="/firmware",
                                    value=self.data['firmware'],
                                    custom_headers=self.data.get('custom_headers'))

        return True, self.MSG_FIRMWARE_UPDATED, dict(logical_enclosure=self.current_resource.data)

    def __support_dump(self):
        generated_dump_uri = self.current_resource.generate_support_dump(self.data['dump'])

        return True, self.MSG_DUMP_GENERATED, dict(generated_dump_uri=generated_dump_uri)

    def __reconfigure(self):
        logical_enclosure = self.current_resource.update_configuration()

        return True, self.MSG_RECONFIGURED, dict(logical_enclosure=logical_enclosure)

    def __update_from_group(self):
        logical_enclosure = self.current_resource.update_from_group()

        return True, self.MSG_UPDATED_FROM_GROUP, dict(logical_enclosure=logical_enclosure)


def main():
    LogicalEnclosureModule().run()


if __name__ == '__main__':
    main()
