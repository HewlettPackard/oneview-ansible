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
from oneview_module_loader import FirmwareDriverModule
from ansible.module_utils.oneview import OneViewClient
from hpe_test_utils import OneViewBaseTestCase

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

FIRMWARE_DRIVER_TEMPLATE = dict(
    customBaselineName="Custom SPP Name",
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


class FirmwareDriverModuleSpec(unittest.TestCase, OneViewBaseTestCase):

    def setUp(self):
        self.configure_mocks(self, FirmwareDriverModule)
        self.resource = self.mock_ov_client.firmware_drivers

    def test_should_create_new_firmware_driver(self):
        my_arr = [[],
                  [dict(uri='/rest/fake1')],
                  [dict(uri='/rest/fake2')],
                  [dict(uri='/rest/fake3')],
                  ]

        self.resource.get_by.side_effect = my_arr

        self.resource.create.return_value = FIRMWARE_DRIVER_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareDriverModule.MSG_CREATED,
            ansible_facts=dict(firmware_driver=FIRMWARE_DRIVER_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [FIRMWARE_DRIVER_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareDriverModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(firmware_driver=FIRMWARE_DRIVER_TEMPLATE)
        )

    def test_should_remove_firmware_driver(self):
        firmwares = [FIRMWARE_DRIVER]
        self.resource.get_by.return_value = firmwares
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareDriverModule.MSG_DELETED
        )

    def test_should_do_nothing_when_firmware_driver_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareDriverModule.MSG_ALREADY_ABSENT
        )

    def test_shoul_fail_when_missing_name_(self):
        fake_data = FIRMWARE_DRIVER_TEMPLATE.copy()
        fake_data.pop('customBaselineName')
        params_missing_name = PARAMS_FOR_PRESENT.copy()
        params_missing_name['data'] = fake_data
        msg = 'A "name" parameter or a "customBaselineName" field inside the "data" parameter'
        msg += 'is required for this operation.'
        self.mock_ansible_module.params = params_missing_name

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)

    def test_should_fail_if_SPP_does_not_exist(self):
        msg = 'Baseline SPP named "SPP1" '
        msg += 'not found in OneView Appliance.'

        self.resource.get_by.side_effect = [[], []]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)

    def test_should_fail_if_hotfix_does_not_exist(self):
        msg = 'Hotfix named "hotfix1" '
        msg += 'not found in OneView Appliance.'

        self.resource.get_by.side_effect = [[], [dict(uri='/rest/fake1')], []]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)


if __name__ == '__main__':
    unittest.main()
