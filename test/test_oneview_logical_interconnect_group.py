#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import LogicalInterconnectGroupModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_LIG_NAME = 'Test Logical Interconnect Group'
RENAMED_LIG = 'Renamed Logical Interconnect Group'

DEFAULT_LIG_TEMPLATE = dict(
    name=DEFAULT_LIG_NAME,
    uplinkSets=[],
    enclosureType='C7000',
    interconnectMapTemplate=dict(
        interconnectMapEntryTemplates=[]
    )
)
DEFAULT_LIG_TEMPLATE_WITH_UPLINKSETS = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_LIG_NAME,
        uplinkSets=[dict(
            logicalPortConfigInfos=[dict(
                desiredSpeed="Auto",
                logicalLocation=dict(
                    locationEntries=[dict(
                        relativeValue=1,
                        type="Bay"
                    ), dict(
                        relativeValue=21,
                        type="Port"
                    ), dict(
                        relativeValue=1,
                        type="Enclosure"
                    )
                    ]
                )
            )
            ],
            name="EnetUplink1",
            networkType="Ethernet",
            networkUris=["/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734797fbd"],
            networkNames=["TestNetwork_1"]
        )
        ],
        enclosureType='C7000',
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[]
        )
    )
)
DEFAULT_LIG_TEMPLATE_WITH_DIFFERENT_UPLINKSETS = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_LIG_NAME,
        uplinkSets=[dict(
            logicalPortConfigInfos=[dict(
                desiredSpeed="Auto",
                logicalLocation=dict(
                    locationEntries=[dict(
                        relativeValue=1,
                        type="Bay"
                    ), dict(
                        relativeValue=21,
                        type="Port"
                    ), dict(
                        relativeValue=1,
                        type="Enclosure"
                    )
                    ]
                )
            )
            ],
            name="EnetUplink1",
            networkType="Ethernet",
            networkUris=["/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734797fbd1"],
            networkNames=["TestNetwork_1"]
        )
        ],
        enclosureType='C7000',
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[]
        )
    )
)
PARAMS_LIG_TEMPLATE_WITH_MAP = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_LIG_NAME,
        uplinkSets=[dict(
            logicalPortConfigInfos=[dict(
                desiredSpeed="Auto",
                logicalLocation=dict(
                    locationEntries=[dict(
                        relativeValue=1,
                        type="Bay"
                    ), dict(
                        relativeValue=21,
                        type="Port"
                    ), dict(
                        relativeValue=1,
                        type="Enclosure"
                    )
                    ]
                )
            )
            ],
            name="EnetUplink1",
            networkType="Ethernet",
            networkUris=["/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734797fbd"],
            networkNames=["TestNetwork_1"]
        )
        ],
        enclosureType='C7000',
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[
                {
                    "logicalDownlinkUri": None,
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "relativeValue": "1",
                                "type": "Bay"
                            },
                            {
                                "relativeValue": 1,
                                "type": "Enclosure"
                            }
                        ]
                    },
                    "permittedInterconnectTypeName": "HP VC Flex-10/10D Module"
                }]
        )
    ))

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_LIG_NAME)
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_LIG_NAME,
              newName=RENAMED_LIG)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_LIG_NAME,
              uplinkSets=[{
                  "logicalPortConfigInfos": [{
                      "desiredSpeed": "Auto",
                      "logicalLocation": {
                          "locationEntries": [{
                              "relativeValue": 1,
                              "type": "Bay"
                          }, {
                              "relativeValue": 21,
                              "type": "Port"
                          }, {
                              "relativeValue": 1,
                              "type": "Enclosure"
                          }]
                      }
                  }],
                  "name": "EnetUplink1",
                  "networkType": "Ethernet",
                  "networkUris": ["/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734797fbd",
                                  "/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734869edg"],
                  "networkNames": ["TestNetwork_1"]
              }]
              )
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_LIG_NAME)
)


