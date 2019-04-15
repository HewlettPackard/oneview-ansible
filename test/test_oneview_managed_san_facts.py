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
from oneview_module_loader import ManagedSanFactsModule

ERROR_MSG = 'Fake message error'

MANAGED_SAN_NAME = 'SAN1_0'
MANAGED_SAN_URI = '/rest/fc-sans/managed-sans/cc64ee18-8f7d-4cdf-9bf8-a68f00e4af9c'
MANAGED_SAN_WWN = '20:00:4A:2B:21:E0:00:01'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None,
    wwn=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=MANAGED_SAN_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=MANAGED_SAN_NAME,
    options=['endpoints']
)

PARAMS_GET_ASSOCIATED_WWN = dict(
    config='config.json',
    name=MANAGED_SAN_NAME,
    options=[{'wwn': {'locate': MANAGED_SAN_WWN}}]
)

MANAGED_SAN = dict(name=MANAGED_SAN_NAME, uri=MANAGED_SAN_URI)

ALL_MANAGED_SANS = [MANAGED_SAN,
                    dict(name='SAN1_1', uri='/rest/fc-sans/managed-sans/928374892-asd-34234234-asd23')]


@pytest.mark.resource(TestManagedSanFactsModule='managed_sans')
class TestManagedSanFactsModule(OneViewBaseFactsTest):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def test_should_get_all(self):
        self.resource.get_all.return_value = ALL_MANAGED_SANS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ManagedSanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=ALL_MANAGED_SANS)
        )

    def test_should_get_by_name(self):
        self.resource.data = MANAGED_SAN
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ManagedSanFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(MANAGED_SAN_NAME)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=[MANAGED_SAN])
        )

    def test_should_get_by_name_with_options(self):
        endpoints = [dict(uri='/rest/fc-sans/endpoints/20:00:00:02:AC:00:08:E2'),
                     dict(uri='/rest/fc-sans/endpoints/20:00:00:02:AC:00:08:FF')]

        self.resource.data = MANAGED_SAN
        self.resource.get_endpoints.return_value = endpoints
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        ManagedSanFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(MANAGED_SAN_NAME)
        self.resource.get_endpoints.assert_called_once_with()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=[MANAGED_SAN], managed_san_endpoints=endpoints)
        )

    def test_should_get_managed_san_for_an_associated_wwn(self):
        self.resource.data = MANAGED_SAN
        self.resource.get_wwn.return_value = MANAGED_SAN
        self.mock_ansible_module.params = PARAMS_GET_ASSOCIATED_WWN

        ManagedSanFactsModule().run()

        self.resource.get_wwn.assert_called_once_with(MANAGED_SAN_WWN)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=[MANAGED_SAN], wwn_associated_sans=MANAGED_SAN)
        )


if __name__ == '__main__':
    pytest.main([__file__])
