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

from oneview_module_loader import ApplianceTimeAndLocaleConfigurationFactsModule
from hpe_test_utils import OneViewBaseTestCase

PARAMS_GET = dict(
    config='config.json',
    name=None
)

PRESENT_CONFIGURATION = [{
    "locale": "en_US.UTF-8",
    "localeDisplayName": "English (United States)"
}]


class ApplianceTimeAndLocaleConfigurationFactsSpec(unittest.TestCase,
                                                   OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, ApplianceTimeAndLocaleConfigurationFactsModule)
        self.appliance_time_and_locale_configuration = self.mock_ov_client.appliance_time_and_locale_configuration

    def test_should_get_appliance_time_and_locale_configuration(self):
        self.appliance_time_and_locale_configuration.get.return_value = PRESENT_CONFIGURATION
        self.mock_ansible_module.params = PARAMS_GET

        ApplianceTimeAndLocaleConfigurationFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_time_and_locale_configuration=PRESENT_CONFIGURATION)
        )


if __name__ == '__main__':
    unittest.main()
