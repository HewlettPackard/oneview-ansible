#!/usr/bin/python

###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import hpOneView as hpov
from hpOneView.exceptions import *
from ansible.module_utils.basic import *

__author__ = 'ChakruHP'

DOCUMENTATION = '''
---
module: oneview_server_profile
short_description: Selects a server hardware automatically based on the server hardware template.
description:
    - Manage servers lifecycle with OneView Server Profiles using an existing server profile template.
requirements:
    - "python 2.7.11"
    - "hpOneView"
options:
  oneview_host:
    description:
      - OneView appliance IP or hostname.
    required: true
    default: null
    aliases: []
  username:
    description:
      - Username that will be used to authenticate on the provided OneView appliance.
    default: null
    required: true
  password:
    description:
      - Password that will be used to authenticate on the provided OneView appliance.
    required: true
    default: null
  server_template:
    description:
      - Name of the server profile template that will be used to provision the server profiles.
    required: true
    default: null
  name:
    description:
      - Name of the server profile that will be created or updated.
    required : true
    default : null
  state:
    description:
      - Desired state for the server profile by the end of the playbook execution.
    default: present
    choices: ['present', 'powered_off', 'absent', 'powered_on', 'restarted']
'''

EXAMPLES = '''
- oneview_server_profile:
    oneview_host: <ip>
    username: oneview_username
    password: oneview_password
    server_template: Compute-node-template
    name: <server-profile-name>
'''


def update_profile(con, server_profile, server_template):
    """ update the server to match the template """
    changed = False
    servers = hpov.servers(con)
    if (server_profile['serverProfileTemplateUri'] != server_template['uri']):
        server_profile['serverProfileTemplateUri'] = server_template['uri']
        server_profile = servers.update_server_profile(server_profile)
        changed = True

    return changed


def create_profile(module, con, server_name, server_template):
    srv = hpov.servers(con)
    # find servers that have no profile, powered off mathing SHT
    SHT = con.get(server_template['serverHardwareTypeUri'])
    server_hardware_name = module.params['server_hardware']

    tries = 0
    while tries < 25:
        try:
            tries += 1
            if server_hardware_name:
                selected_server_hardware = srv.get_server_by_name(server_hardware_name)
                if selected_server_hardware is None:
                    module.fail_json(msg="Invalid server hardware")
                selected_sh_uri = selected_server_hardware['uri']
            else:
                # we need to find an available server.
                # we may need to try this multiple times just in case someone else is also trying to use an available
                # server.
                # Lets use a file lock so that ansible module concurrency does not step cause this on each other
                available_server_hardware = srv.get_available_servers(server_hardware_type=SHT)

                if available_server_hardware['targets'].count == 0:
                    module.fail_json(msg='No Servers are available')

                # targets will list empty bays. We need to pick one that has a server
                selected_sh_uri = None
                index = 0
                while selected_sh_uri is None and index < len(available_server_hardware['targets']):
                    selected_sh_uri = available_server_hardware['targets'][index]['serverHardwareUri']
                    index = index + 1
                selected_server_hardware = con.get(selected_sh_uri)

            # power off the server
            srv.set_server_powerstate(selected_server_hardware, 'Off', True)
            server_profile = srv.get_server_profile_from_template(server_template)
            server_profile['name'] = server_name
            server_profile['serverHardwareUri'] = selected_sh_uri

            return srv.create_server_profile_from_dict(server_profile)
        except Exception:
            # if this is because the server is already assigned, someone grabbed it before we assigned,
            # ignore and try again
            # This waiting time was chosen empirically and it could differ according to the hardware.
            time.sleep(10)
            pass

    raise Exception("Could not allocate server hardware")


def delete_profile(con, server_profile):
    servers = hpov.servers(con)
    servers.remove_server_profile(server_profile)


def gather_facts(con, server_profile):
    facts = {}
    facts['serial_number'] = server_profile['serialNumber']
    facts['server_profile'] = server_profile
    facts['server_hardware'] = con.get(server_profile['serverHardwareUri'])
    srv = hpov.servers(con)
    facts['compliance_preview'] = srv.get_server_profile_compliance(server_profile)
    facts['created'] = False
    return facts


def make_compliant(con, server_profile):
    changed = False
    srv = hpov.servers(con)

    changed = False
    if (server_profile['templateCompliance'] != 'Compliant'):
        # check if server can be remediated while powered on
        srv.update_server_profile_from_template(server_profile)
        changed = True

    return changed


def set_power_state(con, server_profile, power_state):
    srv = hpov.servers(con)
    server_hardware_uri = server_profile['serverHardwareUri']
    server_hardware = con.get(server_hardware_uri)
    power_state_mapping = {'powered_on': 'On', 'powered_off': 'Off'}
    srv.set_server_powerstate(server_hardware, power_state_mapping[power_state], True)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            oneview_host=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            server_template=dict(required=False, type='str'),
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
                default='present'),
            name=dict(required=True, type='str'),
            server_hardware=dict(required=False, type='str', default=None)))

    oneview_host = module.params['oneview_host']
    credentials = {'userName': module.params['username'], 'password': module.params['password']}
    server_template_name = module.params['server_template']
    server_name = module.params['name']
    state = module.params['state']

    try:
        con = hpov.connection(oneview_host)

        con.login(credentials)
        servers = hpov.servers(con)
        server_template = None
        if server_template_name:
            server_template = servers.get_server_profile_template_by_name(server_template_name)

        # check if the server already exists - edit it to match the desired state
        server_profile = servers.get_server_profile_by_name(server_name)
        if server_profile:
            if state == 'present':
                changed = update_profile(con, server_profile, server_template)
                facts = gather_facts(con, server_profile)
                module.exit_json(
                    changed=changed, msg='Updated profile', ansible_facts=facts
                )
            elif state == 'absent':
                delete_profile(con, server_profile)
                module.exit_json(
                    changed=True, msg='Deleted profile'
                )
            elif state in ["powered_on", "powered_off"]:
                set_power_state(con, server_profile, state)
                module.exit_json(
                    changed=True, msg='Set power state'
                )
            elif state in ["compliant"]:
                changed = make_compliant(con, server_profile)
                module.exit_json(
                    changed=changed, msg='Made compliant', ansible_facts=gather_facts(con, server_profile)
                )
            elif state in ['no-op']:
                module.exit_json(
                    changed=False, ansible_facts=gather_facts(con, server_profile)
                )

        else:
            if state in ["powered_on", "powered_off"]:
                module.fail_json(msg="Cannot find server to put in state :" + state)
            # we didnt find an existing one, so we create a profile
            elif state in ['present']:
                server_profile = create_profile(module, con, server_name, server_template)
                facts = gather_facts(con, server_profile)
                facts['created'] = True
                module.exit_json(
                    changed=True, msg='Created profile', ansible_facts=facts
                )
    except Exception, e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
