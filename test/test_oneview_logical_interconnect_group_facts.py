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

from hpe_test_utils import FactsParamsTestCase
from oneview_module_loader import LogicalInterconnectGroupFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Interconnect Group"
)

PRESENT_LIGS = [{
    "name": "Test Logical Interconnect Group",
    "uri": "/rest/logical-interconnect-groups/ebb4ada8-08df-400e-8fac-9ff987ac5140"
}]


class LogicalInterconnectGroupFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectGroupFactsModule)
        self.logical_interconnect_groups = self.mock_ov_client.logical_interconnect_groups
        FactsParamsTestCase.configure_client_mock(self, self.logical_interconnect_groups)

    def test_should_get_all_ligs(self):
        self.logical_interconnect_groups.get_all.return_value = PRESENT_LIGS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnect_groups=(PRESENT_LIGS))
        )

    def test_should_get_lig_by_name(self):
        self.logical_interconnect_groups.get_by.return_value = PRESENT_LIGS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnect_groups=(PRESENT_LIGS))
        )


if __name__ == '__main__':
    unittest.main()
