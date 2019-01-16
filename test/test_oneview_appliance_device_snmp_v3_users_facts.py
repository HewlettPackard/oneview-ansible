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
from oneview_module_loader import ApplianceDeviceSnmpV3UsersFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json'
)

PARAMS_GET_ALL = dict(
    config='config.json'
)

PARAMS_GET_BY_ID = dict(
    config='config.json',
    id='3953867c-5283-4059-a9ae-33487f901e85'
)

PRESENT_CONFIGURATION = [{
    "authenticationPassphrase": "",
    "authenticationProtocol": "SHA512",
    "category": "SnmpV3User",
    "id": "3953867c-5283-4059-a9ae-33487f901e85",
    "privacyPassphrase": "",
    "privacyProtocol": "AES-256",
    "securityLevel": "Authentication and privacy",
    "type": "Users",
    "uri": "/rest/appliance/snmpv3-trap-forwarding/users/3953867c-5283-4059-a9ae-33487f901e85",
    "userName": "TestUser1"
}]


@pytest.mark.resource(TestApplianceDeviceSnmpV3UsersFactsModule='appliance_device_snmp_v3_users')
class TestApplianceDeviceSnmpV3UsersFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_snmp_v3_users(self):
        self.resource.get_all.return_value = PRESENT_CONFIGURATION
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ApplianceDeviceSnmpV3UsersFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_device_snmp_v3_users=(PRESENT_CONFIGURATION))
        )

    def test_should_get_by_id_snmp_v3_users(self):
        self.resource.get_by_id.return_value = PRESENT_CONFIGURATION
        self.mock_ansible_module.params = PARAMS_GET_BY_ID

        ApplianceDeviceSnmpV3UsersFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_device_snmp_v3_users=(PRESENT_CONFIGURATION))
        )


if __name__ == '__main__':
    pytest.main([__file__])
