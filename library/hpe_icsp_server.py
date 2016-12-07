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
  state:
    description:
      - Indicates the desired state for the ICsp server.
        'present' will register the resource on ICsp.
        'absent' will remove the resource from ICsp, if it exists.
        'network_configured' will set the network configuration.
    choices: ['present', 'absent', 'network_configured']
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

SERVER_CREATED = "Server created: '{}'"
SERVER_ALREADY_PRESENT = "Server is already present."
SERVER_ALREADY_ABSENT = "Target server is already absent in ICsp."
SERVER_REMOVED = "Server '{}' removed successfully from ICsp."
CUSTOM_ATTR_NETWORK_UPDATED = 'Network Custom Attribute Updated.'
SERVER_NOT_FOUND = "Target server is not present in ICsp."
SERVER_PERSONALITY_DATA_REQUIRED = 'server_personality_data must be informed.'


class ICspServerModule(object):
    argument_spec = dict(
        # Connection
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
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.connection = self.__authenticate()

    def run(self):

        state = self.module.params['state']
        ilo_address = self.module.params['server_ipAddress']
        target_server = self.__get_server_by_ilo_address(ilo_address)

        if state == 'present':
            self.__present(target_server)

        elif state == 'absent':
            self.__absent(target_server)

        elif state == 'network_configured':
            self.__configure_network(target_server)

    def __authenticate(self):
        # Credentials
        icsp_host = self.module.params['icsp_host']
        username = self.module.params['username']
        password = self.module.params['password']

        con = hpICsp.connection(icsp_host)

        credential = {'userName': username, 'password': password}
        con.login(credential)
        return con

    def __present(self, target_server):
        # check if server exists
        if target_server:
            return self.module.exit_json(changed=False,
                                         msg=SERVER_ALREADY_PRESENT,
                                         ansible_facts=dict(target_server=target_server))

        return self._add_server()

    def __absent(self, target_server):
        # check if server exists
        if not target_server:
            return self.module.exit_json(changed=False, msg=SERVER_ALREADY_ABSENT)

        server_uri = target_server['uri']
        servers_service = hpICsp.servers(self.connection)

        try:
            servers_service.delete_server(server_uri)
            return self.module.exit_json(changed=True,
                                         msg=SERVER_REMOVED.format(server_uri))

        except HPICspException as icsp_exe:
            self.module.fail_json(msg=json.dumps(icsp_exe.__dict__))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __configure_network(self, target_server):
        personality_data = self.module.params.get('server_personality_data')

        if not personality_data:
            return self.module.fail_json(msg=SERVER_PERSONALITY_DATA_REQUIRED)

        # check if server exists
        if not target_server:
            return self.module.exit_json(changed=False, msg=SERVER_NOT_FOUND)

        server_data = {"serverUri": target_server['uri'], "personalityData": personality_data, "skipReboot": True}
        network_config = {"serverData": [server_data], "failMode": None, "osbpUris": []}

        # Save nework personalization attribute, without running the job
        self.__add_write_only_job(network_config)

        servers_service = hpICsp.servers(self.connection)
        server = servers_service.get_server(target_server['uri'])
        return self.module.exit_json(changed=True,
                                     msg=CUSTOM_ATTR_NETWORK_UPDATED,
                                     ansible_facts={'target_server': server})

    def __add_write_only_job(self, body):
        body = self.connection.post("/rest/os-deployment-jobs/?writeOnly=true", body)
        return body

    def __get_server_by_ilo_address(self, ilo):
        servers = self.connection.get("/rest/os-deployment-servers/?count=-1")
        srv = self.__filter_by_ilo(servers['members'], ilo)
        return srv

    def __filter_by_ilo(self, seq, value):
        for srv in seq:
            if srv['ilo']['ipAddress'] == value:
                return srv
        return None

    def _add_server(self):
        ilo_address = self.module.params['server_ipAddress']

        # Creates a JSON body for adding an iLo.
        ilo_body = {'ipAddress': ilo_address,
                    'username': self.module.params['server_username'],
                    'password': self.module.params['server_password'],
                    'port': self.module.params['server_port']}

        job_monitor = hpICsp.jobs(self.connection)
        servers_service = hpICsp.servers(self.connection)

        # Monitor_execution is a utility method to watch job progress on the command line.
        add_server_job = servers_service.add_server(ilo_body)
        hpICsp.common.monitor_execution(add_server_job, job_monitor)

        # Python bindings throw an Exception when the status != ok
        # So if we got this far, the job execution finished as expected

        # gets the target server added to ICsp to return on ansible facts
        target_server = self.__get_server_by_ilo_address(ilo_address)
        return self.module.exit_json(changed=True,
                                     msg=SERVER_CREATED.format(target_server['uri']),
                                     ansible_facts=dict(target_server=target_server))


def main():
    ICspServerModule().run()


if __name__ == '__main__':
    main()
