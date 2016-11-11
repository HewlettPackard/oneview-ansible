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

APPLIANCE_BAY_NOT_FOUND = 'The informed bay is not supported.'

try:
    from hpOneView.oneview_client import OneViewClient

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_enclosure
short_description: Manage OneView Enclosure resources.
description:
    - Provides an interface to manage Enclosure resources. Can add, update, remove, reconfigure, refresh and power on
      appliance bays.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
      description:
        - Indicates the desired state for the Enclosure resource.
          'present' will ensure data properties are compliant with OneView.
          'absent' will remove the resource from OneView, if it exists.
          'reconfigured' will reapply the appliance's configuration on the enclosure. This includes
          running the same configuration steps that were performed as part of the enclosure add.
          'refreshed' will refresh the enclosure along with all of its components, including interconnects and
          servers. Any new hardware is added, and any hardware that is no longer present within the enclosure is
          removed.
          'appliance_bays_power_on' will set the appliance bay power state on.
          'uid_on' will set the UID state on.
          'uid_on' will set the UID state off.
      choices: ['present', 'absent', 'reconfigured', 'refreshed', 'appliance_bays_power_on', 'uid_on', 'uid_off']
    data:
      description:
        - List with the Enclosure properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
      newName : 'Test-Enclosure-Renamed'

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
  oneview_enclosure:
    config: "{{ config }}"
    state: present
    data:
      name: 'Test-Enclosure'
      calibratedMaxPower: 1700

- name: Set the appliance bay power state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: appliance_bays_power_on
    data:
      name: 'Test-Enclosure'
      applianceBay: 1

- name: Set the appliance UID state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: uid_on
    data:
      name: 'Test-Enclosure'

- name: Set the appliance UID state off
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: uid_off
    data:
      name: 'Test-Enclosure'
'''

RETURN = '''
enclosure:
    description: Has all the facts about the enclosure.
    returned: On states 'present', 'reconfigured', 'refreshed'. Can be null.
    type: complex
'''

ENCLOSURE_ADDED = 'Enclosure added successfully.'
ENCLOSURE_REMOVED = 'Enclosure removed successfully.'
ENCLOSURE_UPDATED = 'Enclosure updated successfully.'
ENCLOSURE_ALREADY_EXIST = 'Enclosure already exists.'
ENCLOSURE_ALREADY_ABSENT = 'Nothing to do.'
ENCLOSURE_RECONFIGURED = 'Enclosure reconfigured successfully.'
ENCLOSURE_REFRESHED = 'Enclosure refreshed successfully.'
ENCLOSURE_NOT_FOUND = 'Enclosure not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'

APPLIANCE_BAY_ALREADY_POWERED_ON = 'The device in specified bay is already powered on.'
APPLIANCE_BAY_POWERED_ON = 'Appliance bay power state set to on successfully.'

UID_ALREADY_POWERED_ON = 'UID state is already On.'
UID_POWERED_ON = 'UID state set to On successfully.'

UID_ALREADY_POWERED_OFF = 'UID state is already Off.'
UID_POWERED_OFF = 'UID state set to Off successfully.'


class EnclosureModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'reconfigured', 'refreshed', 'appliance_bays_power_on', 'uid_on', 'uid_off']
        ),
        data=dict(required=True, type='dict')
    )

    patch_params = dict(
        appliance_bays_power_on=dict(operation='replace', path='/applianceBays/{}/power', value='On'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
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
            resource = self.__get_by_name(data)

            if state == 'present':
                self.__present(resource, data)
            elif state == 'absent':
                self.__absent(resource, data)
            else:

                if not resource:
                    raise Exception(ENCLOSURE_NOT_FOUND)

                if state == 'reconfigured':
                    self.__reconfigure(resource)
                elif state == 'refreshed':
                    self.__refresh(resource, data)
                elif state == 'appliance_bays_power_on':
                    self.__set_appliance_bays_power_on(resource, data)
                elif state == 'uid_on':
                    self.__set_uid_on(resource)
                elif state == 'uid_off':
                    self.__set_uid_off(resource)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

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

    def __reconfigure(self, resource):
        reconfigured_enclosure = self.oneview_client.enclosures.update_configuration(resource['uri'])
        self.module.exit_json(changed=True,
                              msg=ENCLOSURE_RECONFIGURED,
                              ansible_facts=dict(enclosure=reconfigured_enclosure))

    def __refresh(self, resource, data):
        refresh_config = data.copy()
        refresh_config.pop('name', None)

        self.oneview_client.enclosures.refresh_state(resource['uri'], refresh_config)
        enclosure = self.oneview_client.enclosures.get(resource['uri'])

        self.module.exit_json(changed=True,
                              ansible_facts=dict(enclosure=enclosure),
                              msg=ENCLOSURE_REFRESHED)

    def __set_appliance_bays_power_on(self, resource, data):
        changed = False
        msg = APPLIANCE_BAY_ALREADY_POWERED_ON
        appliance_bay = None
        bay_number = data.get('applianceBay')

        if resource.get('applianceBays'):
            appliance_bay = next((bay for bay in resource['applianceBays'] if bay['bayNumber'] == bay_number), None)

        if appliance_bay and not appliance_bay['poweredOn']:
            changed = True
            msg = APPLIANCE_BAY_POWERED_ON
            resource = self.__patch(resource, bay_number)

        elif not resource.get('applianceBays') or not appliance_bay:
            raise Exception(APPLIANCE_BAY_NOT_FOUND)

        self.module.exit_json(changed=changed,
                              ansible_facts=dict(enclosure=resource),
                              msg=msg)

    def __set_uid_on(self, resource):
        changed = False
        msg = UID_ALREADY_POWERED_ON

        if resource.get('uidState', '') != 'On':
            changed = True
            msg = UID_POWERED_ON
            resource = self.__patch(resource)

        self.module.exit_json(changed=changed,
                              ansible_facts=dict(enclosure=resource),
                              msg=msg)

    def __set_uid_off(self, resource):
        changed = False
        msg = UID_ALREADY_POWERED_OFF

        if resource.get('uidState', '') != 'Off':
            changed = True
            msg = UID_POWERED_OFF
            resource = self.__patch(resource)

        self.module.exit_json(changed=changed,
                              ansible_facts=dict(enclosure=resource),
                              msg=msg)

    def __patch(self, resource, *path_params):
        state_name = self.module.params['state']
        state = self.patch_params[state_name].copy()

        if path_params:
            state['path'] = state['path'].format(*path_params)

        return self.oneview_client.enclosures.patch(resource['uri'], **state)

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
