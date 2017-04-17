#!/usr/bin/env python3

###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

import hpICsp
from hpICsp.exceptions import *
import argparse
import configparser

#Retrieve various credentials from a configuration file.
parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument('--file',
                    dest='configFile',
                    type=str,
                    help='Config File',
                    default='config.cfg')
args = parser.parse_args()
config = configparser.RawConfigParser()
config.read(args.configFile)

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
def main():
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
