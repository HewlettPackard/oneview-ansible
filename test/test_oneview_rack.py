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
import mock
from copy import deepcopy
from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import RackModule


FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_RACK_TEMPLATE = dict(
    name='New Rack 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='Rename Rack')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)


@pytest.mark.resource(TestRackModule='racks')
class TestRackModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case.
    """

    def test_should_create_new_rack(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = DEFAULT_RACK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_ADDED,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RackModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    @mock.patch('module_utils.oneview.dict_merge')
    @mock.patch('oneview_rack.__mergeRackMounts')
    @mock.patch('module_utils.oneview.compare')
    def test_update_when_data_has_modified_attributes(self, mock_resource_compare, mock_merge_rackMounts, mock_dict_merge):
        data_merged = deepcopy(DEFAULT_RACK_TEMPLATE)

        data_merged['name'] = 'Rename Rack'
        self.resource.data = deepcopy(DEFAULT_RACK_TEMPLATE)

        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        mock_merge_rackMounts.return_value = data_merged
        mock_dict_merge.return_value = data_merged
        mock_resource_compare.return_value = False
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = DEFAULT_RACK_TEMPLATE

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_UPDATED,
            ansible_facts=dict(rack=data_merged)
        )

    def test_should_remove_rack(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_DELETED,
            ansible_facts=dict(rack=None)
        )

    def test_should_do_nothing_when_rack_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RackModule.MSG_ALREADY_ABSENT,
            ansible_facts=dict(rack=None)
        )


if __name__ == '__main__':
    pytest.main([__file__])
