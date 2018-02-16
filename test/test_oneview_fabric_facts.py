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
from oneview_module_loader import FabricFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="DefaultFabric"
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="DefaultFabric",
    options=['reservedVlanRange']
)

PRESENT_FABRICS = [{
    "name": "DefaultFabric",
    "uri": "/rest/fabrics/421fe408-589a-4a7e-91c5-a998e1cf3ec1"
}]

PRESENT_FABRIC_VLAN_RANGE = [{
    "name": "DefaultFabric",
    "uri": "/rest/fabrics/421fe408-589a-4a7e-91c5-a998e1cf3ec1",
    "reservedVlanRangeParameters": {
        "start": 300,
        "length": 62
    }
}]

FABRIC_RESERVED_VLAN_RANGE = 'a7896ce7-c11d-4658-829d-142bc66a85e4'

DEFAULT_FABRIC_VLAN_RANGE = dict(
    name='New FC Network 2',
    reservedVlanRangeParameters=dict(start=300, length=62)
)


@pytest.mark.resource(TestFabricFactsModule='fabrics')
class TestFabricFactsModule(OneViewBaseFactsTest):
    def test_should_get_all(self):
        self.resource.get_all.return_value = PRESENT_FABRICS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FabricFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fabrics=(PRESENT_FABRICS))
        )

    def test_should_get_by_name(self):
        self.resource.get_by.return_value = PRESENT_FABRICS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FabricFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fabrics=(PRESENT_FABRICS))
        )

    def test_should_get_fabric_by_name_with_options(self):
        self.resource.get_by.return_value = PRESENT_FABRICS
        self.resource.get_reserved_vlan_range.return_value = FABRIC_RESERVED_VLAN_RANGE
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        FabricFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fabrics=PRESENT_FABRICS,
                               fabric_reserved_vlan_range=FABRIC_RESERVED_VLAN_RANGE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
