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

from oneview_module_loader import ServerHardwareTypeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="MyServerHardwareType"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)


class ServerHardwareTypeFactsSpec(unittest.TestCase,
                                  FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ServerHardwareTypeFactsModule)
        self.server_hardware_types = self.mock_ov_client.server_hardware_types
        FactsParamsTestCase.configure_client_mock(self, self.server_hardware_types)

    def test_should_get_all(self):
        self.server_hardware_types.get_all.return_value = {"name": "Server Hardware Type Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ServerHardwareTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardware_types=({"name": "Server Hardware Type Name"}))
        )

    def test_should_get_server_hardware_type_by_name(self):
        self.server_hardware_types.get_by.return_value = [{"name": "Server Hardware Type Name"}]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ServerHardwareTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardware_types=([{"name": "Server Hardware Type Name"}]))
        )


if __name__ == '__main__':
    unittest.main()