@pytest.mark.resource(TestLogicalInterconnectGroupModule='logical_interconnect_groups')
class TestLogicalInterconnectGroupModule(OneViewBaseTest):
    def test_should_create_new_lig(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectGroupModule.MSG_CREATED,
            ansible_facts=dict(logical_interconnect_group=DEFAULT_LIG_TEMPLATE)
        )

    def test_should_create_new_with_named_permitted_interconnect_type(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = PARAMS_FOR_PRESENT
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]
        self.mock_ov_client.logical_interconnect_groups.get_by.return_value = [dict(uplinkSets=[{
                                            "logicalPortConfigInfos": [{
                                                "desiredSpeed": "Auto",
                                                "logicalLocation": {
                                                    "locationEntries": [{
                                                        "relativeValue": 1,
                                                        "type": "Bay"
                                                    }, {
                                                        "relativeValue": 21,
                                                        "type": "Port"
                                                    }, {
                                                        "relativeValue": 1,
                                                        "type": "Enclosure"
                                                    }]
                                                }
                                            }],
                                            "name": "EnetUplink1",
                                            "networkType": "Ethernet",
                                            "networkUris": ["/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734797fbd",
                                                            "/rest/ethernet-networks/5c3aefcb-0dd5-4fcc-b652-c9e734869edg"],
                                            "networkNames": ["TestNetwork_1"]
                                        }])
                                    ]
        self.mock_ansible_module.params = deepcopy(PARAMS_LIG_TEMPLATE_WITH_MAP)

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectGroupModule.MSG_CREATED,
            ansible_facts=dict(logical_interconnect_group=PARAMS_FOR_PRESENT.copy())
        )

    def test_should_fail_when_permitted_interconnect_type_name_not_exists(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = PARAMS_FOR_PRESENT
        self.mock_ov_client.interconnect_types.get_by.return_value = []

        self.mock_ansible_module.params = deepcopy(PARAMS_LIG_TEMPLATE_WITH_MAP)

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=LogicalInterconnectGroupModule.MSG_INTERCONNECT_TYPE_NOT_FOUND)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectGroupModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(logical_interconnect_group=DEFAULT_LIG_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectGroupModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(logical_interconnect_group=self.resource.data)
        )

    def test_update_when_data_has_modified_uplinkset_attributes(self):
        self.mock_ansible_module.params = DEFAULT_LIG_TEMPLATE_WITH_DIFFERENT_UPLINKSETS

        self.resource.data = DEFAULT_LIG_TEMPLATE_WITH_UPLINKSETS

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectGroupModule.MSG_UPDATED,
            ansible_facts=dict(logical_interconnect_group=self.resource.data)
        )

    def test_rename_when_resource_exists(self):
        data_merged = DEFAULT_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = params_to_rename

        LogicalInterconnectGroupModule().run()

        self.resource.update.assert_called_once_with(data_merged)

    def test_create_with_newName_when_resource_not_exists(self):
        data_merged = DEFAULT_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = params_to_rename

        LogicalInterconnectGroupModule().run()

        self.resource.create.assert_called_once_with(PARAMS_TO_RENAME['data'])

    def test_should_remove_lig(self):
        self.resource.data = DEFAULT_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalInterconnectGroupModule.MSG_DELETED
        )

    def test_should_do_nothing_when_lig_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        LogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalInterconnectGroupModule.MSG_ALREADY_ABSENT
        )

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_LIG_TEMPLATE.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/lig/fake'
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        obj = mock.Mock()
        obj.data = patch_return
        self.resource.patch.return_value = obj

        LogicalInterconnectGroupModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(logical_interconnect_group=patch_return),
            msg=LogicalInterconnectGroupModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_LIG_TEMPLATE.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.data = resource_data

        LogicalInterconnectGroupModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnect_group=resource_data),
            msg=LogicalInterconnectGroupModule.MSG_ALREADY_PRESENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
