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

import mock
import pytest

from oneview_module_loader import ICspHelper

DEFAULT_SERVER = {
    "name": "SP-01",
    "uri": "/uri/239",
    "ilo": {"ipAddress": "16.124.135.239"},
    "state": "",
    'attributes': {'osdServerId': '123456', 'osdServerSerialNumber': 'VCGYZ33007'},
    "customAttributes": []
}

DEFAULT_SERVER_NO_ILO = {
    "name": "SP-01",
    "uri": "/uri/239",
    "ilo": None,
    "state": "",
    'attributes': {'osdServerId': '123456', 'osdServerSerialNumber': 'VCGYZ33007'},
    "customAttributes": []
}

DEFAULT_BUILD_PLAN = {"name": "RHEL 7.2 x64", "uri": "/rest/os-deployment-build-plans/222"}


class TestICspHelper():
    """
    ICspHelperSpec provides the mocks used in this test case.
    """

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.mock_connection = mock.Mock()
        self.mock_connection.login.return_value = {}

    def get_as_rest_collection(self, server):
        return {
            'members': server,
            'count': len(server)
        }

    def test_get_build_plan_with_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN])]

        icsphelper = ICspHelper(self.mock_connection)
        plan = icsphelper.get_build_plan('RHEL 7.2 x64')

        expected = {'name': 'RHEL 7.2 x64', 'uri': '/rest/os-deployment-build-plans/222'}
        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?filter="name=\'RHEL%207.2%20x64\'"&category=osdbuildplan')

        assert plan == expected

    def test_get_build_plan_with_non_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN])]

        icsphelper = ICspHelper(self.mock_connection)
        plan = icsphelper.get_build_plan('BuildPlan')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?filter="name=\'BuildPlan\'"&category=osdbuildplan')

        assert plan is None

    def test_should_fail_when_os_build_plan_not_found(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([])]

        icsphelper = ICspHelper(self.mock_connection)
        plan = icsphelper.get_build_plan('RHEL 7.2 x64')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?filter="name=\'RHEL%207.2%20x64\'"&category=osdbuildplan')

        assert plan is None

    def test_get_server_by_ilo_address_with_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_ilo_address('16.124.135.239')

        self.mock_connection.get.assert_called_once_with(
            '/rest/os-deployment-servers/?count=-1')

        assert server == DEFAULT_SERVER

    def test_get_server_by_ilo_address_with_non_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_ilo_address('16.124.135.255')

        self.mock_connection.get.assert_called_once_with(
            '/rest/os-deployment-servers/?count=-1')

        assert server is None

    def test_get_server_by_ilo_address_with_servers_with_no_ilo(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER_NO_ILO])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_ilo_address('16.124.135.239')

        self.mock_connection.get.assert_called_once_with(
            '/rest/os-deployment-servers/?count=-1')

        assert server is None

    def test_get_server_by_ilo_address_with_no_registered_servers(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_ilo_address('16.124.135.239')

        self.mock_connection.get.assert_called_once_with(
            '/rest/os-deployment-servers/?count=-1')

        assert server is None

    def test_get_server_by_serial_with_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_serial('VCGYZ33007')

        expected = {'uri': '/rest/os-deployment-servers/123456'}
        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:"VCGYZ33007"\'')

        assert server == expected

    def test_get_server_by_serial_with_non_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_serial('000')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:"000"\'')

        assert server is None

    def test_get_server_by_serial_with_no_registered_servers(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([])]

        icsphelper = ICspHelper(self.mock_connection)
        server = icsphelper.get_server_by_serial('000')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:"000"\'')

        assert server is None


if __name__ == '__main__':
    pytest.main([__file__])
