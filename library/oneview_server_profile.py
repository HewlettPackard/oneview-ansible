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

CONCURRENCY_FAILOVER_RETRIES = 25

DOCUMENTATION = '''
---
module: oneview_server_profile
short_description: Manage OneView Server Profile resources.
description:
    - Manage the servers lifecycle with OneView Server Profiles using an existing server profile template. On 'present'
      state it selects a server hardware automatically based on the server profile template if no server hardware was
      provided.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Chakravarthy Racharla"
options:
  config:
    description:
      - Path to a .json configuration file containing the OneView client configuration.
    required: true
  state:
    description:
      - Indicates the desired state for the Server Profile resource by the end of the playbook execution.
        'present' will ensure data properties are compliant to OneView.
        'absent' will remove the resource from OneView, if it exists.
        'powered_off' requests a power operation to change the power state of the physical server to Off.
        'powered_on' requests a power operation to change the power state of the physical server to On.
        'no-op' gather facts about the Server Profile
    default: present
    choices: ['present', 'powered_off', 'absent', 'powered_on', 'no-op']
  server_template:
    description:
      - Name of the server profile template that will be used to provision the server profiles.
    required: false
  name:
    description:
      - Name of the server profile that will be created or updated.
    required : true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Create a Server Profile from a Server Profile Template
  oneview_server_profile:
    config: "{{ config }}"
    server_template: Compute-node-template
    name: Web-Server-L2

- debug: var=server_profile
- debug: var=serial_number
- debug: var=server_hardware
- debug: var=compliance_preview
- debug: var=created

- name : Remediate compliance issues
  oneview_server_profile:
     config: "{{ config }}"
     name: Web-Server-L2
     state: "compliant"
  when: server_profile.templateCompliance != 'Compliant'

- name : Power on servers
  oneview_server_profile:
     config: "{{ config }}"
     name: Web-Server-L2
     state: "powered_on"
  when: server_hardware.powerState == "Off"

- name : Power off server to remove server profile
  oneview_server_profile:
    config: "{{ config }}"
    name: Web-Server-L2
    state: "powered_off"

- name : Remove the server profile
  oneview_server_profile:
    config: "{{ config }}"
    name: Web-Server-L2
    state: "absent"
'''

RETURN = '''
server_profile:
    description: Has the OneView facts about the Server Profile.
    returned: On states 'present', 'compliant' and 'no-op'
    type: complex
serial_number:
    description: Has the Server Profile serial number.
    returned: On states 'present', 'compliant' and 'no-op'
    type: complex
server_hardware:
    description: Has the OneView facts about the Server Hardware.
    returned: On states 'present', 'compliant' and 'no-op'
    type: complex
compliance_preview:
    description:
        Has the OneView facts about the manual and automatic updates required to make the server profile
        consistent with its template.
    returned: On states 'present', 'compliant' and 'no-op'
    type: complex
created:
    description: Indicates if the Server Profile was created.
    returned: On states 'present', 'compliant' and 'no-op'
    type: bool
'''


class ServerProfileModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=False,
            choices=[
                'powered_on',
                'powered_off',
                'present',
                'absent',
                'compliant',
                'no_op'
            ],
            default='present'
        ),
        server_template=dict(required=False, type='str'),
        name=dict(required=True, type='str'),
        server_hardware=dict(required=False, type='str', default=None)
    )

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):

        server_template_name = self.module.params['server_template']
        server_name = self.module.params['name']
        state = self.module.params['state']

        try:
            server_template = None
            if server_template_name:
                server_template = self.oneview_client.server_profile_templates.get_by_name(server_template_name)

            # check if the server already exists - edit it to match the desired state
            server_profile = self.oneview_client.server_profiles.get_by_name(server_name)
            if server_profile:
                if state == 'present':
                    changed = self.update_profile(server_profile, server_template)
                    facts = self.gather_facts(server_profile)
                    self.module.exit_json(
                        changed=changed, msg='Updated profile', ansible_facts=facts
                    )
                elif state == 'absent':
                    self.delete_profile(server_profile)
                    self.module.exit_json(
                        changed=True, msg='Deleted profile'
                    )
                elif state in ["powered_on", "powered_off"]:
                    self.set_power_state(server_profile, state)
                    self.module.exit_json(
                        changed=True, msg='Set power state'
                    )
                elif state in ["compliant"]:
                    changed = self.make_compliant(server_profile)
                    self.module.exit_json(
                        changed=changed, msg='Made compliant', ansible_facts=self.gather_facts(server_profile)
                    )
                elif state in ['no-op']:
                    self.module.exit_json(
                        changed=False, ansible_facts=self.gather_facts(server_profile)
                    )

            else:
                if state in ["powered_on", "powered_off"]:
                    self.module.fail_json(msg="Cannot find server to put in state : " + state)
                # we didnt find an existing one, so we create a profile
                elif state in ['present']:
                    server_profile = self.create_profile(server_name, server_template)
                    facts = self.gather_facts(server_profile)
                    facts['created'] = True
                    self.module.exit_json(
                        changed=True, msg='Created profile', ansible_facts=facts
                    )
        except Exception as e:
            self.module.fail_json(msg=e.message)

    def update_profile(self, server_profile, server_template):
        """ update the server to match the template """
        changed = False
        if (server_profile['serverProfileTemplateUri'] != server_template['uri']):
            server_profile['serverProfileTemplateUri'] = server_template['uri']
            self.oneview_client.server_profiles.update(server_profile)
            changed = True

        return changed

    def create_profile(self, server_name, server_template):

        # find servers that have no profile, powered off mathing Server hardware type
        server_hardware_name = self.module.params.get('server_hardware')
        tries = 0
        while tries < CONCURRENCY_FAILOVER_RETRIES:
            try:
                tries += 1
                if server_hardware_name:
                    selected_server_hardware = self.oneview_client.server_hardware.get_by_name(server_hardware_name)
                    if not selected_server_hardware:
                        self.module.fail_json(msg="Invalid server hardware")
                    selected_sh_uri = selected_server_hardware['uri']
                else:
                    # we need to find an available server.
                    # we may need to try this multiple times just in case someone else is also trying to use an
                    # available server.
                    # Lets use a file lock so that ansible module concurrency does not step cause this on each other
                    available_server_hardware = self.oneview_client.server_profiles.get_available_targets(
                        enclosureGroupUri=server_template.get('enclosureGroupUri', ''),
                        serverHardwareTypeUri=server_template.get('serverHardwareTypeUri', ''))

                    # targets will list empty bays. We need to pick one that has a server
                    selected_sh_uri = None
                    index = 0
                    while selected_sh_uri is None and index < len(available_server_hardware['targets']):
                        selected_sh_uri = available_server_hardware['targets'][index]['serverHardwareUri']
                        index = index + 1
                    selected_server_hardware = self.oneview_client.server_hardware.get(selected_sh_uri)
                # power off the server
                self.oneview_client.server_hardware.update_power_state(
                    dict(powerState='Off', powerControl='PressAndHold'), selected_sh_uri)

                server_profile = self.oneview_client.server_profile_templates.get_new_profile(server_template['uri'])
                server_profile['name'] = server_name
                server_profile['serverHardwareUri'] = selected_sh_uri

                return self.oneview_client.server_profiles.create(server_profile)
            except Exception:
                # if this is because the server is already assigned, someone grabbed it before we assigned,
                # ignore and try again
                # This waiting time was chosen empirically and it could differ according to the hardware.
                time.sleep(10)
                pass

        raise Exception("Could not allocate server hardware")

    def delete_profile(self, server_profile):
        self.oneview_client.server_profiles.delete(server_profile)

    def gather_facts(self, server_profile):
        facts = {
            'serial_number': server_profile.get('serialNumber'),
            'server_profile': server_profile,
            'server_hardware': self.oneview_client.server_hardware.get(server_profile['serverHardwareUri']),
            'compliance_preview': self.oneview_client.server_profiles.get_compliance_preview(server_profile['uri']),
            'created': False
        }

        return facts

    def make_compliant(self, server_profile):
        changed = False
        if (server_profile['templateCompliance'] != 'Compliant'):
            # check if server can be remediated while powered on
            # replace | Path: / templateCompliance | Value: Compliant
            self.oneview_client.server_profiles.patch(server_profile['uri'],
                                                      'replace', '/templateCompliance', 'Compliant')
            changed = True

        return changed

    def set_power_state(self, server_profile, power_state):

        power_state_mapping = {'powered_on': 'On', 'powered_off': 'Off'}

        state = power_state_mapping[power_state]
        control = 'PressAndHold' if (state == 'Off') else 'MomentaryPress'

        configuration = {'powerState': state,
                         'powerControl': control}

        self.oneview_client.server_hardware.update_power_state(configuration, server_profile['serverHardwareUri'])


def main():
    ServerProfileModule().run()


if __name__ == '__main__':
    main()
