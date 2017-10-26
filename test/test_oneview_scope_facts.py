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

import copy

from ansible.compat.tests import unittest
from oneview_module_loader import ScopeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Scope 2"
)

SCOPE_1 = dict(name="Scope 1", uri='/rest/scopes/a0336853-58d7-e021-b740-511cf971e21f0')
SCOPE_2 = dict(name="Scope 2", uri='/rest/scopes/b3213123-44sd-y334-d111-asd34sdf34df3')

ALL_SCOPES = [SCOPE_1, SCOPE_2]


class ScopeFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ScopeFactsModule)
        self.resource = self.mock_ov_client.scopes

        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_scopes(self):
        self.resource.get_all.return_value = ALL_SCOPES
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        ScopeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=ALL_SCOPES)
        )

    def test_should_get_scope_by_name(self):
        self.resource.get_by_name.return_value = SCOPE_2
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        ScopeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=[SCOPE_2])
        )


if __name__ == '__main__':
    unittest.main()
