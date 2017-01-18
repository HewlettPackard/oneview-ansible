# -*- coding: utf-8 -*-
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

import yaml
from mock import Mock, patch
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException


def create_ansible_mock(params):
    mock_ansible = Mock()
    mock_ansible.params = params
    return mock_ansible


def create_ansible_mock_yaml(yaml_config):
    mock_ansible = Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class PreloadedMocksBaseTestCase(object):
    _testing_class = None
    _testing_module = None
    mock_ov_client_from_json_file = None
    mock_ov_client_from_env_vars = None
    mock_ansible_module = None
    mock_ov_client = None

    def configure_mocks(self, test_case, testing_class):
        """
        Preload mocked OneViewClient instance and AnsibleModule
        Args:
            test_case (object): class instance (self) that are inheriting from ModuleContructorTestCase
            testing_class (object): class being tested
        """
        self._testing_class = testing_class
        self._testing_module = testing_class.__module__

        # Define OneView Client Mock (FILE)
        patcher_json_file = patch.object(OneViewClient, 'from_json_file')
        test_case.addCleanup(patcher_json_file.stop)
        self.mock_ov_client_from_json_file = patcher_json_file.start()

        # Define OneView Client Mock
        self.mock_ov_client = self.mock_ov_client_from_json_file.return_value

        # Define OneView Client Mock (ENV)
        patcher_env = patch.object(OneViewClient, 'from_environment_variables')
        test_case.addCleanup(patcher_env.stop)
        self.mock_ov_client_from_env_vars = patcher_env.start()

        # Define Ansible Module Mock
        patcher_ansible = patch(self._testing_module + '.AnsibleModule')
        test_case.addCleanup(patcher_ansible.stop)
        mock_ansible_module = patcher_ansible.start()
        self.mock_ansible_module = Mock()
        mock_ansible_module.return_value = self.mock_ansible_module


class ModuleContructorTestCase(PreloadedMocksBaseTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function

    When inheriting this class, the class and main function tests are added to your test case.
    """

    def __validations(self):
        if not self._testing_class:
            raise Exception("Mocks are not configured, you must call 'configure_mocks' before running this test.")

    def test_should_load_config_from_file(self):
        self.__validations()

        self.mock_ansible_module.params = {'config': 'config.json'}

        # Call the constructor
        self._testing_class()

        self.mock_ov_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ov_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):
        self.__validations()

        self.mock_ansible_module.params = {'config': None}

        # Call the constructor
        self._testing_class()

        self.mock_ov_client_from_env_vars.assert_called_once()
        self.mock_ov_client_from_json_file.not_been_called()

    def test_should_call_fail_json_when_not_have_oneview(self):
        self.__validations()
        self.mock_ansible_module.params = {'config': 'config.json'}

        with patch(self._testing_module + ".HAS_HPE_ONEVIEW", False):
            self._testing_class()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg='HPE OneView Python SDK is required for this module.')

    def test_main_function_should_call_run_method(self):
        self.__validations()
        self.mock_ansible_module.params = {'config': 'config.json'}

        module = __import__(self._testing_module)
        main_func = getattr(module, 'main')

        with patch.object(self._testing_class, "run") as mock_run:
            main_func()
            mock_run.assert_called_once()


class ValidateEtagTestCase(PreloadedMocksBaseTestCase):
    """
    ValidateEtagTestCase has common tests for modules that handle validate_etag attribute.

    When inheriting this class, validate_etag implementation tests are added to your test case.
    """

    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data={'name': 'resource name'}
    )

    def test_should_validate_etag_when_set_as_true(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = True

        self._testing_class().run()

        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.not_been_called()

    def test_should_not_validate_etag_when_set_as_false(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        self.mock_ansible_module.params['validate_etag'] = False

        self._testing_class().run()

        self.mock_ov_client.connection.enable_etag_validation.not_been_called()
        self.mock_ov_client.connection.disable_etag_validation.assert_called_once()


class FactsParamsTestCase(PreloadedMocksBaseTestCase):
    """
    FactsParamsTestCase has common test for classes that support pass additional
        parameters when retrieving all resources.
    """

    def configure_client_mock(self, resorce_client):
        """
        Args:
             resorce_client: Resource client that is being called
        """
        self._resource_client = resorce_client

    def __validations(self):
        if not self._testing_class:
            raise Exception("Mocks are not configured, you must call 'configure_mocks' before running this test.")

        if not self._resource_client:
            raise Exception(
                "Mock for the client not configured, you must call 'configure_client_mock' before running this test.")

    def test_should_get_all_using_filters(self):
        self.__validations()
        self._resource_client.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None,
            params={
                'start': 1,
                'count': 3,
                'sort': 'name:descending',
                'filter': 'purpose=General',
                'query': 'imported eq true'
            })
        self.mock_ansible_module.params = params_get_all_with_filters

        self._testing_class().run()

        self._resource_client.get_all.assert_called_once_with(start=1, count=3, sort='name:descending',
                                                              filter='purpose=General',
                                                              query='imported eq true')

    def test_should_get_all_without_params(self):
        self.__validations()
        self._resource_client.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None
        )
        self.mock_ansible_module.params = params_get_all_with_filters

        self._testing_class().run()

        self._resource_client.get_all.assert_called_once_with()


class ErrorHandlingTestCase(PreloadedMocksBaseTestCase):
    """
    ErrorHandlingTestCase has common test for the modules error handling.
    """
    params_present = dict(
        config='config.json',
        state='present',
        data=dict(name='Resource Identifier'))

    error_message = 'Fake message error'

    def configure_client_mock(self, resorce_client):
        """
        Args:
             resorce_client: Resource client that is being called
        """
        self._resource_client = resorce_client

    def test_should_call_fail_json_when_oneview_exception(self):
        self.mock_ansible_module.params = self.params_present
        fake_exception = Mock(side_effect=HPOneViewException(self.error_message))
        self.mock_possible_calls_for_present(fake_exception)

        self._testing_class().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=self.error_message)

    def test_should_not_handle_value_error_exception(self):
        self.mock_ansible_module.params = self.params_present
        fake_exception = Mock(side_effect=ValueError(self.error_message))
        self.mock_possible_calls_for_present(fake_exception)

        try:
            self._testing_class().run()
        except ValueError as e:
            self.assertEqual(e.args[0], self.error_message)
        else:
            self.fail('Expected ValueError was not raised')

    def test_should_not_handle_exception(self):
        self.mock_ansible_module.params = self.params_present
        self.mock_possible_calls_for_present(Mock(side_effect=Exception(self.error_message)))

        try:
            self._testing_class().run()
        except Exception as e:
            self.assertEqual(e.args[0], self.error_message)
        else:
            self.fail('Expected Exception was not raised')

    def mock_possible_calls_for_present(self, side_effect):
        self._resource_client.get.side_effect = side_effect
        self._resource_client.get_all.side_effect = side_effect
        self._resource_client.get_by.side_effect = side_effect
        self._resource_client.get_by_name.side_effect = side_effect
        self._resource_client.create.side_effect = side_effect
        self._resource_client.add.side_effect = side_effect
        self._resource_client.update.side_effect = side_effect
