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
from oneview_datacenter import DatacenterModule, DATACENTER_ADDED, DATACENTER_REMOVED, DATACENTER_ALREADY_ABSENT, \
    RACK_NOT_FOUND, DATACENTER_ALREADY_UPDATED, DATACENTER_UPDATED
from test.utils import create_ansible_mock
from test.utils import create_ansible_mock_yaml

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


class DatacenterClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class DatacenterPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_create_new_datacenter(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = []
        mock_ov_instance.datacenters.add.return_value = {"name": "name"}
        mock_ov_instance.racks.get_by.return_value = [{'uri': RACK_URI}]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER_CHANGE)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER)
        mock_ansible_module.return_value = mock_ansible_instance

        DatacenterModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=DATACENTER_ALREADY_UPDATED,
            ansible_facts=dict(datacenter=DICT_DEFAULT_DATACENTER)
        )


class DatacenterAbsentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_datacenter.AnsibleModule')
    def test_should_remove_datacenter(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.datacenters.get_by.return_value = [DICT_DEFAULT_DATACENTER]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER_ABSENT)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER_ABSENT)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER)
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
        mock_ansible_instance = create_ansible_mock_yaml(YAML_DATACENTER_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, DatacenterModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
