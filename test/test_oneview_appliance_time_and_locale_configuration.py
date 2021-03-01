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
import mock

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ApplianceTimeAndLocaleConfigurationModule

DEFAULT_CONFIGURATION_TEMPLATE = dict(
    locale='en_US.UTF-8',
    type='TimeAndLocale',
    timezone='UTC'
)

CHANGED_CONFIGURATION_TEMPLATE = dict(
    locale='ja_JP.UTF-8',
    type='TimeAndLocale',
    timezone='UTC'
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=CHANGED_CONFIGURATION_TEMPLATE
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=DEFAULT_CONFIGURATION_TEMPLATE
)


@pytest.mark.resource(TestApplianceTimeAndLocaleConfigurationModule='appliance_time_and_locale_configuration')
class TestApplianceTimeAndLocaleConfigurationModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_not_update_when_data_is_equal(self):
        self.resource.get_all.return_value = self.resource
        self.resource.data = DEFAULT_CONFIGURATION_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceTimeAndLocaleConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceTimeAndLocaleConfigurationModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_time_and_locale_configuration=DEFAULT_CONFIGURATION_TEMPLATE)
        )

    def test_should_update_when_data_is_modified(self):
        self.resource.get_all.return_value = self.resource
        self.resource.data = DEFAULT_CONFIGURATION_TEMPLATE
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES
        obj = mock.Mock()
        obj.data = {"locale"="ja_JP.UTF-8", "type"="TimeAndLocale", "timezone"="UTC"}
        self.mock_ov_client.appliance_time_and_locale_configuration.create.return_value = obj

        ApplianceTimeAndLocaleConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceTimeAndLocaleConfigurationModule.MSG_CREATED,
            ansible_facts=dict(appliance_time_and_locale_configuration=CHANGED_CONFIGURATION_TEMPLATE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
