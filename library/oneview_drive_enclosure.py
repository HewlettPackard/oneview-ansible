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
module: oneview_drive_enclosure
short_description: Manage OneView Drive Enclosure resources.
description:
    - Provides an interface to manage Drive Enclosure resources. Can create, update, delete. ??????????TODO
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin(@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Drive Enclosure resource.
              'power_state_set' will set the power state of the Drive Enclosure.
              'uid_state_set' will set the uid state of the Drive Enclosure.
              'hard_reset_state_set' will request a hard reset of the Drive Enclosure.
              'refresh_state_set' will refresh a Drive Enclosure.
        choices: ['power_state_set', 'uid_state_set', 'hard_reset_state_set', 'refresh_state_set']
    data:
        description:
            - List with the Drive Enclosure properties.
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Power off the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: power_state_set
    data:
        name: '0000A66108, bay 1'
        powerState: 'Off'

- name: Power on the UID for the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: uid_state_set
    data:
        name: '0000A66108, bay 1'
        uidState: 'On'

- name: Request a hard reset of the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: hard_reset_state_set
    data:
        name: '0000A66108, bay 1'

- name: Refresh the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: refresh_state_set
    data:
        name: '0000A66108, bay 1'
        refreshState: 'RefreshPending'
'''

RETURN = '''
oneview_drive_enclosure:
    description: Has the facts about the Drive Enclosure.
    returned: Always, but can be null.
    type: complex
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'
DRIVE_ENCLOSURE_NAME_REQUIRED = 'Inform the Drive Enclosure name is required.'
DRIVE_ENCLOSURE_NOT_FOUND = 'Drive Enclosure with specified name not found.'


class DriveEnclosureModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['power_state_set', 'uid_state_set', 'hard_reset_state_set', 'refresh_state_set']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:

            drive_enclosure = self.__get_drive_enclosure(data)
            drive_enclosure_uri = drive_enclosure['uri']

            resource_updated = drive_enclosure
            changed = False

            if state == 'power_state_set':
                changed = data.get('powerState') != drive_enclosure['powerState']
                if changed:
                    resource_updated = self.oneview_client.drive_enclosures.patch(
                        drive_enclosure_uri, operation='replace', path='/powerState', value=data.get('powerState'))

            elif state == 'uid_state_set':
                changed = data.get('uidState') != drive_enclosure['uidState']
                if changed:
                    resource_updated = self.oneview_client.drive_enclosures.patch(
                        drive_enclosure_uri, operation='replace', path='/uidState', value=data.get('uidState'))

            elif state == 'hard_reset_state_set':
                changed = True
                resource_updated = self.oneview_client.drive_enclosures.patch(
                    drive_enclosure_uri, operation='replace', path='/hardResetState', value='Reset')

            elif state == 'refresh_state_set':
                changed = True
                refresh_data = dict(refreshState=data.get('refreshState'))
                resource_updated = self.oneview_client.drive_enclosures.refresh_state(drive_enclosure_uri, refresh_data)

            self.module.exit_json(changed=changed, ansible_facts=dict(oneview_drive_enclosure=resource_updated))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_drive_enclosure(self, data):
        name = data.get('name')
        if not name:
            raise Exception(DRIVE_ENCLOSURE_NAME_REQUIRED)
        else:
            result = self.oneview_client.drive_enclosures.get_by('name', name)

            if not result:
                raise Exception(DRIVE_ENCLOSURE_NOT_FOUND)

            return result[0]


def main():
    DriveEnclosureModule().run()


if __name__ == '__main__':
    main()
