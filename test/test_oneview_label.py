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
import mock

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import LabelModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_LABEL_TEMPLATE = dict(
    category='enclosures',
    labels=[{'name': 'enclosureDemo', 'uri': '/rest/labels/21'},
            {'name': 'labelSample', 'uri': '/rest/labels/22'}],
    resourceUri='/rest/enclosures/0000000000A66102',
    uri='/rest/labels/resources/rest/enclosures/0000000000A66102'
)

G_DEFAULT_LABEL_TEMPLATE = dict(
    category='enclosures',
    labels=[],
    resourceUri='/rest/enclosures/0000000000A66102',
    uri='/rest/labels/resources/rest/enclosures/0000000000A66102'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(resourceUri=DEFAULT_LABEL_TEMPLATE['resourceUri'],
              labels=[{'name': 'enclosureDemo'}, {'name': 'labelSample'}])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(resourceUri=DEFAULT_LABEL_TEMPLATE['resourceUri'],
              labels=[{'name': 'enclosureDemo', 'uri': '/rest/labels/21'},
                      {'name': 'labelSample', 'uri': '/rest/labels/22'}])
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(resourceUri=DEFAULT_LABEL_TEMPLATE['resourceUri'])
)


@pytest.mark.resource(TestLabelModule='labels')
class TestLabelModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_label(self):
        self.mock_ov_client.labels.get_by_resource().data = G_DEFAULT_LABEL_TEMPLATE
        self.resource.data = DEFAULT_LABEL_TEMPLATE
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LabelModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LabelModule.MSG_CREATED,
            ansible_facts=dict(Labels=DEFAULT_LABEL_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_LABEL_TEMPLATE.copy()
        data_merged['labels'][0]['name'] = 'NewName'
        self.mock_ov_client.labels.get_by_resource().data = data_merged
        self.resource.data = data_merged
        self.resource.update.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        LabelModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LabelModule.MSG_UPDATED,
            ansible_facts=dict(Labels=data_merged)
        )

    def test_deletes_when_state_is_absent(self):
        self.mock_ov_client.labels.get_by_resource().data = DEFAULT_LABEL_TEMPLATE
        self.resource.data = DEFAULT_LABEL_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        LabelModule().run()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LabelModule.MSG_DELETED
        )


if __name__ == '__main__':
    pytest.main([__file__])
