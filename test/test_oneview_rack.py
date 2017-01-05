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

from oneview_rack import RackModule, RACK_CREATED, RACK_ALREADY_EXIST, RACK_UPDATED, \
    RACK_DELETED, RACK_ALREADY_ABSENT
from utils import ModuleContructorTestCase, ValidateEtagTestCase


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

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='Rename Rack')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_RACK_TEMPLATE['name'])
)


class RackPresentStateSpec(unittest.TestCase, ModuleContructorTestCase, ValidateEtagTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    ValidateEtagTestCase has common tests for the validate_etag attribute.
    """

    def setUp(self):
        self.configure_mocks(self, RackModule)
        self.resource = self.mock_ov_client.racks

    def test_should_create_new_rack(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = DEFAULT_RACK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_CREATED,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RACK_ALREADY_EXIST,
            ansible_facts=dict(rack=DEFAULT_RACK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_RACK_TEMPLATE.copy()

        data_merged['name'] = 'Rename Rack'

        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_UPDATED,
            ansible_facts=dict(rack=data_merged)
        )

    def test_should_fail_when_create_raises_exception(self):
        self.resource.get_by.return_value = []
        self.resource.add.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        self.assertRaises(Exception, RackModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_update_raises_exception(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        self.resource.update.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        self.assertRaises(Exception, RackModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_remove_rack(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RACK_DELETED
        )

    def test_should_do_nothing_when_rack_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RackModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RACK_ALREADY_ABSENT
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by.return_value = [DEFAULT_RACK_TEMPLATE]
        self.resource.remove.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        self.assertRaises(Exception, RackModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
