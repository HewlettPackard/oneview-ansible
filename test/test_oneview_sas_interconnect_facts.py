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
from oneview_module_loader import SasInterconnectFactsModule

SAS_INTERCONNECT_1_NAME = '0000A66103, interconnect 1'

SAS_INTERCONNECT_1 = dict(
    name=SAS_INTERCONNECT_1_NAME,
    uri='/rest/sas-interconnects/2M220104SL'
)

SAS_INTERCONNECT_4 = dict(
    name='0000A66102, interconnect 4',
    uri='/rest/sas-interconnects/2M220103SL'
)

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=SAS_INTERCONNECT_1_NAME
)


@pytest.mark.resource(TestSasInterconnectFactsModule='sas_interconnects')
class TestSasInterconnectFactsModule(OneViewBaseFactsTest):
    def test_get_all_sas_interconnects(self):
        all_sas_interconnects = [SAS_INTERCONNECT_1, SAS_INTERCONNECT_4]

        self.resource.get_all.return_value = all_sas_interconnects

        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnects=all_sas_interconnects)
        )

    def test_get_sas_interconnects_by_name(self):
        self.resource.get_by.return_value = [SAS_INTERCONNECT_1]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasInterconnectFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_1_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnects=[SAS_INTERCONNECT_1])
        )


if __name__ == '__main__':
    pytest.main([__file__])
