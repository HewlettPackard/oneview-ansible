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

import pytest
import mock

from copy import deepcopy
from hpe_test_utils import OneViewBaseFactsTest
from oneview_module_loader import HypervisorClusterProfileFactsModule

PROFILE_URI = '/rest/hypervisor-cluster-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea4d'

PARAMS_GET_ALL = dict(
    config='config.json'
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Cluster Profile"
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/test/123"
)
PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Cluster Profile",
    options=[
        'compliancePreview',
    ]
)


@pytest.mark.resource(TestHypervisorClusterProfileFactsModule='hypervisor_cluster_profiles')
class TestHypervisorClusterProfileFactsModule(OneViewBaseFactsTest):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def test_should_get_all_cluster_profiles(self):
        cluster_profiles = [
            {"name": "Cluster Profile Name 1"},
            {"name": "Cluster Profile Name 2"}
        ]
        self.mock_ov_client.hypervisor_cluster_profiles.get_all.return_value = cluster_profiles

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_ALL)

        HypervisorClusterProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_cluster_profiles=cluster_profiles)
        )

    def test_should_get_by_name(self):
        profile = {"name": "Test Cluster Profile", 'uri': '/rest/test/123'}
        obj = mock.Mock()
        obj.data = profile
        self.mock_ov_client.hypervisor_cluster_profiles.get_by_name.return_value = obj

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_BY_NAME)

        HypervisorClusterProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_cluster_profiles=[profile])
        )

    def test_should_get_by_uri(self):
        cluster_profile = {"name": "Test Cluster Profile", 'uri': '/rest/test/123'}
        obj = mock.Mock()
        obj.data = cluster_profile
        self.mock_ov_client.hypervisor_cluster_profiles.get_by_uri.return_value = obj

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_BY_URI)

        HypervisorClusterProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_cluster_profiles=[cluster_profile])
        )

    def test_should_get_cluster_profile_by_name_with_all_options(self):
        mock_option_return = {'subresource': 'value'}
        self.mock_ov_client.hypervisor_cluster_profiles.data = {"name": "Test Cluster Profile", "uri": PROFILE_URI}
        self.mock_ov_client.hypervisor_cluster_profiles.get_by_name.return_value = \
            self.mock_ov_client.hypervisor_cluster_profiles
        self.mock_ov_client.hypervisor_cluster_profiles.get_compliance_preview.return_value = mock_option_return

        self.mock_ansible_module.params = deepcopy(PARAMS_WITH_OPTIONS)

        HypervisorClusterProfileFactsModule().run()

        self.mock_ov_client.hypervisor_cluster_profiles.get_compliance_preview.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'hypervisor_cluster_profiles': [{'name': 'Test Cluster Profile', 'uri': PROFILE_URI}],
                           'hypervisor_cluster_profile_compliance_preview': mock_option_return,
                           }
        )


if __name__ == '__main__':
    pytest.main([__file__])
