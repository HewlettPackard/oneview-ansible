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
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_interconnect_link_topology_facts import InterconnectLinkTopologyFactsModule
from test.utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Interconnect Link Topology Name 2"
)

INTERCONNECT_LINK_TOPOLOGIES = [{"name": "Interconnect Link Topology 1"},
                                {"name": "Interconnect Link Topology 2"},
                                {"name": "Interconnect Link Topology 3"}]


class InterconnectLinkTopologyFactsClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class InterconnectLinkTopologyFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_get_all_interconnect_link_topologies(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_link_topologies.get_all.return_value = INTERCONNECT_LINK_TOPOLOGIES

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=(INTERCONNECT_LINK_TOPOLOGIES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_link_topologies.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_get_all_interconnect_link_topology_by_name(self, mock_ansible_module,
                                                               mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_link_topologies.get_by.return_value = [INTERCONNECT_LINK_TOPOLOGIES[1]]

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=([INTERCONNECT_LINK_TOPOLOGIES[1]]))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_link_topology_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnect_link_topologies.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectLinkTopologyFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
