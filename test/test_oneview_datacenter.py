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
from copy import deepcopy

from hpOneView.oneview_client import OneViewClient
from oneview_datacenter import DatacenterModule, DATACENTER_ADDED, DATACENTER_REMOVED, DATACENTER_ALREADY_ABSENT, \
    RACK_NOT_FOUND, DATACENTER_ALREADY_UPDATED, DATACENTER_UPDATED, DATACENTER_NOT_FOUND, \
    DATACENTER_NEW_NAME_ALREADY_EXISTS

FAKE_MSG_ERROR = 'Fake message error'

RACK_URI = '/rest/racks/rackid'

YAML_DATACENTER = """
        config: "{{ config }}"
        state: present
        data:
            name: "MyDatacenter"
            width: 5000
            depth: 6000
            contents:
                - resourceName: "Rack-221"
                  resourceUri: '/rest/racks/rackid'
                  x: 1000
                  y: 1000
          """

YAML_DATACENTER_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            name: "MyDatacenter"
            newName: "MyDatacenter1"
            width: 5000
            depth: 5000
            contents:
                - resourceUri: '/rest/racks/rackid'
                  x: 1000
                  y: 1000
      """

YAML_DATACENTER_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'MyDatacenter'
        """

DICT_DEFAULT_DATACENTER = yaml.load(YAML_DATACENTER)["data"]
DICT_DEFAULT_DATACENTER_CHANGED = yaml.load(YAML_DATACENTER_CHANGE)["data"]


def create_ansible_mock(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class DatacenterPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_create_new_datacenter(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = []
        mock_ov_instance.datacenters.add.return_value = {"name": "name"}
        mock_ov_instance.racks.get_by.return_value = [{'uri': RACK_URI}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=DATACENTER_ADDED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_update_the_datacenter(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.side_effect = [[DICT_DEFAULT_DATACENTER], []]
        mock_ov_instance.datacenters.update.return_value = {"name": "name"}

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_CHANGE)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=DATACENTER_UPDATED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        datacenter_replaced = DICT_DEFAULT_DATACENTER.copy()
        del datacenter_replaced['contents'][0]['resourceName']

        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = [DICT_DEFAULT_DATACENTER]
        mock_ov_instance.racks.get_by.return_value = [{'uri': RACK_URI}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=DATACENTER_ALREADY_UPDATED,
            ansible_facts=dict(datacenter=DICT_DEFAULT_DATACENTER)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_warning_rename_when_datacenter_not_exist(self, mock_datacenter_module, mock_from_json):
        mock_ov_instance = mock.Mock()

        mock_ov_instance.datacenters.get_by.return_value = []

        mock_ov_instance.datacenters.add.return_value = {"name": "name"}
        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_CHANGE)
        mock_datacenter_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        exit_json_calls = [
            mock.call(changed=False, msg=DATACENTER_NOT_FOUND),
            mock.call(changed=True, msg=DATACENTER_ADDED, ansible_facts=dict(datacenter={"name": "name"}))]
        mock_ansible_instance.exit_json.assert_has_calls(exit_json_calls)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_warning_rename_when_new_name_in_use(self, mock_datacenter_module, mock_from_json):
        fail_msg = "There is already a datacenter with the name 'MyDatacenter1'"

        datacenter_to_update = deepcopy(DICT_DEFAULT_DATACENTER_CHANGED)
        datacenter_to_update['name'] = datacenter_to_update.pop('newName')

        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = [DICT_DEFAULT_DATACENTER]

        mock_from_json.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_CHANGE)
        mock_datacenter_module.return_value = mock_ansible_instance
        mock_ov_instance.datacenters.update.side_effect = Exception(fail_msg)

        DatacenterModule().run()

        mock_ov_instance.datacenters.update.assert_called_once_with(datacenter_to_update)

        mock_ansible_instance.exit_json.assert_called_once_with(changed=False, msg=DATACENTER_NEW_NAME_ALREADY_EXISTS)
        mock_ansible_instance.fail_json.assert_called_once_with(msg=fail_msg)


class DatacenterAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_remove_datacenter(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = [DICT_DEFAULT_DATACENTER]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=DATACENTER_REMOVED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_do_nothing_when_datacenter_not_exist(self, mock_ansible_module,
                                                         mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=DATACENTER_ALREADY_ABSENT
        )


class DatacenterErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_fail_when_create_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = []
        mock_ov_instance.datacenters.add.side_effect = Exception(FAKE_MSG_ERROR)
        mock_ov_instance.racks.get_by.return_value = [{'uri': RACK_URI}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, DatacenterModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_fail_when_switch_type_was_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = []
        mock_ov_instance.datacenters.add.side_effect = Exception(FAKE_MSG_ERROR)
        mock_ov_instance.racks.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, DatacenterModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=RACK_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_fail_when_delete_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = [DICT_DEFAULT_DATACENTER]
        mock_ov_instance.datacenters.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(YAML_DATACENTER_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, DatacenterModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
