#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2018) Hewlett Packard Enterprise Development LP
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
    data=dict(destination=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'])
)

PARAMS_FOR_PRESENT_WITH_URI = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_SNMPv1_TRAP_TEMPLATE['uri'])
)

PARAMS_FOR_INVALID = dict(
    config='config.json',
    state='present',
    data=dict(communityString=DEFAULT_SNMPv1_TRAP_TEMPLATE['communityString'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(destination=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'],
              communityString='private')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(destination=DEFAULT_SNMPv1_TRAP_TEMPLATE['destination'])
)

PARAMS_FOR_ABSENT_WITH_URI = dict(
    config='config.json',
    state='absent',
    data=dict(uri=DEFAULT_SNMPv1_TRAP_TEMPLATE['uri'])
)


@pytest.mark.resource(TestApplianceDeviceSnmpV1TrapDestinationsModule='appliance_device_snmp_v1_trap_destinations')
class TestApplianceDeviceSnmpV1TrapDestinationsModule(OneViewBaseTest):

    def test_should_create_new_snmp_v1_trap_destination(self):
        self.resource.get_all.return_value = []
        self.resource.create.return_value = DEFAULT_SNMPv1_TRAP_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_CREATED,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=DEFAULT_SNMPv1_TRAP_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_SNMPv1_TRAP_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=DEFAULT_SNMPv1_TRAP_TEMPLATE)
        )

    def test_should_get_the_same_resource_by_uri(self):
        self.resource.get_by.return_value = [DEFAULT_SNMPv1_TRAP_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_WITH_URI

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=(DEFAULT_SNMPv1_TRAP_TEMPLATE))
        )

    def test_should_fail_with_missing_required_attributes(self):
        self.mock_ansible_module.params = PARAMS_FOR_INVALID

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_VALUE_ERROR
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SNMPv1_TRAP_TEMPLATE.copy()
        data_merged['communityString'] = 'private'

        self.resource.get_by.return_value = [DEFAULT_SNMPv1_TRAP_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_UPDATED,
            ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=data_merged)
        )

    def test_should_remove_snmp_v1_trap_destination(self):
        self.resource.get_by.return_value = [DEFAULT_SNMPv1_TRAP_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_DELETED
        )

    def test_should_remove_snmp_v1_trap_destination_by_uri(self):
        self.resource.get_by.return_value = [DEFAULT_SNMPv1_TRAP_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT_WITH_URI

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_DELETED
        )

    def test_should_do_nothing_when_snmp_v1_trap_destination_not_exist(self):
        self.resource.get_all.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV1TrapDestinationsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV1TrapDestinationsModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
