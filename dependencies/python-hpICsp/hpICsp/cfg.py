# -*- coding: utf-8 -*-

"""
cfg.py
~~~~~~~~~~~~

This module implements Configuration Files HP ICsp REST API
"""

__title__ = 'cfg'
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


class cfg(object):

    def __init__(self, con):
        self._con = con

    def get_cfg(self, URI=None):
        if (URI):
            body = self._con.get(URI)
        else:
            body = self._con.get(hpICsp.common.uri['cfg'])
        return body

    def update_cfg(self, body):
        cfgID=body['uri'].split('/')[-1]	
        body = self._con.put(hpICsp.common.uri['cfg'] + '/%s' % (cfgID), body)
        return body

    def add_cfg(self, body):
        body = self._con.post(hpICsp.common.uri['cfg'], body)
        return body

    def delete_cfg(self, URI):
        body = self._con.delete(URI)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
