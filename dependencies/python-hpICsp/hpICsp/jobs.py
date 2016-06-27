 # -*- coding: utf-8 -*-

"""
jobs.py
~~~~~~~~~~~~

This module implements Jobs HP ICsp REST API
"""

__title__ = 'jobs'
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

from hpICsp.exceptions import *
import hpICsp.common


class jobs(object):

    def __init__(self, con):
        self._con = con

    def get_job(self, URI=None):
        if (URI):
            body = self._con.get(URI)
        else:
            body = self._con.get(hpICsp.common.uri['job'])
        return body
		
    def add_job(self, body, runTime = None, jobName= None, force= False):
        if (runTime):
            if (jobName):
                body = self._con.post(hpICsp.common.uri['job'] + '?time=%s&title=%s' % (runTime,jobName), body)
            else:
                body = self._con.post(hpICsp.common.uri['job'] + '?time=%s' % (runTime), body)			
        elif (jobName):
            body = self._con.post(hpICsp.common.uri['job'] + '?title=%s' % (jobName), body)
        else:
            force_args=''
            if force:
                force_args = '?force=true'
            body = self._con.post(hpICsp.common.uri['job'] + force_args , body)
        return body

    def stop_job(self, URI):
        jobParse = self._con.get(URI)
        if (jobParse['name'] != 'Run OS Build Plans'):
            bpID=jobParse['uriOfJobType'].split('/')[-1]
            if (len(jobParse['jobServerInfo']) == 1):
                servID=jobParse['jobServerInfo'][0]['jobServerUri'].split('/')[-1]
                newURI=URI + '/stop?bp=' + bpID + '&server=' + servID
                body=self._con.put(newURI, None)
            else:
                for serv in jobParse['jobServerInfo']:
                    servID=serv['jobServerUri'].split('/')[-1]
                    newURI=URI+'/stop?bp='+bpID+'&server='+servID
                    body=self._con.put(newURI, None)						
        else:
            newURI=URI+'/stop?bp=0&server=0'
            stopBody={'uri':URI,'bpURI':'/rest/os-deployment-apxs/1770001','serverURI':'/rest/os-deployment-servers/0','serverName':"",'chainedJob':'true','pendingJob':'False'}
            body=self._con.put(newURI,stopBody)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
