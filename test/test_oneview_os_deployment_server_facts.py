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

import pytest

from hpe_test_utils import OneViewBaseFactsTest
from oneview_module_loader import OsDeploymentServerFactsModule

SERVERS = [
    {
        "name": 'Test Deployment Server',
        "description": "OS Deployment Server"
    }
]


@pytest.mark.resource(TestOsDeploymentServerFactsModule='os_deployment_servers')
class TestOsDeploymentServerFactsModule(OneViewBaseFactsTest):
    # Load scenarios from module examples
    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp, testing_module):
        self.PARAMS_GET_ALL = self.EXAMPLES[0]['oneview_os_deployment_server_facts']
        self.PARAMS_GET_BY_NAME = self.EXAMPLES[2]['oneview_os_deployment_server_facts']
        self.PARAMS_GET_BY_NAME_WITH_OPTIONS = self.EXAMPLES[4]['oneview_os_deployment_server_facts']

    def test_should_get_all_os_deployment_server(self):
        self.resource.get_all.return_value = SERVERS

        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        OsDeploymentServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_deployment_servers=SERVERS)
        )

    def test_should_get_os_deployment_server_by_name(self):
        self.resource.get_by.return_value = SERVERS

        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        OsDeploymentServerFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', "OS Deployment Server-Name")

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_deployment_servers=SERVERS)
        )

    def test_should_get_os_deployment_servers_with_options(self):
        networks = [{"name": "net"}]
        appliances = [{"name": "appl1"}, {"name": "appl2"}]
        appliance = {"name": "appl1"}
        self.resource.get_by.return_value = SERVERS
        self.resource.get_networks.return_value = networks
        self.resource.get_appliances.return_value = appliances
        self.resource.get_appliance_by_name.return_value = appliance

        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME_WITH_OPTIONS

        OsDeploymentServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                os_deployment_servers=SERVERS,
                os_deployment_server_networks=networks,
                os_deployment_server_appliances=appliances,
                os_deployment_server_appliance=appliance
            )
        )


if __name__ == '__main__':
    pytest.main([__file__])
