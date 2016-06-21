#!/usr/bin/env python


import hpICsp
from hpICsp.exceptions import *

import urllib

def get_build_plan(con, bp_name):
    #search_uri='/rest/index/resources?category=osdbuildplan&query=\'osbuildplanname:\"'+urllib.quote_plus(bp_name)+'\"\''
    #search_result = con.get(search_uri)
    #print search_result
    #if search_result['count'] > 0 and search_result['members'][0]['attributes']['name'] == bp_name:
    #    osbp_uri = search_result['members'][0]['attributes']['uri']
    #    bp=hpICsp.buildPlans(con)
    #    return bp.get_build_plans(osbp_uri)


    #return None
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
        #sv=hpICsp.servers(con)
        #return sv.get_server(server_id)
    return None


def get_server(con, serial_number):
    sv=hpICsp.servers(con)

    servers = sv.get_server()['members']
    return next((server for server in servers if server['serialNumber'] == serial_number), None)

def main():

    icsp_host = 'icsp.vse.rdlabs.hpecorp.net'
    username = 'Administrator'
    password = 'hpvse123'
    server_id = ''
    os_build_plan = ''
    #args = module.params['args']

    con=hpICsp.connection(icsp_host)
    #Create objects for all necessary resources.
    bp=hpICsp.buildPlans(con)
    jb=hpICsp.jobs(con)


    credential = {'userName': username, 'password': password}
    con.login(credential)
    #try:
        #bp = get_build_plan(con, "CHEF - RHEL 7.0 x64")
        #print bp
        #print str(bp)

    #except Exception , e:
    #    print e.message
    #    raise
    #'uri': u'/rest/os-deployment-build-plans/1340001'

    sv=hpICsp.servers(con)
    server = get_server_by_serial(con, "VCGUS6O00W")
    server = sv.get_server(server['uri'])
    print server
    #'uri': u'/rest/os-deployment-servers/2050001'


    existing_ca_list = server['customAttributes']
    print "existing"
    print existing_ca_list

    print "after"
    existing_ca_list = [ {'key':ca.keys()[0], 'values':[{'scope': 'server', 'value':ca.values()[0]}]} for ca in existing_ca_list if ca['key'] not in ['hpsa_netconfig'] ]
    print existing_ca_list
    #print bp
    #print server
    #buildPlanBody={"osbpUris":[bp['uri']],"serverData":[{"serverUri":server['uri']}]}
    #hpICsp.common.monitor_execution(jb.add_job(buildPlanBody),jb)

    return


    #Parse the job output to retrieve the ServerID and create a JSON body with it.
    serverID=status['jobResult'][0]['jobResultLogDetails'].split('ServerRef:')[1].split(')')[0]
    buildPlanBody={"osbpUris":[buildPlanURI],"serverData":[{"serverUri":"/rest/os-deployment-servers/" + serverID}]}

    #Monitor the execution of a build plan which installs RedHat 6.4 on the server just added.
    hpICsp.common.monitor_execution(jb.add_job(buildPlanBody),jb)

    #Generate a JSON body for some post network configuration.
    networkConfig = {"serverData":[{"serverUri":'/rest/os-deployment-servers/' + serverID,"personalityData":{"hostName":hostName,"displayName":displayName}}]}

    #Monitor the execution of a nework personalization job.
    hpICsp.common.monitor_execution(jb.add_job(networkConfig),jb)




def old_main():
    #Credentials to login to Insight Control server provisioning appliance.
    applianceIP = config.get('Main', 'applianceIP')
    applianceUser = config.get('Main', 'applianceUser')
    appliancePassword = config.get('Main', 'appliancePassword')
    #Build Plan URI of Red Hat 6.4 Installation.
    buildPlanURI = config.get('Main','buildPlanURI')
    #iLo Credentials for server to be added.
    iLoIP = config.get('Main','iLoIP')
    iLoUser = config.get('Main','iLoUser')
    iLoPassword = config.get('Main','iLoPassword')
    #Post network condiguration parameters to be altered.
    hostName = config.get('Main','hostName')
    displayName = config.get('Main','displayName')

    #Creates a JSON body for adding an iLo.
    iLoBody={'username' : iLoUser, 'password' : iLoPassword, 'port' : 443 , 'ipAddress' : iLoIP}

#Add a server from its iLo credentials, runs a build plan to install an OS on it, run a personalization apx for post network configuration.
def main2():
    #Creates a connection with the appliance.
    con=hpICsp.connection(applianceIP)
	#Create objects for all necessary resources.
    bp=hpICsp.buildPlans(con)
    jb=hpICsp.jobs(con)
    sv=hpICsp.servers(con)

    #Login using parsed login information
    credential = {'userName': applianceUser, 'password': appliancePassword}
    con.login(credential)


    #Add server by iLo credentials.
	#Monitor_execution is a utility method to watch job progress on the command line.
	#Pass in the method which starts a job as well as a job resource object.
    status=hpICsp.common.monitor_execution(sv.add_server(iLoBody),jb)
	
	#Parse the job output to retrieve the ServerID and create a JSON body with it.
    serverID=status['jobResult'][0]['jobResultLogDetails'].split('ServerRef:')[1].split(')')[0]
    buildPlanBody={"osbpUris":[buildPlanURI],"serverData":[{"serverUri":"/rest/os-deployment-servers/" + serverID}]}
	
    #Monitor the execution of a build plan which installs RedHat 6.4 on the server just added.
    hpICsp.common.monitor_execution(jb.add_job(buildPlanBody),jb)

 	#Generate a JSON body for some post network configuration.
    networkConfig = {"serverData":[{"serverUri":'/rest/os-deployment-servers/' + serverID,"personalityData":{"hostName":hostName,"displayName":displayName}}]}
	
	#Monitor the execution of a nework personalization job.
    hpICsp.common.monitor_execution(jb.add_job(networkConfig),jb)

    #Logout when everything has completed.
    con.logout()

if __name__ == '__main__':
    import sys
    sys.exit(main())
