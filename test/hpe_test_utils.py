#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import importlib
import pytest
import re
import yaml

from mock import mock
from oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH
from hpOneView.oneview_client import OneViewClient


class OneViewBaseTest(object):
    @pytest.fixture(autouse=True)
    def setUp(self, mock_ansible_module, mock_ov_client, request):
        class_name = type(self).__name__
        marker = request.node.get_marker('resource')
        self.resource = getattr(mock_ov_client, "%s" % (marker.kwargs[class_name]))
        self.mock_ov_client = mock_ov_client
        self.mock_ansible_module = mock_ansible_module

    @pytest.fixture
    def testing_module(self):
        resource_name = type(self).__name__.replace('Test', '')
        resource_module_path_name = self.underscore(resource_name.replace('Module', ''))

        testing_module = importlib.import_module('library.' + resource_module_path_name)
        self.testing_class = getattr(testing_module, resource_name)
        try:
            # Load scenarios from module examples (Also checks if it is a valid yaml)
            self.EXAMPLES = yaml.load(testing_module.EXAMPLES, yaml.SafeLoader)

        except yaml.scanner.ScannerError:
            message = "Something went wrong while parsing yaml from {}.EXAMPLES".format(self.testing_class.__module__)
            raise Exception(message)
        return testing_module

    def underscore(self, word):
        word = re.findall('[A-Z][^A-Z]*', word)
        word = 'oneview_' + str.join('_', word).lower()
        return word

    def test_main_function_should_call_run_method(self, testing_module, mock_ansible_module):
        mock_ansible_module.params = {'config': 'config.json'}

        main_func = getattr(testing_module, 'main')

        with mock.patch.object(self.testing_class, "run") as mock_run:
            main_func()
            mock_run.assert_called_once()


class OneViewBaseFactsTest(OneViewBaseTest):
    def test_should_get_all_using_filters(self, testing_module):
        self.resource.get_all.return_value = []

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

        self.testing_class().run()

        self.resource.get_all.assert_called_once_with(start=1, count=3, sort='name:descending', filter='purpose=General', query='imported eq true')

    def test_should_get_all_without_params(self, testing_module):
        self.resource.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None
        )
        self.mock_ansible_module.params = params_get_all_with_filters

        self.testing_class().run()

        self.resource.get_all.assert_called_once_with()


class OneViewBaseTestCase(object):
    mock_ov_client_from_json_file = None
    testing_class = None
    mock_ansible_module = None
    mock_ov_client = None
    testing_module = None
    EXAMPLES = None

    def configure_mocks(self, test_case, testing_class):
        """
        Preload mocked OneViewClient instance and AnsibleModule
        Args:
            test_case (object): class instance (self) that are inheriting from OneViewBaseTestCase
            testing_class (object): class being tested
        """
        self.testing_class = testing_class

        # Define OneView Client Mock (FILE)
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        test_case.addCleanup(patcher_json_file.stop)
        self.mock_ov_client_from_json_file = patcher_json_file.start()

        # Define OneView Client Mock
        self.mock_ov_client = self.mock_ov_client_from_json_file.return_value

        # Define Ansible Module Mock
        patcher_ansible = mock.patch(ONEVIEW_MODULE_UTILS_PATH + '.AnsibleModule')
        test_case.addCleanup(patcher_ansible.stop)
        mock_ansible_module = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_module

        self._set_module_examples()

    def test_main_function_should_call_run_method(self):
        self.mock_ansible_module.params = {'config': 'config.json'}

        main_func = getattr(self.testing_module, 'main')

        with mock.patch.object(self.testing_class, "run") as mock_run:
            main_func()
            mock_run.assert_called_once_with()

    def _set_module_examples(self):
        self.testing_module = importlib.import_module(self.testing_class.__module__)

        try:
            # Load scenarios from module examples (Also checks if it is a valid yaml)
            self.EXAMPLES = yaml.load(self.testing_module.EXAMPLES, yaml.SafeLoader)

        except yaml.scanner.ScannerError:
            message = "Something went wrong while parsing yaml from {}.EXAMPLES".format(self.testing_class.__module__)
            raise Exception(message)


class FactsParamsTestCase(OneViewBaseTestCase):
    """
    FactsParamsTestCase has common test for classes that support pass additional
        parameters when retrieving all resources.
    """

    def configure_client_mock(self, resorce_client):
        """
        Args:
             resorce_client: Resource client that is being called
        """
        self.resource_client = resorce_client

    def __validations(self):
        if not self.testing_class:
            raise Exception("Mocks are not configured, you must call 'configure_mocks' before running this test.")

        if not self.resource_client:
            raise Exception(
                "Mock for the client not configured, you must call 'configure_client_mock' before running this test.")

    def test_should_get_all_using_filters(self):
        self.__validations()
        self.resource_client.get_all.return_value = []

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

        self.testing_class().run()

        self.resource_client.get_all.assert_called_once_with(start=1, count=3, sort='name:descending',
                                                             filter='purpose=General',
                                                             query='imported eq true')

    def test_should_get_all_without_params(self):
        self.__validations()
        self.resource_client.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None
        )
        self.mock_ansible_module.params = params_get_all_with_filters

        self.testing_class().run()

        self.resource_client.get_all.assert_called_once_with()
