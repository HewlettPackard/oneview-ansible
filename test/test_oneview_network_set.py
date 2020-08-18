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

import mock
import pytest
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import NetworkSetModule

FAKE_MSG_ERROR = 'Fake message error'

NETWORK_SET = dict(
    name='OneViewSDK Test Network Set',
    networkUris=['/rest/ethernet-networks/aaa-bbb-ccc']
)

NETWORK_SET_WITH_NEW_NAME = dict(name='OneViewSDK Test Network Set - Renamed')

CONNECTION_TEMPLATE = dict(bandwidth=dict(maximumBandwidth=15000,
                           typicalBandwidth=3000),
                           name='name828625927-1592834188743',
                           type='connection-template',
                           uri='/rest/connection-templates/aaa-bbb-ccc')

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              newName=NETWORK_SET['name'] + " - Renamed",
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc', 'Name of a Network'])
)

YAML_PARAMS_WITH_CONNECTION_TEMPLATE = """
    config: "config.json"
    state: present
    data:
        name: 'name828625927-1592834188743'
        type: 'connection-template'
        uri: '/rest/connection-templates/aaa-bbb-ccc'
        bandwidth:
            maximumBandwidth: 15000
            typicalBandwidth: 3000
"""

YAML_PARAMS_WITH_CHANGES = """
    config: "config.json"
    state: present
    data:
      name: 'Test Network Set'
      purpose: Management
      connectionTemplateUri: ~
      bandwidth:
          maximumBandwidth: 3000
          typicalBandwidth: 2000
"""


PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=NETWORK_SET['name'])
)

DICT_PARAMS_WITH_CHANGES = yaml.load(YAML_PARAMS_WITH_CHANGES)["data"]
DICT_PARAMS_CONNECTION_TEMPLATE = yaml.load(YAML_PARAMS_WITH_CONNECTION_TEMPLATE)["data"]


@pytest.mark.resource(TestNetworkSetModule='network_sets')
class TestNetworkSetModule(OneViewBaseTest):
    """
    OneViewBaseTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case.
    """

    def test_should_create_new_network_set(self):
        self.resource.get_by_name.return_value = []
        self.resource.create.return_value = self.resource
        self.resource.data = NETWORK_SET

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NetworkSetModule.MSG_CREATED,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = NETWORK_SET

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NetworkSetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = dict(name=NETWORK_SET['name'] + " - Renamed",
                           networkUris=['/rest/ethernet-networks/aaa-bbb-ccc',
                                        '/rest/ethernet-networks/ddd-eee-fff']
                           )

        self.resource.data = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NetworkSetModule.MSG_UPDATED,
            ansible_facts=dict(network_set=data_merged)
        )

    def test_should_raise_exception_when_ethernet_network_not_found(self):
        self.resource.get_by.side_effect = [NETWORK_SET], []
        self.resource.get_by_name.return_value = None
        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES.copy()
        self.mock_ansible_module.params['data']['networkUris'] = ['Name of a Network']

        NetworkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=NetworkSetModule.MSG_ETHERNET_NETWORK_NOT_FOUND + "Name of a Network")

    def test_should_raise_exception_when_native_ethernet_network_not_found(self):
        self.resource.get_by.side_effect = [NETWORK_SET], []
        self.resource.get_by_name.return_value = None
        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES.copy()
        self.mock_ansible_module.params['data']['networkUris'] = ['/rest/ethernet-networks/aaa-bbb-ccc']
        self.mock_ansible_module.params['data']['nativeNetworkUri'] = 'Name of a Native Network'

        NetworkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=NetworkSetModule.MSG_ETHERNET_NETWORK_NOT_FOUND + "Name of a Native Network")

    def test_should_remove_network(self):
        self.resource.data = NETWORK_SET

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NetworkSetModule.MSG_DELETED
        )

    def test_update_when_only_bandwidth_has_modified_attributes(self):
        self.resource.data = DICT_PARAMS_WITH_CHANGES
        obj = mock.Mock()
        obj.data = CONNECTION_TEMPLATE
        self.mock_ov_client.connection_templates.get_by_uri.return_value = obj

        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_WITH_CHANGES)

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NetworkSetModule.MSG_UPDATED,
            ansible_facts=dict(network_set=DICT_PARAMS_WITH_CHANGES)
        )

    def test_update_when_data_has_modified_attributes_but_bandwith_is_equal(self):
        self.resource.data = NETWORK_SET
        obj = mock.Mock()
        obj.data = {"bandwidth": DICT_PARAMS_WITH_CHANGES['bandwidth']}
        self.mock_ov_client.connection_templates.get_by_uri.return_value = obj

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NetworkSetModule.MSG_UPDATED,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_should_not_update_when_connection_template_is_equal(self):
        resource_data = NETWORK_SET
        resource_data['connection_template'] = CONNECTION_TEMPLATE.copy()
        self.resource.data = resource_data

        obj = mock.Mock()
        obj.data = CONNECTION_TEMPLATE
        self.mock_ov_client.connection_templates.get_by_uri.return_value = obj

        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_WITH_CONNECTION_TEMPLATE)

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NetworkSetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_should_do_nothing_when_network_set_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NetworkSetModule.MSG_ALREADY_ABSENT
        )

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = NETWORK_SET.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/network-sets/fake'
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj
        NetworkSetModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(network_set=patch_return),
            msg=NetworkSetModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = NETWORK_SET.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.data = resource_data

        NetworkSetModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(network_set=resource_data),
            msg=NetworkSetModule.MSG_ALREADY_PRESENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
