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
import hpICsp
from hpICsp.exceptions import *
from ansible.module_utils.basic import *

__author__ = 'tiagomtotti'

DOCUMENTATION = '''
---
module: hpe_icsp_server
short_description: Adds, removes and configures servers in ICsp.
description:
    - This module allows to add, remove and configure servers in Insight Control Server Provisioning (ICsp). A server,
     often referred to as a Target Server, in ICsp is a physical ProLiant server or a virtual machine that can have
     actions taken upon it.

requirements:
    - "python >= 2.7.9"
    - "hpICsp"
options:
  icsp_host:
    description:
      - ICsp hostname.
    required: true
  username:
    description:
      - ICsp username.
    required: true
  password:
    description:
      - ICsp password.
    required: true
  server_ipAddress:
    description:
      - The IP address of the iLO of the server.
    required: true
  server_username:
    description:
      - The user name required to log into the server's iLO.
     required: true
  server_password:
    description:
      - The password required to log into the server's iLO
    required: true
  server_port:
    description:
     - The iLO port to use when logging in.
    default:
      - 443
    required: false
  server_personality_data:
    description:
      - Aditional data to send to ICsp.
    required: false
'''

EXAMPLES = '''
  - name: Ensure the server is registered in ICsp
    hpe_icsp_server:
      icsp_host: "{{icsp_host}}"
      username: "{{icsp_username}}"
      password: "{{icsp_password}}"
      server_ipAddress: "{{server_iLO_ip}}"
      server_username: "Admin"
      server_password: "admin"
      state: present
    delegate_to: localhost

  - name: Set the network configuration
    hpe_icsp_server:
      icsp_host: "{{ icsp }}"
      username: "{{ icsp_username }}"
      password: "{{ icsp_password }}"
      server_ipAddress: "{{ server_ipAddress }}"
      server_username: "{{ server_username }}"
      server_password: "{{ server_password }}"
      server_personality_data: "{{ network_config }}"
      state: network_configured
    delegate_to: localhost

  - name: Ensure the server is removed from ICsp
    hpe_icsp_server:
      icsp_host: "{{icsp_host}}"
      username: "{{icsp_username}}"
      password: "{{icsp_password}}"
      server_ipAddress: "{{server_iLO_ip}}"
      server_username: "Admin"
      server_password: "admin"
      state: absent
    delegate_to: localhost
'''

RETURN = '''
target_server:
    description: Has the facts about the server that was added to ICsp.
    returned: On states 'present' and 'network_configured' . Can be null.
    type: complex
'''


def filter_by_ilo(seq, value):
    for srv in seq:
        if srv['ilo']['ipAddress'] == value:
            return srv
    return None


def get_server_by_ilo_address(con, ilo):
    servers = con.get("/rest/os-deployment-servers/?count=-1")
    srv = filter_by_ilo(servers['members'], ilo)
    return srv


def authenticate(module):
    # Credentials
    icsp_host = module.params['icsp_host']
    username = module.params['username']
    password = module.params['password']

    con = hpICsp.connection(icsp_host)

    credential = {'userName': username, 'password': password}
    con.login(credential)
    return con


def __absent(module):

    ilo_address = module.params['server_ipAddress']
    con = authenticate(module)

    # check if server exists
    server = get_server_by_ilo_address(con, ilo_address)
    if server is None:
        return module.exit_json(changed=False, msg="Target server is already absent in ICsp.")

    server_uri = server['uri']
    servers_service = hpICsp.servers(con)

    try:
        servers_service.delete_server(server_uri)
        return module.exit_json(changed=True,
                                msg="Server " + server_uri + " removed successfully from ICsp.")

    except Exception:
        return module.fail_json(msg="Error removing server.")


def __present(module):

    connection = authenticate(module)
    ilo_address = module.params['server_ipAddress']

    # check if server exists
    server = get_server_by_ilo_address(connection, ilo_address)
    if server:
        return module.exit_json(changed=False,
                                msg="Server is already present.",
                                ansible_facts=dict(target_server=server))

    return _add_server(connection, module)


def _add_server(connection, module):

    ilo_address = module.params['server_ipAddress']

    # Creates a JSON body for adding an iLo.
    ilo_body = {'ipAddress': ilo_address,
                'username': module.params['server_username'],
                'password': module.params['server_password'],
                'port': module.params['server_port']}

    job_monitor = hpICsp.jobs(connection)
    servers_service = hpICsp.servers(connection)

    # Monitor_execution is a utility method to watch job progress on the command line.
    add_server_job = servers_service.add_server(ilo_body)
    hpICsp.common.monitor_execution(add_server_job, job_monitor)

    # Python bindings trhow an Exception when the status != ok
    # So if we got this far the job execution finished as expected

    # gets the target server added to ICsp to return on ansible facts
    target_server = get_server_by_ilo_address(connection, ilo_address)
    return module.exit_json(changed=True,
                            msg="Server created: " + target_server['uri'],
                            ansible_facts=dict(target_server=target_server))


def configure_network(module):

    personality_data = module.params['server_personality_data']

    if personality_data is None:
        return module.fail_json(msg='server_personality_data must be informed.')

    connection = authenticate(module)
    ilo_address = module.params['server_ipAddress']

    # check if server exists
    server = get_server_by_ilo_address(connection, ilo_address)
    if server is None:
        return module.exit_json(changed=False, msg="Target server is not present in ICsp.")

    server_data = {"serverUri": server['uri'], "personalityData": personality_data, "skipReboot": True}
    networkConfig = {"serverData": [server_data], "failMode": None, "osbpUris": []}

    # Save nework personalization attribute, without running the job
    add_write_only_job(connection, networkConfig)

    servers_service = hpICsp.servers(connection)
    server = servers_service.get_server(server['uri'])
    return module.exit_json(changed=True,
                            msg='Network Custom Attribute Updated.',
                            ansible_facts={'target_server': server})


def add_write_only_job(connection, body):
    body = connection.post("/rest/os-deployment-jobs/?writeOnly=true", body)
    return body


def main():
    module = AnsibleModule(
        argument_spec=dict(
            # connection
            icsp_host=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            # options
            state=dict(
                required=True,
                choices=['present', 'absent', 'network_configured']
            ),
            # server data
            server_ipAddress=dict(required=True, type='str'),
            server_username=dict(required=True, type='str'),
            server_password=dict(required=True, type='str'),
            server_port=dict(required=False, type='int', default=443),
            server_personality_data=dict(required=False, type='dict')
        ))

#    try:
    state = module.params['state']
    if state == 'present':
        __present(module)

    elif state == 'absent':
        __absent(module)

    elif state == 'network_configured':
        configure_network(module)


#    except Exception, e:
#        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
