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
    - Provides an interface to manage Enclosure resources.
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
          'present' will ensure data properties are compliant with OneView. You can rename the enclosure providing an
          attribute 'newName'. You can also rename the rack providing an attribute 'rackName'.
          'absent' will remove the resource from OneView, if it exists.
          'reconfigured' will reapply the appliance's configuration on the enclosure. This includes
          running the same configuration steps that were performed as part of the enclosure add.
          'refreshed' will refresh the enclosure along with all of its components, including interconnects and
          servers. Any new hardware is added, and any hardware that is no longer present within the enclosure is
          removed.
          'appliance_bays_powered_on' will set the appliance bay power state on.
          'uid_on' will set the UID state on.
          'uid_off' will set the UID state off.
          'manager_bays_uid_on' will set the UID state on for the Synergy Frame Link Module.
          'manager_bays_uid_off' will set the UID state off for the Synergy Frame Link Module.
          'manager_bays_power_state_e_fuse' will E-Fuse the Synergy Frame Link Module bay in the path.
          'manager_bays_power_state_reset' will Reset the Synergy Frame Link Module bay in the path.
          'appliance_bays_power_state_e_fuse' will E-Fuse the appliance bay in the path.
          'device_bays_power_state_e_fuse' will E-Fuse the device bay in the path.
          'device_bays_power_state_reset' will Reset the device bay in the path.
          'interconnect_bays_power_state_e_fuse' will E-Fuse the IC bay in the path.
          'manager_bays_role_active' will set the active Synergy Frame Link Module.
          'device_bays_ipv4_removed' will release the IPv4 address in the device bay.
          'interconnect_bays_ipv4_removed' will release the IPv4 address in the interconnect bay.
          'support_data_collection_set' will set the support data collection state for the enclosure. The supported
          values for this state are 'PendingCollection', 'Completed', 'Error' and 'NotSupported'
      choices: [
        'present', 'absent', 'reconfigured', 'refreshed', 'appliance_bays_powered_on', 'uid_on', 'uid_off',
        'manager_bays_uid_on', 'manager_bays_uid_off', 'manager_bays_power_state_e_fuse',
        'manager_bays_power_state_reset', 'appliance_bays_power_state_e_fuse', 'device_bays_power_state_e_fuse',
        'device_bays_power_state_reset', 'interconnect_bays_power_state_e_fuse', 'manager_bays_role_active',
        'device_bays_ipv4_removed', 'interconnect_bays_ipv4_removed', 'support_data_collection_set'
        ]
    data:
      description:
        - List with the Enclosure properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - "These states are only available on HPE Synergy: 'appliance_bays_powered_on', 'uid_on', 'uid_off',
      'manager_bays_uid_on', 'manager_bays_uid_off', 'manager_bays_power_state_e_fuse',
      'manager_bays_power_state_reset', 'appliance_bays_power_state_e_fuse', 'device_bays_power_state_e_fuse',
      'device_bays_power_state_reset', 'interconnect_bays_power_state_e_fuse', 'manager_bays_role_active',
      'device_bays_ipv4_removed' and 'interconnect_bays_ipv4_removed'"
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
      licensingIntent : 'OneView'

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
    state: appliance_bays_powered_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

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

- name: Set the UID for the Synergy Frame Link Module state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_uid_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Set the UID for the Synergy Frame Link Module state off
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_uid_off
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the Synergy Frame Link Module bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Reset the Synergy Frame Link Module bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the appliance bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: appliance_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the device bay 10
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 10

- name: Reset the device bay 8
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 8

- name: E-Fuse the IC bay 3
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: interconnect_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 3

- name: Set the active Synergy Frame Link Module on bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_role_active
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: interconnect_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Set the supportDataCollectionState for the enclosure
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: support_data_collection_set
    data:
      name: 'Test-Enclosure'
      supportDataCollectionState: 'PendingCollection'
'''

RETURN = '''
enclosure:
    description: Has all the facts about the enclosure.
    returned: On states 'present', 'reconfigured', and 'refreshed'. Can be null.
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
MANAGER_BAY_UID_ON = 'UID for the Synergy Frame Link Module set to On successfully.'
MANAGER_BAY_UID_ALREADY_ON = 'The UID for the Synergy Frame Link Module is already On.'
BAY_NOT_FOUND = 'Bay not found.'
MANAGER_BAY_UID_ALREADY_OFF = 'The UID for the Synergy Frame Link Module is already Off.'
MANAGER_BAY_UID_OFF = 'UID for the Synergy Frame Link Module set to Off successfully.'
MANAGER_BAY_POWER_STATE_E_FUSED = 'E-Fuse the Synergy Frame Link Module bay in the path.'
MANAGER_BAY_POWER_STATE_RESET = 'Reset the Synergy Frame Link Module bay in the path.'
APPLIANCE_BAY_POWER_STATE_E_FUSED = 'E-Fuse the appliance bay in the path.'
DEVICE_BAY_POWER_STATE_E_FUSED = 'E-Fuse the device bay in the path.'
DEVICE_BAY_POWER_STATE_RESET = 'Reset the device bay in the path.'
INTERCONNECT_BAY_POWER_STATE_E_FUSE = 'E-Fuse the IC bay in the path.'
MANAGER_BAY_ROLE_ACTIVE = 'Set the active Synergy Frame Link Module.'
DEVICE_BAY_IPV4_SETTING_REMOVED = 'Release IPv4 address in the device bay.'
INTERCONNECT_BAY_IPV4_SETTING_REMOVED = 'Release IPv4 address in the interconnect bay'
SUPPORT_DATA_COLLECTION_STATE_SET = 'Support data collection state set.'
SUPPORT_DATA_COLLECTION_STATE_ALREADY_SET = 'The support data collection state is already set with the desired value.'


class EnclosureModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'reconfigured',
                'refreshed',
                'appliance_bays_powered_on',
                'uid_on',
                'uid_off',
                'manager_bays_uid_on',
                'manager_bays_uid_off',
                'manager_bays_power_state_e_fuse',
                'manager_bays_power_state_reset',
                'appliance_bays_power_state_e_fuse',
                'device_bays_power_state_e_fuse',
                'device_bays_power_state_reset',
                'interconnect_bays_power_state_e_fuse',
                'manager_bays_role_active',
                'device_bays_ipv4_removed',
                'interconnect_bays_ipv4_removed',
                'support_data_collection_set',
            ]
        ),
        data=dict(required=True, type='dict')
    )

    patch_params = dict(
        appliance_bays_powered_on=dict(operation='replace', path='/applianceBays/{bayNumber}/power', value='On'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
        manager_bays_uid_on=dict(operation='replace', path='/managerBays/{bayNumber}/uidState', value='On'),
        manager_bays_uid_off=dict(operation='replace', path='/managerBays/{bayNumber}/uidState', value='Off'),
        manager_bays_power_state_e_fuse=dict(operation='replace', path='/managerBays/{bayNumber}/bayPowerState',
                                             value='E-Fuse'),
        manager_bays_power_state_reset=dict(operation='replace', path='/managerBays/{bayNumber}/bayPowerState',
                                            value='Reset'),
        appliance_bays_power_state_e_fuse=dict(operation='replace', path='/applianceBays/{bayNumber}/bayPowerState',
                                               value='E-Fuse'),
        device_bays_power_state_e_fuse=dict(operation='replace', path='/deviceBays/{bayNumber}/bayPowerState',
                                            value='E-Fuse'),
        device_bays_power_state_reset=dict(operation='replace', path='/deviceBays/{bayNumber}/bayPowerState',
                                           value='Reset'),
        interconnect_bays_power_state_e_fuse=dict(operation='replace',
                                                  path='/interconnectBays/{bayNumber}/bayPowerState', value='E-Fuse'),
        manager_bays_role_active=dict(operation='replace', path='/managerBays/{bayNumber}/role', value='active'),
        device_bays_ipv4_removed=dict(operation='remove', path='/deviceBays/{bayNumber}/ipv4Setting', value=''),
        interconnect_bays_ipv4_removed=dict(operation='remove', path='/interconnectBays/{bayNumber}/ipv4Setting',
                                            value=''),
    )

    patch_messages = dict(
        appliance_bays_powered_on=dict(changed=APPLIANCE_BAY_POWERED_ON, not_changed=APPLIANCE_BAY_ALREADY_POWERED_ON),
        uid_on=dict(changed=UID_POWERED_ON, not_changed=UID_ALREADY_POWERED_ON),
        uid_off=dict(changed=UID_POWERED_OFF, not_changed=UID_ALREADY_POWERED_OFF),
        manager_bays_uid_on=dict(changed=MANAGER_BAY_UID_ON, not_changed=MANAGER_BAY_UID_ALREADY_ON),
        manager_bays_uid_off=dict(changed=MANAGER_BAY_UID_OFF, not_changed=MANAGER_BAY_UID_ALREADY_OFF),
        manager_bays_power_state_e_fuse=dict(changed=MANAGER_BAY_POWER_STATE_E_FUSED),
        manager_bays_power_state_reset=dict(changed=MANAGER_BAY_POWER_STATE_RESET),
        appliance_bays_power_state_e_fuse=dict(changed=APPLIANCE_BAY_POWER_STATE_E_FUSED),
        device_bays_power_state_e_fuse=dict(changed=DEVICE_BAY_POWER_STATE_E_FUSED),
        device_bays_power_state_reset=dict(changed=DEVICE_BAY_POWER_STATE_RESET),
        interconnect_bays_power_state_e_fuse=dict(changed=INTERCONNECT_BAY_POWER_STATE_E_FUSE),
        manager_bays_role_active=dict(changed=MANAGER_BAY_ROLE_ACTIVE),
        device_bays_ipv4_removed=dict(changed=DEVICE_BAY_IPV4_SETTING_REMOVED),
        interconnect_bays_ipv4_removed=dict(changed=INTERCONNECT_BAY_IPV4_SETTING_REMOVED),
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
                    changed, msg, resource = self.__reconfigure(resource)
                elif state == 'refreshed':
                    changed, msg, resource = self.__refresh(resource, data)
                elif state == 'support_data_collection_set':
                    changed, msg, resource = self.__support_data_collection_set(resource, data)
                else:
                    changed, msg, resource = self.__patch(resource, data)

                self.module.exit_json(changed=changed,
                                      msg=msg,
                                      ansible_facts=dict(enclosure=resource))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, resource_by_name, data):
        resource_added = False
        resource_updated = False

        configuration_data = data.copy()

        name = configuration_data.pop('newName', configuration_data.pop('name', None))
        rack_name = configuration_data.pop('rackName', None)
        calibrated_max_power = configuration_data.pop('calibratedMaxPower', None)

        if 'hostname' in data:
            resource = self.__get_by_hostname(data['hostname'])
            if not resource:
                resource = self.oneview_client.enclosures.add(configuration_data)
                resource_added = True
        else:
            resource = resource_by_name

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
        return True, ENCLOSURE_RECONFIGURED, reconfigured_enclosure

    def __refresh(self, resource, data):
        refresh_config = data.copy()
        refresh_config.pop('name', None)

        self.oneview_client.enclosures.refresh_state(resource['uri'], refresh_config)
        enclosure = self.oneview_client.enclosures.get(resource['uri'])

        return True, ENCLOSURE_REFRESHED, enclosure

    def __support_data_collection_set(self, resource, data):
        current_value = resource.get('supportDataCollectionState')
        desired_value = data.get('supportDataCollectionState')

        if current_value != desired_value:
            updated_resource = self.oneview_client.enclosures.patch(resource['uri'], operation='replace',
                                                                    path='/supportDataCollectionState',
                                                                    value=desired_value)
            return True, SUPPORT_DATA_COLLECTION_STATE_SET, updated_resource

        return False, SUPPORT_DATA_COLLECTION_STATE_ALREADY_SET, resource

    def __patch(self, resource, data):
        changed = False
        state_name = self.module.params['state']
        state = self.patch_params[state_name].copy()

        property_current_value = self.__get_current_property_value(state_name, state, resource, data)

        if self.__is_update_needed(state_name, state, property_current_value):
            resource = self.oneview_client.enclosures.patch(resource['uri'], **state)
            changed = True

        msg = self.patch_messages[state_name]['changed'] if changed else self.patch_messages[state_name]['not_changed']

        return changed, msg, resource

    def __is_update_needed(self, state_name, state, property_current_value):
        need_request_update = False
        if state['value'] in ['E-Fuse', 'Reset', 'active']:
            need_request_update = True
        elif state['operation'] == 'remove':
            need_request_update = True
        elif state_name == 'appliance_bays_powered_on':
            if not property_current_value:
                need_request_update = True
        elif property_current_value != state['value']:
            need_request_update = True

        return need_request_update

    def __get_current_property_value(self, state_name, state, resource, data):
        property_name = state['path'].split('/')[1]
        sub_property_name = state['path'].split('/')[-1]

        if sub_property_name == property_name:
            sub_property_name = None

        if state_name == 'appliance_bays_powered_on':
            sub_property_name = 'poweredOn'

        filter = set(data.keys()) - set(["name"])
        if filter:
            filter = filter.pop()

        property_current_value = None

        if filter:
            sub_resource = None
            if resource.get(property_name):
                sub_resource = next(
                    (item for item in resource[property_name] if str(item[filter]) == str(data[filter])), None)

            if not sub_resource:
                # Resource doesn't have that property or subproperty
                raise Exception(BAY_NOT_FOUND)

            property_current_value = sub_resource.get(sub_property_name)
            state['path'] = state['path'].format(**data)

        else:
            property_current_value = resource[property_name]

        return property_current_value

    def __name_has_changes(self, resource, name):
        return name and resource['name'] != name

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
        if 'name' not in data:
            return None
        result = self.oneview_client.enclosures.get_by('name', data['name'])
        return result[0] if result else None

    def __get_by_hostname(self, hostname):
        def filter_by_hostname(hostname, enclosure):
            is_primary_ip = ('activeOaPreferredIP' in enclosure and enclosure['activeOaPreferredIP'] == hostname)
            is_standby_ip = ('standbyOaPreferredIP' in enclosure and enclosure['standbyOaPreferredIP'] == hostname)
            return is_primary_ip or is_standby_ip

        enclosures = self.oneview_client.enclosures.get_all()
        result = [x for x in enclosures if filter_by_hostname(hostname, x)]
        return result[0] if result else None


def main():
    EnclosureModule().run()


if __name__ == '__main__':
    main()
