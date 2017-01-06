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

from oneview_datacenter import DatacenterModule, DATACENTER_ADDED, DATACENTER_REMOVED, DATACENTER_ALREADY_ABSENT, \
    RACK_NOT_FOUND, DATACENTER_ALREADY_UPDATED, DATACENTER_UPDATED
from test.utils import ModuleContructorTestCase, ValidateEtagTestCase

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


class DatacenterPresentStateSpec(unittest.TestCase, ModuleContructorTestCase, ValidateEtagTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    ValidateEtagTestCase has common tests for the validate_etag attribute.
    """

    def setUp(self):
        self.configure_mocks(self, DatacenterModule)
        self.resource = self.mock_ov_client.datacenters

    def test_should_create_new_datacenter(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = {"name": "name"}
        self.mock_ov_client.racks.get_by.return_value = [{'uri': RACK_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DATACENTER_ADDED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    def test_should_update_the_datacenter(self):
        self.resource.get_by.side_effect = [[DICT_DEFAULT_DATACENTER], []]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_CHANGE)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DATACENTER_UPDATED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        datacenter_replaced = DICT_DEFAULT_DATACENTER.copy()
        del datacenter_replaced['contents'][0]['resourceName']

        self.resource.get_by.return_value = [DICT_DEFAULT_DATACENTER]
        self.mock_ov_client.racks.get_by.return_value = [{'uri': RACK_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DATACENTER_ALREADY_UPDATED,
            ansible_facts=dict(datacenter=DICT_DEFAULT_DATACENTER)
        )

    def test_should_remove_datacenter(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_DATACENTER]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_ABSENT)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=DATACENTER_REMOVED
        )

    def test_should_do_nothing_when_datacenter_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_ABSENT)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=DATACENTER_ALREADY_ABSENT
        )

    def test_should_fail_when_create_raises_exception(self):
        self.resource.get_by.return_value = []
        self.resource.add.side_effect = Exception(FAKE_MSG_ERROR)
        self.mock_ov_client.racks.get_by.return_value = [{'uri': RACK_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        self.assertRaises(Exception, DatacenterModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_switch_type_was_not_found(self):
        self.resource.get_by.return_value = []
        self.resource.add.side_effect = Exception(FAKE_MSG_ERROR)
        self.mock_ov_client.racks.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        self.assertRaises(Exception, DatacenterModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=RACK_NOT_FOUND
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_DATACENTER]
        self.resource.remove.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_ABSENT)

        self.assertRaises(Exception, DatacenterModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
