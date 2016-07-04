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
module: oneview_interconnect
short_description: Manage the OneView Interconnects resources.
description:
    - Provides an interface to manage the Interconnects power state and the UID light state. Can change power state and
    UID light state.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Interconnect resource.
              'powered_on' turns the power on.
              'powered_off' turns the power off.
              'uid_on' turns the UID light on.
              'uid_off' turns the UID light off.
        choices: ['powered_on', 'powered_off']
    id:
      description:
        - Interconnect ID.
      required: true
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Turn the power off for Interconnect d9583219-2f06-4908-979f-66bde4b51294
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'powered_off'
    id: 'd9583219-2f06-4908-979f-66bde4b51294'

- name: Turn the UID light to 'On' for interconnect d9583219-2f06-4908-979f-66bde4b51294'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    id: 'd9583219-2f06-4908-979f-66bde4b51294'
'''


class InterconnectModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['powered_on', 'powered_off', 'uid_on', 'uid_off']
        ),
        id=dict(required=True, type='str')
    )

    states = dict(
        powered_on=dict(path='/powerState', value='On'),
        powered_off=dict(path='/powerState', value='Off'),
        uid_on=dict(path='/uidState', value='On'),
        uid_off=dict(path='/uidState', value='Off')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        interconnect_id = self.module.params['id']
        state_name = self.module.params['state']
        state = self.states[state_name]

        try:
            resource = self.oneview_client.interconnects.get(interconnect_id)
            changed = False

            property_name = state['path'][1:]

            if resource[property_name] != state['value']:
                resource = self.oneview_client.interconnects.patch(
                    id_or_uri=interconnect_id,
                    operation='replace',
                    path=state['path'],
                    value=state['value']
                )
                changed = True

            self.module.exit_json(
                changed=changed,
                ansible_facts=dict(interconnect=resource)
            )
        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    InterconnectModule().run()


if __name__ == '__main__':
    main()
