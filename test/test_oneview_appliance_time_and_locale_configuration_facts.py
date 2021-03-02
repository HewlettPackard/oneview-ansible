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
from oneview_module_loader import ApplianceTimeAndLocaleConfigurationFactsModule

PARAMS_GET = dict(
    config='config.json',
    name=None
)

PRESENT_CONFIGURATION = [{
    "locale": "en_US.UTF-8",
    "localeDisplayName": "English (United States)"
}]


@pytest.mark.resource(TestApplianceTimeAndLocaleConfigurationFactsModule='appliance_time_and_locale_configuration')
class TestApplianceTimeAndLocaleConfigurationFactsModule(OneViewBaseTest):
    def test_should_get_appliance_time_and_locale_configuration(self):
        self.resource.get_all.return_value = PRESENT_CONFIGURATION
        self.mock_ansible_module.params = PARAMS_GET

        ApplianceTimeAndLocaleConfigurationFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_time_and_locale_configuration=PRESENT_CONFIGURATION)
        )


if __name__ == '__main__':
    pytest.main([__file__])
