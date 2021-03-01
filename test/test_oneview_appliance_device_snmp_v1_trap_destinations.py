#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import ApplianceDeviceSnmpV1TrapDestinationsModule

ERROR_MSG = 'Fake message error'

DEFAULT_SNMPv1_TRAP_TEMPLATE = dict(
    communityString='public',
    destination='10.0.0.1',
    uri='/rest/appliance/trap-destinations/1',
    port=162
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    name=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'],
    data=dict(destination=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination']))

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    name=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'],
    data=dict(destination=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'],
              communityString='private')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    name=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination']
)


@pytest.mark.resource(TestApplianceDeviceSnmpV1TrapDestinationsModule='appliance_device_snmp_v1_trap_destinations')
class TestApplianceDeviceSnmpV1TrapDestinationsModule(OneViewBaseTest):
    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp):
        self.mock_ov_client.api_version = 600

    def test_should_create_new_snmp_v1_trap_destination(self):
        self.resource.get_by_name.return_value = None
        self.resource.get_by_uri.return_value = None
        self.resource.data = DEFAULT_SNMPv1_TRAP_TEMPLATE
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_CREATED,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=DEFAULT_SNMPv1_TRAP_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_SNMPv1_TRAP_TEMPLATE
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=DEFAULT_SNMPv1_TRAP_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        self.resource.data = DEFAULT_SNMPv1_TRAP_TEMPLATE
        data_merged = DEFAULT_SNMPv1_TRAP_TEMPLATE.copy()

        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_UPDATED,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=data_merged)
        )

    def test_should_remove_snmp_v1_trap_destination(self):
        self.resource.data = DEFAULT_SNMPv1_TRAP_TEMPLATE
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_DELETED
        )

    def test_should_do_nothing_when_snmp_v1_trap_destination_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
