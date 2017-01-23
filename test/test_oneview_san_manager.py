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

from oneview_san_manager import SanManagerModule
from oneview_san_manager import SAN_MANAGER_CREATED, SAN_MANAGER_ALREADY_EXIST, SAN_MANAGER_UPDATED
from oneview_san_manager import SAN_MANAGER_DELETED, SAN_MANAGER_ALREADY_ABSENT

from utils import ValidateEtagTestCase, ModuleContructorTestCase, ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SAN_MANAGER_TEMPLATE = dict(
    providerDisplayName='Brocade Network Advisor',
    uri='/rest/fc-sans/device-managers/UUU-AAA-BBB'
)


class SanManagerModuleSpec(unittest.TestCase,
                           ModuleContructorTestCase,
                           ValidateEtagTestCase,
                           ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case

    ValidateEtagTestCase has common tests for the validate_etag attribute.

    ErrorHandlingTestCase has common tests for the module error handling.
    """

    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
                  connectionInfo=None)
    )

    PARAMS_WITH_CHANGES = dict(
        config='config.json',
        state='present',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
                  refreshState='RefreshPending',
                  connectionInfo=None)
    )

    PARAMS_FOR_ABSENT = dict(
        config='config.json',
        state='absent',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
                  connectionInfo=None)
    )

    def setUp(self):
        self.configure_mocks(self, SanManagerModule)
        self.resource = self.mock_ov_client.san_managers
        ErrorHandlingTestCase.configure(self, ansible_params=self.PARAMS_FOR_PRESENT,
                                        method_to_fire=self.resource.get_by_provider_display_name)

    def test_should_add_new_san_manager(self):
        self.resource.get_by_provider_display_name.return_value = None
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_CREATED,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_should_find_provider_uri_to_add(self):
        self.resource.get_by_provider_display_name.return_value = None
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        provider_display_name = DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName']
        self.resource.get_provider_uri.assert_called_once_with(provider_display_name)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAN_MANAGER_ALREADY_EXIST,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.resource.update.return_value = data_merged
        self.mock_ansible_module.params = self.PARAMS_WITH_CHANGES

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_UPDATED,
            ansible_facts=dict(san_manager=data_merged)
        )

    def test_should_remove_san_manager(self):
        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAN_MANAGER_DELETED
        )

    def test_should_do_nothing_when_san_manager_not_exist(self):
        self.resource.get_by_provider_display_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAN_MANAGER_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
