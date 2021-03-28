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

from copy import deepcopy
from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import UplinkSetModule

DEFAULT_UPLINK_NAME = 'Test Uplink Set'
RENAMED_UPLINK_SET = 'Renamed Uplink Set'

LOGICAL_INTERCONNECT = dict(uri="/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66",
                            name='Name of the Logical Interconnect')

ETHERNET = dict(uri="/rest/ethernet-networks/0de81de6-6652-4861-94f9-9104b2fd0d77",
                name='EthernetNetwork')

FCNETWORK = dict(uri="/rest/fc-networks/0de94de6-6652-4861-94f9-9c24b2fd0d87",
                 name='FcNetwork')

FCOENETWORK = dict(uri="/rest/fcoe-networks/0de89de6-6652-4861-94f9-9c24b2fd0d99",
                   name='FcoeNetwork')

EXISTENT_UPLINK_SETS = [
    dict(name=DEFAULT_UPLINK_NAME,
         logicalInterconnectUri="/rest/logical-interconnects/c4ae6a56-a595-4b06-8c7a-405212df8b93",
         uri="/rest/uplink-sets/test"),
    dict(name=DEFAULT_UPLINK_NAME,
         status="OK",
         logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
         networkUris=[
             '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
             '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
         ],
         uri="/rest/uplink-sets/test"),
    dict(name=DEFAULT_UPLINK_NAME,
         logicalInterconnectUri="/rest/logical-interconnects/c4ae6a56-a595-4b06-8c7a-405212df8b93",
         uri="/rest/uplink-sets/test")]

UPLINK_SETS = dict(
    name=DEFAULT_UPLINK_NAME,
    logicalInterconnectUri="/rest/logical-interconnects/c4ae6a56-a595-4b06-8c7a-405212df8b93",
    networkUris=[
        "/rest/ethernet-networks/0de81de6-6652-4861-94f9-9104b2fd0d77"],
    fcNetworkUris=["/rest/fc-networks/0de94de6-6652-4861-94f9-9c24b2fd0d87"],
    fcoeNetworkUris=["/rest/fcoe-networks/0de89de6-6652-4861-94f9-9c24b2fd0d99"],
    uri="/rest/uplink-sets/test")

UPLINK_SET_FOUND_BY_KEY = EXISTENT_UPLINK_SETS[1]

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
        networkUris=[
            '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
            '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
        ]
    )
)

PARAMS_FOR_PRESENT_WITH_NETWORK_NAME = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
        networkUris=[
            "EthernetNetwork"],
        fcNetworkUris=["FcNetwork"],
        fcoeNetworkUris=["FcoeNetwork"]
    )
)

PARAMS_FOR_PRESENT_WITH_LI_NAME = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectName=LOGICAL_INTERCONNECT['name'],
        networkUris=[
            '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
            '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
        ]
    )
)

PARAMS_FOR_PRESENT_WITH_NETWORK = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
        networkUris=[
            "/rest/ethernet-networks/0de81de6-6652-4861-94f9-9104b2fd0d77"],
        fcNetworkUris=["/rest/fc-networks/0de94de6-6652-4861-94f9-9c24b2fd0d87"],
        fcoeNetworkUris=["/rest/fcoe-networks/0de89de6-6652-4861-94f9-9c24b2fd0d99"]
    )
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_UPLINK_NAME,
              logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
              newName=RENAMED_UPLINK_SET)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
        networkUris=[
            '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
            '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2',
            '/rest/ethernet-networks/96g7df9g-6njb-n5jg-54um-fmsd879gdfgm'
        ],
    )
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_UPLINK_NAME,
              logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'])
)

PARAMS_FOR_ABSENT_WITH_LI_NAME = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_UPLINK_NAME,
              logicalInterconnectName=LOGICAL_INTERCONNECT['name'])
)


