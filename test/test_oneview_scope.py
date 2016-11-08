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
import copy
import unittest
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_scope import ScopeModule
from oneview_scope import SCOPE_CREATED, SCOPE_UPDATED, SCOPE_ALREADY_EXIST
from oneview_scope import SCOPE_DELETED, SCOPE_ALREADY_ABSENT
from oneview_scope import SCOPE_RESOURCE_ASSIGNMENTS_UPDATED, SCOPE_NOT_FOUND
from test.utils import create_ansible_mock
from mock import patch

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


class ScopeClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_scope.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        ScopeModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_scope.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        ScopeModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class ScopeModuleSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ov_client_from_json_file = patch.object(OneViewClient, 'from_json_file')
        mock_from_json_file = self.patcher_ov_client_from_json_file.start()

        mock_ov_client = mock.Mock()
        mock_from_json_file.return_value = mock_ov_client

        self.resource = mock_ov_client.scopes

        self.patcher_ansible_module = patch('oneview_scope.AnsibleModule')
        mock_ansible_module = self.patcher_ansible_module.start()

        self.mock_ansible_instance = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_instance

    def tearDown(self):
        self.patcher_ov_client_from_json_file.stop()
        self.patcher_ansible_module.stop()

    def test_should_create_new_scope_when_not_found(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = RESOURCE
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SCOPE_CREATED,
            ansible_facts=dict(scope=RESOURCE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SCOPE_ALREADY_EXIST,
            ansible_facts=dict(scope=RESOURCE)
        )

    def test_should_update_when_data_has_changes(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.update.return_value = RESOURCE_UPDATED
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_WITH_CHANGES)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SCOPE_UPDATED,
            ansible_facts=dict(scope=RESOURCE_UPDATED)
        )

    def test_should_remove_scope_when_found(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_ABSENT)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=SCOPE_DELETED
        )

    def test_should_not_delete_when_scope_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_ABSENT)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=SCOPE_ALREADY_ABSENT
        )

    def test_should_update_resource_assignments(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.update_resource_assignments.return_value = RESOURCE
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(scope=RESOURCE),
            msg=SCOPE_RESOURCE_ASSIGNMENTS_UPDATED
        )

    def test_should_fail_when_scope_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_RESOURCE_ASSIGNMENTS)

        ScopeModule().run()

        self.mock_ansible_instance.fail_json.assert_called_once_with(
            msg=SCOPE_NOT_FOUND
        )

    def test_should_fail_when_create_raises_exception(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.side_effect = Exception(FAKE_MSG_ERROR)
        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_PRESENT)

        self.assertRaises(Exception, ScopeModule().run())

        self.mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_update_raises_exception(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.update.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_WITH_CHANGES)

        self.assertRaises(Exception, ScopeModule().run())

        self.mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by_name.return_value = RESOURCE
        self.resource.delete.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_instance.params = copy.deepcopy(PARAMS_FOR_ABSENT)

        self.assertRaises(Exception, ScopeModule().run())

        self.mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
