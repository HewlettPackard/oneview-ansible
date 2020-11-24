#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
import mock
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ScopeModule

FAKE_MSG_ERROR = 'Fake message error'

RESOURCE = dict(name='ScopeName', uri='/rest/scopes/id')
RESOURCE_UPDATED = dict(name='ScopeNameRenamed', uri='/rest/scopes/id')
RESOURCE_ASSIGNMENTS = dict(name='ScopeName',
                            addedResourceUris=['/rest/resource/id-1', '/rest/resource/id-4'])

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

PARAMS_WITH_CHANGES_HAVING_RESOURCES_1 = dict(
    config='config.json',
    state='present',
    data=dict(name='ScopeName',
              addedResourceUris=['/rest/resource/id-1', '/rest/resource/id-2'],
              removedResourceUris=['/rest/resource/id-3'])
)

PARAMS_WITH_CHANGES_HAVING_RESOURCES_2 = dict(
    config='config.json',
    state='present',
    data=dict(name='ScopeName',
              addedResourceUris=['/rest/resource/id-1', '/rest/resource/id-2'],
              removedResourceUris=['/rest/resource/id-2'])
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

PARAMS_NO_RESOURCE_ASSIGNMENTS = dict(
    config='config.json',
    state='resource_assignments_updated',
    data=dict(name='ScopeName',
              resourceAssignments=dict(addedResourceUris=None,
                                       removedResourceUris=None))
)


@pytest.mark.resource(TestScopeModule='scopes')
class TestScopeModule(OneViewBaseTest):
    def test_should_create_new_scope_when_not_found(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = PARAMS_FOR_PRESENT
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_CREATED,
            ansible_facts=dict(scope=PARAMS_FOR_PRESENT)
        )

    def test_should_not_update_when_data_is_equals(self):
        response_data = PARAMS_FOR_PRESENT['data']
        self.resource.data = response_data
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ScopeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(scope=response_data)
        )

    def test_should_not_update_when_no_new_add_remove_resources(self):
        self.resource.get_by_name.return_value = self.resource
        current_data = copy.deepcopy(PARAMS_WITH_CHANGES_HAVING_RESOURCES_1['data'])
        self.resource.data = current_data
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES_HAVING_RESOURCES_1

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_UPDATED,
            ansible_facts=dict(scope=current_data)
        )
        
    def test_should_update_when_new_remove_resources(self):
        self.resource.get_by_name.return_value = self.resource
        current_data = copy.deepcopy(PARAMS_WITH_CHANGES_HAVING_RESOURCES_2['data'])
        self.resource.data = current_data
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES_HAVING_RESOURCES_2

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_UPDATED,
            ansible_facts=dict(scope=current_data)
        )

    def test_should_update_when_new_add_resources(self):
        self.resource.get_by_name.return_value = self.resource
        current_data = copy.deepcopy(RESOURCE_ASSIGNMENTS)
        self.resource.data = current_data
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES_HAVING_RESOURCES_1

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_UPDATED,
            ansible_facts=dict(scope=current_data)
        )

    def test_should_update_when_data_has_changes(self):
        data_merged = PARAMS_FOR_PRESENT.copy()
        data_merged['name'] = 'ScopeNameRenamed'

        self.resource.data = PARAMS_FOR_PRESENT
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ScopeModule.MSG_UPDATED,
            ansible_facts=dict(scope=PARAMS_FOR_PRESENT)
        )

    def test_should_remove_scope_when_found(self):
        self.resource.get_by_name.return_value = self.resource
        self.resource.data = PARAMS_FOR_PRESENT
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

    def test_should_fail_resource_assignments_when_scope_not_found(self):
        self.mock_ov_client.api_version = 300
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            failed=True,
            changed=False,
            msg=ScopeModule.MSG_RESOURCE_NOT_FOUND
        )

    def test_should_not_update_resource_assignments_in_api300(self):
        self.mock_ov_client.api_version = 300
        self.resource.get_by_name.return_value = self.resource
        resource_data = PARAMS_NO_RESOURCE_ASSIGNMENTS.copy()
        self.resource.data = resource_data
        self.resource.update_resource_assignments.return_value = self.resource
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_NO_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scope=PARAMS_NO_RESOURCE_ASSIGNMENTS),
            msg=ScopeModule.MSG_RESOURCE_ASSIGNMENTS_NOT_UPDATED
        )

    def test_should_add_and_remove_resource_assignments_in_api300(self):
        self.mock_ov_client.api_version = 300
        self.resource.get_by_name.return_value = self.resource

        resource_data = PARAMS_RESOURCE_ASSIGNMENTS.copy()
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope=PARAMS_RESOURCE_ASSIGNMENTS),
            msg=ScopeModule.MSG_RESOURCE_ASSIGNMENTS_UPDATED
        )

    def test_should_update_name_in_api300(self):
        self.mock_ov_client.api_version = 300
        self.resource.get_by_name.return_value = self.resource

        PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_NAME = dict(
            config='config.json',
            state='resource_assignments_updated',
            data=dict(name='ScopeName',
                      resourceAssignments=dict(name='TestScope'))
        )

        resource_data = PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_NAME.copy()
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_NAME)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope=PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_NAME),
            msg=ScopeModule.MSG_RESOURCE_ASSIGNMENTS_UPDATED
        )

    def test_should_update_description_in_api300(self):
        self.mock_ov_client.api_version = 300
        self.resource.get_by_name.return_value = self.resource

        PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_DESCRIPTION = dict(
            config='config.json',
            state='resource_assignments_updated',
            data=dict(name='ScopeName',
                      resourceAssignments=dict(description='Test'))
        )

        resource_data = PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_DESCRIPTION.copy()
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        self.mock_ansible_module.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_DESCRIPTION)

        ScopeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope=PARAMS_RESOURCE_ASSIGNMENTS_UPDATED_DESCRIPTION),
            msg=ScopeModule.MSG_RESOURCE_ASSIGNMENTS_UPDATED
        )


if __name__ == '__main__':
    pytest.main([__file__])
