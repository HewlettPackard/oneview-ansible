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
from oneview_module_loader import DatacenterFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="MyDatacenter"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_CONNECTED = dict(
    config='config.json',
    name="MyDatacenter",
    options=['visualContent']
)


@pytest.mark.resource(TestDatacenterFactsModule='datacenters')
class TestDatacenterFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_datacenters(self):
        self.resource.get_all.return_value = {"name": "Data Center Name"}

        self.mock_ansible_module.params = PARAMS_GET_ALL

        DatacenterFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(datacenters=({"name": "Data Center Name"}))
        )

    def test_should_get_datacenter_by_name(self):
        self.resource.get_by.return_value = [{"name": "Data Center Name"}]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DatacenterFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(datacenters=([{"name": "Data Center Name"}]))
        )

    def test_should_get_datacenter_visual_content(self):
        self.resource.get_by.return_value = [{"name": "Data Center Name", "uri": "/rest/datacenter/id"}]

        self.resource.get_visual_content.return_value = {
            "name": "Visual Content"}

        self.mock_ansible_module.params = PARAMS_GET_CONNECTED

        DatacenterFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'datacenter_visual_content': {'name': 'Visual Content'},
                           'datacenters': [{'name': 'Data Center Name', 'uri': '/rest/datacenter/id'}]}
        )

    def test_should_get_none_datacenter_visual_content(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_GET_CONNECTED

        DatacenterFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'datacenter_visual_content': None,
                           'datacenters': []}
        )


if __name__ == '__main__':
    pytest.main([__file__])
