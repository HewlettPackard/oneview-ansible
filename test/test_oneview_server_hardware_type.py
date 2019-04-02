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
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ServerHardwareTypeModule

FAKE_MSG_ERROR = 'Fake message error'

YAML_SERVER_HARDWARE_TYPE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          description: "New Description"
          """

YAML_SERVER_HARDWARE_TYPE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          newName: 'My New Server Hardware Type'
          description: "Another Description"
          """

YAML_SERVER_HARDWARE_TYPE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'MyServerHardwareType'
        """

DICT_DEFAULT_SERVER_HARDWARE_TYPE = yaml.load(YAML_SERVER_HARDWARE_TYPE)["data"]
DICT_DEFAULT_SERVER_HARDWARE_TYPE_CHANGED = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)["data"]


@pytest.mark.resource(TestServerHardwareTypeModule='server_hardware_types')
class TestServerHardwareTypeModule(OneViewBaseTest):
    def test_should_update_the_server_hardware_type(self):
        srv_hw_type = DICT_DEFAULT_SERVER_HARDWARE_TYPE.copy()
        srv_hw_type['uri'] = '/rest/id'

        self.resource.data = srv_hw_type

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareTypeModule.MSG_UPDATED,
            ansible_facts=dict(server_hardware_type=srv_hw_type)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DICT_DEFAULT_SERVER_HARDWARE_TYPE

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareTypeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(server_hardware_type=DICT_DEFAULT_SERVER_HARDWARE_TYPE)
        )

    def test_should_remove_server_hardware_type(self):
        self.resource.data = DICT_DEFAULT_SERVER_HARDWARE_TYPE

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareTypeModule.MSG_DELETED
        )

    def test_should_do_nothing_when_server_hardware_type_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareTypeModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_server_hardware_type_was_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ServerHardwareTypeModule.MSG_RESOURCE_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
