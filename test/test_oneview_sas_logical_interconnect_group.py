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

from oneview_sas_logical_interconnect_group import (SasLogicalInterconnectGroupModule,
                                                    SAS_LIG_CREATED,
                                                    SAS_LIG_ALREADY_EXIST,
                                                    SAS_LIG_UPDATED,
                                                    SAS_LIG_DELETED,
                                                    SAS_LIG_ALREADY_ABSENT)
from test.utils import ModuleContructorTestCase, ValidateEtagTestCase, ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_SAS_LIG_NAME = 'Test SAS Logical Interconnect Group'
RENAMED_SAS_LIG = 'Renamed SAS Logical Interconnect Group'

DEFAULT_SAS_LIG_TEMPLATE = dict(
    type='sas-logical-interconnect-group',
    name=DEFAULT_SAS_LIG_NAME,
    state='Active',
    enclosureType='SY12000',
    interconnectBaySet="1"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              newName=RENAMED_SAS_LIG)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              interconnectBaySet='2')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)


class SasLogicalInterconnectGroupSpec(unittest.TestCase,
                                      ModuleContructorTestCase,
                                      ValidateEtagTestCase,
                                      ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function

    ValidateEtagTestCase has common tests for the validate_etag attribute, also provides the mocks used in this test
    case.

    ErrorHandlingTestCase has common tests for the module error handling.
    """

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectGroupModule)
        self.resource = self.mock_ov_client.sas_logical_interconnect_groups
        ErrorHandlingTestCase.configure(self, method_to_fire=self.resource.get_by)

    def test_should_create(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_CREATED,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_create_with_newName_when_resource_not_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        self.mock_ansible_module.params = params_to_rename

        SasLogicalInterconnectGroupModule().run()

        self.resource.create.assert_called_once_with(PARAMS_TO_RENAME['data'])

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_LIG_ALREADY_EXIST,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['description'] = 'New description'

        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_UPDATED,
            ansible_facts=dict(sas_logical_interconnect_group=data_merged)
        )

    def test_rename_when_resource_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = params_to_rename

        SasLogicalInterconnectGroupModule().run()

        self.resource.update.assert_called_once_with(data_merged)

    def test_should_remove(self):
        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LIG_DELETED
        )

    def test_should_do_nothing_when_resource_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_LIG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
