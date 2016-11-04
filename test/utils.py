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

import mock
import yaml
import unittest
from mock import patch
from hpOneView.oneview_client import OneViewClient


def create_ansible_mock(params):
    mock_ansible = mock.Mock()
    mock_ansible.params = params
    return mock_ansible


def create_ansible_mock_yaml(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class PreloadedMocksTestCase(unittest.TestCase):
    def configure_mocks(self, test_module):
        """
        Preload mocked OneViewClient instance and AnsibleModule
        Args:
            test_module (str): module name being tested
        """
        # Define One View Client Mock
        patcher = patch.object(OneViewClient, 'from_json_file')
        self.addCleanup(patcher.stop)
        mock_from_json_file = patcher.start()
        mock_from_json_file.return_value = mock.Mock()
        self.mock_ov_client = mock_from_json_file.return_value

        # Define Ansible Module Mock
        patcher_ansible = patch(test_module + '.AnsibleModule')
        self.addCleanup(patcher_ansible.stop)
        mock_ansible_module = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_module


class ModuleContructorTestCase():
    _testing_class = None

    def configure_mocks(self, test_module, testing_class):
        """
        Preload mocked OneViewClient instance and AnsibleModule
        Args:
            test_module (str): module name being tested
        """
        self.__testing_module = test_module

        # Define One View Client Mock (FILE)
        patcher = patch.object(OneViewClient, 'from_json_file')
        self.addCleanup(patcher.stop)
        self.mock_ov_client_from_json_file = patcher.start()

        # Define One View Client Mock (ENV)
        patcher = patch.object(OneViewClient, 'from_environment_variables')
        self.addCleanup(patcher.stop)
        self.mock_ov_client_from_env_vars = patcher.start()

        # Define Ansible Module Mock
        patcher_ansible = patch(test_module + '.AnsibleModule')
        self.addCleanup(patcher_ansible.stop)
        mock_ansible_module = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        mock_ansible_module.return_value = self.mock_ansible_module

        self._testing_class = testing_class

    def __valitations(self):
        if not self._testing_class:
            self.fail("Mocks are not configured, you must call 'configure_mocks' before running this test")

    def test_should_load_config_from_file(self):
        self.__valitations()

        self.mock_ansible_module.params = {'config': 'config.json'}

        # Call the constructor
        self._testing_class()

        self.mock_ov_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ov_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):
        self.__valitations()

        self.mock_ansible_module.params = {'config': None}

        # Call the constructor
        self._testing_class()

        self.mock_ov_client_from_env_vars.assert_called_once()
        self.mock_ov_client_from_json_file.not_been_called()

    def test_should_call_fail_json_when_not_have_oneview(self):
        self.__valitations()
        self.mock_ansible_module.params = {'config': 'config.json'}

        with mock.patch(self.__testing_module + ".HAS_HPE_ONEVIEW", False):
            with mock.patch(self.__testing_module + ".HPE_ONEVIEW_SDK_REQUIRED", "SDK NEEDED"):
                self._testing_class()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg="SDK NEEDED")

    def test_main_function_should_call_run_method(self):
        self.__valitations()
        self.mock_ansible_module.params = {'config': 'config.json'}

        module = __import__(self.__testing_module)
        main_func = getattr(module, 'main')

        with mock.patch.object(self._testing_class, "run") as mock_run:
            main_func()
            mock_run.assert_called_once()
