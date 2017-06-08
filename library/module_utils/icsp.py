#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright 2017 Hewlett Packard Enterprise Development LP
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

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from future import standard_library
from urllib.parse import quote
import logging

standard_library.install_aliases()
logger = logging.getLogger(__name__)


class ICspHelper(object):

    def __init__(self, connection):
        """
        ICspHelper constructor.

        Args:
            connection (connection): ICsp connection.
        """
        self.connection = connection

    def get_build_plan(self, bp_name):
        search_uri = '/rest/index/resources?filter="name=\'' + quote(bp_name) + '\'"&category=osdbuildplan'
        search_result = self.connection.get(search_uri)

        if search_result['count'] > 0 and search_result['members'][0]['name'] == bp_name:
            return search_result['members'][0]
        return None

    def get_server_by_ilo_address(self, ilo):
        servers = self.connection.get("/rest/os-deployment-servers/?count=-1")
        for srv in servers['members']:
            if srv['ilo']:
                if srv['ilo']['ipAddress'] == ilo:
                    return srv
        return None

    def get_server_by_serial(self, serial):
        search_uri = '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:\"' + serial + '\"\''
        search_result = self.connection.get(search_uri)
        if search_result['count'] > 0:
            same_serial_number = search_result['members'][0]['attributes']['osdServerSerialNumber'] == serial

            if same_serial_number:
                server_id = search_result['members'][0]['attributes']['osdServerId']
                server = {'uri': '/rest/os-deployment-servers/' + server_id}
                return server
        return None
