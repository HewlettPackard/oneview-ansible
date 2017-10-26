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

from ansible.compat.tests import unittest, mock
from hpe_test_utils import OneViewBaseTestCase
from oneview_module_loader import FabricModule

FAKE_MSG_ERROR = 'Fake message error'
NO_CHANGE_MSG = 'No change found'


class FabricModuleSpec(unittest.TestCase,
                       OneViewBaseTestCase):
    PRESENT_FABRIC_VLAN_RANGE = dict(
        name="DefaultFabric",
        uri="/rest/fabrics/421fe408-589a-4a7e-91c5-a998e1cf3ec1",
        reservedVlanRange=dict(
            start=300,
            length=62
        ))

    FABRIC_PARAMS = dict(
        config="{{ config }}",
        state="reserved_vlan_range_updated",
        data=dict(
            name="DefaultFabric",
            reservedVlanRangeParameters=dict(
                start=300,
                length=67
            )
        )
    )

    FABRIC_PARAMS_DATA_IS_EQUALS = dict(
        config="{{ config }}",
        state="reserved_vlan_range_updated",
        data=dict(
            name="DefaultFabric",
            reservedVlanRangeParameters=dict(
                start=300,
                length=62
            )
        )
    )

    EXPECTED_FABRIC_VLAN_RANGE = dict(start=300, length=67)

    def setUp(self):
        self.configure_mocks(self, FabricModule)
        self.resource = self.mock_ov_client.fabrics

    def test_should_update_vlan_range(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [self.PRESENT_FABRIC_VLAN_RANGE]
        self.resource.update_reserved_vlan_range.return_value = self.PRESENT_FABRIC_VLAN_RANGE

        # Mock Ansible params
        self.mock_ansible_module.params = self.FABRIC_PARAMS

        FabricModule().run()

        self.resource.update_reserved_vlan_range.assert_called_once_with(
            self.PRESENT_FABRIC_VLAN_RANGE["uri"],
            self.EXPECTED_FABRIC_VLAN_RANGE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fabric=self.PRESENT_FABRIC_VLAN_RANGE)
        )

    def test_should_fail_update_vlan_range_when_fabric_not_found(self):
        self.resource.get_by.return_value = []
        self.resource.update_reserved_vlan_range.return_value = self.PRESENT_FABRIC_VLAN_RANGE

        self.mock_ansible_module.params = self.FABRIC_PARAMS

        FabricModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=FabricModule.MSG_NOT_FOUND)

    def test_should_not_update_when_data_is_equals(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [self.PRESENT_FABRIC_VLAN_RANGE]
        self.resource.update_reserved_vlan_range.return_value = self.PRESENT_FABRIC_VLAN_RANGE

        # Mock Ansible params
        self.mock_ansible_module.params = self.FABRIC_PARAMS_DATA_IS_EQUALS

        FabricModule().run()

        self.resource.update_reserved_vlan_range.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NO_CHANGE_MSG,
            ansible_facts=dict(fabric=self.PRESENT_FABRIC_VLAN_RANGE)
        )
