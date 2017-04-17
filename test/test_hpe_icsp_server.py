#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

import unittest
import mock
import yaml

from test.utils import create_ansible_mock_yaml, create_ansible_mock

from hpe_icsp_server import ICspServerModule
from hpe_icsp_server import SERVER_ALREADY_PRESENT, SERVER_ALREADY_ABSENT, CUSTOM_ATTR_NETWORK_UPDATED, \
    SERVER_PERSONALITY_DATA_REQUIRED, SERVER_NOT_FOUND

from hpICsp.exceptions import HPICspInvalidResource

SERVER_IP = "16.124.135.239"

YAML_SERVER_PRESENT = """
    state: present
    icsp_host: "16.124.133.245"
    username: "Administrator"
    password: "admin"
    server_ipAddress: "16.124.135.239"
    server_username: "Admin"
    server_password: "serveradmin"
    server_port: 443
"""

YAML_SERVER_ABSENT = """
    state: absent
    icsp_host: "16.124.133.251"
    username: "Administrator"
    password: "admin"
    server_ipAddress: "16.124.135.239"
"""

YAML_NETWORK_CONFIGURED = """
    state: network_configured
    icsp_host: "16.124.133.245"
    username: "Administrator"
    password: "admin"
    server_ipAddress: "16.124.135.239"
    server_username: "Admin"
    server_password: "serveradmin"
    server_port: 443
    server_personality_data:
      network_config:
          hostname: "test-web.io.fc.hpe.com"
          domain: "demo.com"
          interfaces:
          - macAddress: "01:23:45:67:89:ab"
            enabled: true
            dhcpv4: false
            ipv6Autoconfig:
            dnsServers:
            - "16.124.133.2"
            staticNetworks:
            - "16.124.133.39/255.255.255.0"
            vlanid: -1
            ipv4gateway: "16.124.133.1"
            ipv6gateway:
          virtualInterfaces:
"""

DEFAULT_SERVER = {"name": "SP-01", "uri": "/uri/239", "ilo": {"ipAddress": SERVER_IP}}
SERVER_ADDED = {"name": "SP-03", "uri": "/uri/188", "ilo": {"ipAddress": "16.124.135.188"}}

SERVERS = {
    "members": [
        DEFAULT_SERVER,
        {"name": "SP-02", "uri": "/uri/233", "ilo": {"ipAddress": "16.124.135.233"}}
    ]
}

CONNECTION = {}
ICSP_JOBS = {}

JOB_RESOURCE = {"uri": "/rest/os-deployment-jobs/123456"}


class IcspServerSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch('hpe_icsp_server.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.patcher_icsp_service = mock.patch('hpe_icsp_server.hpICsp')
        self.mock_icsp = self.patcher_icsp_service.start()

        self.mock_connection = mock.Mock()
        self.mock_connection.login.return_value = CONNECTION
        self.mock_icsp.connection.return_value = self.mock_connection

        self.mock_server_service = mock.Mock()
        self.mock_icsp.servers.return_value = self.mock_server_service

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_icsp_service.stop()

    def test_should_not_add_server_when_already_present(self):
        self.mock_connection.get.return_value = SERVERS
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SERVER_ALREADY_PRESENT,
            ansible_facts=dict(target_server=DEFAULT_SERVER)
        )

    def test_should_add_server(self):
        self.mock_connection.get.side_effect = [{'members': []}, SERVERS]
        self.mock_server_service.add_server.return_value = JOB_RESOURCE
        self.mock_icsp.jobs.return_value = ICSP_JOBS

        self.mock_icsp.common = mock.Mock()
        self.mock_icsp.common.monitor_execution.return_value = {}

        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        ilo_body = {'ipAddress': "16.124.135.239",
                    'username': "Admin",
                    'password': "serveradmin",
                    'port': 443}
        self.mock_server_service.add_server.assert_called_once_with(ilo_body)
        self.mock_icsp.common.monitor_execution.assert_called_once_with(JOB_RESOURCE, ICSP_JOBS)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg="Server created: '/uri/239'",
            ansible_facts=dict(target_server=DEFAULT_SERVER)
        )

    def test_expect_exception_not_caught_when_create_server_raise_exception(self):
        self.mock_connection.get.side_effect = [{'members': []}, SERVERS]
        self.mock_server_service.add_server.side_effect = Exception("message")

        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        try:
            ICspServerModule().run()
        except Exception as e:
            self.assertEqual("message", e.args[0])
        else:
            self.fail("Expected Exception was not raised")

    def test_should_not_try_delete_server_when_it_is_already_absent(self):
        self.mock_connection.get.return_value = {'members': []}
        self.mock_server_service.delete_server.return_value = {}
        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        self.mock_server_service.delete_server.assert_not_called()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SERVER_ALREADY_ABSENT
        )

    def test_should_delete_server(self):
        self.mock_connection.get.return_value = SERVERS

        self.mock_server_service.delete_server.return_value = {}

        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        self.mock_server_service.delete_server.assert_called_once_with("/uri/239")

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg="Server '/uri/239' removed successfully from ICsp."
        )

    def test_should_fail_with_all_exe_attr_when_HPICspException_raised_on_delete(self):
        self.mock_connection.get.return_value = SERVERS
        exeption_value = {"message": "Fake Message", "details": "Details", "errorCode": "INVALID_RESOURCE"}
        self.mock_server_service.delete_server.side_effect = HPICspInvalidResource(exeption_value)

        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg='{"errorCode": "INVALID_RESOURCE", "message": "Fake Message", "details": "Details"}')

    def test_should_fail_with_args_joined_when_common_exception_raised_on_delete(self):
        self.mock_connection.get.return_value = SERVERS
        self.mock_server_service.delete_server.side_effect = Exception("Fake Message", "INVALID_RESOURCE")

        mock_ansible_instance = create_ansible_mock_yaml(YAML_SERVER_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg='Fake Message; INVALID_RESOURCE')

    def test_should_configure_network(self):
        self.mock_connection.get.side_effect = [SERVERS, SERVERS]
        self.mock_connection.post.return_value = JOB_RESOURCE
        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        mock_ansible_instance = create_ansible_mock_yaml(YAML_NETWORK_CONFIGURED)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        network_config_state = yaml.load(YAML_NETWORK_CONFIGURED)

        network_config = {
            "serverData": [
                {"serverUri": DEFAULT_SERVER['uri'], "personalityData": network_config_state['server_personality_data'],
                 "skipReboot": True}],
            "failMode": None,
            "osbpUris": []
        }

        uri = '/rest/os-deployment-jobs/?writeOnly=true'

        self.mock_connection.post.assert_called_once_with(uri, network_config)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=CUSTOM_ATTR_NETWORK_UPDATED,
            ansible_facts=dict(target_server=DEFAULT_SERVER)
        )

    def test_should_fail_when_try_configure_network_without_inform_personality_data(self):
        self.mock_connection.get.return_value = SERVERS
        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        params_config_network = yaml.load(YAML_NETWORK_CONFIGURED)
        params_config_network['server_personality_data'] = {}

        mock_ansible_instance = create_ansible_mock(params_config_network)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=SERVER_PERSONALITY_DATA_REQUIRED)

    def test_should_fail_when_try_configure_network_for_not_found_server(self):
        self.mock_connection.get.return_value = {'members': []}

        mock_ansible_instance = create_ansible_mock_yaml(YAML_NETWORK_CONFIGURED)
        self.mock_ansible_module.return_value = mock_ansible_instance

        ICspServerModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(changed=False, msg=SERVER_NOT_FOUND)

    def test_expect_exception_not_caught_when_configure_network_raise_exception(self):
        self.mock_connection.get.return_value = SERVERS
        self.mock_connection.post.side_effect = Exception("message")

        mock_ansible_instance = create_ansible_mock_yaml(YAML_NETWORK_CONFIGURED)
        self.mock_ansible_module.return_value = mock_ansible_instance

        try:
            ICspServerModule().run()
        except Exception as e:
            self.assertEqual("message", e.args[0])
        else:
            self.fail("Expected Exception was not raised")

    if __name__ == '__main__':
        unittest.main()
