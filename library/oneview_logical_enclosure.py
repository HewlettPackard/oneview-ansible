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
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_logical_enclosure
short_description: Manage OneView Logical Enclosure resources.
description:
    - Provides an interface to manage Logical Enclosure resources. Can update, update firmware, perform dump,
      update configuration script, reapply configuration, or update from group.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Logical Enclosure resource.
              'present' enable to change the Logical Enclosure name.
              'firmware_updated' update the firmware for the Logical Enclosure.
              'script_updated' update the Logical Enclosure configuration script.
              'dumped' generates a support dump for the Logical Enclosure.
              'reconfigured' reconfigure all enclosures associated with logical enclosure.
              'updated_from_group' makes the logical enclosure consistent with the enclosure group.
        choices: ['present', 'firmware_updated', 'script_updated', 'dumped', 'reconfigured', 'updated_from_group']
        required: true
    data:
        description:
            - List with Logical Enclosure properties and its associated states
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
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
'''

RETURN = '''
logical_enclosure:
    description: Has the facts about the OneView Logical Enclosure.
    returned: On states 'present', 'firmware_updated', 'reconfigured', 'updated_from_group'. Can be null.
    type: complex

configuration_script:
    description: Has the facts about the Logical Enclosure configuration script.
    returned: On state 'script_updated'. Can be null.
    type: complex

generated_dump_uri:
    description: Has the facts about the Logical Enclosure generated support dump uri.
    returned: On state 'dumped'. Can be null.
    type: complex
'''

LOGICAL_ENCLOSURE_UPDATED = 'Logical Enclosure updated successfully.'
LOGICAL_ENCLOSURE_ALREADY_UPDATED = 'Logical Enclosure already updated.'
LOGICAL_ENCLOSURE_REQUIRED = "An existing Logical Enclosure is required."
LOGICAL_ENCLOSURE_UPDATED_FROM_GROUP = 'Logical Enclosure updated from group successfully.'
LOGICAL_ENCLOSURE_FIRMWARE_UPDATED = 'Logical Enclosure firmware updated.'
LOGICAL_ENCLOSURE_CONFIGURATION_SCRIPT_UPDATED = 'Logical Enclosure configuration script updated.'
LOGICAL_ENCLOSURE_DUMP_GENERATED = 'Logical Enclosure support dump generated.'
LOGICAL_ENCLOSURE_RECONFIGURED = 'Logical Enclosure configuration reapplied.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class LogicalEnclosureModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'firmware_updated', 'script_updated',
                     'dumped', 'reconfigured', 'updated_from_group']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            # get logical enclosure by name
            logical_enclosure = self.oneview_client.logical_enclosures.get_by_name(data['name'])

            if not logical_enclosure:
                raise Exception(LOGICAL_ENCLOSURE_REQUIRED)

            logical_enclosure_uri = logical_enclosure['uri']

            if state == 'present':
                changed, msg, ansible_facts = self.__update(data, logical_enclosure)
            elif state == 'firmware_updated':
                changed, msg, ansible_facts = self.__update_firmware(data, logical_enclosure_uri)
            elif state == 'script_updated':
                changed, msg, ansible_facts = self.__update_script(data, logical_enclosure_uri)
            elif state == 'dumped':
                changed, msg, ansible_facts = self.__support_dump(data, logical_enclosure_uri)
            elif state == 'reconfigured':
                changed, msg, ansible_facts = self.__reconfigure(logical_enclosure_uri)
            elif state == 'updated_from_group':
                changed, msg, ansible_facts = self.__update_from_group(logical_enclosure_uri)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __update(self, new_data, existent_resource):
        if "newName" in new_data:
            new_data["name"] = new_data["newName"]
            del new_data["newName"]

        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if not resource_compare(existent_resource, merged_data):
            # update resource
            existent_resource = self.oneview_client.logical_enclosures.update(merged_data)
            return True, LOGICAL_ENCLOSURE_UPDATED, dict(logical_enclosure=existent_resource)
        else:
            return False, LOGICAL_ENCLOSURE_ALREADY_UPDATED, dict(logical_enclosure=existent_resource)

    def __update_script(self, data, logical_enclosure_uri):
        script = data.pop("configurationScript")

        # update the configuration script
        self.oneview_client.logical_enclosures.update_script(logical_enclosure_uri, script)
        return True, LOGICAL_ENCLOSURE_CONFIGURATION_SCRIPT_UPDATED, dict(configuration_script=script)

    def __update_firmware(self, data, logical_enclosure_uri):
        logical_enclosure = self.oneview_client.logical_enclosures.patch(logical_enclosure_uri,
                                                                         operation="replace",
                                                                         path="/firmware",
                                                                         value=data['firmware'])

        return True, LOGICAL_ENCLOSURE_FIRMWARE_UPDATED, dict(logical_enclosure=logical_enclosure)

    def __support_dump(self, data, logical_enclosure_uri):
        generated_dump_uri = self.oneview_client.logical_enclosures.generate_support_dump(
            data['dump'],
            logical_enclosure_uri)

        return True, LOGICAL_ENCLOSURE_DUMP_GENERATED, dict(generated_dump_uri=generated_dump_uri)

    def __reconfigure(self, logical_enclosure_uri):
        logical_enclosure = self.oneview_client.logical_enclosures.update_configuration(logical_enclosure_uri)

        return True, LOGICAL_ENCLOSURE_RECONFIGURED, dict(logical_enclosure=logical_enclosure)

    def __update_from_group(self, logical_enclosure_uri):
        logical_enclosure = self.oneview_client.logical_enclosures.update_from_group(logical_enclosure_uri)

        return True, LOGICAL_ENCLOSURE_UPDATED_FROM_GROUP, dict(logical_enclosure=logical_enclosure)


def main():
    LogicalEnclosureModule().run()


if __name__ == '__main__':
    main()
