#!/usr/bin/env python
"""
HP ICsp Library
~~~~~~~~~~~~~~~~~~~~~

"""

__title__ = 'hpICsp'
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
# AUTHORS OR COPYRIGHT HOLDERS be LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import sys

from hpICsp.common import *
from hpICsp.exceptions import *
from hpICsp.buildPlans import *
from hpICsp.serverScripts import *
from hpICsp.ogfsScripts import *
from hpICsp.settings import *
from hpICsp.packages import *
from hpICsp.servers import *
from hpICsp.jobs import *
from hpICsp.facility import *
from hpICsp.cfg import *
from hpICsp.deviceGroups import *
from hpICsp.connectionHPOneView import *
from hpICsp.connection import *


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HP ICsp Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=True,
                        help='HP ICsp Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=True,
                        help='HP ICsp Password')
    parser.add_argument('-c', '--certificate', dest='cert', required=False,
                        help='Trusted SSL Certificate Bundle in PEM '
                        '(Base64 Encoded DER) Format')
    parser.add_argument('-r', '--proxy', dest='proxy', required=False,
                        help='Proxy (host:port format')
    args = parser.parse_args()
    con = connection(args.host)
    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)
    credential = {'userName': args.user, 'password': args.passwd}
    con.login(credential)
    con.logout()

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
