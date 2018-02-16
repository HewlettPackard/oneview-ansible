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
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import EnclosureGroupModule

FAKE_MSG_ERROR = 'Fake message error'

YAML_ENCLOSURE_GROUP = """
        config: "{{ config }}"
        state: present
        data:
            name: "Enclosure Group 1"
            stackingMode: "Enclosure"
            interconnectBayMappings:
                - interconnectBay: 1
                - interconnectBay: 2
                - interconnectBay: 3
                - interconnectBay: 4
                - interconnectBay: 5
                - interconnectBay: 6
                - interconnectBay: 7
                - interconnectBay: 8
          """

YAML_ENCLOSURE_GROUP_CHANGES = """
    config: "{{ config }}"
    state: present
    data:
        name: "Enclosure Group 1"
        newName: "Enclosure Group 1 (Changed)"
        stackingMode: "Enclosure"
        interconnectBayMappings:
            - interconnectBay: 1
            - interconnectBay: 2
            - interconnectBay: 3
            - interconnectBay: 4
            - interconnectBay: 5
            - interconnectBay: 6
            - interconnectBay: 7
            - interconnectBay: 8
      """

YAML_ENCLOSURE_GROUP_CHANGE_SCRIPT = """
    config: "{{ config }}"
    state: present
    data:
        name: "Enclosure Group 1"
        configurationScript: "# test script "
      """

YAML_ENCLOSURE_GROUP_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
          name: "Enclosure Group 1 (renamed)"
        """

DICT_DEFAULT_ENCLOSURE_GROUP = yaml.load(YAML_ENCLOSURE_GROUP)["data"]


@pytest.mark.resource(TestEnclosureGroupModule='enclosure_groups')
class TestEnclosureGroupModule(OneViewBaseTest):
    """
    OneViewBaseTestCase has tests for main function, also provides the mocks used in this test case
    """

    def test_should_create_new_enclosure_group(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureGroupModule.MSG_CREATED,
            ansible_facts=dict(enclosure_group={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureGroupModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(enclosure_group=DICT_DEFAULT_ENCLOSURE_GROUP)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DICT_DEFAULT_ENCLOSURE_GROUP.copy()
        data_merged['newName'] = 'New Name'

        self.resource.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP_CHANGES)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureGroupModule.MSG_UPDATED,
            ansible_facts=dict(enclosure_group=data_merged)
        )

    def test_update_when_script_attribute_was_modified(self):
        data_merged = DICT_DEFAULT_ENCLOSURE_GROUP.copy()
        data_merged['newName'] = 'New Name'
        data_merged['uri'] = '/rest/uri'

        self.resource.get_by.return_value = [data_merged]
        self.resource.update.return_value = {"res": "updated"}
        self.resource.get_script.return_value = "# test script"

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP_CHANGE_SCRIPT)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureGroupModule.MSG_UPDATED,
            ansible_facts=dict(enclosure_group={"res": "updated"})
        )

    def test_update_when_script_attribute_was_not_modified(self):
        data_merged = DICT_DEFAULT_ENCLOSURE_GROUP.copy()
        data_merged['newName'] = 'New Name'
        data_merged['uri'] = '/rest/uri'

        self.resource.get_by.return_value = [data_merged]
        self.resource.update_script.return_value = ""
        self.resource.get_script.return_value = "# test script "

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP_CHANGE_SCRIPT)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureGroupModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(enclosure_group=data_merged)
        )

    def test_should_remove_enclosure_group(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP_ABSENT)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureGroupModule.MSG_DELETED
        )

    def test_should_do_nothing_when_enclosure_group_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_ENCLOSURE_GROUP_ABSENT)

        EnclosureGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureGroupModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
