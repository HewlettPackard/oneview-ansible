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

from ansible.compat.tests import unittest
from oneview_module_loader import SasLogicalJbodFactsModule
from hpe_test_utils import FactsParamsTestCase


class SasLogicalJbodsFactsSpec(unittest.TestCase,
                               FactsParamsTestCase):

    ERROR_MSG = 'Fake message error'

    PARAMS_GET_ALL = dict(
        config='config.json',
        name=None
    )

    PARAMS_GET_BY_NAME = dict(
        config='config.json',
        name="SAS Logical JBOD 2"
    )

    PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
        config='config.json',
        name="SAS Logical JBOD 2",
        options=['drives']
    )

    SAS_LOGICAL_JBOD_1 = dict(name="SAS Logical JBOD 1", uri='/sas-logical-jbods/a0336853-58d7-e021-b740-511cf971e21f0')
    SAS_LOGICAL_JBOD_2 = dict(name="SAS Logical JBOD 2", uri='/sas-logical-jbods/b3213123-44sd-y334-d111-asd34sdf34df3')

    ALL_SAS_LOGICAL_JBODS = [SAS_LOGICAL_JBOD_1, SAS_LOGICAL_JBOD_2]

    def setUp(self):
        self.configure_mocks(self, SasLogicalJbodFactsModule)
        self.resource = self.mock_ov_client.sas_logical_jbods
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_sas_logical_jbods(self):
        self.resource.get_all.return_value = self.ALL_SAS_LOGICAL_JBODS
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=(self.ALL_SAS_LOGICAL_JBODS))
        )

    def test_should_get_sas_logical_jbod_attachment_by_name(self):
        self.resource.get_by.return_value = [self.SAS_LOGICAL_JBOD_2]
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=([self.SAS_LOGICAL_JBOD_2]))
        )

    def test_should_get_sas_logical_jbod_with_options(self):
        self.resource.get_by.return_value = [self.SAS_LOGICAL_JBOD_2]
        self.resource.get_drives.return_value = [{"name": "Drive 1"}]
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME_WITH_OPTIONS

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=[self.SAS_LOGICAL_JBOD_2],
                               sas_logical_jbod_drives=[{"name": "Drive 1"}])
        )


if __name__ == '__main__':
    unittest.main()
