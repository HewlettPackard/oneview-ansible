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
import mock
import yaml

from hpOneView.oneview_client import OneViewClient
from oneview_enclosure_group import EnclosureGroupModule, ENCLOSURE_GROUP_CREATED, ENCLOSURE_GROUP_ALREADY_EXIST, \
    ENCLOSURE_GROUP_UPDATED, ENCLOSURE_GROUP_DELETED, ENCLOSURE_GROUP_ALREADY_ABSENT
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

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


class EnclosureGroupClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class EnclosureGroupPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_create_new_enclosure_group(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = []
        mock_ov_instance.enclosure_groups.create.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_GROUP_CREATED,
            ansible_facts=dict(enclosure_group={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_GROUP_ALREADY_EXIST,
            ansible_facts=dict(enclosure_group=DICT_DEFAULT_ENCLOSURE_GROUP)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DICT_DEFAULT_ENCLOSURE_GROUP.copy()
        data_merged['newName'] = 'New Name'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]
        mock_ov_instance.enclosure_groups.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_GROUP_UPDATED,
            ansible_facts=dict(enclosure_group=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_update_when_script_attribute_was_modified(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DICT_DEFAULT_ENCLOSURE_GROUP.copy()
        data_merged['newName'] = 'New Name'
        data_merged['uri'] = '/rest/uri'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [data_merged]
        mock_ov_instance.enclosure_groups.update_script.return_value = ""
        mock_ov_instance.enclosure_groups.get_by.get_script = "# test script"

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_CHANGE_SCRIPT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_GROUP_UPDATED,
            ansible_facts=dict(enclosure_group=data_merged)
        )


class EnclosureGroupAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_remove_enclosure_group(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_GROUP_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_do_nothing_when_enclosure_group_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_GROUP_ALREADY_ABSENT
        )


class EnclosureGroupErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = []
        mock_ov_instance.enclosure_groups.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]
        mock_ov_instance.enclosure_groups.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_group.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosure_groups.get_by.return_value = [DICT_DEFAULT_ENCLOSURE_GROUP]
        mock_ov_instance.enclosure_groups.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_ENCLOSURE_GROUP_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
