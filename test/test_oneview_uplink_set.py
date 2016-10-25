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
from oneview_uplink_set import UplinkSetModule
from oneview_uplink_set import UPLINK_SET_ALREADY_ABSENT, UPLINK_SET_ALREADY_EXIST, UPLINK_SET_CREATED, \
    UPLINK_SET_DELETED, UPLINK_SET_UPDATED, UPLINK_SET_KEY_REQUIRED
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_UPLINK_NAME = 'Test Uplink Set'
RENAMED_UPLINK_SET = 'Renamed Uplink Set'

LOGICAL_INTERCONNECT = dict(uri="/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66",
                            name='Name of the Logical Interconnect')

EXISTENT_UPLINK_SETS = [dict(name=DEFAULT_UPLINK_NAME,
                             logicalInterconnectUri="/rest/logical-interconnects/c4ae6a56-a595-4b06-8c7a-405212df8b93"),
                        dict(name=DEFAULT_UPLINK_NAME,
                             status="OK",
                             logicalInterconnectUri=LOGICAL_INTERCONNECT['uri'],
                             networkUris=[
                                 '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
                                 '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2']),
                        dict(name=DEFAULT_UPLINK_NAME,
                             logicalInterconnectUri="/rest/logical-interconnects/c4ae6a56-a595-4b06-8c7a-405212df8b93")]

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
        ],
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


class UplinkSetClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class UplinkSetPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_create(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []
        mock_ov_instance.uplink_sets.create.return_value = UPLINK_SET_FOUND_BY_KEY

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UPLINK_SET_CREATED,
            ansible_facts=dict(uplink_set=UPLINK_SET_FOUND_BY_KEY)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_replace_logical_interconnect_name_by_uri(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT_WITH_LI_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with('Name of the Logical Interconnect')
        mock_ov_instance.uplink_sets.create.assert_called_once_with(PARAMS_FOR_PRESENT['data'])

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=UPLINK_SET_ALREADY_EXIST,
            ansible_facts=dict(uplink_set=UPLINK_SET_FOUND_BY_KEY)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = UPLINK_SET_FOUND_BY_KEY.copy()
        data_merged['description'] = 'New description'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS
        mock_ov_instance.uplink_sets.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UPLINK_SET_UPDATED,
            ansible_facts=dict(uplink_set=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_rename_when_resource_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = UPLINK_SET_FOUND_BY_KEY.copy()
        data_merged['name'] = RENAMED_UPLINK_SET
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by = mock.MagicMock(side_effect=[EXISTENT_UPLINK_SETS, []])
        mock_ov_instance.uplink_sets.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ov_instance.uplink_sets.update.assert_called_once_with(data_merged)


class UplinkSetAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_delete(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UPLINK_SET_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_replace_logical_interconnect_name_by_uri(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS
        mock_ov_instance.logical_interconnects.get_by_name.return_value = LOGICAL_INTERCONNECT

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT_WITH_LI_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ov_instance.logical_interconnects.get_by_name.assert_called_once_with('Name of the Logical Interconnect')
        mock_ov_instance.uplink_sets.delete.assert_called_once_with(UPLINK_SET_FOUND_BY_KEY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_do_nothing_when_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=UPLINK_SET_ALREADY_ABSENT
        )


class UplinkSetErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_ansible_module,
                                                      mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []
        mock_ov_instance.uplink_sets.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS
        mock_ov_instance.uplink_sets.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = EXISTENT_UPLINK_SETS
        mock_ov_instance.uplink_sets.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_name_not_set(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        params = PARAMS_FOR_ABSENT.copy()
        params['data'].pop('name')

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=UPLINK_SET_KEY_REQUIRED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_logical_interconnect_uri_not_set(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        params = PARAMS_FOR_ABSENT.copy()
        params['data'].pop('logicalInterconnectUri')

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=UPLINK_SET_KEY_REQUIRED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_fail_when_logical_interconnect_name_not_set(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        params = PARAMS_FOR_ABSENT_WITH_LI_NAME.copy()
        params['data'].pop('logicalInterconnectName')

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=UPLINK_SET_KEY_REQUIRED
        )


if __name__ == '__main__':
    unittest.main()
