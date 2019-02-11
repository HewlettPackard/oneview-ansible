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

import mock
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ApplianceDeviceSnmpV3TrapDestinationsModule, OneViewModuleException

ERROR_MSG = 'Fake message error'

DEFAULT_PARAMS = dict(
    type='Destination',
    destinationAddress='10.0.0.1',
    port=162,
    userId='8e57d829-2f17-4167-ae23-8fb46607c76c'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=DEFAULT_PARAMS
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(destinationAddress=DEFAULT_PARAMS['destinationAddress'],
              userId='3953867c-5283-4059-a9ae-33487f901e85')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(destinationAddress=DEFAULT_PARAMS['destinationAddress'])
)


@pytest.mark.resource(TestApplianceDeviceSnmpV3TrapDestinationsModule='appliance_device_snmp_v3_trap_destinations')
class TestApplianceDeviceSnmpV3TrapDestinationsModule(OneViewBaseTest):
    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp):
        self.mock_ov_client.api_version = 600

    def test_should_create_new_snmp_v3_trap_destination(self):
        self.resource.create.return_value = DEFAULT_PARAMS

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_CREATED,
            ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=DEFAULT_PARAMS)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_PARAMS]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=DEFAULT_PARAMS)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_PARAMS.copy()

        self.resource.get_by.return_value = [DEFAULT_PARAMS]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_UPDATED,
            ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=data_merged)
        )

    def test_should_raise_exception_when_snmpv3_user_not_found(self):
        self.resource.get_by.side_effect = OneViewModuleException(ERROR_MSG)
        self.mock_ov_client.appliance_device_snmp_v3_users.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES.copy()
        self.mock_ansible_module.params['data']['userUri'] = 'Name of a SNMPv3 User'

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_USER_NOT_FOUND)

    def test_should_remove_snmp_v3_trap_destination(self):
        self.resource.get_by.return_value = [DEFAULT_PARAMS]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_DELETED
        )

    def test_should_do_nothing_when_snmp_v3_trap_destination_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV3TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV3TrapDestinationsModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
