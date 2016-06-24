###
# Copyright (2016) Hewlett Packard Enterprise Development LP 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
###
import unittest
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_logical_interconnect_group import LogicalInterconnectGroupModule
from oneview_logical_interconnect_group import LIG_CREATED, LIG_ALREADY_EXIST, LIG_UPDATED, LIG_DELETED, \
    LIG_ALREADY_ABSENT

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_LIG_NAME = 'Test Logical Interconnect Group'
RENAMED_LIG = 'Renamed Logical Interconnect Group'

DEFAULT_LIG_TEMPLATE = dict(
    type='logical-interconnect-groupV3',
    name=DEFAULT_LIG_NAME,
    uplinkSets=[],
    enclosureType='C7000',
    interconnectMapTemplate=dict(
        interconnectMapEntryTemplates=[]
    )
)

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
              description='It is an example')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_LIG_NAME)
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class LogicalInterconnectGroupPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_create_new_lig(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = []
        mock_ov_instance.logical_interconnect_groups.create.return_value = DEFAULT_LIG_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LIG_CREATED,
            ansible_facts=dict(logical_interconnect_group=DEFAULT_LIG_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = [DEFAULT_LIG_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LIG_ALREADY_EXIST,
            ansible_facts=dict(logical_interconnect_group=DEFAULT_LIG_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_LIG_TEMPLATE.copy()
        data_merged['description'] = 'New description'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = [DEFAULT_LIG_TEMPLATE]
        mock_ov_instance.logical_interconnect_groups.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LIG_UPDATED,
            ansible_facts=dict(logical_interconnect_group=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_rename_when_resource_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = [DEFAULT_LIG_TEMPLATE]
        mock_ov_instance.logical_interconnect_groups.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ov_instance.logical_interconnect_groups.update.assert_called_once_with(data_merged)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_create_with_newName_when_resource_not_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = []
        mock_ov_instance.logical_interconnect_groups.create.return_value = DEFAULT_LIG_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ov_instance.logical_interconnect_groups.create.assert_called_once_with(PARAMS_TO_RENAME['data'])


class LogicalInterconnectGroupAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_remove_lig(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = [DEFAULT_LIG_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LIG_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_do_nothing_when_lig_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalInterconnectGroupModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LIG_ALREADY_ABSENT
        )


class LogicalInterconnectGroupErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_not_update_when_create_raises_exception(self, mock_ansible_module,
                                                            mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = []
        mock_ov_instance.logical_interconnect_groups.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_interconnect_group.AnsibleModule')
    def test_should_not_delete_when_oneview_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_interconnect_groups.get_by.return_value = [DEFAULT_LIG_TEMPLATE]
        mock_ov_instance.logical_interconnect_groups.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, LogicalInterconnectGroupModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
