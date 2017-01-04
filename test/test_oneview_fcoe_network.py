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

from oneview_fcoe_network import FcoeNetworkModule, FCOE_NETWORK_CREATED, FCOE_NETWORK_ALREADY_EXIST, \
    FCOE_NETWORK_UPDATED, FCOE_NETWORK_DELETED, FCOE_NETWORK_ALREADY_ABSENT
from test.utils import ModuleContructorTestCase, ValidateEtagTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FCOE_NETWORK_TEMPLATE = dict(
    name='New FCoE Network 2',
    vlanId="201",
    connectionTemplateUri=None
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'],
              fabricType='DirectAttach',
              newName='New Name')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'])
)


class FcoeNetworkSpec(unittest.TestCase, ModuleContructorTestCase, ValidateEtagTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    ValidateEtagTestCase has common tests for the validate_etag attribute.
    """

    def setUp(self):
        self.configure_mocks(self, FcoeNetworkModule)
        self.resource = self.mock_ov_client.fcoe_networks

    def test_should_create_new_fcoe_network(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_FCOE_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FCOE_NETWORK_CREATED,
            ansible_facts=dict(fcoe_network=DEFAULT_FCOE_NETWORK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_FCOE_NETWORK_TEMPLATE]
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT.copy()

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FCOE_NETWORK_ALREADY_EXIST,
            ansible_facts=dict(fcoe_network=DEFAULT_FCOE_NETWORK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_FCOE_NETWORK_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by.return_value = [DEFAULT_FCOE_NETWORK_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FCOE_NETWORK_UPDATED,
            ansible_facts=dict(fcoe_network=data_merged)
        )

    def test_should_remove_fcoe_network(self):
        self.resource.get_by.return_value = [DEFAULT_FCOE_NETWORK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FCOE_NETWORK_DELETED,
            ansible_facts={}
        )

    def test_should_do_nothing_when_fcoe_network_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FCOE_NETWORK_ALREADY_ABSENT,
            ansible_facts={}
        )

    def test_should_fail_when_create_raises_exception(self):
        self.resource.get_by.return_value = []
        self.resource.create.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_update_raises_exception(self):
        self.resource.get_by.return_value = [DEFAULT_FCOE_NETWORK_TEMPLATE]
        self.resource.update.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcoeNetworkModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by.return_value = [DEFAULT_FCOE_NETWORK_TEMPLATE]
        self.resource.delete.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
