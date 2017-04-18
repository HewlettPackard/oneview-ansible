#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import urllib
from hpICsp.exceptions import *
from ansible.module_utils.basic import *


__author__ = 'ChakruHP, tiagomtotti'

DOCUMENTATION = '''
---
module: hpe_icsp_os_deployment
short_description: Deploy the operating system on a server using HPE ICsp.
description:
    - Deploy the operating system on a server based on the available ICsp OS build plan.
requirements:
    - "python >= 2.7.9"
    - "hpICsp"
options:
  api_version:
    description:
      - ICsp API version.
    required: true
    default: 300
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
  server_id:
    description:
      - Server ID.
    required: true
  os_build_plan:
    description:
      - OS Build plan.
    required: true
  custom_attributes:
    description:
      - Custom Attributes.
    required: false
    default: null
  personality_data:
    description:
      - Personality Data.
    required: false
    default: null
'''

EXAMPLES = '''
- name: Deploy OS
  hpe_icsp_os_deployment:
    icsp_host: "{{ icsp }}"
    username: "{{ icsp_username }}"
    password: "{{ icsp_password }}"
    server_id: "{{ server_profile.serialNumber }}"
    os_build_plan: "{{ os_build_plan }}"
    custom_attributes: "{{ osbp_custom_attributes }}"
    personality_data: "{{ network_config }}"
  delegate_to: localhost
'''

RETURN = '''
icsp_server:
    description: Has the facts about the server that was provisioned with ICsp.
    returned: When the module runs successfully, but can be null.
    type: complex
'''


def get_build_plan(con, bp_name):
    search_uri = '/rest/index/resources?filter="name=\'' + urllib.quote(bp_name) + '\'"&category=osdbuildplan'
    search_result = con.get(search_uri)

    if search_result['count'] > 0 and search_result['members'][0]['name'] == bp_name:
        return search_result['members'][0]
    return None


def get_server_by_serial(con, serial_number):
    search_uri = '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:\"' + serial_number + '\"\''
    search_result = con.get(search_uri)
    same_serial_number = search_result['members'][0]['attributes']['osdServerSerialNumber'] == serial_number
    if search_result['count'] > 0 and same_serial_number:
        server_id = search_result['members'][0]['attributes']['osdServerId']
        server = {'uri': '/rest/os-deployment-servers/' + server_id}
        return server
    return None


def deploy_server(module):
    # Credentials
    icsp_host = module.params['icsp_host']
    icsp_api_version = module.params['api_version']
    username = module.params['username']
    password = module.params['password']

    # Build Plan Options
    server_id = module.params['server_id']
    os_build_plan = module.params['os_build_plan']
    custom_attributes = module.params['custom_attributes']
    personality_data = module.params['personality_data']
    con = hpICsp.connection(icsp_host, icsp_api_version)

    # Create objects for all necessary resources.
    credential = {'userName': username, 'password': password}
    con.login(credential)

    bp = hpICsp.buildPlans(con)
    jb = hpICsp.jobs(con)
    sv = hpICsp.servers(con)

    bp = get_build_plan(con, os_build_plan)

    if bp is None:
        return module.fail_json(msg='Cannot find OS Build plan: ' + os_build_plan)

    timeout = 600
    while True:
        server = get_server_by_serial(con, server_id)
        if server:
            break
        if timeout < 0:
            module.fail_json(msg='Cannot find server in ICSP.')
            return
        timeout -= 30
        time.sleep(30)

    server = sv.get_server(server['uri'])
    if server['state'] == 'OK':
        return module.exit_json(changed=False, msg="Server already deployed.", ansible_facts={'icsp_server': server})

    if custom_attributes:
        ca_list = []

        for ca in custom_attributes:
            ca_list.append({
                'key': list(ca.keys())[0],
                'values': [{'scope': 'server', 'value': str(list(ca.values())[0])}]})

        ca_list.extend(server['customAttributes'])
        server['customAttributes'] = ca_list
        sv.update_server(server)

    server_data = {"serverUri": server['uri'], "personalityData": None}

    build_plan_body = {"osbpUris": [bp['uri']], "serverData": [server_data], "stepNo": 1}

    hpICsp.common.monitor_execution(jb.add_job(build_plan_body), jb)

    # If the playbook included network personalization, update the server to include it
    if personality_data:
        server_data['personalityData'] = personality_data
        network_config = {"serverData": [server_data]}
        # Monitor the execution of a nework personalization job.
        hpICsp.common.monitor_execution(jb.add_job(network_config), jb)

    server = sv.get_server(server['uri'])
    return module.exit_json(changed=True, msg='OS Deployed Successfully.', ansible_facts={'icsp_server': server})


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_version=dict(required=True, type='int', default=300),
            icsp_host=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            server_id=dict(required=True, type='str'),
            os_build_plan=dict(required=True, type='str'),
            custom_attributes=dict(required=False, type='list', default=None),
            personality_data=dict(required=False, type='dict', default=None)
        ))

    deploy_server(module)


if __name__ == '__main__':
    main()
