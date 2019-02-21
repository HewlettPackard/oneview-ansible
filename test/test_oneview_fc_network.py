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

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import FcNetworkModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'],
              newName="New Name",
              fabricType='DirectAttach')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)


@pytest.mark.resource(TestFcNetworkModule='fc_networks')
class TestFcNetworkModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_fc_network(self):
        self.resource.get_by_name.return_value = []

        self.resource.data =  DEFAULT_FC_NETWORK_TEMPLATE
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_FC_NETWORK_TEMPLATE

        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.data = DEFAULT_FC_NETWORK_TEMPLATE
        self.resource.get_by_name.return_value = self.resource

        self.resource.data = data_merged
        self.resource.update.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_UPDATED,
            ansible_facts=dict(fc_network=data_merged)
        )

    def test_should_remove_fc_network(self):
        self.resource.data = [DEFAULT_FC_NETWORK_TEMPLATE]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_DELETED
        )

    def test_should_do_nothing_when_fc_network_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_ABSENT
        )

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/fc/fake'

        self.resource.data = resource_data
        self.resource.get_by_name.return_value = self.resource

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']

        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value =  patch_return_obj

        FcNetworkModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fc_network=patch_return),
            msg=FcNetworkModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['test']

        self.resource.data = resource_data

        self.resource.get_by_name.return_value = self.resource

        FcNetworkModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fc_network=resource_data),
            msg=FcNetworkModule.MSG_ALREADY_PRESENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
