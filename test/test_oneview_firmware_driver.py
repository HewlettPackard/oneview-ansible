#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import FirmwareDriverModule

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

FIRMWARE_DRIVER_TEMPLATE = dict(
    customBaselineName=FIRMWARE_DRIVER_NAME,
    baselineName="SPP1",
    hotfixNames=["hotfix1", "hotfix2"]
)

SPP_HOTFIX_DATA = dict(
    name="hotfix1",
    uri='/rest/fake'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=FIRMWARE_DRIVER_TEMPLATE
)

PARAMS_ABSENT = dict(
    config='config.json',
    state='absent',
    name=FIRMWARE_DRIVER_NAME
)

FIRMWARE_DRIVER = dict(name=FIRMWARE_DRIVER_NAME)


@pytest.mark.resource(TestFirmwareDriverModule='firmware_drivers')
class TestFirmwareDriverModule(OneViewBaseTest):
    def test_should_create_new_firmware_driver(self):
        self.resource.data = {'uri':'/rest/fake'}
        self.resource.get_by_name.side_effect = [None, self.resource, self.resource]

#        self.resource.create.return_value = self.resource
        self.resource.create.return_value = PARAMS_FOR_PRESENT

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareDriverModule.MSG_CREATED,
            ansible_facts=dict(firmware_driver=FIRMWARE_DRIVER_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = FIRMWARE_DRIVER_TEMPLATE
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareDriverModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(firmware_driver=FIRMWARE_DRIVER_TEMPLATE)
        )

    def test_should_remove_firmware_driver(self):
        self.resource.data = FIRMWARE_DRIVER
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareDriverModule.MSG_DELETED
        )

    def test_should_do_nothing_when_firmware_driver_not_exist(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareDriverModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_missing_name_(self):
        fake_data = FIRMWARE_DRIVER_TEMPLATE.copy()
        fake_data.pop('customBaselineName')
        params_missing_name = PARAMS_FOR_PRESENT.copy()
        params_missing_name['data'] = fake_data
        msg = "A 'name' parameter or a 'customBaselineName' field inside the 'data' parameter "
        msg += "is required for this operation."
        self.mock_ansible_module.params = params_missing_name

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)

    def test_should_fail_if_spp_does_not_exist(self):
        msg = "Baseline SPP named 'SPP1' not found in OneView Appliance."
        self.resource.get_by_name.side_effect = [None, None, None]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)

    def test_should_fail_if_hotfix_does_not_exist(self):
        msg = "Hotfix named 'hotfix1' not found in OneView Appliance."
        self.resource.data = {'uri':'/rest/fake'}
        self.resource.get_by_name.side_effect = [None, self.resource, None]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)


if __name__ == '__main__':
    pytest.main([__file__])
