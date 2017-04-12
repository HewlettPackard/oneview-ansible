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
from oneview_module_loader import LogicalSwitchGroupFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class LogicalSwitchGroupFactsSpec(unittest.TestCase,
                                  FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchGroupFactsModule)
        self.logical_switch_groups = self.mock_ov_client.logical_switch_groups
        FactsParamsTestCase.configure_client_mock(self, self.logical_switch_groups)

        self.PARAMS_GET_ALL = self.EXAMPLES[0]['oneview_logical_switch_group_facts']
        self.PARAMS_GET_BY_NAME = self.EXAMPLES[4]['oneview_logical_switch_group_facts']

    def test_should_get_logical_switch_group_by_name(self):
        self.logical_switch_groups.get_by.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )

    def test_should_get_all_logical_switch_groups(self):
        self.logical_switch_groups.get_all.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )


if __name__ == '__main__':
    unittest.main()
