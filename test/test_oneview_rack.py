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
from oneview_rack import RackModule
from oneview_rack import RACK_CREATED, RACK_ALREADY_EXIST, RACK_UPDATED
from oneview_rack import RACK_DELETED, RACK_ALREADY_ABSENT

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_RACK_TEMPLATE = dict(
    name='New Rack 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class RackPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_create_new_rack(self, mock_rack_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = []
        mock_ov_instance.racks.add.return_value = DEFAULT_RACK_TEMPLATE

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_rack_module.return_value = mock_ansible_instance

        RackModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_CREATED,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    @mock.patch('oneview_rack.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_rack_module, mock_from_json_file, mock_resource_compare):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        mock_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_rack_module.return_value = mock_ansible_instance

        mock_resource_compare.return_value = True

        RackModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=RACK_ALREADY_EXIST,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    @mock.patch('oneview_rack.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_rack_module, mock_from_json, mock_resource_compare):
        mock_resource_compare.return_value = False
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        mock_ov_instance.racks.update.return_value = DEFAULT_RACK_TEMPLATE

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_rack_module.return_value = mock_ansible_instance

        RackModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_UPDATED,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_rack_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = []
        mock_ov_instance.racks.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_rack_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, RackModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch('oneview_rack.resource_compare')
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_rack_module, mock_from_json, mock_resource_compare):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        mock_ov_instance.racks.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_resource_compare.return_value = False

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_rack_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, RackModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class RackAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_remove_rack(self, mock_rack_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_rack_module.return_value = mock_ansible_instance

        RackModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_do_nothing_when_rack_not_exist(self, mock_rack_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = []

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_rack_module.return_value = mock_ansible_instance

        RackModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=RACK_ALREADY_ABSENT
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_rack.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_rack_module, mock_from_json):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.racks.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        mock_ov_instance.racks.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_rack_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, RackModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
