#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

UPDATED_RACK_TEMPLATE = dict(
    name='New Rack 2',
    newName='Rename Rack',
    autoLoginRedistribution=True,
    fabricType='FabricAttach',
    rackMounts=[{'mountUri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E', 'topUSlot': 20},
                {'mountUri': '/rest/server-hardware/31393736-3831-4753-567h-30335837526F', 'topUSlot': 20}]
)

UPDATED_RACK_TEMPLATE_WITH_DIFFERENT_MOUNTURIS = dict(
    name='New Rack 2',
    newName='Rename Rack',
    autoLoginRedistribution=True,
    fabricType='FabricAttach',
    rackMounts=[{'mountUri': '/rest/server-hardware/31393736-3831-4753-568h-30335837526F', 'topUSlot': 22}]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=UPDATED_RACK_TEMPLATE
)

PARAMS_WITH_MOUNTURI = dict(
    config='config.json',
    state='present',
    data=UPDATED_RACK_TEMPLATE_WITH_DIFFERENT_MOUNTURIS
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)

RACK_TEMPLATE_WITH_NEWNAME = dict(
    name='Rename Rack',
    autoLoginRedistribution=True,
    fabricType='FabricAttach',
    rackMounts=[{'mountUri': '/rest/server-hardware/31393736-3831-4753-568h-30335837526F', 'topUSlot': 22}]
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

    def test_should_create_new_rack_if_newName_not_exists(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = RACK_TEMPLATE_WITH_NEWNAME

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_ADDED,
            ansible_facts=dict(rack=RACK_TEMPLATE_WITH_NEWNAME)
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

    def test_should_update(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        self.resource.update.return_value = DEFAULT_RACK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_UPDATED,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes_with_different_mountUris(self):
        data_merged = DEFAULT_RACK_TEMPLATE.copy()
        DEFAULT_RACK_TEMPLATE['rackMounts'] = [{'mountUri': '/rest/server-hardware/31393736-3831-4753-569h-30335837524E', 'topUSlot': 20}]
        data_merged['name'] = 'Rename Rack'

        self.resource.update.return_value = data_merged
        self.resource.data = DEFAULT_RACK_TEMPLATE
        self.resource.get_by.return_value = [UPDATED_RACK_TEMPLATE_WITH_DIFFERENT_MOUNTURIS]
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_UPDATED,
            ansible_facts=dict(rack=data_merged)
        )

    def test_update_when_data_has_modified_attributes_with_same_mountUris(self):
        UPDATED_RACK_TEMPLATE_WITH_MOUNTURIS = dict(
            name='Rename Rack',
            autoLoginRedistribution=True,
            fabricType='FabricAttach',
            rackMounts=[{'mountUri': '/rest/server-hardware/31393736-3831-4753-568h-30335837526F', 'topUSlot': 22}]
        )

        self.resource.update.return_value = UPDATED_RACK_TEMPLATE_WITH_MOUNTURIS
        self.resource.data = UPDATED_RACK_TEMPLATE_WITH_MOUNTURIS
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES
        self.resource.get_by.return_value = [UPDATED_RACK_TEMPLATE_WITH_DIFFERENT_MOUNTURIS]

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_UPDATED,
            ansible_facts=dict(rack=UPDATED_RACK_TEMPLATE_WITH_MOUNTURIS)
        )

    def test_should_remove_rack(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackModule.MSG_DELETED
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
