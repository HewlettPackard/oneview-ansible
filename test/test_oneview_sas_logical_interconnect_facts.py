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

import unittest

from oneview_module_loader import SasLogicalInterconnectFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Sas Logical Interconnect Name",
)

PARAMS_GET_BY_NAME_WITH_FIRMWARE = dict(
    config='config.json',
    name="Sas Logical Interconnect Name",
    options=['firmware']
)

SAS_LOGICAL_INTERCONNECT = dict(
    name="Sas Logical Interconnect Name",
    uri="/rest/sas-logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0"
)

ALL_INTERCONNECTS = [SAS_LOGICAL_INTERCONNECT]


class SasLogicalInterconnectFactsSpec(unittest.TestCase,
                                      FactsParamsTestCase):

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectFactsModule)
        self.resource = self.mock_ov_client.sas_logical_interconnects
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_sas_logical_interconnects(self):
        self.resource.get_all.return_value = ALL_INTERCONNECTS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=ALL_INTERCONNECTS)
        )

    def test_should_get_a_sas_logical_interconnects_by_name(self):
        self.resource.get_by.return_value = ALL_INTERCONNECTS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=[SAS_LOGICAL_INTERCONNECT])
        )

    def test_should_get_a_sas_logical_interconnects_by_name_with_firmware(self):
        self.resource.get_by.return_value = ALL_INTERCONNECTS
        self.resource.get_firmware.return_value = {"firmware": "data"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_FIRMWARE

        SasLogicalInterconnectFactsModule().run()

        self.resource.get_firmware.assert_called_once_with(SAS_LOGICAL_INTERCONNECT['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                sas_logical_interconnects=[SAS_LOGICAL_INTERCONNECT],
                sas_logical_interconnect_firmware={"firmware": "data"}
            )
        )


if __name__ == '__main__':
    unittest.main()
