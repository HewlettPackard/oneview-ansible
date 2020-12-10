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

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import FcNetworkModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
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

PARAMS_WITH_BANDWIDTH = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'],
              newName="New Name",
              fabricType='DirectAttach',
              connectionTemplateUri='/rest/',
              bandwidth=dict(maximumBandwidth=3000,
                             typicalBandwidth=2000))
)

CHECK_MODE_PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'],
              newName="New Name")
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
        self.mock_ansible_module.check_mode = False
        self.resource.data = DEFAULT_FC_NETWORK_TEMPLATE
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_to_check_create_new_fc_network(self):
        self.resource.get_by_name.return_value = []
        self.mock_ansible_module.check_mode = True
        self.resource.data = CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_CREATED,
            ansible_facts=dict(fc_network=CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_FC_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        self.mock_ansible_module.check_mode = False
        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_with_check_mode_should_not_update_when_data_is_equals(self):
        self.resource.data = CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        self.mock_ansible_module.check_mode = True
        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(fc_network=CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.data = data_merged
        self.resource.update.return_value = self.resource
        self.mock_ansible_module.check_mode = False
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_UPDATED,
            ansible_facts=dict(fc_network=data_merged)
        )

    def test_with_check_mode_update_when_data_has_modified_attributes(self):
        data_merged = CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE.copy()

        self.resource.data = data_merged
        self.resource.update.return_value = self.resource
        self.mock_ansible_module.check_mode = True
        self.mock_ansible_module.params = CHECK_MODE_PARAMS_WITH_CHANGES

        FcNetworkModule().run()

        data_merged['name'] = 'New Name'
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_UPDATED,
            ansible_facts=dict(fc_network=data_merged)
        )

    def test_should_remove_fc_network(self):
        self.resource.data = [DEFAULT_FC_NETWORK_TEMPLATE]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT
        self.mock_ansible_module.check_mode = False
        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_DELETED
        )

    def test_with_check_mode_should_remove_fc_network(self):
        self.resource.data = [DEFAULT_FC_NETWORK_TEMPLATE]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT
        self.mock_ansible_module.check_mode = True
        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_DELETED
        )

    def test_should_do_nothing_when_fc_network_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT
        self.mock_ansible_module.check_mode = False
        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_ABSENT
        )

    def test_with_check_mode_should_do_nothing_when_fc_network_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT
        self.mock_ansible_module.check_mode = True
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

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']

        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj
        self.mock_ansible_module.check_mode = False
        FcNetworkModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fc_network=patch_return),
            msg=FcNetworkModule.MSG_UPDATED
        )

    def test_with_check_mode_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = CHECK_MODE_DEFAULT_FC_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['fake']

        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']

        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj
        self.mock_ansible_module.check_mode = True
        FcNetworkModule().run()

        del(patch_return['scopeUris'])
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fc_network=patch_return),
            msg=FcNetworkModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope
        self.mock_ansible_module.check_mode = False
        resource_data = DEFAULT_FC_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['test']

        self.resource.data = resource_data

        FcNetworkModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fc_network=resource_data),
            msg=FcNetworkModule.MSG_ALREADY_PRESENT
        )

    def test_should_delete_bulk_fc_networks(self):
        networkUris = [
            "/rest/fc-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
            "/rest/fc-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
            "/rest/fc-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
        ]

        PARAMS_FOR_BULK_DELETED = dict(
            config='config.json',
            state='absent',
            data=dict(networkUris=[
                "/rest/fc-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
                "/rest/fc-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
                "/rest/fc-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
            ])
        )

        self.resource.delete_bulk.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_BULK_DELETED

        FcNetworkModule().run()

        self.resource.delete_bulk.assert_called_once_with({'networkUris': networkUris})
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True, msg=FcNetworkModule.BULK_MSG_DELETED,
            ansible_facts=dict(fc_network_bulk_delete=None))

    def test_update_when_only_bandwidth_has_modified_attributes(self):
        DEFAULT_FC_NETWORK_TEMPLATE_WITH_BANDWIDTH = {'name': 'New FC Network 2',
                                                      'connectionTemplateUri': '/rest/',
                                                      'bandwidth': {
                                                          'maximumBandwidth': 20,
                                                          'typicalBandwidth': 10
                                                      },
                                                      'autoLoginRedistribution': 'True',
                                                      'fabricType': 'FabricAttach',
                                                      }
        self.resource.data = DEFAULT_FC_NETWORK_TEMPLATE_WITH_BANDWIDTH
        self.mock_ansible_module.check_mode = False
        self.mock_ansible_module.params = PARAMS_WITH_BANDWIDTH
        self.resource.update.return_value = self.resource
        obj = mock.Mock()
        obj.data = {"uri": "uri"}
        self.mock_ov_client.connection_templates.get_by_uri.return_value = obj

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE_WITH_BANDWIDTH)
        )


if __name__ == '__main__':
    pytest.main([__file__])
