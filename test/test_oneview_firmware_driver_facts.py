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
from oneview_module_loader import FirmwareDriverFactsModule

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=FIRMWARE_DRIVER_NAME
)

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

FIRMWARE_DRIVER = dict(
    category='firmware-drivers',
    name=FIRMWARE_DRIVER_NAME,
    uri='/rest/firmware-drivers/Service_0Pack_0for_0ProLiant',
)


@pytest.mark.resource(TestFirmwareDriverFactsModule='firmware_drivers')
class TestFirmwareDriverFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_firmware_drivers(self):
        firmwares = [FIRMWARE_DRIVER]
        self.resource.get_all.return_value = firmwares

        self.mock_ansible_module.params = PARAMS_GET_ALL

        FirmwareDriverFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(firmware_drivers=firmwares)
        )

    def test_should_get_by_name(self):
        firmwares = [FIRMWARE_DRIVER]
        self.resource.get_by.return_value = firmwares

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FirmwareDriverFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(firmware_drivers=firmwares)
        )


if __name__ == '__main__':
    pytest.main([__file__])
