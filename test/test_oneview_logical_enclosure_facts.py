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
from oneview_module_loader import LogicalEnclosureFactsModule

ERROR_MSG = 'Fake message error'

LOGICAL_ENCLOSURE = {"uri": "/rest/logical-enclosures/a0a5d4a1-c4a7-4c9b-b05d-feb0a9d8190d",
                     "name": "Logical Enclosure Name"}

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Enclosures",
    options=None
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Logical Enclosures",
    options=['script']
)


@pytest.mark.resource(TestLogicalEnclosureFactsModule='logical_enclosures')
class TestLogicalEnclosureFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_logical_enclosure(self):
        self.resource.get_all.return_value = [LOGICAL_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=([LOGICAL_ENCLOSURE]))
        )

    def test_should_get_logical_enclosure_by_name(self):
        self.resource.get_by.return_value = [LOGICAL_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=[LOGICAL_ENCLOSURE])
        )

    def test_should_get_logical_enclosure_by_name_with_options(self):
        self.resource.get_by.return_value = [LOGICAL_ENCLOSURE]
        self.resource.get_script.return_value = "# script code"

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=[LOGICAL_ENCLOSURE],
                               logical_enclosure_script="# script code")
        )


if __name__ == '__main__':
    pytest.main([__file__])
