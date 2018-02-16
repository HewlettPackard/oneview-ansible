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
from oneview_switch_facts import SwitchFactsModule


ERROR_MSG = 'Fake message error'

SWITCH_NAME = '172.18.20.1'

SWITCH_URI = '/rest/switches/028e81d0-831b-4211-931c-8ac63d687ebd'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=['environmentalConfiguration']
)

SWITCH = dict(name=SWITCH_NAME, uri=SWITCH_URI)

ALL_SWITCHES = [SWITCH, dict(name='172.18.20.2')]


@pytest.mark.resource(TestSwitchFactsModule='switches')
class TestSwitchFactsModule(OneViewBaseFactsTest):
    def test_should_get_all(self):
        self.resource.get_all.return_value = ALL_SWITCHES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=ALL_SWITCHES)
        )

    def test_should_get_by_name(self):
        switches = [SWITCH]
        self.resource.get_by.return_value = switches
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SwitchFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', SWITCH_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches)
        )

    def test_should_get_by_name_with_options(self):
        switches = [SWITCH]
        environmental_configuration = dict(calibratedMaxPower=0, capHistorySupported=False)

        self.resource.get_by.return_value = switches
        self.resource.get_environmental_configuration.return_value = environmental_configuration
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        SwitchFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', SWITCH_NAME)
        self.resource.get_environmental_configuration.assert_called_once_with(id_or_uri=SWITCH_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches, switch_environmental_configuration=environmental_configuration)
        )


if __name__ == '__main__':
    pytest.main([__file__])
