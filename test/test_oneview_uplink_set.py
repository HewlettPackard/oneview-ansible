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
    UPLINK_SET_DELETED, UPLINK_SET_UPDATED, UPLINK_SET_NEW_NAME_INVALID, UPLINK_SET_NOT_EXIST

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_UPLINK_NAME = 'Test Uplink Set'
RENAMED_LIG = 'Renamed Uplink Set'

DEFAULT_UPLINK_TEMPLATE = dict(
    name=DEFAULT_UPLINK_NAME,
    status="OK",
    logicalInterconnectUri="/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66",
    networkUris=[
        '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
        '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
    ]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
        logicalInterconnectUri="/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66",
        networkUris=[
            '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
            '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
        ],
    )
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_UPLINK_NAME,
              newName=RENAMED_LIG)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(
        name=DEFAULT_UPLINK_NAME,
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
    data=dict(name=DEFAULT_UPLINK_NAME)
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class UplinkSetPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_create(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []
        mock_ov_instance.uplink_sets.create.return_value = DEFAULT_UPLINK_TEMPLATE

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=UPLINK_SET_CREATED,
            ansible_facts=dict(uplink_set=DEFAULT_UPLINK_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=UPLINK_SET_ALREADY_EXIST,
            ansible_facts=dict(uplink_set=DEFAULT_UPLINK_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_UPLINK_TEMPLATE.copy()
        data_merged['description'] = 'New description'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]
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
        data_merged = DEFAULT_UPLINK_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by = mock.MagicMock(side_effect=[[DEFAULT_UPLINK_TEMPLATE], []])
        mock_ov_instance.uplink_sets.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ov_instance.uplink_sets.update.assert_called_once_with(data_merged)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_fail_rename_when_resource_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_UPLINK_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = []
        mock_ov_instance.uplink_sets.update.return_value = data_merged

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=UPLINK_SET_NOT_EXIST
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_fail_rename_when_new_name_already_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DEFAULT_UPLINK_TEMPLATE.copy()
        data_merged['name'] = RENAMED_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        mock_ov_instance = mock.Mock()
        # get_by is called twice (with 'name' and with 'newName')
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_to_rename)
        mock_ansible_module.return_value = mock_ansible_instance

        UplinkSetModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=UPLINK_SET_NEW_NAME_INVALID
        )


class UplinkSetAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_uplink_set.AnsibleModule')
    def test_should_remove(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]

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
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]
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
        mock_ov_instance.uplink_sets.get_by.return_value = [DEFAULT_UPLINK_TEMPLATE]
        mock_ov_instance.uplink_sets.delete.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, UplinkSetModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
