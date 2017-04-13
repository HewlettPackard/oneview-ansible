###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import copy
import unittest

from oneview_module_loader import ScopeModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

RESOURCE = dict(name='ScopeName', uri='/rest/scopes/id')
RESOURCE_UPDATED = dict(name='ScopeNameRenamed', uri='/rest/scopes/id')

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name='ScopeName')
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='ScopeName',
              newName='ScopeNameRenamed')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name='ScopeName')
)

PARAMS_RESOURCE_ASSIGNMENTS = dict(
    config='config.json',
    state='resource_assignments_updated',
    data=dict(name='ScopeName',
              resourceAssignments=dict(addedResourceUris=['/rest/resource/id-1', '/rest/resource/id-2'],
                                       removedResourceUris=['/rest/resource/id-3']))
)


class ScopeModuleSpec(unittest.TestCase, OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, ScopeModule)
        self.resource = self.mock_ov_client.scopes

    def test_should_create_new_scope_when_not_found(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = RESOURCE
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_CREATED,
            ansible_facts=dict(scope=RESOURCE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ScopeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(scope=RESOURCE)
        )

    def test_should_update_when_data_has_changes(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.update.return_value = RESOURCE_UPDATED
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_WITH_CHANGES)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_UPDATED,
            ansible_facts=dict(scope=RESOURCE_UPDATED)
        )

    def test_should_remove_scope_when_found(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_FOR_ABSENT)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_DELETED
        )

    def test_should_not_delete_when_scope_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_FOR_ABSENT)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ScopeModule.MSG_ALREADY_ABSENT
        )

    def test_should_update_resource_assignments(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.update_resource_assignments.return_value = RESOURCE
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope=RESOURCE),
            msg=ScopeModule.MSG_RESOURCE_ASSIGNMENTS_UPDATED
        )

    def test_should_fail_when_scope_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ScopeModule.MSG_RESOURCE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
