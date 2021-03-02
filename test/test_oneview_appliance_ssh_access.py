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
from oneview_module_loader import ApplianceSshAccessModule

DEFAULT_CONFIGURATION_TEMPLATE = dict(
    allowSshAccess='True'
)

CHANGED_CONFIGURATION_TEMPLATE = dict(
    allowSshAccess='False'
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=CHANGED_CONFIGURATION_TEMPLATE
)


@pytest.mark.resource(TestApplianceSshAccessModule='appliance_ssh_access')
class TestApplianceSshAccessModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_update_when_data_has_modified_attributes(self):
        self.resource.get_all.return_value = self.resource
        self.resource.data = DEFAULT_CONFIGURATION_TEMPLATE
        obj = mock.Mock()
        obj.data = CHANGED_CONFIGURATION_TEMPLATE
        self.mock_ov_client.appliance_ssh_access.update.return_value = obj
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ApplianceSshAccessModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceSshAccessModule.MSG_UPDATED,
            ansible_facts=dict(appliance_ssh_access=CHANGED_CONFIGURATION_TEMPLATE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
