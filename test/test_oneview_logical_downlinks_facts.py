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
from oneview_module_loader import LogicalDownlinksFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

LOGICAL_DOWNLINK_URI = "/rest/logical-downlinks/97cb2d39-55a0-47b0-83b2-7feaefcd720d"
LOGICAL_DOWNLINK_NAME = "LD415a472f-ed77-42cc-9a5e-b9bd5d096923 (HP VC FlexFabric-20/40 F8 Module)"

LOGICAL_DOWNLINK = dict(name=LOGICAL_DOWNLINK_NAME, uri=LOGICAL_DOWNLINK_URI)

PARAMS_FOR_GET_ALL = dict(
    config='config.json',
    name=None,
    excludeEthernet=False
)

PARAMS_FOR_GET_BY_NAME = dict(
    config='config.json',
    name=LOGICAL_DOWNLINK_NAME,
    excludeEthernet=False
)

PARAMS_FOR_GET_ALL_WITHOUT_ETHERNET = dict(
    config='config.json',
    name=None,
    excludeEthernet=True
)

PARAMS_FOR_GET_WITHOUT_ETHERNET = dict(
    config='config.json',
    name=LOGICAL_DOWNLINK_NAME,
    excludeEthernet=True
)


class LogicalDownlinksFactsSpec(unittest.TestCase,
                                FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalDownlinksFactsModule)
        self.logical_downlinks = self.mock_ov_client.logical_downlinks
        self.configure_client_mock(self.logical_downlinks)

    def test_should_get_all_logical_downlinks(self):
        logical_downlinks = [
            dict(name="test1"),
            dict(name="test2")
        ]

        self.logical_downlinks.get_all.return_value = logical_downlinks

        self.mock_ansible_module.params = PARAMS_FOR_GET_ALL

        LogicalDownlinksFactsModule().run()

        self.logical_downlinks.get_all.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_downlinks=logical_downlinks)
        )

    def test_should_get_by_name(self):
        logical_downlinks = [LOGICAL_DOWNLINK]

        self.logical_downlinks.get_by.return_value = logical_downlinks

        self.mock_ansible_module.params = PARAMS_FOR_GET_BY_NAME

        LogicalDownlinksFactsModule().run()

        self.logical_downlinks.get_by.assert_called_once_with("name", LOGICAL_DOWNLINK_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_downlinks=logical_downlinks)
        )

    def test_should_get_all_without_ethernet(self):
        logical_downlinks = [LOGICAL_DOWNLINK]

        self.logical_downlinks.get_all_without_ethernet.return_value = logical_downlinks

        self.mock_ansible_module.params = PARAMS_FOR_GET_ALL_WITHOUT_ETHERNET

        LogicalDownlinksFactsModule().run()

        self.logical_downlinks.get_all_without_ethernet.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_downlinks=logical_downlinks)
        )

    def test_should_get_without_ethernet(self):
        logical_downlinks = [LOGICAL_DOWNLINK]

        self.logical_downlinks.get_by.return_value = logical_downlinks
        self.logical_downlinks.get_without_ethernet.return_value = {'name': 'Logical Downlink Without Ethernet'}

        self.mock_ansible_module.params = PARAMS_FOR_GET_WITHOUT_ETHERNET

        LogicalDownlinksFactsModule().run()

        self.logical_downlinks.get_by.assert_called_once_with('name', LOGICAL_DOWNLINK_NAME)
        self.logical_downlinks.get_without_ethernet.assert_called_once_with(id_or_uri=LOGICAL_DOWNLINK_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_downlinks=[{'name': 'Logical Downlink Without Ethernet'}])
        )

    def test_should_not_get_without_ethernet_when_not_found(self):
        logical_downlinks = []

        self.logical_downlinks.get_by.return_value = logical_downlinks
        self.logical_downlinks.get_without_ethernet.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_GET_WITHOUT_ETHERNET

        LogicalDownlinksFactsModule().run()

        self.logical_downlinks.get_by.assert_called_once_with('name', LOGICAL_DOWNLINK_NAME)
        self.logical_downlinks.get_without_ethernet.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_downlinks=[])
        )


if __name__ == '__main__':
    unittest.main()
