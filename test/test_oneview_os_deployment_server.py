#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2017) Hewlett Packard Enterprise Development LP
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

from oneview_module_loader import OsDeploymentServerModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class OsDeploymentServerkModuleSpec(unittest.TestCase,
                                    OneViewBaseTestCase):
    """
    OneViewBaseTestCase has common test for main function,
    also provides the mocks used in this test case.
    """

    def setUp(self):
        self.configure_mocks(self, OsDeploymentServerModule)
        self.os_deployment_plans = self.mock_ov_client.os_deployment_servers

        # Load scenarios from module examples
        self.DEPLOYMENT_SERVER_CREATE = self.EXAMPLES[0]['oneview_os_deployment_server']
        self.DEPLOYMENT_SERVER_UPDATE = self.EXAMPLES[2]['oneview_os_deployment_server']
        self.DEPLOYMENT_SERVER_DELETE = self.EXAMPLES[4]['oneview_os_deployment_server']
        self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES = {
            "config": "{{ config_file_path }}",
            "state": "present",
            "data": {
                "name": 'Test Deployment Server',
                "description": "OS Deployment Server",
                "mgmtNetworkName": "Deployment",
                "applianceName": "0000A66103, appliance 2"
            }

        }

    def test_add_deployment_server(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE

        OsDeploymentServerModule().run()

        self.os_deployment_plans.add.assert_called_once_with({
            "name": 'Test Deployment Server',
            "description": "OS Deployment Server",
            "mgmtNetworkUri": "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535",
            "applianceUri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_CREATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_should_replace_names_by_uris_before_add(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}
        self.mock_ov_client.ethernet_networks.get_by.return_value = [
            {"name": "Deployment", "uri": "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"}]
        self.mock_ov_client.os_deployment_servers.get_appliance_by_name.return_value = {
            "name": "0000A66103, appliance 2",
            "uri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.os_deployment_plans.add.assert_called_once_with({
            "name": 'Test Deployment Server',
            "description": "OS Deployment Server",
            "mgmtNetworkUri": "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535",
            "applianceUri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_CREATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_replace_net_names_by_uris_should_search_fc(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}

        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ov_client.fc_networks.get_by.return_value = [
            {"name": "Deployment", "uri": "/rest/fc-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"}]
        self.mock_ov_client.os_deployment_servers.get_appliance_by_name.return_value = {
            "name": "0000A66103, appliance 2",
            "uri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.os_deployment_plans.add.assert_called_once_with({
            "name": 'Test Deployment Server',
            "description": "OS Deployment Server",
            "mgmtNetworkUri": "/rest/fc-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535",
            "applianceUri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_CREATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_replace_net_names_by_uris_should_search_fcoe(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}

        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.fcoe_networks.get_by.return_value = [
            {"name": "Deployment", "uri": "/rest/fcoe-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"}]
        self.mock_ov_client.os_deployment_servers.get_appliance_by_name.return_value = {
            "name": "0000A66103, appliance 2",
            "uri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.os_deployment_plans.add.assert_called_once_with({
            "name": 'Test Deployment Server',
            "description": "OS Deployment Server",
            "mgmtNetworkUri": "/rest/fcoe-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535",
            "applianceUri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_CREATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_should_fail_when_appliance_name_not_found(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}
        self.mock_ov_client.ethernet_networks.get_by.return_value = [{"uri": "/rest/ethernet-networks/123"}]
        self.mock_ov_client.os_deployment_servers.get_appliance_by_name.return_value = None

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg='Appliance "0000A66103, appliance 2" not found.'
        )

    def test_should_fail_when_network_name_not_found(self):
        self.os_deployment_plans.get_by.return_value = []
        self.os_deployment_plans.add.return_value = {"name": "name"}
        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.fcoe_networks.get_by.return_value = []
        self.mock_ov_client.os_deployment_servers.get_appliances.return_value = [
            {"name": "0000A66103, appliance 2",
             "uri": "/rest/deployment-servers/image-streamer-appliances/123"}]

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg='Network "Deployment" not found.'
        )

    def test_should_replace_names_by_uris_before_update(self):
        self.os_deployment_plans.get_by.return_value = [{"name": "name"}]
        self.os_deployment_plans.update.return_value = {"name": "name"}
        self.mock_ov_client.ethernet_networks.get_by.return_value = [
            {"name": "Deployment", "uri": "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"}]
        self.mock_ov_client.os_deployment_servers.get_appliance_by_name.return_value = {
            "name": "0000A66103, appliance 2",
            "uri": "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_CREATE_WITH_NAMES

        OsDeploymentServerModule().run()

        self.os_deployment_plans.update.assert_called_once_with({
            "name": 'Test Deployment Server',
            "description": "OS Deployment Server",
            "mgmtNetworkUri": "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535",
            "primaryActiveAppliance":
                "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_UPDATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_update_deployment_server(self):
        self.os_deployment_plans.get_by.return_value = [self.DEPLOYMENT_SERVER_CREATE['data']]
        self.os_deployment_plans.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_UPDATE

        OsDeploymentServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_UPDATED,
            ansible_facts=dict(os_deployment_server={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.os_deployment_plans.get_by.return_value = [self.DEPLOYMENT_SERVER_UPDATE['data']]

        del self.DEPLOYMENT_SERVER_UPDATE['data']['newName']

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_UPDATE

        OsDeploymentServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=OsDeploymentServerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(os_deployment_server=self.DEPLOYMENT_SERVER_UPDATE['data'])
        )

    def test_delete_deployment_server(self):
        self.os_deployment_plans.get_by.return_value = [self.DEPLOYMENT_SERVER_CREATE['data']]

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_DELETE

        OsDeploymentServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=OsDeploymentServerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_deployment_server(self):
        self.os_deployment_plans.get_by.return_value = []

        self.mock_ansible_module.params = self.DEPLOYMENT_SERVER_DELETE

        OsDeploymentServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=OsDeploymentServerModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
