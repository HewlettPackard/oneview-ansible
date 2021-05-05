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

import mock
import logging
import pytest
import sys

from module_utils import oneview

ONEVIEW_MODULE_UTILS_PATH = 'module_utils.oneview'

sys.modules['ansible.module_utils.oneview'] = oneview

from copy import deepcopy
from module_utils.oneview import (OneViewModuleBase,
                                  OneViewModule,
                                  OneViewClient,
                                  OneViewModuleException,
                                  OneViewModuleValueError,
                                  OneViewModuleResourceNotFound,
                                  SPKeys,
                                  ServerProfileMerger,
                                  ServerProfileReplaceNamesByUris,
                                  sort_by_uplink_set_location,
                                  _sort_by_keys,
                                  _str_sorted,
                                  merge_list_by_key,
                                  transform_list_to_dict,
                                  compare,
                                  compare_lig,
                                  get_logger)

MSG_GENERIC_ERROR = 'Generic error message'
MSG_GENERIC = "Generic message"


class StubResource(OneViewModule):
    """Stub class to test the resource object"""


class TestOneViewModule():
    """
    OneViewModuleSpec provides the mocks used in this test case.
    """
    mock_ov_client_from_json_file = None
    mock_ov_client_from_env_vars = None
    mock_ansible_module = None
    mock_ansible_module_init = None
    mock_ov_client = None

    MODULE_EXECUTE_RETURN_VALUE = dict(
        changed=True,
        msg=MSG_GENERIC,
        ansible_facts={'ansible_facts': None}
    )

    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data={'name': 'resource name'}
    )

    PARAMS_FOR_PRESENT_WITH_URI = dict(
        config='config.json',
        state='present',
        data={'uri': '/rest/resource/id'}
    )

    RESOURCE_COMMON = {'uri': '/rest/resource/id',
                       'name': 'Resource Name'}

    CHECK_RESOURCE_COMMON = {'name': 'Resource Name'}

    EXPECTED_ARG_SPEC = {'api_version': {'type': u'int'},
                         'config': {'type': 'path'},
                         'hostname': {'type': 'str'},
                         'image_streamer_hostname': {'type': 'str'},
                         'password': {'type': 'str', 'no_log': True},
                         'username': {'type': 'str'},
                         'auth_login_domain': {'type': 'str'},
                         'validate_etag': {'type': 'bool', 'default': True}}

    @pytest.fixture(autouse=True)
    def setUp(self):
        # Define OneView Client Mock (FILE)
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client_from_json_file = patcher_json_file.start()

        # Define OneView Client Mock
        self.mock_ov_client = self.mock_ov_client_from_json_file.return_value

        # Define OneView Client Mock (ENV)
        patcher_env = mock.patch.object(OneViewClient, 'from_environment_variables')
        self.mock_ov_client_from_env_vars = patcher_env.start()

        # Define Ansible Module Mock
        patcher_ansible = mock.patch(OneViewModule.__module__ + '.AnsibleModule')
        self.mock_ansible_module_init = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        self.mock_ansible_module_init.return_value = self.mock_ansible_module

        yield
        patcher_json_file.stop
        patcher_env.stop
        patcher_ansible.stop

    def test_should_call_ov_exception_with_a_data(self):

        error = {'message': 'Failure with data'}

        OneViewModuleException(error)

    def test_should_call_exit_json_properly(self):

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.return_value = self.MODULE_EXECUTE_RETURN_VALUE.copy()

        base_mod = OneViewModule()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_call_exit_json_adding_changed_false_when_undefined(self):

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.return_value = dict(
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

        base_mod = OneViewModule()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_load_config_from_file(self):

        self.mock_ansible_module.params = {'config': 'config.json'}

        OneViewModule()

        self.mock_ov_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ov_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):

        self.mock_ansible_module.params = {'config': None}

        OneViewModule()

        self.mock_ov_client_from_env_vars.assert_called_once_with()
        self.mock_ov_client_from_json_file.not_been_called()

    def test_should_load_config_from_parameters(self):

        params = {'hostname': '172.16.1.1', 'username': 'admin', 'password': 'mypass', 'api_version': 500,
                  'image_streamer_hostname': '172.16.1.2'}
        params_for_expect = {'image_streamer_ip': '172.16.1.2', 'api_version': 500, 'ip': '172.16.1.1',
                             'credentials': {'userName': 'admin', 'password': 'mypass', 'authLoginDomain': ''}}
        self.mock_ansible_module.params = params

        with mock.patch('module_utils.oneview.OneViewClient', first='one', second='two') as mock_ov_client_from_credentials:
            OneViewModule()

        self.mock_ov_client_from_env_vars.not_been_called()
        self.mock_ov_client_from_json_file.not_been_called()
        mock_ov_client_from_credentials.assert_called_once_with(params_for_expect)

    def test_should_load_config_from_parameters_with_domain(self):

        params = {'hostname': '172.16.1.1', 'username': 'admin', 'password': 'mypass', 'api_version': 500,
                  'image_streamer_hostname': '172.16.1.2', 'auth_login_domain': 'ADDomain'}
        params_for_expect = {'image_streamer_ip': '172.16.1.2', 'api_version': 500, 'ip': '172.16.1.1',
                             'credentials': {'userName': 'admin', 'password': 'mypass', 'authLoginDomain': 'ADDomain'}}
        self.mock_ansible_module.params = params

        with mock.patch('module_utils.oneview.OneViewClient', first='one', second='two') as mock_ov_client_from_credentials:
            OneViewModule()

        self.mock_ov_client_from_env_vars.not_been_called()
        self.mock_ov_client_from_json_file.not_been_called()
        mock_ov_client_from_credentials.assert_called_once_with(params_for_expect)

    def test_should_call_fail_json_when_oneview_sdk_not_installed(self):
        self.mock_ansible_module.params = {'config': 'config.json'}

        with mock.patch(OneViewModule.__module__ + ".HAS_HPE_ONEVIEW", False):
            OneViewModule()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg='HPE OneView Python SDK is required for this module.')

    def test_should_validate_etag_when_set_as_true(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = True

        OneViewModule(validate_etag_support=True).run()
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=self.EXPECTED_ARG_SPEC,
                                                              supports_check_mode=True)
        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.not_been_called()

    def test_should_not_validate_etag_when_set_as_false(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = False

        OneViewModule(validate_etag_support=True).run()
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=self.EXPECTED_ARG_SPEC,
                                                              supports_check_mode=True)
        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.assert_called_once_with()

    def test_should_not_validate_etag_when_not_supported(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = False

        OneViewModule(validate_etag_support=False).run()

        expected_arg_spec = deepcopy(self.EXPECTED_ARG_SPEC)
        expected_arg_spec.pop('validate_etag')
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=expected_arg_spec,
                                                              supports_check_mode=True)

        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.not_been_called()

    def test_additional_argument_spec_construction(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        OneViewModule(validate_etag_support=False, additional_arg_spec={'options': 'list'})

        expected_arg_spec = deepcopy(self.EXPECTED_ARG_SPEC)
        expected_arg_spec.pop('validate_etag')
        expected_arg_spec['options'] = 'list'

        self.mock_ansible_module_init.assert_called_once_with(argument_spec=expected_arg_spec,
                                                              supports_check_mode=True)

    def test_should_call_fail_json_when_oneview_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = OneViewModuleException(MSG_GENERIC_ERROR)

        base_mod = OneViewModule(validate_etag_support=True)
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=MSG_GENERIC_ERROR)

    def test_should_not_handle_value_error_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = ValueError(MSG_GENERIC_ERROR)

        try:
            base_mod = OneViewModule(validate_etag_support=True)
            base_mod.execute_module = mock_run
            base_mod.run()
        except ValueError as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected ValueError was not raised')

    def test_should_not_handle_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = Exception(MSG_GENERIC_ERROR)

        try:
            base_mod = OneViewModule(validate_etag_support=True)
            base_mod.execute_module = mock_run
            base_mod.run()
        except Exception as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected Exception was not raised')

    def test_resource_present_should_create(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()

        resource_obj = StubResource()
        resource_obj.data = self.RESOURCE_COMMON.copy()
        ov_base.resource_client.create.return_value = resource_obj
        ov_base.data = {'name': 'Resource Name'}

        facts = ov_base.resource_present(fact_name="resource")

        expected = self.RESOURCE_COMMON.copy()

        ov_base.resource_client.create.assert_called_once_with({'name': 'Resource Name'})

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_CREATED,
                             ansible_facts=dict(resource=expected))

    def test_to_check_resource_present_should_create(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()

        resource_obj = StubResource()
        resource_obj.data = self.CHECK_RESOURCE_COMMON.copy()
        ov_base.resource_client.create.return_value = resource_obj
        ov_base.data = {'name': 'Resource Name'}

        facts = ov_base.check_resource_present(fact_name="resource")

        expected = self.CHECK_RESOURCE_COMMON.copy()

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_CREATED,
                             ansible_facts=dict(resource=expected))

    def test_resource_present_should_not_update_when_data_is_equals(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()

        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        facts = ov_base.resource_present(fact_name="resource")
        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_to_check_resource_present_should_not_update_when_data_is_equals(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()

        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        facts = ov_base.check_resource_present(fact_name="resource")
        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_resource_present_should_not_update_when_data_is_equals_with_resource_uri(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT_WITH_URI

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        data = self.RESOURCE_COMMON.copy()
        del data["name"]
        ov_base.data = data

        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        facts = ov_base.resource_present(fact_name="resource")
        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_to_check_resource_present_should_not_update_when_data_is_equals_with_resource_uri(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT_WITH_URI

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        data = self.RESOURCE_COMMON.copy()

        ov_base.data = data

        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        facts = ov_base.check_resource_present(fact_name="resource")
        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_resource_present_should_update_when_data_has_modified_attributes(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        resource_obj = StubResource()
        updated_value = self.RESOURCE_COMMON.copy()
        updated_value['name'] = 'Resource Name New'
        resource_obj.data = updated_value

        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        ov_base.data = {'newName': 'Resource Name New'}
        facts = ov_base.resource_present('resource')

        expected = self.RESOURCE_COMMON.copy()
        expected['name'] = 'Resource Name New'

        ov_base.current_resource.update.assert_called_once_with(expected)

        assert dict(changed=facts['changed'], msg=facts['msg']) == dict(changed=True,
                                                                        msg=OneViewModule.MSG_UPDATED)

    def test_to_check_resource_present_should_update_when_data_has_modified_attributes(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        resource_obj = StubResource()
        updated_value = self.RESOURCE_COMMON.copy()
        updated_value['name'] = 'Resource Name New'
        resource_obj.data = updated_value

        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        ov_base.current_resource.data = self.RESOURCE_COMMON.copy()

        ov_base.data = {'newName': 'Resource Name New'}
        facts = ov_base.check_resource_present('resource')

        expected = self.RESOURCE_COMMON.copy()
        expected['name'] = 'Resource Name New'

        assert dict(changed=facts['changed'], msg=facts['msg']) == dict(changed=True,
                                                                        msg=OneViewModule.MSG_UPDATED)

    def test_resource_absent_should_remove(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)

        facts = ov_base.resource_absent()
        ov_base.current_resource.delete.assert_called_once_with()

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_DELETED)

    def test_to_check_resource_absent_should_remove(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)

        facts = ov_base.check_resource_absent()

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_DELETED)

    def test_resource_absent_should_do_nothing_when_not_exist(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = None
        ov_base.set_resource_object(ov_base.resource_client)

        facts = ov_base.resource_absent()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_ABSENT)

    def test_to_check_resource_absent_should_do_nothing_when_not_exist(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = None
        ov_base.set_resource_object(ov_base.resource_client)

        facts = ov_base.check_resource_absent()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_ABSENT)

    def scope_update_helper(self, before_value=None, action_value=None, expected_value=None):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        resource_obj = StubResource()
        resource_obj.data = {'return': 'value'}
        ov_base.current_resource.patch.return_value = resource_obj
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = before_value

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModule.MSG_ALREADY_PRESENT),
                                            'resource',
                                            action_value)

        ov_base.current_resource.patch.assert_called_once_with(operation='replace',
                                                               path='/scopeUris',
                                                               value=expected_value)

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_UPDATED,
                             ansible_facts=dict(resource={'return': 'value'}))

    def check_scope_update_helper(self, before_value=None, action_value=None, expected_value=None):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by_name.return_value = mock.Mock()
        ov_base.set_resource_object(ov_base.resource_client)
        resource_obj = StubResource()
        resource_obj.data = {'return': 'value'}
        ov_base.current_resource.patch.return_value = resource_obj
        ov_base.data = self.CHECK_RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = before_value

        facts = ov_base.check_resource_scopes_set(dict(changed=False,
                                                       ansible_facts=dict(resource=ov_base.data),
                                                       msg=OneViewModule.MSG_ALREADY_PRESENT),
                                                  'resource',
                                                  action_value)

        assert facts == dict(changed=True,
                             msg=OneViewModule.MSG_UPDATED,
                             ansible_facts=dict(resource=ov_base.data))

    def test_update_scopes_when_not_defined_before(self):
        self.scope_update_helper(before_value=None, action_value=['test'], expected_value=['test'])

    def test_to_check_update_scopes_when_not_defined_before(self):
        self.check_scope_update_helper(before_value=None, action_value=['test'], expected_value=['test'])

    def test_update_scopes_when_empty_before(self):
        self.scope_update_helper(before_value=[], action_value=['test'], expected_value=['test'])

    def test_to_check_update_scopes_when_empty_before(self):
        self.check_scope_update_helper(before_value=[], action_value=['test'], expected_value=['test'])

    def test_update_scopes_with_empty_list(self):
        self.scope_update_helper(before_value=['test1', 'test2'], action_value=[], expected_value=[])

    def test_update_scopes_with_none(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()
        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()

        self.scope_update_helper(before_value=['test1', 'test2'], action_value=None, expected_value=[])

    def test_should_do_nothing_when_scopes_are_the_same(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = ['test']

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModule.MSG_ALREADY_PRESENT),
                                            'resource',
                                            ['test'])

        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_to_check_should_do_nothing_when_scopes_are_the_same(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = ['test']

        facts = ov_base.check_resource_scopes_set(dict(changed=False,
                                                       ansible_facts=dict(resource=ov_base.data),
                                                       msg=OneViewModule.MSG_ALREADY_PRESENT),
                                                  'resource',
                                                  ['test'])

        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_should_do_nothing_when_scopes_empty_and_none_wanted(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = []

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModule.MSG_ALREADY_PRESENT),
                                            'resource',
                                            None)
        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_to_check_should_do_nothing_when_scopes_empty_and_none_wanted(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = []

        facts = ov_base.check_resource_scopes_set(dict(changed=False,
                                                       ansible_facts=dict(resource=ov_base.data),
                                                       msg=OneViewModule.MSG_ALREADY_PRESENT),
                                                  'resource',
                                                  None)
        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_get_by_name_when_resource_exists(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by.return_value = [{'resource': 1}]

        res = ov_base.get_by_name('name')

        ov_base.resource_client.get_by.assert_called_once_with('name', 'name')

        assert res == {'resource': 1}

    def test_get_by_name_when_resource_not_found(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModule()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by.return_value = []

        res = ov_base.get_by_name('name')

        ov_base.resource_client.get_by.assert_called_once_with('name', 'name')

        assert res is None


class TestOneViewModuleBase():
    """
    OneViewModuleBaseSpec provides the mocks used in this test case.
    """
    mock_ov_client_from_json_file = None
    mock_ov_client_from_env_vars = None
    mock_ansible_module = None
    mock_ansible_module_init = None
    mock_ov_client = None

    MODULE_EXECUTE_RETURN_VALUE = dict(
        changed=True,
        msg=MSG_GENERIC,
        ansible_facts={'ansible_facts': None}
    )

    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data={'name': 'resource name'}
    )

    RESOURCE_COMMON = {'uri': '/rest/resource/id',
                       'name': 'Resource Name'
                       }

    EXPECTED_ARG_SPEC = {'api_version': {'type': u'int'},
                         'config': {'type': 'path'},
                         'hostname': {'type': 'str'},
                         'image_streamer_hostname': {'type': 'str'},
                         'password': {'type': 'str', 'no_log': True},
                         'username': {'type': 'str'},
                         'auth_login_domain': {'type': 'str'},
                         'validate_etag': {'type': 'bool', 'default': True}}

    @pytest.fixture(autouse=True)
    def setUp(self):
        # Define OneView Client Mock (FILE)
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client_from_json_file = patcher_json_file.start()

        # Define OneView Client Mock
        self.mock_ov_client = self.mock_ov_client_from_json_file.return_value

        # Define OneView Client Mock (ENV)
        patcher_env = mock.patch.object(OneViewClient, 'from_environment_variables')
        self.mock_ov_client_from_env_vars = patcher_env.start()

        # Define Ansible Module Mock
        patcher_ansible = mock.patch(OneViewModuleBase.__module__ + '.AnsibleModule')
        self.mock_ansible_module_init = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        self.mock_ansible_module_init.return_value = self.mock_ansible_module

        yield
        patcher_json_file.stop
        patcher_env.stop
        patcher_ansible.stop

    def test_should_call_ov_exception_with_a_data(self):

        error = {'message': 'Failure with data'}

        OneViewModuleException(error)

    def test_should_call_exit_json_properly(self):

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.return_value = self.MODULE_EXECUTE_RETURN_VALUE.copy()

        base_mod = OneViewModuleBase()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_call_exit_json_adding_changed_false_when_undefined(self):

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.return_value = dict(
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

        base_mod = OneViewModuleBase()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_load_config_from_file(self):

        self.mock_ansible_module.params = {'config': 'config.json'}

        OneViewModuleBase()

        self.mock_ov_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ov_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):

        self.mock_ansible_module.params = {'config': None}

        OneViewModuleBase()

        self.mock_ov_client_from_env_vars.assert_called_once_with()
        self.mock_ov_client_from_json_file.not_been_called()

    def test_should_load_config_from_parameters(self):

        params = {'hostname': '172.16.1.1', 'username': 'admin', 'password': 'mypass', 'api_version': 500,
                  'image_streamer_hostname': '172.16.1.2'}
        params_for_expect = {'image_streamer_ip': '172.16.1.2', 'api_version': 500, 'ip': '172.16.1.1',
                             'credentials': {'userName': 'admin', 'password': 'mypass', 'authLoginDomain': ''}}
        self.mock_ansible_module.params = params

        with mock.patch('module_utils.oneview.OneViewClient', first='one', second='two') as mock_ov_client_from_credentials:
            OneViewModuleBase()

        self.mock_ov_client_from_env_vars.not_been_called()
        self.mock_ov_client_from_json_file.not_been_called()
        mock_ov_client_from_credentials.assert_called_once_with(params_for_expect)

    def test_should_load_config_from_parameters_with_domain(self):

        params = {'hostname': '172.16.1.1', 'username': 'admin', 'password': 'mypass', 'api_version': 500,
                  'image_streamer_hostname': '172.16.1.2', 'auth_login_domain': 'ADDomain'}
        params_for_expect = {'image_streamer_ip': '172.16.1.2', 'api_version': 500, 'ip': '172.16.1.1',
                             'credentials': {'userName': 'admin', 'password': 'mypass', 'authLoginDomain': 'ADDomain'}}
        self.mock_ansible_module.params = params

        with mock.patch('module_utils.oneview.OneViewClient', first='one', second='two') as mock_ov_client_from_credentials:
            OneViewModuleBase()

        self.mock_ov_client_from_env_vars.not_been_called()
        self.mock_ov_client_from_json_file.not_been_called()
        mock_ov_client_from_credentials.assert_called_once_with(params_for_expect)

    def test_should_call_fail_json_when_oneview_sdk_not_installed(self):
        self.mock_ansible_module.params = {'config': 'config.json'}

        with mock.patch(OneViewModuleBase.__module__ + ".HAS_HPE_ONEVIEW", False):
            OneViewModuleBase()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg='HPE OneView Python SDK is required for this module.')

    def test_should_validate_etag_when_set_as_true(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = True

        OneViewModuleBase(validate_etag_support=True).run()
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=self.EXPECTED_ARG_SPEC,
                                                              supports_check_mode=False)
        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.not_been_called()

    def test_should_not_validate_etag_when_set_as_false(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = False

        OneViewModuleBase(validate_etag_support=True).run()
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=self.EXPECTED_ARG_SPEC,
                                                              supports_check_mode=False)
        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.assert_called_once_with()

    def test_should_not_validate_etag_when_not_supported(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = False

        OneViewModuleBase(validate_etag_support=False).run()

        expected_arg_spec = deepcopy(self.EXPECTED_ARG_SPEC)
        expected_arg_spec.pop('validate_etag')
        self.mock_ansible_module_init.assert_called_once_with(argument_spec=expected_arg_spec,
                                                              supports_check_mode=False)

        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.not_been_called()

    def test_additional_argument_spec_construction(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        OneViewModuleBase(validate_etag_support=False, additional_arg_spec={'options': 'list'})

        expected_arg_spec = deepcopy(self.EXPECTED_ARG_SPEC)
        expected_arg_spec.pop('validate_etag')
        expected_arg_spec['options'] = 'list'

        self.mock_ansible_module_init.assert_called_once_with(argument_spec=expected_arg_spec,
                                                              supports_check_mode=False)

    def test_should_call_fail_json_when_oneview_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = OneViewModuleException(MSG_GENERIC_ERROR)

        base_mod = OneViewModuleBase(validate_etag_support=True)
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=MSG_GENERIC_ERROR)

    def test_should_not_handle_value_error_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = ValueError(MSG_GENERIC_ERROR)

        try:
            base_mod = OneViewModuleBase(validate_etag_support=True)
            base_mod.execute_module = mock_run
            base_mod.run()
        except ValueError as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected ValueError was not raised')

    def test_should_not_handle_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = Exception(MSG_GENERIC_ERROR)

        try:
            base_mod = OneViewModuleBase(validate_etag_support=True)
            base_mod.execute_module = mock_run
            base_mod.run()
        except Exception as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected Exception was not raised')

    def test_resource_present_should_create(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.create.return_value = self.RESOURCE_COMMON
        ov_base.data = {'name': 'Resource Name'}

        facts = ov_base.resource_present(None, fact_name="resource")

        expected = self.RESOURCE_COMMON.copy()

        ov_base.resource_client.create.assert_called_once_with({'name': 'Resource Name'})

        assert facts == dict(changed=True,
                             msg=OneViewModuleBase.MSG_CREATED,
                             ansible_facts=dict(resource=expected))

    def test_resource_present_should_not_update_when_data_is_equals(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()

        facts = ov_base.resource_present(self.RESOURCE_COMMON.copy(), fact_name="resource")

        assert facts == dict(changed=False,
                             msg=OneViewModuleBase.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_resource_present_should_update_when_data_has_modified_attributes(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.update.return_value = {'return': 'value'}
        ov_base.data = {'newName': 'Resource Name New'}

        facts = ov_base.resource_present(self.RESOURCE_COMMON, 'resource')

        expected = self.RESOURCE_COMMON.copy()
        expected['name'] = 'Resource Name New'

        ov_base.resource_client.update.assert_called_once_with(expected)

        assert facts == dict(changed=True,
                             msg=OneViewModuleBase.MSG_UPDATED,
                             ansible_facts=dict(resource={'return': 'value'}))

    def test_resource_absent_should_remove(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()

        facts = ov_base.resource_absent(self.RESOURCE_COMMON.copy())
        ov_base.resource_client.delete.assert_called_once_with(self.RESOURCE_COMMON.copy())

        assert facts == dict(changed=True,
                             msg=OneViewModuleBase.MSG_DELETED)

    def test_resource_absent_should_do_nothing_when_not_exist(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()

        facts = ov_base.resource_absent(None)
        ov_base.resource_client.delete.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModuleBase.MSG_ALREADY_ABSENT)

    def scope_update_helper(self, before_value=None, action_value=None, expected_value=None):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.patch.return_value = {'return': 'value'}
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = before_value

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModuleBase.MSG_ALREADY_PRESENT),
                                            'resource',
                                            action_value)

        ov_base.resource_client.patch.assert_called_once_with(ov_base.data['uri'],
                                                              operation='replace',
                                                              path='/scopeUris',
                                                              value=expected_value)

        assert facts == dict(changed=True,
                             msg=OneViewModuleBase.MSG_UPDATED,
                             ansible_facts=dict(resource={'return': 'value'}))

    def test_update_scopes_when_not_defined_before(self):
        self.scope_update_helper(before_value=None, action_value=['test'], expected_value=['test'])

    def test_update_scopes_when_empty_before(self):
        self.scope_update_helper(before_value=[], action_value=['test'], expected_value=['test'])

    def test_update_scopes_with_empty_list(self):
        self.scope_update_helper(before_value=['test1', 'test2'], action_value=[], expected_value=[])

    def test_update_scopes_with_none(self):
        self.scope_update_helper(before_value=['test1', 'test2'], action_value=None, expected_value=[])

    def test_should_do_nothing_when_scopes_are_the_same(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = ['test']

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModuleBase.MSG_ALREADY_PRESENT),
                                            'resource',
                                            ['test'])

        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModuleBase.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_should_do_nothing_when_scopes_empty_and_none_wanted(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT.copy()

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.data = self.RESOURCE_COMMON.copy()
        ov_base.data['scopeUris'] = []

        facts = ov_base.resource_scopes_set(dict(changed=False,
                                                 ansible_facts=dict(resource=ov_base.data),
                                                 msg=OneViewModuleBase.MSG_ALREADY_PRESENT),
                                            'resource',
                                            None)

        ov_base.resource_client.patch.assert_not_called()

        assert facts == dict(changed=False,
                             msg=OneViewModuleBase.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=ov_base.data))

    def test_get_by_name_when_resource_exists(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by.return_value = [{'resource': 1}]

        res = ov_base.get_by_name('name')

        ov_base.resource_client.get_by.assert_called_once_with('name', 'name')

        assert res == {'resource': 1}

    def test_get_by_name_when_resource_not_found(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ov_base = OneViewModuleBase()
        ov_base.resource_client = mock.Mock()
        ov_base.resource_client.get_by.return_value = []

        res = ov_base.get_by_name('name')

        ov_base.resource_client.get_by.assert_called_once_with('name', 'name')

        assert res is None

    def test_transform_list_to_dict(self):
        list_ = ['one', 'two', {'tree': 3}, 'four', 5]

        dict_transformed = transform_list_to_dict(list_=list_)

        assert dict_transformed == {'5': True,
                                    'four': True,
                                    'one': True,
                                    'tree': 3,
                                    'two': True}

    def test_transform_list_to_dict_with_none(self):

        dict_transformed = transform_list_to_dict(None)

        assert dict_transformed == {}

    DICT_ORIGINAL = {u'status': u'OK', u'category': u'fcoe-networks',
                     u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                     u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                     u'state': u'Active',
                     u'vlanId': 201,
                     u'modified': u'2016-06-13T20:39:15.993Z',
                     u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                     u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                     u'connectionTemplateUri': u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                     u'type': u'fcoe-network',
                     u"sub": {
                         "ssub": "ssub",
                         'fs_item': 1,
                         'level3': {
                             "lvl3_t1": "lvl3_t1"
                         },
                         "list": [1, 2, "3"]
                     },
                     u'name': u'Test FCoE Network'}

    DICT_EQUAL_ORIGINAL = {u'status': u'OK', u'category': u'fcoe-networks',
                           u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                           u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                           u'vlanId': '201',
                           "sub": {
                               "ssub": "ssub",
                               'fs_item': "1",
                               'level3': {
                                   "lvl3_t1": u"lvl3_t1"
                               },
                               "list": [1, '3', 2]
                           },
                           u'modified': u'2016-06-13T20:39:15.993Z',
                           u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                           u'state': u'Active',
                           u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                           u'connectionTemplateUri': u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                           u'type': u'fcoe-network',
                           u'name': 'Test FCoE Network'}

    DICT_DIF_ORIGINAL_LV3 = {u'status': u'OK', u'category': u'fcoe-networks',
                             u'description': None, u'created': u'2016-06-13T20:39:15.991Z',
                             u'uri': u'/rest/fcoe-networks/36c56106-3b14-4f0d-8df9-627700b8e01b',
                             u'vlanId': '201',
                             "sub": {
                                 "ssub": "ssub",
                                 'fs_item': "1",
                                 'level3': {
                                     "lvl3_t1": u"lvl3_t1x"
                                 },
                                 "list": [1, 2, 3]
                             },
                             u'modified': u'2016-06-13T20:39:15.993Z',
                             u'fabricUri': u'/rest/fabrics/a3cff65e-6d95-4d4d-9047-3548b6aca902',
                             u'state': u'Active',
                             u'eTag': u'7275bfe5-2e41-426a-844a-9eb00ac8be41', u'managedSanUri': None,
                             u'connectionTemplateUri':
                                 u'/rest/connection-templates/0799d26c-68db-4b4c-b007-d31cf9d60a2f',
                             u'type': u'fcoe-network',
                             u'name': 'Test FCoE Network'}

    DICT_EMPTY_NONE1 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                },
                {
                    "interconnectBay": 2,
                },
            ]
    }

    DICT_EMPTY_NONE2 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                    'logicalInterconnectGroupUri': None
                },
                {
                    "interconnectBay": 2,
                    'logicalInterconnectGroupUri': None
                },
            ]
    }

    DICT_EMPTY_NONE3 = {
        "name": "Enclosure Group 1",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                    'logicalInterconnectGroupUri': ''
                },
                {
                    "interconnectBay": 2,
                    'logicalInterconnectGroupUri': None
                },
            ]
    }

    DICT_UPLINK_SET1 = {
        "name": "UplinkSet",
        "uplinkSets": 
            [
                {
                    "logicalPortConfigInfos": 
                        [
                            {
                                "desiredSpeed": "Auto",
                                "logicalLocation": 
                                    {
                                        "locationEntries": [
                                            {
                                                "relativeValue": 1,
                                                "type": "Bay"
                                            },
                                            {
                                                "relativeValue": 21,
                                                "type": "Port"
                                            },
                                            {
                                                "relativeValue": 1,
                                                "type": "Enclosure"
                                            }
                                        ]
                                    }
                            }
                        ]
                }
            ]
    }

    DICT_UPLINK_SET2 = {
        "name": "UplinkSet",
        "uplinkSets": 
            [
                {
                    "logicalPortConfigInfos": 
                        [
                            {
                                "desiredSpeed": "Auto",
                                "logicalLocation": 
                                    {
                                        "locationEntries": [
                                            {
                                                "relativeValue": 1,
                                                "type": "Bay"
                                            },
                                            {
                                                "relativeValue": 56,
                                                "type": "Port"
                                            },
                                            {
                                                "relativeValue": 1,
                                                "type": "Enclosure"
                                            }
                                        ]
                                    }
                            }
                        ]
                }
            ]
    }

    def test_resource_compare_equals(self):
        assert compare(self.DICT_ORIGINAL, self.DICT_EQUAL_ORIGINAL)

    def test_resource_compare_missing_entry_in_first(self):
        dict1 = self.DICT_ORIGINAL.copy()
        del dict1['state']

        assert not compare(dict1, self.DICT_EQUAL_ORIGINAL)

    def test_resource_compare_missing_entry_in_second(self):
        dict2 = self.DICT_EQUAL_ORIGINAL.copy()
        del dict2['state']

        assert not compare(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3)

    def test_resource_compare_different_on_level3(self):
        assert not compare(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3)

    def test_resource_compare_equals_with_empty_eq_none(self):
        assert compare(self.DICT_EMPTY_NONE1, self.DICT_EMPTY_NONE2)

    def test_resource_compare_equals_with_empty_eq_none_inverse(self):
        assert compare(self.DICT_EMPTY_NONE2, self.DICT_EMPTY_NONE1)

    def test_resource_compare_equals_with_empty_eq_none_different(self):
        assert not compare(self.DICT_EMPTY_NONE3, self.DICT_EMPTY_NONE1)

    def test_resource_compare_lig_equals(self):
        assert compare_lig(self.DICT_ORIGINAL, self.DICT_EQUAL_ORIGINAL)

    def test_resource_compare_lig_resource_empty(self):
        assert not compare_lig(self.DICT_EQUAL_ORIGINAL, {})

    def test_resource_compare_lig_uplink_sets_ports_same(self):
        assert compare_lig(self.DICT_UPLINK_SET1, self.DICT_UPLINK_SET1)

    def test_resource_compare_lig_uplink_sets_ports_different(self):
        assert not compare_lig(self.DICT_UPLINK_SET1, self.DICT_UPLINK_SET2)

    def test_resource_compare_lig_missing_entry_in_first(self):
        dict1 = self.DICT_ORIGINAL.copy()
        del dict1['state']

        assert not compare_lig(dict1, self.DICT_EQUAL_ORIGINAL)

    def test_resource_compare_lig_missing_entry_in_second(self):
        dict2 = self.DICT_EQUAL_ORIGINAL.copy()
        del dict2['state']

        assert not compare_lig(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3)

    def test_resource_compare_lig_different_on_level3(self):
        assert not compare_lig(self.DICT_ORIGINAL, self.DICT_DIF_ORIGINAL_LV3)

    def test_resource_compare_lig_equals_with_empty_eq_none(self):
        assert compare_lig(self.DICT_EMPTY_NONE1, self.DICT_EMPTY_NONE2)

    def test_resource_compare_lig_equals_with_empty_eq_none_inverse(self):
        assert compare_lig(self.DICT_EMPTY_NONE2, self.DICT_EMPTY_NONE1)

    def test_resource_compare_lig_equals_with_empty_eq_none_different(self):
        assert not compare_lig(self.DICT_EMPTY_NONE3, self.DICT_EMPTY_NONE1)

    def test_resource_compare_lig_with_double_level_list(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "6"]
        ]}

        assert compare_lig(dict1, dict2)

    def test_resource_compare_lig_with_double_level_list_different(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "7"]
        ]}

        assert not compare_lig(dict1, dict2)

    def test_resource_compare_with_double_level_list(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "6"]
        ]}

        assert compare(dict1, dict2)

    def test_resource_compare_with_double_level_list_different(self):
        dict1 = {list: [
            [1, 2, 3],
            [4, 5, 6]
        ]}

        dict2 = {list: [
            [1, 2, 3],
            [4, 5, "7"]
        ]}

        assert not compare(dict1, dict2)

    def test_comparison_with_int_and_float(self):
        dict1 = {
            "name": "name",
            "lvalue": int(10)
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10)
        }
        assert compare(dict1, dict2)

    def test_comparison_with_str_and_integer_float(self):
        dict1 = {
            "name": "name",
            "lvalue": '10'
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10)
        }
        assert compare(dict1, dict2)

    def test_comparison_with_str_and_float(self):
        dict1 = {
            "name": "name",
            "lvalue": '10.1'
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10.1)
        }
        assert compare(dict1, dict2)

    def test_comparison_dict_and_list(self):
        dict1 = {
            "name": "name",
            "value": {"id": 123}
        }

        dict2 = {
            "name": "name",
            "value": [1, 2, 3]
        }
        assert not compare(dict1, dict2)

    def test_comparison_list_and_dict(self):
        dict1 = {
            "name": "name",
            "value": [1, 2, 3]
        }

        dict2 = {
            "name": "name",
            "value": {"id": 123}
        }
        assert not compare(dict1, dict2)

    def test_comparison_with_different_float_values(self):
        dict1 = {
            "name": "name",
            "lvalue": 10.2
        }

        dict2 = {
            "name": "name",
            "lvalue": float(10.1)
        }
        assert not compare(dict1, dict2)

    def test_comparison_empty_list_and_none(self):
        dict1 = {
            "name": "name",
            "values": []
        }

        dict2 = {
            "name": "name",
            "values": None
        }
        assert compare(dict1, dict2)

    def test_comparison_none_and_empty_list(self):
        dict1 = {
            "name": "name",
            "values": None
        }
        dict2 = {
            "name": "name",
            "values": []
        }
        assert compare(dict1, dict2)

    def test_comparison_true_and_false(self):
        dict1 = {
            "name": "name",
            "values": True
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        assert not compare(dict1, dict2)

    def test_comparison_false_and_true(self):
        dict1 = {
            "name": "name",
            "values": False
        }

        dict2 = {
            "name": "name",
            "values": True
        }
        assert not compare(dict1, dict2)

    def test_comparison_true_and_true(self):
        dict1 = {
            "name": "name",
            "values": True
        }

        dict2 = {
            "name": "name",
            "values": True
        }
        assert compare(dict1, dict2)

    def test_comparison_false_and_false(self):
        dict1 = {
            "name": "name",
            "values": False
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        assert compare(dict1, dict2)

    def test_comparison_none_and_false(self):
        dict1 = {
            "name": "name",
            "values": None
        }

        dict2 = {
            "name": "name",
            "values": False
        }
        assert compare(dict1, dict2)

    def test_comparison_false_and_none(self):
        dict1 = {
            "name": "name",
            "values": False
        }
        dict2 = {
            "name": "name",
            "values": None
        }
        assert compare(dict1, dict2)

    def test_comparison_list_and_none_level_1(self):
        dict1 = {
            "name": "name of the resource",
            "value": [{"name": "item1"},
                      {"name": "item2"}]
        }
        dict2 = {
            "name": "name of the resource",
            "value": None
        }
        assert not compare(dict1, dict2)

    def test_comparison_none_and_list_level_1(self):
        dict1 = {
            "name": "name",
            "value": None
        }
        dict2 = {
            "name": "name",
            "value": [{"name": "item1"},
                      {"name": "item2"}]
        }
        assert not compare(dict1, dict2)

    def test_comparison_dict_and_none_level_1(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource"}
        }
        dict2 = {
            "name": "name",
            "value": None
        }
        assert not compare(dict1, dict2)

    def test_comparison_none_and_dict_level_1(self):
        dict1 = {
            "name": "name",
            "value": None
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource"}
        }
        assert not compare(dict1, dict2)

    def test_comparison_none_and_dict_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": None}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": {
                          "name": "sub-sub-resource"
                      }}
        }
        assert not compare(dict1, dict2)

    def test_comparison_dict_and_none_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": {
                          "name": "sub-sub-resource"
                      }}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "value": None}
        }
        assert not compare(dict1, dict2)

    def test_comparison_none_and_list_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": None}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": ["item1", "item2"]}
        }
        assert not compare(dict1, dict2)

    def test_comparison_list_and_none_level_2(self):
        dict1 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": ["item1", "item2"]}
        }
        dict2 = {
            "name": "name",
            "value": {"name": "subresource",
                      "list": None}
        }
        assert not compare(dict1, dict2)

    def test_comparison_list_of_dicts_with_diff_order(self):
        resource1 = {'connections': [
            {
                u'allocatedMbps': 0,
                u'networkUri': u'/rest/fc-networks/617a2c3b-1505-4369-a0a5-4c169183bf9d',
                u'requestedMbps': u'2500',
                u'portId': u'None',
                u'name': u'connection2',
                u'maximumMbps': 0,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Reserved',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': u'10:00:c2:54:96:f0:00:03',
                u'mac': u'46:E0:32:50:00:01',
                u'macType': u'Virtual',
                u'wwpn': u'10:00:c2:54:96:f0:00:02',
                u'interconnectUri': None,
                u'requestedVFs': None,
                u'functionType': u'FibreChannel',
                u'id': 2,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 1000,
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'requestedMbps': u'1000',
                u'portId': u'Flb 1:1-a',
                u'name': u'connection3',
                u'maximumMbps': 1000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': None,
                u'mac': u'46:E0:32:50:00:02',
                u'macType': u'Virtual',
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': u'Auto',
                u'functionType': u'Ethernet',
                u'id': 3,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 1000,
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'requestedMbps': u'1000',
                u'portId': u'Flb 1:2-a',
                u'name': u'connection4',
                u'maximumMbps': 1000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': None,
                u'mac': u'46:E0:32:50:00:03',
                u'macType': u'Virtual',
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/a3c936f2-2993-4779-a6e3-dc302b6f1bc6',
                u'requestedVFs': u'Auto',
                u'functionType': u'Ethernet',
                u'id': 4,
                u'allocatedVFs': None
            },
            {
                u'allocatedMbps': 2500,
                u'networkUri': u'/rest/fc-networks/179222e0-d59e-4898-b2bf-5c053c872ee6',
                u'requestedMbps': u'2500',
                u'portId': u'Flb 1:1-b',
                u'name': u'connection1',
                u'maximumMbps': 10000,
                u'wwpnType': u'Virtual',
                u'deploymentStatus': u'Deployed',
                u'boot': {
                    u'priority': u'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'wwnn': u'10:00:c2:54:96:f0:00:01',
                u'mac': u'46:E0:32:50:00:00',
                u'macType': u'Virtual',
                u'wwpn': u'10:00:c2:54:96:f0:00:00',
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': None,
                u'functionType': u'FibreChannel',
                u'id': 1,
                u'allocatedVFs': None
            }
        ]
        }

        resource2 = {'connections': [
            {
                u'requestedMbps': 1000,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'mac': u'46:E0:32:50:00:02',
                u'wwpnType': u'Virtual',
                u'id': 3,
                u'macType': u'Virtual',
                u'allocatedMbps': 1000,
                u'wwnn': None,
                u'maximumMbps': 1000,
                u'portId': u'Flb 1:1-a',
                u'name': 'connection3',
                u'functionType': 'Ethernet',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': u'Auto'
            },
            {
                u'requestedMbps': 1000,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/ethernet-networks/7704a66f-fa60-4375-8e9d-e72111bf4b3a',
                u'mac': u'46:E0:32:50:00:03',
                u'wwpnType': u'Virtual',
                u'id': 4,
                u'macType': u'Virtual',
                u'allocatedMbps': 1000,
                u'wwnn': None,
                u'maximumMbps': 1000,
                u'portId': u'Flb 1:2-a',
                u'name': 'connection4',
                u'functionType': 'Ethernet',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': None,
                u'interconnectUri': u'/rest/interconnects/a3c936f2-2993-4779-a6e3-dc302b6f1bc6',
                u'requestedVFs': u'Auto'
            },
            {
                u'requestedMbps': 2500,
                u'deploymentStatus': u'Deployed',
                u'networkUri': u'/rest/fc-networks/179222e0-d59e-4898-b2bf-5c053c872ee6',
                u'mac': u'46:E0:32:50:00:00',
                u'wwpnType': u'Virtual',
                u'id': 1,
                u'macType': u'Virtual',
                u'allocatedMbps': 2500,
                u'wwnn': u'10:00:c2:54:96:f0:00:01',
                u'maximumMbps': 10000,
                u'portId': u'Flb 1:1-b',
                u'name': 'connection1',
                u'functionType': 'FibreChannel',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': u'10:00:c2:54:96:f0:00:00',
                u'interconnectUri': u'/rest/interconnects/6930962f-8aba-42ac-8bbc-3794890ea945',
                u'requestedVFs': None
            },
            {
                u'requestedMbps': 2500,
                u'deploymentStatus': u'Reserved',
                u'networkUri': u'/rest/fc-networks/617a2c3b-1505-4369-a0a5-4c169183bf9d',
                u'mac': u'46:E0:32:50:00:01',
                u'wwpnType': u'Virtual',
                u'id': 2,
                u'macType': u'Virtual',
                u'allocatedMbps': 0,
                u'wwnn': u'10:00:c2:54:96:f0:00:03',
                u'maximumMbps': 0,
                u'portId': 'None',
                u'name': 'connection2',
                u'functionType': 'FibreChannel',
                u'boot': {
                    u'priority': 'NotBootable',
                    u'chapLevel': u'None',
                    u'initiatorNameSource': u'ProfileInitiatorName'
                },
                u'allocatedVFs': None,
                u'wwpn': u'10:00:c2:54:96:f0:00:02',
                u'interconnectUri': None,
                u'requestedVFs': None
            }
        ]
        }

        assert compare(resource1, resource2)

    def test_comparison_list_when_dict_has_diff_key(self):
        dict1 = {
            "name": "name",
            "value": [{'name': 'value1'},
                      {'name': 'value2'},
                      {'name': 'value3'}]
        }

        dict2 = {
            "name": "name",
            "value": [{'count': 3, 'name': 'value0'},
                      {'name': 'value1'},
                      {'name': 'value2'}]
        }
        assert not compare(dict1, dict2)

    def test_merge_list_by_key_when_original_list_is_empty(self):
        original_list = []
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        assert merged_list == expected_list

    def test_merge_list_by_key_when_original_list_is_null(self):
        original_list = None
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        assert merged_list == expected_list

    def test_merge_list_by_key_with_same_lenght_and_order(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        assert merged_list == expected_list

    def test_merge_list_by_key_with_different_order(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        assert merged_list == expected_list

    def test_merge_list_by_key_with_removed_items(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500)]

        assert merged_list == expected_list

    def test_merge_list_by_key_with_added_items(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, requestedMbps=1005)]

        assert merged_list == expected_list

    def test_merge_list_by_key_should_ignore_key_when_null(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value1=None, value2="345-changed")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1', 'value2'])

        expected_list = [dict(id=1, value1="123", value2="345-changed")]

        assert merged_list == expected_list

    def test_merge_list_by_key_should_not_fail_when_ignored_key_absent(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value3="678")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1'])

        expected_list = [dict(id=1, value1="123", value2="345", value3="678")]

        assert merged_list == expected_list

    def test_sort_by_keys(self):
        resource_list = [dict(networkType="Ethernet", name="name-2"),
                         dict(networkType="Ethernet", name="name-1")]
        result1, result2 = _sort_by_keys(resource_list, resource_list)
        expected_list = [dict(networkType="Ethernet", name="name-1"),
                         dict(networkType="Ethernet", name="name-2")]
        assert result1 == expected_list


class TestServerProfileReplaceNamesByUris():
    SERVER_PROFILE_NAME = "Profile101"
    SERVER_PROFILE_URI = "/rest/server-profiles/94B55683-173F-4B36-8FA6-EC250BA2328B"
    SHT_URI = "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
    ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    TEMPLATE_URI = '/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'
    FAKE_SERVER_HARDWARE = {'uri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'}

    BASIC_PROFILE = dict(
        name=SERVER_PROFILE_NAME,
        serverHardwareTypeUri=SHT_URI,
        enclosureGroupUri=ENCLOSURE_GROUP_URI,
        uri=SERVER_PROFILE_URI
    )

    PROFILE_CONNECTIONS = [{"name": "connection-1", "networkUri": "/rest/fc-networks/98"},
                           {"name": "connection-2", "networkName": "FC Network"},
                           {"name": "connection-3", "networkName": "FCoE Network"},
                           {"name": "connection-4", "networkName": "Network Set"},
                           {"name": "connection-5", "networkName": 'Ethernet Network'}]

    PROFILE_CONNECTIONS_WITH_NETWORK_URIS = [{"name": "connection-1", "networkUri": "/rest/fc-networks/98"},
                                             {"name": "connection-2", "networkUri": "/rest/fc-networks/14"},
                                             {"name": "connection-3", "networkUri": "/rest/fcoe-networks/16"},
                                             {"name": "connection-4", "networkUri": "/rest/network-sets/20"},
                                             {"name": "connection-5", "networkUri": "/rest/ethernet-networks/18"}]

    @pytest.fixture(autouse=True)
    def setUp(self):
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client = patcher_json_file.start()

        yield
        patcher_json_file.stop

    def test_should_replace_os_deployment_name_by_uri(self):
        uri = '/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493'

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.os_deployment_plans.get_by.return_value = [dict(uri=uri)]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data[SPKeys.OS_DEPLOYMENT] == dict(osDeploymentPlanUri=uri)

    def test_should_fail_when_deployment_plan_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.os_deployment_plans.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND + "Deployment Plan Name"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_enclosure_group_name_by_uri(self):
        uri = '/rest/enclosure-groups/81decf85-0dff-4a5e-8a95-52994eeb6493'

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.enclosure_groups.get_by.return_value = [dict(uri=uri)]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data.get('enclosureGroupUri') == uri
        assert not sp_data.get('enclosureGroupName')

    def test_should_fail_when_enclosure_group_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.enclosure_groups.get_by.return_value = []

        message = ServerProfileReplaceNamesByUris.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND + "Enclosure Group Name"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == message
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_replace_network_name_by_uri_with_connections(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[SPKeys.CONNECTIONS] = self.PROFILE_CONNECTIONS

        self.mock_ov_client.fc_networks.get_by.side_effect = [[dict(uri='/rest/fc-networks/14')], [], [], []]
        self.mock_ov_client.fcoe_networks.get_by.side_effect = [[dict(uri='/rest/fcoe-networks/16')], [], []]
        self.mock_ov_client.network_sets.get_by.side_effect = [[dict(uri='/rest/network-sets/20')], []]
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        expected_connections = self.PROFILE_CONNECTIONS_WITH_NETWORK_URIS
        assert sp_data.get(SPKeys.CONNECTIONS) == expected_connections

    def test_replace_network_name_by_uri_with_connection_settings(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data["connectionSettings"] = {SPKeys.CONNECTIONS: self.PROFILE_CONNECTIONS}

        self.mock_ov_client.fc_networks.get_by.side_effect = [[dict(uri='/rest/fc-networks/14')], [], [], []]
        self.mock_ov_client.fcoe_networks.get_by.side_effect = [[dict(uri='/rest/fcoe-networks/16')], [], []]
        self.mock_ov_client.network_sets.get_by.side_effect = [[dict(uri='/rest/network-sets/20')], []]
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        expected_connections = self.PROFILE_CONNECTIONS_WITH_NETWORK_URIS
        assert sp_data["connectionSettings"][SPKeys.CONNECTIONS] == expected_connections

    def test_should_fail_when_network_not_found(self):
        conn = dict(name="connection-1", networkName='FC Network')

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[SPKeys.CONNECTIONS] = [conn]

        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.fcoe_networks.get_by.return_value = []
        self.mock_ov_client.network_sets.get_by.return_value = []
        self.mock_ov_client.ethernet_networks.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_NETWORK_NOT_FOUND + "FC Network"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_server_hardware_type_name_by_uri(self):
        sht_uri = "/rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C"
        sht = {"name": "SY 480 Gen9 1", "uri": sht_uri}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_hardware_types.get_by.return_value = [sht]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data.get('serverHardwareTypeUri') == sht_uri
        assert sp_data.get('serverHardwareTypeName') is None

    def test_should_fail_when_server_hardware_type_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_hardware_types.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_HARDWARE_TYPE_NOT_FOUND + "SY 480 Gen9 1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_volume_names_by_uri(self):
        volume1 = {"name": "volume1", "uri": "/rest/storage-volumes/1"}
        volume2 = {"name": "volume2", "uri": "/rest/storage-volumes/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1"},
                {"id": 2, "volumeName": "volume2"}
            ]
        }
        expected_dict = deepcopy(sp_data)
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeUri": "/rest/storage-volumes/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeUri": "/rest/storage-volumes/2"}

        self.mock_ov_client.volumes.get_by.side_effect = [[volume1], [volume2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict

    def test_should_not_replace_volume_names_when_volume_uri_is_none(self):
        volume2 = {"name": "volume2", "uri": "/rest/storage-volumes/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1", "volumeUri": None},
                {"id": 2, "volumeName": "volume2"}
            ]
        }
        expected_dict = deepcopy(sp_data)
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeName": "volume1", "volumeUri": None}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeUri": "/rest/storage-volumes/2"}

        self.mock_ov_client.volumes.get_by.side_effect = [{}, [volume2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict

    def test_should_not_replace_when_inform_volume_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_replace_storage_pool_names_by_uri(self):
        pool1 = {"name": "pool1", "uri": "/rest/storage-pools/1"}
        pool2 = {"name": "pool2", "uri": "/rest/storage-pools/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"},
                {"id": 2, "volumeStoragePoolName": "pool2"}
            ]
        }
        expected_dict = deepcopy(sp_data)
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStoragePoolUri": "/rest/storage-pools/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStoragePoolUri": "/rest/storage-pools/2"}

        self.mock_ov_client.storage_pools.get_by.side_effect = [[pool1], [pool2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict

    def test_should_not_replace_when_inform_storage_pool_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeStoragePoolUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_fail_when_storage_pool_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"}
            ]
        }

        self.mock_ov_client.storage_pools.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_POOL_NOT_FOUND + "pool1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_storage_system_names_by_uri(self):
        storage_system1 = {"name": "system1", "uri": "/rest/storage-systems/1"}
        storage_system2 = {"name": "system2", "uri": "/rest/storage-systems/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"},
                {"id": 2, "volumeStorageSystemName": "system2"}
            ]
        }
        expected = deepcopy(sp_data)
        expected['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"}
        expected['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}

        self.mock_ov_client.storage_systems.get_by.side_effect = [[storage_system1], [storage_system2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_replace_volume_template_names_by_uri(self):
        volume_template = {"name": "tempalte name", "uri": "/rest/storage-volume-templates/1"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [{"id": 1, "volume": {"templateName": "teplate name"}}]
        }
        expected = deepcopy(sp_data)
        expected['sanStorage']['volumeAttachments'][0] = {"id": 1,
                                                          "volume": {"templateUri": "/rest/storage-volume-templates/1"}}

        self.mock_ov_client.storage_volume_templates.get_by.return_value = [volume_template]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_replace_storage_pool_names_inside_properties(self):
        storage_pool = {"name": "storage pool name", "uri": "/rest/storage-pools/1"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [{"id": 1,
                                   "volume": {"properties": {"storagePoolName": "storage pool name"}}}]
        }
        expected = deepcopy(sp_data)
        expected['sanStorage']['volumeAttachments'][0] = {"id": 1,
                                                          "volume": {"properties":
                                                                     {"storagePool": "/rest/storage-pools/1"}}}

        self.mock_ov_client.storage_pools.get_by.return_value = [storage_pool]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_not_replace_when_inform_storage_system_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"},
                {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_fail_when_storage_system_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"}
            ]
        }

        self.mock_ov_client.storage_systems.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_SYSTEM_NOT_FOUND + "system1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_enclosure_name_by_uri(self):
        uri = "/rest/enclosures/09SGH100X6J1"
        enclosure = {"name": "Enclosure-474", "uri": uri}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.enclosures.get_by.return_value = [enclosure]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data.get('enclosureUri') == uri
        assert sp_data.get('enclosureName') is None

    def test_should_fail_when_enclosure_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.enclosures.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.ENCLOSURE_NOT_FOUND + "Enclosure-474"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_interconnect_name_by_uri(self):
        interconnect1 = {"name": "interconnect1", "uri": "/rest/interconnects/1"}
        interconnect2 = {"name": "interconnect2", "uri": "/rest/interconnects/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [
            {"id": 1, "interconnectName": "interconnect1"},
            {"id": 2, "interconnectName": "interconnect2"}
        ]

        expected = deepcopy(sp_data)
        expected['connections'][0] = {"id": 1, "interconnectUri": "/rest/interconnects/1"}
        expected['connections'][1] = {"id": 2, "interconnectUri": "/rest/interconnects/2"}

        self.mock_ov_client.interconnects.get_by.side_effect = [[interconnect1], [interconnect2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_not_replace_when_inform_interconnect_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [
            {"id": 1, "interconnectUri": "/rest/interconnects/1"},
            {"id": 2, "interconnectUri": "/rest/interconnects/2"}
        ]

        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_not_replace_interconnect_name_when_connections_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_fail_when_interconnect_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [{"id": 1, "interconnectName": "interconnect1"}]

        self.mock_ov_client.interconnects.get_by.return_value = None

        expected_error = ServerProfileReplaceNamesByUris.INTERCONNECT_NOT_FOUND + "interconnect1"
        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_firmware_baseline_name_by_uri(self):
        firmware_driver = {"name": "firmwareName001", "uri": "/rest/firmware-drivers/1"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        expected = deepcopy(sp_data)
        expected['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        self.mock_ov_client.firmware_drivers.get_by.return_value = [firmware_driver]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_not_replace_when_inform_firmware_baseline_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_not_replace_firmware_baseline_name_when_firmware_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_fail_when_firmware_baseline_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        self.mock_ov_client.firmware_drivers.get_by.return_value = None

        expected_error = ServerProfileReplaceNamesByUris.FIRMWARE_DRIVER_NOT_FOUND + "firmwareName001"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_sas_logical_jbod_names_by_uris(self):
        sas_logical_jbod1 = {"name": "jbod1", "uri": "/rest/sas-logical-jbods/1"}
        sas_logical_jbod2 = {"name": "jbod2", "uri": "/rest/sas-logical-jbods/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"},
                {"id": 2, "sasLogicalJBODName": "jbod2"}
            ]
        }
        expected = deepcopy(sp_data)
        expected['localStorage']['sasLogicalJBODs'][0] = {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"}
        expected['localStorage']['sasLogicalJBODs'][1] = {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}

        self.mock_ov_client.sas_logical_jbods.get_by.side_effect = [[sas_logical_jbod1], [sas_logical_jbod2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_not_replace_when_inform_sas_logical_jbod_uris(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"},
                {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_jbod_list_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_local_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected_dict
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_fail_when_sas_logical_jbod_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"}
            ]
        }

        self.mock_ov_client.sas_logical_jbods.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SAS_LOGICAL_JBOD_NOT_FOUND + "jbod1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except OneViewModuleResourceNotFound as e:
            assert e.msg == expected_error
        else:
            pytest.fail(msg="Expected Exception was not raised")

    def test_should_replace_scope_names_by_uri(self):
        scope1 = {"name": "scope1", "uri": "/rest/scopes/1"}
        scope2 = {"name": "scope2", "uri": "/rest/scopes/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)

        expected = deepcopy(sp_data)
        sp_data['initialScopeNames'] = ["scope1", "scope2"]
        expected['initialScopeUris'] = ["/rest/scopes/1", "/rest/scopes/2"]

        self.mock_ov_client.scopes.get_by_name.side_effect = [scope1, scope2]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        assert sp_data == expected

    def test_should_fail_when_scope_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['initialScopeNames'] = ["scope1"]

        self.mock_ov_client.scopes.get_by_name.return_value = None

        with pytest.raises(OneViewModuleResourceNotFound):
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)


class TestServerProfileMerger():
    SERVER_PROFILE_NAME = "Profile101"

    CREATED_BASIC_PROFILE = dict(
        affinity="Bay",
        bios=dict(manageBios=False, overriddenSettings=[]),
        boot=dict(manageBoot=False, order=[]),
        bootMode=dict(manageMode=False, mode=None, pxeBootPolicy=None),
        category="server-profile-templates",
        enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
        name=SERVER_PROFILE_NAME,
        serialNumber='VCGGU8800W',
        serialNumberType="Virtual",
        serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B",
        serverHardwareUri='/rest/server-hardware/37333036-3831-76jh-4831-303658389766',
        status="OK",
        type="ServerProfileV5",
        uri="/rest/server-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea490",
        serverProfileTemplateUri='/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda',
        templateCompliance='Compliant',
        wwnType="Virtual"
    )

    FAKE_SERVER_HARDWARE = {'uri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'}

    BOOT_CONN = dict(priority="NotBootable", chapLevel="none")

    CONNECTION_1 = dict(id=1, name="connection-1", mac="E2:4B:0D:30:00:29", boot=BOOT_CONN)
    CONNECTION_2 = dict(id=2, name="connection-2", mac="E2:4B:0D:30:00:2A", boot=BOOT_CONN)

    CONNECTION_1_WITH_WWPN = dict(name="connection-1", wwpnType="Virtual",
                                  wwnn="10:00:3a:43:88:50:00:01", wwpn="10:00:3a:43:88:50:00:00")
    CONNECTION_2_WITH_WWPN = dict(name="connection-2", wwpnType="Physical",
                                  wwnn="10:00:3a:43:88:50:00:03", wwpn="10:00:3a:43:88:50:00:02")

    CONN_1_NO_MAC_BASIC_BOOT = dict(id=1, name="connection-1", boot=dict(priority="NotBootable"))
    CONN_2_NO_MAC_BASIC_BOOT = dict(id=2, name="connection-2", boot=dict(priority="NotBootable"))

    PATH_1 = dict(isEnabled=True, connectionId=1, storageTargets=["20:00:00:02:AC:00:08:D6"])
    PATH_2 = dict(isEnabled=True, connectionId=2, storageTargetType="Auto")

    VOLUME_1 = dict(id=1, volumeUri="/rest/volume/id1", lun=123, lunType="Auto", storagePaths=[PATH_1, PATH_2])
    VOLUME_2 = dict(id=2, volumeUri="/rest/volume/id2", lun=345, lunType="Auto", storagePaths=[])

    SAN_STORAGE = dict(hostOSType="Windows 2012 / WS2012 R2",
                       volumeAttachments=[VOLUME_1, VOLUME_2])

    OS_CUSTOM_ATTRIBUTES = [dict(name="hostname", value="newhostname"),
                            dict(name="username", value="administrator")]

    OS_DEPLOYMENT_SETTINGS = dict(osDeploymentPlanUri="/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493",
                                  osVolumeUri="/rest/deployed-targets/a166c84a-4964-4f20-b4ba-ef2f154b8596",
                                  osCustomAttributes=OS_CUSTOM_ATTRIBUTES)

    SAS_LOGICAL_JBOD_1 = dict(id=1, deviceSlot="Mezz 1", name="jbod-1", driveTechnology="SasHdd", status="OK",
                              sasLogicalJBODUri="/rest/sas-logical-jbods/3128c9e6-e3de-43e7-b196-612707b54967")

    SAS_LOGICAL_JBOD_2 = dict(id=2, deviceSlot="Mezz 1", name="jbod-2", driveTechnology="SataHdd", status="Pending")

    DRIVES_CONTROLLER_EMBEDDED = [dict(driveNumber=1, name="drive-1", raidLevel="RAID1", bootable=False,
                                       sasLogicalJBODId=None),
                                  dict(driveNumber=2, name="drive-2", raidLevel="RAID1", bootable=False,
                                       sasLogicalJBODId=None)]

    CONTROLLER_EMBEDDED = dict(deviceSlot="Embedded", mode="RAID", initialize=False, importConfiguration=True,
                               logicalDrives=DRIVES_CONTROLLER_EMBEDDED)

    DRIVES_CONTROLLER_MEZZ_1 = [dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=1),
                                dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=2)]
    CONTROLLER_MEZZ_1 = dict(deviceSlot="Mezz 1", mode="RAID", initialize=False, importConfiguration=True,
                             logicalDrives=DRIVES_CONTROLLER_MEZZ_1)

    INDEX_EMBED = 1
    INDEX_MEZZ = 0

    profile_with_san_storage = CREATED_BASIC_PROFILE.copy()
    profile_with_san_storage[SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
    profile_with_san_storage[SPKeys.SAN] = SAN_STORAGE

    profile_with_os_deployment = CREATED_BASIC_PROFILE.copy()
    profile_with_os_deployment[SPKeys.OS_DEPLOYMENT] = OS_DEPLOYMENT_SETTINGS

    profile_with_local_storage = CREATED_BASIC_PROFILE.copy()
    profile_with_local_storage[SPKeys.LOCAL_STORAGE] = dict()
    profile_with_local_storage[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS] = [SAS_LOGICAL_JBOD_2,
                                                                                  SAS_LOGICAL_JBOD_1]
    profile_with_local_storage[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS] = [CONTROLLER_MEZZ_1, CONTROLLER_EMBEDDED]

    profile_with_connection_settings = CREATED_BASIC_PROFILE.copy()
    profile_with_connection_settings[SPKeys.CONNECTION_SETTINGS] = dict()
    profile_with_connection_settings[SPKeys.CONNECTION_SETTINGS][SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]

    @pytest.fixture(autouse=True)
    def setUp(self):
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.mock_ov_client = patcher_json_file.start()

        self.mock_ov_client.server_hardware.get_by.return_value = [self.FAKE_SERVER_HARDWARE]
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ov_client.server_profiles.update.return_value = deepcopy(self.profile_with_san_storage)

        yield
        patcher_json_file.stop

    def test_merge_when_having_connection_settings(self):
        connection_added = dict(id=3, name="new-connection")
        data = dict(name="Profile101",
                    connectionSettings=dict(connections=[self.CONN_1_NO_MAC_BASIC_BOOT.copy(),
                                                         self.CONN_2_NO_MAC_BASIC_BOOT.copy(),
                                                         connection_added.copy()]))
        resource = deepcopy(self.profile_with_connection_settings)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy(), connection_added]
        assert merged_data[SPKeys.CONNECTION_SETTINGS][SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_connections_have_new_item(self):
        connection_added = dict(id=3, name="new-connection")
        data = dict(name="Profile101",
                    connections=[self.CONN_1_NO_MAC_BASIC_BOOT.copy(),
                                 self.CONN_2_NO_MAC_BASIC_BOOT.copy(),
                                 connection_added.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy(), connection_added]
        assert merged_data[SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_connections_have_removed_item(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1]
        assert merged_data[SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_connections_have_changed_item(self):
        connection_2_renamed = dict(id=2, name="connection-2-renamed", boot=dict(priority="NotBootable"))
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), connection_2_renamed.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        connection_2_merged = dict(id=2, name="connection-2-renamed", mac="E2:4B:0D:30:00:2A", boot=self.BOOT_CONN)
        expected_connections = [self.CONNECTION_1.copy(), connection_2_merged.copy()]
        assert merged_data[SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_connection_list_is_removed(self):
        data = dict(name="Profile101",
                    connections=[])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.CONNECTIONS]

    def test_merge_when_connection_list_is_null(self):
        data = dict(name="Profile101",
                    connections=None)
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.CONNECTIONS]

    def test_merge_when_connection_list_not_provided(self):
        data = dict(name="Profile101")

        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy()]
        assert merged_data[SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_existing_connection_list_is_null(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), self.CONNECTION_2.copy()])

        resource = deepcopy(self.profile_with_san_storage)
        resource[SPKeys.CONNECTIONS] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy()]
        assert merged_data[SPKeys.CONNECTIONS] == expected_connections

    def test_merge_when_san_storage_is_equals(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), self.CONNECTION_2.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data == resource

    def test_merge_when_san_storage_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[SPKeys.SAN].pop('hostOSType')
        data[SPKeys.SAN]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_san_storage = deepcopy(self.SAN_STORAGE)
        expected_san_storage['newField'] = "123"
        assert merged_data[SPKeys.SAN] == expected_san_storage

    def test_merge_when_san_storage_is_removed_from_profile_with_san(self):
        data = dict(name="Profile101",
                    sanStorage=None)
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_san_storage = dict(manageSanStorage=False,
                                    volumeAttachments=[])
        assert merged_data[SPKeys.SAN] == expected_san_storage

    def test_merge_when_san_storage_is_removed_from_basic_profile(self):
        data = dict(name="Profile101",
                    sanStorage=None,
                    newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.SAN]

    def test_merge_when_san_storage_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.SAN] == resource[SPKeys.SAN]

    def test_merge_when_existing_san_storage_is_null(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.SAN] == self.SAN_STORAGE

    def test_merge_when_volume_attachments_are_removed(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[SPKeys.SAN][SPKeys.VOLUMES] = None
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.SAN][SPKeys.VOLUMES]

    def test_merge_when_volume_attachments_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[SPKeys.SAN][SPKeys.VOLUMES][0]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_volumes = [deepcopy(self.VOLUME_1), deepcopy(self.VOLUME_2)]
        expected_volumes[0]['newField'] = "123"
        assert merged_data[SPKeys.SAN][SPKeys.VOLUMES] == expected_volumes

    def test_merge_when_storage_paths_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[SPKeys.SAN][SPKeys.VOLUMES][0][SPKeys.PATHS][1]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)
        merged_volumes = merged_data[SPKeys.SAN].get(SPKeys.VOLUMES)

        expected_paths_storage_1 = [deepcopy(self.PATH_1), deepcopy(self.PATH_2)]
        expected_paths_storage_1[1]['newField'] = "123"
        assert expected_paths_storage_1 == merged_volumes[0][SPKeys.PATHS]
        assert [] == merged_volumes[1][SPKeys.PATHS]

    def test_merge_should_add_storage_path(self):
        profile = deepcopy(self.profile_with_san_storage)
        path3 = dict(isEnabled=True, connectionId=3, storageTargetType="Auto")
        profile[SPKeys.SAN][SPKeys.VOLUMES][0][SPKeys.PATHS].append(deepcopy(path3))

        resource = deepcopy(self.profile_with_san_storage)
        merged_data = ServerProfileMerger().merge_data(resource, profile)

        expected_paths = [self.PATH_1, self.PATH_2, path3]

        assert expected_paths == merged_data[SPKeys.SAN][SPKeys.VOLUMES][0][SPKeys.PATHS]

    def test_merge_when_storage_paths_are_removed(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[SPKeys.SAN][SPKeys.VOLUMES][0][SPKeys.PATHS] = []
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)
        merged_volumes = merged_data[SPKeys.SAN].get(SPKeys.VOLUMES)

        assert [] == merged_volumes[1][SPKeys.PATHS]

    def test_merge_when_bios_has_changes(self):
        data = dict(name="Profile101")
        data[SPKeys.BIOS] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_bios = dict(manageBios=False, overriddenSettings=[], newField="123")
        assert merged_data[SPKeys.BIOS] == expected_bios

    def test_merge_when_bios_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BIOS] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.BIOS]

    def test_merge_when_bios_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_bios = dict(manageBios=False, overriddenSettings=[])
        assert merged_data[SPKeys.BIOS] == expected_bios

    def test_merge_when_existing_bios_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BIOS] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[SPKeys.BIOS] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.BIOS] == dict(newField="123")

    def test_merge_when_boot_has_changes(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot = dict(manageBoot=False, order=[], newField="123")
        assert merged_data[SPKeys.BOOT] == expected_boot

    def test_merge_when_boot_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.BOOT]

    def test_merge_when_boot_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot = dict(manageBoot=False, order=[])
        assert merged_data[SPKeys.BOOT] == expected_boot

    def test_merge_when_existing_boot_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[SPKeys.BOOT] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.BOOT] == dict(newField="123")

    def test_merge_when_boot_mode_has_changes(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT_MODE] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot_mode = dict(manageMode=False, mode=None, pxeBootPolicy=None, newField="123")
        assert merged_data[SPKeys.BOOT_MODE] == expected_boot_mode

    def test_merge_when_boot_mode_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT_MODE] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.BOOT_MODE]

    def test_merge_when_boot_mode_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot_mode = dict(manageMode=False, mode=None, pxeBootPolicy=None)
        assert merged_data[SPKeys.BOOT_MODE] == expected_boot_mode

    def test_merge_when_existing_boot_mode_is_null(self):
        data = dict(name="Profile101")
        data[SPKeys.BOOT_MODE] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[SPKeys.BOOT_MODE] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.BOOT_MODE] == dict(newField="123")

    def test_merge_when_os_deployment_is_equals(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data == resource

    def test_merge_when_os_deployment_has_changes(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[SPKeys.OS_DEPLOYMENT]['osDeploymentPlanUri'] = "/rest/os-deployment-plans/other-id"
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment['osDeploymentPlanUri'] = "/rest/os-deployment-plans/other-id"
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_os_deployment_not_provided(self):
        data = dict(name="Profile101")

        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = resource[SPKeys.OS_DEPLOYMENT]
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_existing_os_deployment_settings_are_null(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))

        resource = deepcopy(self.profile_with_os_deployment)
        resource[SPKeys.OS_DEPLOYMENT] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_custom_attributes_have_changes(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][0]['hostname'] = 'updatedhostname'
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[SPKeys.ATTRIBUTES][0]['hostname'] = 'updatedhostname'
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_custom_attributes_have_new_item(self):
        new_item = dict(name="password", value="secret123")
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES].append(new_item.copy())

        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[SPKeys.ATTRIBUTES].append(new_item.copy())
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_custom_attributes_have_removed_item(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES].pop()
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[SPKeys.ATTRIBUTES].pop()
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_custom_attributes_are_equals_with_different_order(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        first_attr = data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][0]
        second_attr = data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][1]

        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][0] = second_attr
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][1] = first_attr
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        list1 = sorted(merged_data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES], key=_str_sorted)
        list2 = sorted(deepcopy(self.profile_with_os_deployment)[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES],
                       key=_str_sorted)

        assert list1 == list2

    def test_merge_when_custom_attributes_have_different_values_and_order(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))

        first_attr = data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][0]
        second_attr = data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][1]

        first_attr['value'] = 'newValue'
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][0] = second_attr
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES][1] = first_attr
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_attributes = [dict(name="username", value="administrator"),
                                  dict(name="hostname", value="newValue")]
        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[SPKeys.ATTRIBUTES] = expected_os_attributes
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_custom_attributes_are_removed(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES] = None
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[SPKeys.ATTRIBUTES] = None
        assert merged_data[SPKeys.OS_DEPLOYMENT] == expected_os_deployment

    def test_merge_when_existing_custom_attributes_are_null(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_attributes = deepcopy(self.OS_DEPLOYMENT_SETTINGS).get(SPKeys.ATTRIBUTES)
        assert merged_data[SPKeys.OS_DEPLOYMENT].get(SPKeys.ATTRIBUTES) == expected_attributes

    def test_merge_when_local_storage_removed(self):
        data = dict(name="Profile101",
                    localStorage=None)
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert merged_data[SPKeys.LOCAL_STORAGE] == dict(sasLogicalJBODs=[], controllers=[])

    def test_merge_when_local_storage_is_null_and_existing_server_profile_is_basic(self):
        data = dict(name="Profile101",
                    localStorage=None)
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.LOCAL_STORAGE]

    def test_merge_when_sas_logical_jbods_have_new_item(self):
        sas_logical_jbod_added = dict(id=3, deviceSlot="Mezz 1", name="new-sas-logical-jbod", driveTechnology="SataHdd")
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_2.copy(),
                                                       self.SAS_LOGICAL_JBOD_1.copy(),
                                                       sas_logical_jbod_added.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_2.copy(),
                                      self.SAS_LOGICAL_JBOD_1.copy(),
                                      sas_logical_jbod_added]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS] == expected_sas_logical_jbods

    def test_merge_when_sas_logical_jbods_have_removed_item(self):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_1.copy()]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS] == expected_sas_logical_jbods

    def test_merge_when_sas_logical_jbods_have_changed_item(self):
        item_2_changed = dict(id=2, numPhysicalDrives=2)
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy(), item_2_changed.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        item_2_merged = dict(numPhysicalDrives=2,
                             id=2, name="jbod-2", deviceSlot="Mezz 1", driveTechnology="SataHdd", status="Pending")
        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_1.copy(), item_2_merged.copy()]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS] == expected_sas_logical_jbods

    @mock.patch.object(oneview, 'merge_list_by_key')
    def test_merge_should_ignore_logical_jbod_uri_when_null(self, mock_merge_list):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy(), self.SAS_LOGICAL_JBOD_2.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        ServerProfileMerger().merge_data(resource, data)

        mock_merge_list.assert_called_once_with(mock.ANY, mock.ANY, key=mock.ANY,
                                                ignore_when_null=[SPKeys.SAS_LOGICAL_JBOD_URI])

    def test_merge_when_sas_logical_jbod_list_is_removed(self):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS]

    def test_merge_when_controllers_have_new_item(self):
        controller_added = dict(deviceSlot="Device Slot Name", mode="RAID", initialize=False, importConfiguration=True)
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy(),
                                                   controller_added.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_controllers = [self.CONTROLLER_MEZZ_1.copy(), self.CONTROLLER_EMBEDDED.copy(), controller_added]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS] == expected_controllers

    def test_merge_when_controllers_have_removed_item(self):
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_controllers = [self.CONTROLLER_MEZZ_1.copy()]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS] == expected_controllers

    def test_merge_when_controllers_have_changed_item(self):
        controller_embedded_changed = dict(deviceSlot="Embedded", initialize=True)
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded_changed.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        item_2_merged = dict(initialize=True,  # initialize value changed from False to True
                             deviceSlot="Embedded", mode="RAID", importConfiguration=True,
                             logicalDrives=self.DRIVES_CONTROLLER_EMBEDDED)
        expected_controllers = [self.CONTROLLER_MEZZ_1.copy(), item_2_merged.copy()]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS] == expected_controllers

    def test_merge_when_controller_list_is_removed(self):
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS]

    def test_merge_when_drives_from_embedded_controller_no_name_no_jbodid(self):
        new_drive = dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=None)
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[SPKeys.LOGICAL_DRIVES].append(new_drive.copy())

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][0],
                           self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][1],
                           new_drive]

        result = merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_EMBED][SPKeys.LOGICAL_DRIVES]

        assert result == expected_drives

    def test_merge_when_drives_from_embedded_controller_have_new_item(self):
        new_drive = dict(name="drive-3", raidLevel="RAID1", bootable=False, sasLogicalJBODId=None)
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[SPKeys.LOGICAL_DRIVES].append(new_drive.copy())

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][0],
                           self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][1],
                           new_drive]
        result = merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_EMBED][SPKeys.LOGICAL_DRIVES]

        assert result == expected_drives

    def test_merge_when_drives_from_embedded_controller_have_removed_item(self):
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[SPKeys.LOGICAL_DRIVES].pop()

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][0]]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_EMBED][SPKeys.LOGICAL_DRIVES] == expected_drives

    def test_merge_when_drives_have_incomplete_data(self):
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[SPKeys.LOGICAL_DRIVES][0] = {}

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drive = self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][1]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][0][SPKeys.LOGICAL_DRIVES][1] == expected_drive

    def test_merge_when_drives_from_embedded_controller_have_changed_item(self):
        """
        Test the drive merge, although it's not supported by OneView.
        """
        drive_changed = dict(name="drive-1", raidLevel="RAID0")
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[SPKeys.LOGICAL_DRIVES][0] = drive_changed

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        drive_1_merged = dict(driveNumber=1, name="drive-1", raidLevel="RAID0", bootable=False, sasLogicalJBODId=None)
        expected_drives = [drive_1_merged,
                           self.CONTROLLER_EMBEDDED[SPKeys.LOGICAL_DRIVES][1]]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_EMBED][SPKeys.LOGICAL_DRIVES] == expected_drives

    def test_merge_when_drives_from_mezz_controller_have_new_item(self):
        new_drive = dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=3)
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[SPKeys.LOGICAL_DRIVES].append(new_drive)

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_MEZZ_1[SPKeys.LOGICAL_DRIVES][0],
                           self.CONTROLLER_MEZZ_1[SPKeys.LOGICAL_DRIVES][1],
                           new_drive]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_MEZZ][SPKeys.LOGICAL_DRIVES] == expected_drives

    def test_merge_when_drives_from_mezz_controller_have_removed_item(self):
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[SPKeys.LOGICAL_DRIVES].pop()

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_MEZZ_1[SPKeys.LOGICAL_DRIVES][0]]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_MEZZ][SPKeys.LOGICAL_DRIVES] == expected_drives

    def test_merge_when_drives_from_mezz_controller_have_changed_item(self):
        """
        Test the drive merge, although it's not supported by OneView.
        """
        drive_changed = dict(sasLogicalJBODId=1, raidLevel="RAID0")
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[SPKeys.LOGICAL_DRIVES][0] = drive_changed

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        drive_1_merged = dict(name=None, raidLevel="RAID0", bootable=False, sasLogicalJBODId=1)
        expected_drives = [drive_1_merged,
                           self.CONTROLLER_MEZZ_1[SPKeys.LOGICAL_DRIVES][1]]
        assert merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_MEZZ][SPKeys.LOGICAL_DRIVES] == expected_drives

    def test_merge_when_controller_drives_are_removed(self):
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[SPKeys.LOGICAL_DRIVES] = []

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        assert not merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][self.INDEX_MEZZ][SPKeys.LOGICAL_DRIVES]

    @mock.patch.dict('os.environ', dict(LOGFILE='/path/log.txt'))
    @mock.patch.object(logging, 'getLogger')
    @mock.patch.object(logging, 'basicConfig')
    def test_should_config_logging_when_logfile_env_var_defined(self, mock_logging_config, mock_get_logger):
        fake_logger = mock.Mock()
        mock_get_logger.return_value = fake_logger

        get_logger('/home/dev/oneview-ansible/library/oneview_server_profile.py')

        mock_get_logger.assert_called_once_with('oneview_server_profile.py')
        fake_logger.addHandler.not_been_called()
        mock_logging_config.assert_called_once_with(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                                                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                                                    filename='/path/log.txt', filemode='a')

    @mock.patch('os.environ')
    @mock.patch.object(logging, 'getLogger')
    @mock.patch.object(logging, 'basicConfig')
    @mock.patch.object(logging, 'NullHandler')
    def test_should_add_null_handler_when_logfile_env_var_undefined(self, mock_null_handler, mock_logging_config,
                                                                    mock_get_logger, mock_env):
        mock_env.get.return_value = None
        fake_logger = mock.Mock()
        mock_get_logger.return_value = fake_logger

        get_logger('/home/dev/oneview-ansible/library/oneview_server_profile.py')

        mock_get_logger.assert_called_once_with('oneview_server_profile.py')
        fake_logger.addHandler.assert_called_once_with(logging.NullHandler())
        mock_logging_config.not_been_called()


if __name__ == '__main__':
    pytest.main([__file__])
