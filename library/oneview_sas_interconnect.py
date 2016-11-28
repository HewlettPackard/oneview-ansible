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
module: oneview_sas_interconnect
short_description: Manage the OneView SAS Interconnect resources.
description:
    - Provides an interface to manage the SAS Interconnect. Can change the power state, UID light state, perform soft
      and hard reset, and refresh the SAS Interconnect state.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Switch.
              'powered_on' turns the power on.
              'powered_off' turns the power off.
              'uid_on' turns the UID light on.
              'uid_off' turns the UID light off.
              'soft_reset' perform a soft reset.
              'hard_reset' perform a hard reset.
              'refreshed' perform a refresh.
        choices: ['powered_on', 'powered_off', 'uid_on', 'uid_off', 'soft_reset', 'hard_reset', 'refreshed']
    name:
      description:
        - The SAS Interconnect name.
      required: True
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Ensure that a SAS Interconnect is powered on
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: powered_on
    name: "0000A66101, interconnect 1"

- name: Refresh a SAS Interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: refreshed
    name: "0000A66101, interconnect 1"

- name: Perform a hard reset
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: hard_reset
    name: "0000A66101, interconnect 1"
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasInterconnectModule(object):

    states = dict(
        refreshed=dict(),
        powered_on=dict(operation='replace', path='/powerState', value='On'),
        powered_off=dict(operation='replace', path='/powerState', value='Off'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
        soft_reset=dict(operation='replace', path='/softResetState', value='Reset'),
        hard_reset=dict(operation='replace', path='/hardResetState', value='Reset')
    )

    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=states.keys()
        ),
        name=dict(required=True, type='str')
    )

    actions = ['soft_reset', 'hard_reset']

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        config = self.module.params['config']

        if config:
            oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        else:
            oneview_client = OneViewClient.from_environment_variables()

        self.resource_client = oneview_client.sas_interconnects

    def run(self):
        try:
            name = self.module.params.get('name')
            state_name = self.module.params.get('state')

            facts = {}
            sas_interconnect = self.__get_by_name(name)

            if state_name == 'refreshed':
                facts['sas_interconnect'] = self.resource_client.refresh_state(
                    id_or_uri=sas_interconnect['uri'],
                    configuration=dict(refreshState="RefreshPending")
                )
                changed = True
            else:
                changed, facts['sas_interconnect'] = self.change_state(state_name, sas_interconnect)

            self.module.exit_json(changed=changed, ansible_facts=facts)
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_by_name(self, name):
        sas_interconnects = self.resource_client.get_by('name', name)

        if not sas_interconnects:
            raise Exception("SAS Interconnect not found.")

        return sas_interconnects[0]

    def change_state(self, state_name, resource):
        changed = False
        state = self.states[state_name]
        property_name = state['path'][1:]

        if state_name in self.actions or resource[property_name] != state['value']:
            resource = self.resource_client.patch(id_or_uri=resource["uri"], **state)
            changed = True

        return changed, resource


def main():
    SasInterconnectModule().run()


if __name__ == '__main__':
    main()
