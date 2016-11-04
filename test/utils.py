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
    def create_common_mocks(self, test_module):
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
