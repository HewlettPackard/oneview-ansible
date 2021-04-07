#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import LabelFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    resourceUri=None,
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Label",
    resourceUri=None
)

PARAMS_GET_BY_RESOURCE = dict(
    config='config.json',
    resourceUri="/rest/enclosure/1",
    name=None
)

PRESENT_LABELS = [{
    "name": "Test Label",
    "uri": "/rest/labels/2",
    "resourceUri": ""
}]

PRESENT_RESOURCE_LABELS = [{
    "name": "Test Label",
    "uri": "/rest/labels/2",
    "resourceUri": "/rest/enclosure/1"
}]


@pytest.mark.resource(TestLabelFactsModule='labels')
class TestLabelFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_labels(self):
        self.resource.get_all.return_value = PRESENT_LABELS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        LabelFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(labels=PRESENT_LABELS)
        )

    def test_should_get_label_by_name(self):
        self.resource.get_by.return_value = PRESENT_LABELS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LabelFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(labels=PRESENT_LABELS)
        )

    def test_should_get_resource_lables(self):
        self.resource.get_by_resource().data = PRESENT_RESOURCE_LABELS
        self.mock_ansible_module.params = PARAMS_GET_BY_RESOURCE

        LabelFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(labels=PRESENT_RESOURCE_LABELS)
        )


if __name__ == '__main__':
    pytest.main([__file__])
