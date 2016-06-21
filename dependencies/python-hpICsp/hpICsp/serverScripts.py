# -*- coding: utf-8 -*-

"""
serverScripts.py
~~~~~~~~~~~~

This module implements Server Scripts HP ICsp REST API
"""

__title__ = 'serverScripts'
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


class serverScripts(object):

    def __init__(self, con):
        self._con = con

    def get_script(self, URI=None, start=0, count=-1):
        if (URI):
            body = self._con.get(URI)
        else:
            body = self._con.get(hpICsp.common.uri['serverScript'] + '?start=%s&count=%s' % (start, count))         
        return body

    def update_script(self, body):
        scriptID=body['uri'].split('/')[-1]
        body = self._con.put(hpICsp.common.uri['serverScript'] + '/%s' % (scriptID), body)
        return body

    def add_script(self, body):
        body = self._con.post(hpICsp.common.uri['serverScript'], body)
        return body

    def delete_script(self, URI):
        body = self._con.delete(URI)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
