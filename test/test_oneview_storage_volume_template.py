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
from oneview_storage_volume_template import StorageVolumeTemplateModule, STORAGE_VOLUME_TEMPLATE_CREATED, \
    STORAGE_VOLUME_TEMPLATE_DELETED, STORAGE_VOLUME_TEMPLATE_ALREADY_ABSENT, \
    STORAGE_VOLUME_TEMPLATE_MANDATORY_FIELD_MISSING, \
    STORAGE_VOLUME_TEMPLATE_ALREADY_UPDATED, STORAGE_VOLUME_TEMPLATE_UPDATED
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

FAKE_MSG_ERROR = 'Fake message error'

YAML_STORAGE_VOLUME_TEMPLATE = """
        config: "{{ config }}"
        state: present
        data:
            name: '{{storage_vol_templ_name}}'
            state: "Configured"
            description: "Example Template"
            provisioning:
                 shareable: true
                 provisionType: "Thin"
                 capacity: "235834383322"
                 storagePoolUri: '{{storage_pool_uri}}'
            stateReason: "None"
            storageSystemUri: '{{ storage_system_uri }}'
            snapshotPoolUri: '{{storage_pool_uri}}'
            type: StorageVolumeTemplateV3
          """

YAML_STORAGE_VOLUME_TEMPLATE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            name: '{{storage_vol_templ_name}}'
            state: "Configured"
            description: "Example Template with a new description"
            provisioning:
                 shareable: true
                 provisionType: "Thin"
                 capacity: "235834383322"
                 storagePoolUri: '{{storage_pool_uri}}'
            stateReason: "None"
            storageSystemUri: '{{ storage_system_uri }}'
            snapshotPoolUri: '{{storage_pool_uri}}'
            type: StorageVolumeTemplateV3
      """

YAML_STORAGE_VOLUME_TEMPLATE_MISSING_KEY = """
        config: "{{ config }}"
        state: present
        data:
            state: "Configured"
    """

YAML_STORAGE_VOLUME_TEMPLATE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: '{{storage_vol_templ_name}}'
        """

DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE = yaml.load(YAML_STORAGE_VOLUME_TEMPLATE)["data"]
DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE_CHANGED = yaml.load(YAML_STORAGE_VOLUME_TEMPLATE_CHANGE)["data"]


class StorageVolumeTemplateClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class StorageVolumeTemplatePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_create_new_storage_volume_template(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = []
        mock_ov_instance.storage_volume_templates.create.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_CREATED,
            ansible_facts=dict(storage_volume_template={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_update_the_storage_volume_template(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]
        mock_ov_instance.storage_volume_templates.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_UPDATED,
            ansible_facts=dict(storage_volume_template={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_VOLUME_TEMPLATE_ALREADY_UPDATED,
            ansible_facts=dict(storage_volume_template=DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE)
        )


class StorageVolumeTemplateAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_remove_storage_volume_template(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_do_nothing_when_storage_volume_template_not_exist(self, mock_ansible_module,
                                                                      mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        StorageVolumeTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=STORAGE_VOLUME_TEMPLATE_ALREADY_ABSENT
        )


class StorageVolumeTemplateErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = []
        mock_ov_instance.storage_volume_templates.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]
        mock_ov_instance.storage_volume_templates.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]
        mock_ov_instance.storage_volume_templates.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_storage_volume_template.AnsibleModule')
    def test_should_raise_exception_when_key_is_missing(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.storage_volume_templates.get_by.return_value = [DICT_DEFAULT_STORAGE_VOLUME_TEMPLATE]
        mock_ov_instance.storage_volume_templates.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_STORAGE_VOLUME_TEMPLATE_MISSING_KEY)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=STORAGE_VOLUME_TEMPLATE_MANDATORY_FIELD_MISSING
        )


if __name__ == '__main__':
    unittest.main()
