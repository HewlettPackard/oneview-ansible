###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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
import yaml

from oneview_server_hardware_type import (ServerHardwareTypeModule,
                                          SERVER_HARDWARE_TYPE_DELETED,
                                          SERVER_HARDWARE_TYPE_ALREADY_ABSENT,
                                          SERVER_HARDWARE_TYPE_ALREADY_UPDATED,
                                          SERVER_HARDWARE_TYPE_UPDATED,
                                          SERVER_HARDWARE_TYPE_NOT_FOUND)
from test.utils import ModuleContructorTestCase, ValidateEtagTestCase

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


class ServerHardwareTypeSpec(unittest.TestCase, ModuleContructorTestCase, ValidateEtagTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function
    ValidateEtagTestCase has common tests for the validate_etag attribute, also provides the mocks used in this test
    case.
    """

    def setUp(self):
        self.configure_mocks(self, ServerHardwareTypeModule)
        self.resource = self.mock_ov_client.server_hardware_types

    def test_should_update_the_server_hardware_type(self):
        srv_hw_type = DICT_DEFAULT_SERVER_HARDWARE_TYPE.copy()
        srv_hw_type['uri'] = '/rest/id'

        self.resource.get_by.return_value = [srv_hw_type]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SERVER_HARDWARE_TYPE_UPDATED,
            ansible_facts=dict(server_hardware_type={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SERVER_HARDWARE_TYPE_ALREADY_UPDATED,
            ansible_facts=dict(server_hardware_type=DICT_DEFAULT_SERVER_HARDWARE_TYPE)
        )

    def test_should_remove_server_hardware_type(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=SERVER_HARDWARE_TYPE_DELETED
        )

    def test_should_do_nothing_when_server_hardware_type_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=SERVER_HARDWARE_TYPE_ALREADY_ABSENT
        )

    def test_should_fail_when_update_raises_exception(self):
        self.resource.get_by.return_value = [{'uri': 'test'}]
        self.resource.update.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_server_hardware_type_was_not_found(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SERVER_HARDWARE_TYPE_NOT_FOUND
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]
        self.resource.delete.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        self.assertRaises(Exception, ServerHardwareTypeModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
