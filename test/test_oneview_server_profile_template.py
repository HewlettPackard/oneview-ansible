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
import unittest
from copy import deepcopy
from oneview_module_loader import ServerProfileTemplateModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'
TEMPLATE_NAME = 'ProfileTemplate101'
SHT_URI = '/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B'
ENCLOSURE_GROUP_URI = '/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89'

BASIC_TEMPLATE = dict(
    name=TEMPLATE_NAME,
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI
)

BASIC_TEMPLATE_MODIFIED = dict(
    name=TEMPLATE_NAME,
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI,
    serialNumberType="Private"
)

CREATED_BASIC_TEMPLATE = dict(
    affinity="Bay",
    bios=dict(manageBios=False, overriddenSettings=[]),
    boot=dict(manageBoot=False, order=[]),
    bootMode=dict(manageMode=False, mode=None, pxeBootPolicy=None),
    category="server-profile-templates",
    enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
    name="ProfileTemplate101",
    serialNumberType="Virtual",
    serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B",
    status="OK",
    type="ServerProfileTemplateV1",
    uri="/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda",
    wwnType="Virtual"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=BASIC_TEMPLATE
)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='present',
    data=BASIC_TEMPLATE_MODIFIED
)

PARAMS_FOR_UPDATE_WITH_NAME = dict(
    config='config.json',
    state='present',
    data=dict(
        name=TEMPLATE_NAME,
        serverHardwareTypeName="Srv HW Type Name",
        enclosureGroupName="EG Name",
        serialNumberType="Private"
    )
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=BASIC_TEMPLATE
)


class ServerProfileTemplateModuleSpec(unittest.TestCase,
                                      OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, ServerProfileTemplateModule)
        self.resource = self.mock_ov_client.server_profile_templates

    def test_should_create_new_template_when_it_not_exists(self):
        self.resource.get_by_name.return_value = []
        self.resource.create.return_value = CREATED_BASIC_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ServerProfileTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileTemplateModule.MSG_CREATED,
            ansible_facts=dict(server_profile_template=CREATED_BASIC_TEMPLATE)
        )

    def test_should_not_modify_when_template_already_exists(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        self.resource.create.return_value = CREATED_BASIC_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ServerProfileTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerProfileTemplateModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(server_profile_template=CREATED_BASIC_TEMPLATE)
        )

    def test_should_update_when_data_has_modified_attributes(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        self.resource.update.return_value = CREATED_BASIC_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        ServerProfileTemplateModule().run()

        expected = CREATED_BASIC_TEMPLATE.copy()
        expected.update(BASIC_TEMPLATE_MODIFIED)

        self.resource.update.assert_called_once_with(
            resource=expected, id_or_uri=expected["uri"]
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileTemplateModule.MSG_UPDATED,
            ansible_facts=dict(server_profile_template=CREATED_BASIC_TEMPLATE)
        )

    def test_update_using_names_for_dependecies(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        self.resource.update.return_value = CREATED_BASIC_TEMPLATE
        self.mock_ov_client.enclosure_groups.get_by.return_value = [{'uri': ENCLOSURE_GROUP_URI}]
        self.mock_ov_client.server_hardware_types.get_by.return_value = [{'uri': SHT_URI}]

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_UPDATE_WITH_NAME)

        ServerProfileTemplateModule().run()

        expected = CREATED_BASIC_TEMPLATE.copy()
        expected.update(BASIC_TEMPLATE_MODIFIED)

        self.resource.update.assert_called_once_with(resource=expected, id_or_uri=expected["uri"])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileTemplateModule.MSG_UPDATED,
            ansible_facts=dict(server_profile_template=CREATED_BASIC_TEMPLATE)
        )

    def test_should_fail_when_server_hardware_type_not_found(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        self.resource.update.return_value = CREATED_BASIC_TEMPLATE
        self.mock_ov_client.enclosure_groups.get_by.return_value = [{'uri': ENCLOSURE_GROUP_URI}]
        self.mock_ov_client.server_hardware_types.get_by.return_value = []

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_UPDATE_WITH_NAME)

        ServerProfileTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ServerProfileTemplateModule.MSG_SRV_HW_TYPE_NOT_FOUND + 'Srv HW Type Name'
        )

    def test_should_fail_when_enclosure_group_not_found(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        self.resource.update.return_value = CREATED_BASIC_TEMPLATE
        self.mock_ov_client.enclosure_groups.get_by.return_value = []
        self.mock_ov_client.server_hardware_types.get_by.return_value = [{'uri': SHT_URI}]

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_UPDATE_WITH_NAME)

        ServerProfileTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ServerProfileTemplateModule.MSG_ENCLOSURE_GROUP_NOT_FOUND + 'EG Name'
        )

    def test_should_delete_when_template_exists(self):
        self.resource.get_by_name.return_value = CREATED_BASIC_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ServerProfileTemplateModule().run()

        self.resource.delete.assert_called_once_with(CREATED_BASIC_TEMPLATE)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileTemplateModule.MSG_DELETED
        )

    def test_should_do_nothing_when_templates_not_exists(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ServerProfileTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerProfileTemplateModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
