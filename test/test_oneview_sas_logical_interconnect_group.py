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

from hpOneView.oneview_client import OneViewClient
from oneview_sas_logical_interconnect_group import SasLogicalInterconnectGroupModule
from oneview_sas_logical_interconnect_group import SAS_LIG_CREATED, SAS_LIG_ALREADY_EXIST, SAS_LIG_UPDATED, \
    SAS_LIG_DELETED, SAS_LIG_ALREADY_ABSENT
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SAS_LIG_NAME = 'Test SAS Logical Interconnect Group'
RENAMED_SAS_LIG = 'Renamed SAS Logical Interconnect Group'

DEFAULT_SAS_LIG_TEMPLATE = dict(
    type='sas-logical-interconnect-group',
    name=DEFAULT_SAS_LIG_NAME,
    state='Active',
    enclosureType='SY12000',
    interconnectBaySet="1"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              newName=RENAMED_SAS_LIG)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              interconnectBaySet='2')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)


class LogicalInterconnectGroupClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_logical_interconnect_group.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_sas_logical_interconnect_group.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class SasLogicalInterconnectGroupSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch('oneview_sas_logical_interconnect_group.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.patcher_ov_client_from_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client_from_json_file = self.patcher_ov_client_from_json_file.start()

        self.mock_ov_instance = mock.Mock()
        self.mock_ov_client_from_json_file.return_value = self.mock_ov_instance

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_ov_client_from_json_file.stop()

    def test_should_create(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = []
        self.mock_ov_instance.sas_logical_interconnect_groups.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_CREATED,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_create_with_newName_when_resource_not_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = []
        self.mock_ov_instance.sas_logical_interconnect_groups.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        mock_ansible_instance = create_ansible_mock(params_to_rename)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        self.mock_ov_instance.sas_logical_interconnect_groups.create.assert_called_once_with(PARAMS_TO_RENAME['data'])

    def test_should_fail_when_create_raises_exception(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = []
        self.mock_ov_instance.sas_logical_interconnect_groups.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SasLogicalInterconnectGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_not_update_when_data_is_equals(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_LIG_ALREADY_EXIST,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['description'] = 'New description'

        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.mock_ov_instance.sas_logical_interconnect_groups.update.return_value = data_merged

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_UPDATED,
            ansible_facts=dict(sas_logical_interconnect_group=data_merged)
        )

    def test_rename_when_resource_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.mock_ov_instance.sas_logical_interconnect_groups.update.return_value = data_merged

        mock_ansible_instance = create_ansible_mock(params_to_rename)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        self.mock_ov_instance.sas_logical_interconnect_groups.update.assert_called_once_with(data_merged)

    def test_should_fail_when_update_raises_exception(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.mock_ov_instance.sas_logical_interconnect_groups.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        self.mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SasLogicalInterconnectGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_remove(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_DELETED
        )

    def test_should_do_nothing_when_resource_not_exist(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = []
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        SasLogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_LIG_ALREADY_ABSENT
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.mock_ov_instance.sas_logical_interconnect_groups.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.mock_ov_instance.sas_logical_interconnect_groups.delete.side_effect = Exception(FAKE_MSG_ERROR)
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, SasLogicalInterconnectGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