@pytest.mark.resource(TestUplinkSetModule='uplink_sets')
class TestUplinkSetModule(OneViewBaseTest):
    def test_should_create(self):
        self.resource.get_by_name.return_value = None
        obj = mock.Mock()
        obj.data = UPLINK_SET_FOUND_BY_KEY
        self.resource.create.return_value = obj

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        UplinkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UplinkSetModule.MSG_CREATED,
            ansible_facts=dict(uplink_set=UPLINK_SET_FOUND_BY_KEY)
        )

    def test_should_replace_network_name_by_uri(self):
        self.resource.get_by_name.return_value = None
        obj = mock.Mock()
        obj.data = UPLINK_SETS
        self.resource.create.return_value = obj

        eth_obj = mock.Mock()
        eth_obj.data = ETHERNET
        self.mock_ov_client.ethernet_networks.get_by_name.return_value = eth_obj

        fc_obj = mock.Mock()
        fc_obj.data = FCNETWORK
        self.mock_ov_client.fc_networks.get_by_name.return_value = fc_obj

        fcoe_obj = mock.Mock()
        fcoe_obj.data = FCOENETWORK
        self.mock_ov_client.fcoe_networks.get_by_name.return_value = fcoe_obj

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT_WITH_NETWORK_NAME)

        UplinkSetModule().run()

        self.mock_ov_client.ethernet_networks.get_by_name.assert_called_once_with(
            'EthernetNetwork')
        self.mock_ov_client.fc_networks.get_by_name.assert_called_once_with(
            'FcNetwork')
        self.mock_ov_client.fcoe_networks.get_by_name.assert_called_once_with(
            'FcoeNetwork')
        self.resource.create.assert_called_once_with(PARAMS_FOR_PRESENT_WITH_NETWORK['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UplinkSetModule.MSG_CREATED,
            ansible_facts=dict(uplink_set=UPLINK_SETS)
        )

    def test_should_replace_logical_interconnect_name_by_uri(self):
        self.resource.get_by_name.return_value = None
        obj = mock.Mock()
        obj.data = UPLINK_SET_FOUND_BY_KEY
        self.resource.create.return_value = obj

        obj = mock.Mock()
        obj.data = LOGICAL_INTERCONNECT
        self.mock_ov_client.logical_interconnects.get_by_name.return_value = obj
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT_WITH_LI_NAME)

        UplinkSetModule().run()

        self.mock_ov_client.logical_interconnects.get_by_name.assert_called_once_with(
            'Name of the Logical Interconnect')
        self.resource.create.assert_called_once_with(PARAMS_FOR_PRESENT['data'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UplinkSetModule.MSG_CREATED,
            ansible_facts=dict(uplink_set=UPLINK_SET_FOUND_BY_KEY)
        )

    def test_should_fail_when_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ov_client.logical_interconnects.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT_WITH_LI_NAME)

        UplinkSetModule().run()

        self.mock_ov_client.logical_interconnects.get_by_name.assert_called_once_with(
            'Name of the Logical Interconnect')

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=UplinkSetModule.MSG_LOGICAL_INTERCONNECT_NOT_FOUND)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = EXISTENT_UPLINK_SETS[1]
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        UplinkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UplinkSetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(uplink_set=UPLINK_SET_FOUND_BY_KEY)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = EXISTENT_UPLINK_SETS[0]
        data_merged['description'] = 'New description'

        self.resource.data = EXISTENT_UPLINK_SETS[0]
        self.resource.get_by_uri.return_value = self.resource
        self.resource.get_by.return_value = EXISTENT_UPLINK_SETS
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = deepcopy(PARAMS_WITH_CHANGES)

        UplinkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UplinkSetModule.MSG_UPDATED,
            ansible_facts=dict(uplink_set=data_merged)
        )

    def test_rename_when_resource_exists(self):
        data_merged = EXISTENT_UPLINK_SETS[0].copy()
        params = PARAMS_TO_RENAME["data"].copy()
        del params["newName"]
        data_merged.update(params)
        data_merged['name'] = RENAMED_UPLINK_SET

        params_to_rename = deepcopy(PARAMS_TO_RENAME)

        self.resource.data = EXISTENT_UPLINK_SETS[0]
        self.resource.get_by_name.return_value = self.resource

        obj = mock.Mock()
        obj.data = data_merged
        self.resource.update.return_value = obj

        self.mock_ansible_module.params = params_to_rename

        UplinkSetModule().run()

        self.resource.update.assert_called_once_with(data_merged)

    def test_should_delete(self):
        self.resource.data = EXISTENT_UPLINK_SETS[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT)

        UplinkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=UplinkSetModule.MSG_DELETED
        )

    def test_should_replace_logical_interconnect_name_by_uri_on_absent_state(self):
        self.resource.data = EXISTENT_UPLINK_SETS[0]
        self.resource.get_by_name.return_value = self.resource
        obj = mock.Mock()
        obj.data = LOGICAL_INTERCONNECT
        self.mock_ov_client.logical_interconnects.get_by_name.return_value = obj
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT_WITH_LI_NAME)

        UplinkSetModule().run()

        self.mock_ov_client.logical_interconnects.get_by_name.assert_called_once_with(
            'Name of the Logical Interconnect')
        self.resource.delete.assert_called_once_with()

    def test_should_do_nothing_when_not_exist(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT)

        UplinkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=UplinkSetModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_name_not_set(self):
        params = deepcopy(PARAMS_FOR_ABSENT)
        params['data'].pop('name')
        self.mock_ansible_module.params = params

        UplinkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=UplinkSetModule.MSG_KEY_REQUIRED)

    def test_should_fail_when_logical_interconnect_uri_not_set(self):
        params = deepcopy(PARAMS_FOR_ABSENT)
        params['data'].pop('logicalInterconnectUri')
        self.mock_ansible_module.params = params

        UplinkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=UplinkSetModule.MSG_KEY_REQUIRED)

    def test_should_fail_when_logical_interconnect_name_not_set(self):
        params = deepcopy(PARAMS_FOR_ABSENT_WITH_LI_NAME)
        params['data'].pop('logicalInterconnectName')
        self.mock_ansible_module.params = params

        UplinkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=UplinkSetModule.MSG_KEY_REQUIRED)


if __name__ == '__main__':
    pytest.main([__file__])
