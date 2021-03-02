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

import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ApplianceConfigurationTimeconfigFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PRESENT_TIMECONFIG = [{
    "locale": "en_US.UTF-8",
    "displayName": "English (United States)"
}]


@pytest.mark.resource(TestApplianceConfigurationTimeconfigFactsModule='appliance_configuration_timeconfig')
class TestApplianceConfigurationTimeconfigFactsModule(OneViewBaseTest):
    def test_should_get_all_timeconfiguration(self):
        self.resource.get_all.return_value = PRESENT_TIMECONFIG
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ApplianceConfigurationTimeconfigFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_configuration_timeconfig=PRESENT_TIMECONFIG)
        )


if __name__ == '__main__':
    pytest.main([__file__])
