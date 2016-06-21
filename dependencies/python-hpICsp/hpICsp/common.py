# -*- coding: utf-8 -*-
from __future__ import print_function

"""
common.py
~~~~~~~~~~~~

This module implements the common and helper functions for ICsp
"""

__title__ = 'common'
__version__ = '1.0.0'
__copyright__ = '(C) Copyright 2014 Hewlett-Packard Development ' \
                ' Company, L.P.'
__license__ = 'MIT'
__status__ = 'Development'

###
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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



import sys
import time
import json
from hpICsp.exceptions import *



uri = {
    'build': '/rest/os-deployment-build-plans', 
    'serverScript': '/rest/os-deployment-server-scripts',
    'ogfsScript': '/rest/os-deployment-ogfs-scripts',
    'settings': '/rest/os-deployment-settings',
    'importContent': '/rest/os-deployment-settings/importContent',
    'exportContent': '/rest/os-deployment-settings/exportContent',
    'zip': '/rest/os-deployment-install-zips',
    'server': '/rest/os-deployment-servers',
    'job': '/rest/os-deployment-jobs',
    'facility': '/rest/os-deployment-facility',
    'cfg': '/rest/os-deployment-install-cfgfiles',
    'deviceGroup': '/rest/os-deployment-device-groups',
	
    'loginSessions': '/rest/login-sessions',
    'version': '/rest/version',
    'eulaStatus': '/rest/appliance/eula/status',
    'eulaSave': '/rest/appliance/eula/save',
    'applianceNetworkInterfaces': '/rest/appliance/network-interfaces',
    'changePassword': '/rest/users/changePassword',
    'serviceAccess': '/rest/appliance/settings/enableServiceAccess',
}

############################################################################
# Utility to print resource to standard output
############################################################################
		
def print_entity(entity):
    print (json.dumps(entity, sort_keys=True, indent=4, separators=(',', ': ')))
	

def get_members(mlist):
    if not mlist:
        return []
    if not mlist['members']:
        return []
    return mlist['members']


def get_member(mlist):
    if not mlist:
        return None
    if not mlist['members']:
        return None
    return mlist['members'][0]	
	
def make_eula_dict(supportAccess):
    return {'supportAccess': supportAccess}


def make_initial_password_change_dict(userName, oldPassword, newPassword):
    return {
        'userName': userName,
        'oldPassword': oldPassword,
        'newPassword': newPassword}	
	
	
	
############################################################################
# Utility to simplify job execution and output
############################################################################		

def monitor_execution(run,job):
# run is the JSON output of an add job call.
# job is a job object connected to the appliance.

# This method allows a user to start a job and monitor its
# progress on the command line. If it fails, an exception will
# print the log associated with the failure. If succesful, the final 
# job status is returned for the user to manipulate if necessary.
    if ('uri' not in run):
        raise HPICspException('Failed to Start Job')
    print('Job Added')
    status=job.get_job(run['uri'])
    while (status['running'] == 'true'):
        for x in range (0,5):
            b = status['name'] + ' Executing' + '.' * x
            print(b, end='\r')
            sys.stdout.write('\033[K')
            time.sleep(5)
        status=job.get_job(run['uri'])   
    if (status['state'] == 'STATUS_FAILURE'):
        log = status['jobResult'][0]['jobResultLogDetails'] 
        raise HPICspException(status['name'] +  ' failed to complete\nPrinting log:\n' + log)
    elif (status['state'] == 'STATUS_SUCCESS'):
        print(status['name'] + ' succesfully executed') 
    elif (status['state'] == 'STATUS_PENDING'):
        print(status['name'] + ' will execute at ' + status['created'])
    else:
        raise HPICspException('Unexpected Job Status')
    return status


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
