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

from oneview_network_set import NetworkSetModule
from oneview_network_set import NETWORK_SET_CREATED, NETWORK_SET_UPDATED, NETWORK_SET_DELETED, \
    NETWORK_SET_ALREADY_EXIST, NETWORK_SET_ALREADY_ABSENT, NETWORK_SET_NEW_NAME_INVALID, \
    NETWORK_SET_ENET_NETWORK_NOT_FOUND
from utils import ModuleContructorTestCase, ValidateEtagTestCase, ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'

NETWORK_SET = dict(
    name='OneViewSDK Test Network Set',
    networkUris=['/rest/ethernet-networks/aaa-bbb-ccc']
)

NETWORK_SET_WITH_NEW_NAME = dict(name='OneViewSDK Test Network Set - Renamed')

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=NETWORK_SET['name'],
              newName=NETWORK_SET['name'] + " - Renamed",
              networkUris=['/rest/ethernet-networks/aaa-bbb-ccc', 'Name of a Network'])
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=NETWORK_SET['name'])
)


class NetworkSetModuleSpec(unittest.TestCase,
                           ModuleContructorTestCase,
                           ValidateEtagTestCase,
                           ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    ValidateEtagTestCase has common tests for the validate_etag attribute.
    ErrorHandlingTestCase has common tests for the module error handling.
    """

    def setUp(self):
        self.configure_mocks(self, NetworkSetModule)
        self.resource = self.mock_ov_client.network_sets
        self.ethernet_network_client = self.mock_ov_client.ethernet_networks
        ErrorHandlingTestCase.configure(self, method_to_fire=self.resource.get_by)

    def test_should_create_new_network_set(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = NETWORK_SET

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_CREATED,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [NETWORK_SET]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NETWORK_SET_ALREADY_EXIST,
            ansible_facts=dict(network_set=NETWORK_SET)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = dict(name=NETWORK_SET['name'] + " - Renamed",
                           networkUris=['/rest/ethernet-networks/aaa-bbb-ccc',
                                        '/rest/ethernet-networks/ddd-eee-fff']
                           )

        self.resource.get_by.side_effect = [NETWORK_SET], []
        self.resource.update.return_value = data_merged
        self.ethernet_network_client.get_by.return_value = [{'uri': '/rest/ethernet-networks/ddd-eee-fff'}]

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_UPDATED,
            ansible_facts=dict(network_set=data_merged)
        )

    def test_should_raise_exception_when_new_name_already_used(self):
        self.resource.get_by.side_effect = [NETWORK_SET], [NETWORK_SET_WITH_NEW_NAME]
        self.ethernet_network_client.get_by.return_value = [{'uri': '/rest/ethernet-networks/ddd-eee-fff'}]

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        NetworkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=NETWORK_SET_NEW_NAME_INVALID
        )

    def test_should_raise_exception_when_ethernet_network_not_found(self):
        self.resource.get_by.side_effect = [NETWORK_SET], []
        self.ethernet_network_client.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        NetworkSetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=NETWORK_SET_ENET_NETWORK_NOT_FOUND + "Name of a Network"
        )

    def test_should_remove_network(self):
        self.resource.get_by.return_value = [NETWORK_SET]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=NETWORK_SET_DELETED
        )

    def test_should_do_nothing_when_network_set_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        NetworkSetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NETWORK_SET_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
