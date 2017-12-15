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
from oneview_module_loader import UplinkSetFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Uplink Set"
)

PRESENT_UPLINKS = [{
    "name": "Test Uplink Set",
    "uri": "/rest/uplink-sets/d60efc8a-15b8-470c-8470-738d16d6b319"
}]


@pytest.mark.resource(TestUplinkSetFactsModule='uplink_sets')
class TestUplinkSetFactsModule(OneViewBaseFactsTest):
    def test_should_get_all(self):
        self.resource.get_all.return_value = PRESENT_UPLINKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        UplinkSetFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(uplink_sets=PRESENT_UPLINKS)
        )

    def test_should_get_by_name(self):
        self.resource.get_by.return_value = PRESENT_UPLINKS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        UplinkSetFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(uplink_sets=PRESENT_UPLINKS)
        )


if __name__ == '__main__':
    pytest.main([__file__])
