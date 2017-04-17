# -*- coding: utf-8 -*

"""
connection.py
~~~~~~~~~~~~

This module maintains communication with the appliance
"""

__title__ = 'connection'
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

import http.client
import json
import shutil  # for shutil.copyfileobj()
import mmap  # so we can upload the iso without having to load it in memory
import os

from hpICsp.common import *
from hpICsp.exceptions import *


class connectionHPOneView(object):

    def __init__(self, applianceIp, api_version=102):
        self._session = None
        self._host = applianceIp
        self._cred = None
        self._apiVersion = api_version
        self._headers = {
            'X-API-Version': self._apiVersion,
            'Accept': 'application/json, */*',
            'Content-Type': 'application/json'}
        self._proxyHost = None
        self._proxyPort = None
        self._doProxy = False
        self._sslTrustedBundle = None
        self._sslTrustAll = True
        self._nextPage = None
        self._prevPage = None
        self._numTotalRecords = 0
        self._numDisplayedRecords = 0
        self._validateVersion()

    def _validateVersion(self):
        global uri
        version = self.get(uri['version'])
        if 'minimumVersion' in version:
            if self._apiVersion < version['minimumVersion']:
                raise HPICspException('Unsupported API Version')
        if 'currentVersion' in version:
            if self._apiVersion > version['currentVersion']:
                raise HPICspException('Unsupported API Version')

    def set_proxy(self, proxyHost, proxyPort):
        self._proxyHost = proxyHost
        self._proxyPort = proxyPort
        self._doProxy = True

    def set_trusted_ssl_bundle(self, sslBundle):
        self._sslTrustAll = False
        self._sslTrustedBundle = sslBundle

    def get_session(self):
        return self._session

    def get_session_id(self):
        return self._headers['auth']

    def get_host(self):
        return self._host

    def make_url(self, path):
        return 'https://%s%s' % (self._host, path)

    def do_http(self, method, path, body):
        bConnected = False
        while bConnected is False:
            try:
                if self._sslTrustAll is False:
                    import ssl
                    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                    context.verify_mode = ssl.CERT_REQUIRED
                    context.load_verify_locations(self._sslTrustedBundle)
                    if self._doProxy is False:
                        conn = http.client.HTTPSConnection(self._host,
                                                           context=context)
                    else:
                        conn = http.client.HTTPSConnection(self._proxyHost,
                                                           self._proxyPort,
                                                           context=context)
                        conn.set_tunnel(self._host, 443)
                    conn.request(method, path, body, self._headers)
                else:
                    import ssl
                    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                    context.verify_mode = ssl.CERT_NONE
                    if self._doProxy is False:
                        conn = http.client.HTTPSConnection(self._host,
                                                           context=context)
                    else:
                        conn = http.client.HTTPSConnection(self._proxyHost,
                                                           self._proxyPort,
                                                           context=context)
                        conn.set_tunnel(self._host, 443)
                    conn.request(method, path, body, self._headers)
                resp = conn.getresponse()
                try:
                    tempbytes = resp.read()
                    tempbody = tempbytes.decode('utf-8')
                except UnicodeDecodeError:  # Might be binary data
                    tempbody = tempbytes
                    conn.close()
                    bConnected = True
                    return resp, tempbody
                if tempbody:
                    try:
                        body = json.loads(tempbody)
                    except ValueError:
                        body = tempbody
                conn.close()
                bConnected = True
            except http.client.BadStatusLine:
                print('Bad Status Line. Trying again...')
                conn.close()
                time.sleep(1)
                continue
        return resp, body

    def encode_multipart_formdata(self, fields, filename, verbose=False):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data
        to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        if verbose is True:
            print(('Encoding ' + filename + ' for upload...'))
        fin = open(filename, 'rb')
        fout = open(filename + '.b64', 'wb')
        fout.write(bytearray('--' + BOUNDARY + CRLF, 'utf-8'))
        fout.write(bytearray('Content-Disposition: form-data'
                             '; name="file"; filename="' +
                             filename + '"' + CRLF, "utf-8"))
        fout.write(bytearray('Content-Type: application/octet-stream' + CRLF,
                             'utf-8'))
        fout.write(bytearray(CRLF, 'utf-8'))
        shutil.copyfileobj(fin, fout)
        fout.write(bytearray(CRLF, 'utf-8'))
        fout.write(bytearray('--' + BOUNDARY + '--' + CRLF, 'utf-8'))
        fout.write(bytearray(CRLF, 'utf-8'))
        fout.close()
        fin.close()
        return content_type

    def post_multipart(self, path, fields, files, fileName, verbose=False):
        content_type = self.encode_multipart_formdata(fields, files, verbose)
        inputfile = open(files + '.b64', 'rb')
        mappedfile = mmap.mmap(inputfile.fileno(), 0, access=mmap.ACCESS_READ)
        if verbose is True:
            print(('Uploading ' + files + '...'))
        if self._doProxy is False:
            conn = http.client.HTTPSConnection(self._host)
        else:
            conn = http.client.HTTPSConnection(self._proxyHost, self._proxyPort)
            conn.set_tunnel(self._host, 443)
        #conn.set_debuglevel(1)
        conn.connect()
        conn.putrequest('POST', path)
        conn.putheader('uploadfilename', fileName)
        conn.putheader('auth', self._headers['auth'])
        conn.putheader('Content-Type', content_type)
        totalSize = os.path.getsize(files + '.b64')
        conn.putheader('Content-Length', totalSize)
        conn.endheaders()
        while mappedfile.tell() < mappedfile.size():
            # Send 1MB at a time
            # NOTE: Be careful raising this value as the read chunk
            # is stored in RAM
            readSize = 1048576
            conn.send(mappedfile.read(readSize))
            if verbose is True:
                sys.stdout.write('%d bytes sent... \r' % mappedfile.tell())
                sys.stdout.flush()
        mappedfile.close()
        inputfile.close()
        os.remove(files + '.b64')
        response = conn.getresponse()
        body = response.read().decode('utf-8')
        if body:
            try:
                body = json.loads(body)
            except ValueError:
                body = response.read().decode('utf-8')
        conn.close()
        return response, body

    def get_content_type(filename):
        return 'application/octet-stream'

    ###########################################################################
    # Utility functions for making requests - the HTTP verbs
    ###########################################################################
    def get(self, uri):
        resp, body = self.do_http('GET', uri, '')
        if resp.status >= 400:
            raise HPICspException(body)
        if resp.status == 302:
            body = self.get(resp.getheader('Location'))
        if type(body) is dict:
            if 'nextPageUri' in body:
                self._nextPage = body['nextPageUri']
            if 'prevPageUri' in body:
                self._prevPage = body['prevPageUri']
            if 'total' in body:
                self._numTotalRecords = body['total']
            if 'count' in body:
                self._numDisplayedRecords = body['count']
        return body

    def getNextPage(self):
        body = self.get(self._nextPage)
        return get_members(body)

    def getPrevPage(self):
        body = self.get(self._prevPage)
        return get_members(body)

    def getLastPage(self):
        while self._nextPage is not None:
            members = self.getNextPage()
        return members

    def getFirstPage(self):
        while self._prevPage is not None:
            members = self.getPrevPage()
        return members

    def put(self, uri, body):
        resp, body = self.do_http('PUT', uri, json.dumps(body))
        if resp.status >= 400:
            raise HPICspException(body)
        return body

    def post(self, uri, body):
        resp, body = self.do_http('POST', uri, json.dumps(body))
        if resp.status >= 400:
            print(resp.status,body)
            raise HPICspException(body)
        return body

    def get_entities_byrange(self, uri, field, xmin, xmax):
        new_uri = uri + '?filter="\'' + field + '\'%20>%20\'' + xmin \
            + '\'"&filter="\'' + field + '\'%20<%20\'' + xmax \
            + '\'"&start=0&count=-1'
        body = self.get(new_uri)
        return get_members(body)

    def get_entities_byfield(self, uri, field, value):
        new_uri = uri + '?filter="' + field + '%20EQ%20\'' + value + '\'"'
        try:
            body = self.get(new_uri)
        except:
            print(new_uri)
            raise
        return get_members(body)

    def get_entity_byfield(self, uri, field, value):
        new_uri = uri + '?filter="\'' + field + '\'%20=%20\'' + value \
            + '\'"&start=0&count=-1'
        body = self.get(new_uri)
        return get_member(body)

    def conditional_post(self, uri, body):
        try:
            entity = self.post(uri, body)
        except HPICspException as e:
            # this may have failed because the entity already exists,
            # unfortunately there is not a uniform way to report this,
            # so we just try to find an existing entity with the same name
            # and return it assuming all names are unique (which is a
            # reasonable assumption)
            if 'DUPLICATE' in e.errorCode and 'NAME' in e.errorCode:
                try:
                    entity = self.get_entity_byfield(uri, 'name', body['name'])
                except Exception:
                    # Didn't find the entity, raise exception
                    raise e
                if not entity:
                    raise e
            else:
                raise e
        return entity

    def delete(self, uri):
        resp, body = self.do_http('DELETE', uri, '')
        if resp.status >= 400 and resp.status != 404:
            raise HPICspException(body)
        return body

    ###########################################################################
    # EULA
    ###########################################################################
    def get_eula_status(self):
        global uri
        return(self.get(uri['eulaStatus']))

    def set_eula(self, supportAccess='yes'):
        global uri
        eula = make_eula_dict(supportAccess)
        self.post(uri['eulaSave'], eula)
        return

    ###########################################################################
    # Appliance Network Interfaces
    ###########################################################################
    def get_appliance_network_interfaces(self):
        global uri
        return(self.get(uri['applianceNetworkInterfaces']))

    def set_appliance_network_interface(self, interfaceConfig):
        global uri
        self.post(uri['applianceNetworkInterfaces'], interfaceConfig)
        return

    ###########################################################################
    # Initial Setup
    ###########################################################################
    def change_initial_password(self, newPassword):
        global uri
        password = make_initial_password_change_dict('Administrator',
                                                     'admin', newPassword)
        # This will throw an exception if the password is already changed
        self.post(uri['changePassword'], password)

    def set_service_access(self, serviceAccess):
        global uri
        resp = self.put(uri['serviceAccess'], serviceAccess)
        if resp is True:
            return
        else:
            raise HPICspException('Could not change Service Access')

    ###########################################################################
    # Login/Logout to/from appliance
    ###########################################################################
    def login(self, cred, verbose=False):
        global uri
        self._cred = cred
        try:
            body = self.post(uri['loginSessions'], self._cred)
        except HPICspException:
            raise
        auth = body['sessionID']
        # Add the auth ID to the headers dictionary
        self._headers['auth'] = auth
        self._session = True
        if verbose is True:
            print(('Session Key: ' + auth))

    def logout(self, verbose=False):
        global uri
        #resp, body = self.do_http(method, uri['loginSessions'] \
        #                        , body, self._headers)
        try:
            self.delete(uri['loginSessions'])
        except HPICspException:
            raise
        if verbose is True:
            print('Logged Out')
        del self._headers['auth']
        self._session = False
        return None
