#!/usr/bin/python

__author__ = 'ChakruHP'

DOCUMENTATION = '''
---
module: hp_icsp
short_description: Manage servers lifecycle using OneView Server profiles using a server profile template.

Example :

   hp_icsp:
     icsp_host:
     icsp_user:
     icsp_pass:
     server_id: serial_number
     os_build_plan: build_plan
     custom_arguments: "{{ args }}"

'''

import hpICsp
from hpICsp.exceptions import *


def get_build_plan(con, bp_name):
    bp=hpICsp.buildPlans(con)
    build_plans = bp.get_build_plans()['members']
    return next((bp  for bp in build_plans if bp['name'] == bp_name), None)


def get_server_by_serial(con, serial_number):
    search_uri='/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:\"'+serial_number+'\"\''
    search_result = con.get(search_uri)
    if search_result['count'] > 0 and search_result['members'][0]['attributes']['osdServerSerialNumber'] == serial_number:
        server_id = search_result['members'][0]['attributes']['osdServerId']
        server= {'uri':'/rest/os-deployment-servers/'+server_id}
        return server
    return None

def deploy_server(module):
    icsp_host = module.params['icsp_host']
    username = module.params['username']
    password = module.params['password']
    server_id = module.params['server_id']
    os_build_plan = module.params['os_build_plan']
    custom_attributes = module.params['custom_attributes']
    personality_data= module.params['personality_data']
    con=hpICsp.connection(icsp_host)
    #Create objects for all necessary resources.

    credential = {'userName': username, 'password': password}
    con.login(credential)

    bp=hpICsp.buildPlans(con)
    jb=hpICsp.jobs(con)
    sv=hpICsp.servers(con)

    bp = get_build_plan(con, os_build_plan)

    if bp is None:
        module.fail_json(msg='Cannot find OS Build plan ' + os_build_plan )

    timeout = 600
    while True:
        server = get_server_by_serial(con, server_id)
        if server:
            break
        if timeout < 0:
            module.fail_json(msg = 'Cannot find server in ICSP')
        timeout -= 30
        time.sleep(30)

    server = sv.get_server(server['uri'])
    if server['state'] == 'OK':
        module.exit_json(changed=False, msg="Server already deployed", ansible_facts={'icsp_server': server} )

    if custom_attributes:
        ca_list = [ {'key':ca.keys()[0], 'values':[{'scope': 'server', 'value':str(ca.values()[0])}]} for ca in custom_attributes ]

        ca_list.extend(server['customAttributes'])
        server['customAttributes'] = ca_list
        sv.update_server(server)

    server_data = {"serverUri":server['uri']}

    buildPlanBody={"osbpUris":[bp['uri']],"serverData":[server_data]}

    hpICsp.common.monitor_execution(jb.add_job(buildPlanBody),jb)

    if personality_data:
        server_data['personalityData'] = personality_data

    networkConfig = {"serverData":[server_data]}

    # Monitor the execution of a nework personalization job.
    hpICsp.common.monitor_execution(jb.add_job(networkConfig),jb)

    server = sv.get_server(server['uri'])
    module.exit_json(changed=True, msg='Deployed OS', ansible_facts={'icsp_server': server})


def main():
    module = AnsibleModule(
        argument_spec=dict(
            icsp_host=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            server_id=dict(required=True, type='str'),
            os_build_plan=dict(required=True, type='str'),
            custom_attributes=dict(required=False, type='list', default=None),
            personality_data=dict(required=False, type='dict', default=None)
            ))

    try:

        deploy_server(module)
        module.exit_json(
            changed=True, msg='Deployed'
        )
    except Exception, e:
        module.fail_json(msg=e.message )

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
