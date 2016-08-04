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
module: oneview_enclosure
short_description: Manage OneView Enclosure resources.
description:
    - Provides an interface to manage Enclosure resources. Can add, update, remove, or reconfigure.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Enclosure resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
              'reconfigured' will reapply the appliance's configuration on the enclosure. This includes
              running the same configure steps that were performed as part of the enclosure add.
              'refreshed' will refreshes the enclosure along with all of its components, including interconnects and
              servers. Any new hardware is added and any hardware that is no longer present within the enclosure is
              removed.
        choices: ['present', 'absent', 'reconfigured', 'refreshed']
    data:
      description:
        - List with the Enclosure properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Ensure that an Enclosure is present using the default configuration
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: present
    data:
      enclosureGroupUri : {{ enclosure_group_uri }},
      hostname : {{ enclosure_hostname }},
      username : {{ enclosure_username }},
      password : {{ enclosure_password }},
      name: 'Test-Enclosure'
      licensingIntent : "OneView"

- name: Updates the enclosure to have a name of "Test-Enclosure-Renamed".
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test-Enclosure'
      newName : "Test-Enclosure-Renamed

- name: Reconfigure the enclosure "Test-Enclosure"
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: reconfigured
    data:
      name: 'Test-Enclosure'

- name: Ensure that enclosure is absent
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test-Enclosure'

- name: Ensure that an enclosure is refreshed
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: refreshed
    data:
      name: 'Test-Enclosure'
      refreshState: Refreshing

- name: Set the calibrated max power of an unmanaged or unsupported enclosure
  config: "{{ config }}"
  state: present
  data:
    name: 'Test-Enclosure'
    calibratedMaxPower: 1700
  delegate_to: localhost
'''


ENCLOSURE_ADDED = 'Enclosure added successfully.'
ENCLOSURE_REMOVED = 'Enclosure removed successfully.'
ENCLOSURE_UPDATED = 'Enclosure updated successfully.'
ENCLOSURE_ALREADY_EXIST = 'Enclosure already exists.'
ENCLOSURE_ALREADY_ABSENT = 'Nothing to do.'
ENCLOSURE_RECONFIGURED = 'Enclosure reconfigured successfully.'
ENCLOSURE_REFRESHED = 'Enclosure refreshed successfully.'
ENCLOSURE_NOT_FOUND = 'Enclosure not found.'


class EnclosureModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'reconfigured', 'refreshed']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            resource = self.__get_by_name(data)

            if state == 'present':
                self.__present(resource, data)
            elif state == 'absent':
                self.__absent(resource, data)
            elif state == 'reconfigured':
                self.__reconfigure(resource, data)
            elif state == 'refreshed':
                self.__refresh(resource, data)

        except Exception as e:
            self.module.fail_json(msg=e.message)

    def __present(self, resource, data):
        resource_added = False
        resource_updated = False

        configuration_data = data.copy()

        name = configuration_data.pop('newName', None)
        rack_name = configuration_data.pop('rackName', None)
        calibrated_max_power = configuration_data.pop('calibratedMaxPower', None)

        if not resource:
            if not name:
                name = configuration_data.pop('name', None)
            resource = self.__add(configuration_data)
            resource_added = True

        if self.__name_has_changes(resource, name):
            resource = self.__replace_enclosure_name(resource, name)
            resource_updated = True
        if self.__rack_name_has_changes(resource, rack_name):
            resource = self.__replace_enclosure_rack_name(resource, rack_name)
            resource_updated = True
        if calibrated_max_power:
            self.__set_calibrated_max_power(resource, calibrated_max_power)
            resource_updated = True

        self.__exit_status_present(resource, added=resource_added, updated=resource_updated)

    def __absent(self, resource, data):
        if resource:
            self.oneview_client.enclosures.remove(resource)
            self.module.exit_json(changed=True,
                                  msg=ENCLOSURE_REMOVED)
        else:
            self.module.exit_json(changed=False, msg=ENCLOSURE_ALREADY_ABSENT)

    def __reconfigure(self, resource, data):
        resource = self.__get_by_name(data)

        if resource:
            reconfigured_enclosure = self.oneview_client.enclosures.update_configuration(resource['uri'])
            self.module.exit_json(changed=True,
                                  msg=ENCLOSURE_RECONFIGURED,
                                  ansible_facts=dict(enclosure=reconfigured_enclosure))
        else:
            self.module.exit_json(changed=False, msg=ENCLOSURE_NOT_FOUND)

    def __refresh(self, resource, data):
        refresh_config = data.copy()
        refresh_config.pop('name', None)

        if resource:
            self.oneview_client.enclosures.refresh_state(resource['uri'], refresh_config)
            enclosure = self.oneview_client.enclosures.get(resource['uri'])

            self.module.exit_json(changed=True,
                                  ansible_facts=dict(enclosure=enclosure),
                                  msg=ENCLOSURE_REFRESHED)
        else:
            self.module.exit_json(changed=False, msg=ENCLOSURE_NOT_FOUND)

    def __add(self, data):
        new_enclosure = self.oneview_client.enclosures.add(data)
        return new_enclosure

    def __name_has_changes(self, resource, name):
        return name and resource.get('name', None) != name

    def __rack_name_has_changes(self, resource, rack_name):
        return rack_name and resource.get('rackName', None) != rack_name

    def __replace_enclosure_name(self, resource, name):
        updated_resource = self.oneview_client.enclosures.patch(resource['uri'], 'replace', '/name', name)
        return updated_resource

    def __replace_enclosure_rack_name(self, resource, rack_name):
        updated_resource = self.oneview_client.enclosures.patch(resource['uri'], 'replace', '/rackName', rack_name)
        return updated_resource

    def __set_calibrated_max_power(self, resource, calibrated_max_power):
        body = {"calibratedMaxPower": calibrated_max_power}
        self.oneview_client.enclosures.update_environmental_configuration(resource['uri'], body)

    def __exit_status_present(self, resource, added, updated):
        if added:
            message = ENCLOSURE_ADDED
        elif updated:
            message = ENCLOSURE_UPDATED
        else:
            message = ENCLOSURE_ALREADY_EXIST

        self.module.exit_json(changed=added or updated,
                              msg=message,
                              ansible_facts=dict(enclosure=resource))

    def __get_by_name(self, data):
        result = self.oneview_client.enclosures.get_by('name', data['name'])
        return result[0] if result else None


def main():
    EnclosureModule().run()


if __name__ == '__main__':
    main()
