#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import LogicalSwitchGroupFactsModule

ERROR_MSG = 'Fake message error'
LOGICAL_SWITCH_GROUP_NAME = 'LogicalSwitchGroupDemo'

PARAMS_GET_ALL = dict(
    config='config.json',
    state='present'
)
PARAMS_GET_BY_NAME = dict(
    config='config.json',
    state='present',
    name=LOGICAL_SWITCH_GROUP_NAME
)


@pytest.mark.resource(TestLogicalSwitchGroupFactsModule='logical_switch_groups')
class TestLogicalSwitchGroupFactsModule(OneViewBaseFactsTest):
    def test_should_get_logical_switch_group_by_name(self):
        self.resource.get_by.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )

    def test_should_get_all_logical_switch_groups(self):
        self.resource.get_all.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )


if __name__ == '__main__':
    pytest.main([__file__])
