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
from oneview_server_profile_facts import ServerProfileFactsModule
from copy import deepcopy

ERROR_MSG = 'Fake message error'
ENCLOSURE_GROUP_URI = '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
HARDWARE_TYPE_URI = '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
HARDWARE_URI = '/rest/server-hardware/C8DEF9A6-9586-465E-A951-3070988BC226'
PROFILE_URI = '/rest/server-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea4d'
STORAGE_SYSTEM_ID = "TXQ1010307"

PARAMS_GET_ALL = dict(
    config='config.json'
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Server Profile"
)

PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Server Profile",
    options=[
        'schema',
        'compliancePreview',
        {'profilePorts': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'serverHardwareUri': HARDWARE_URI,
        }
        },
        'messages',
        {'transformation': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'serverHardwareUri': HARDWARE_URI,
        }
        },
        {'availableNetworks': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'serverHardwareUri': HARDWARE_URI,
            'view': 'FibreChannel'
        }
        },
        {'availableServers': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'profileUri': PROFILE_URI
        }
        },
        {'availableStorageSystem': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'storageSystemId': STORAGE_SYSTEM_ID
        }
        },
        {'availableStorageSystems': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'start': 1,
            'count': 15,
            'filter': "\"'status'='OK'\"",
            'sort': 'name:ascending'
        }
        },
        {'availableTargets': {
            'enclosureGroupUri': ENCLOSURE_GROUP_URI,
            'serverHardwareTypeUri': HARDWARE_TYPE_URI,
            'profileUri': PROFILE_URI
        }
        }
    ]
)


def create_ansible_mock(dict_params):
    mock_ansible = mock.Mock()
    mock_ansible.params = dict_params
    return mock_ansible


class ServerHardwareFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_get_all_servers(self, mock_ansible_module, mock_ov_client_from_json_file):
        server_profiles = [
            {"name": "Server Profile Name 1"},
            {"name": "Server Profile Name 2"}
        ]
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_all.return_value = server_profiles

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profiles=server_profiles)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_get_by_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        servers = [{"name": "Server Profile Name", 'uri': '/rest/test/123'}]
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_by.return_value = servers

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profiles=servers)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_get_server_profile_by_name_with_all_options(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_option_return = {'subresource': 'value'}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_by.return_value = [{"name": "Server Profile Name", "uri": PROFILE_URI}]
        mock_ov_instance.server_profiles.get_messages.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_transformation.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_compliance_preview.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_schema.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_profile_ports.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_networks.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_servers.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_storage_system.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_storage_systems.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_targets.return_value = mock_option_return

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ov_instance.server_profiles.get_messages.assert_called_once_with(PROFILE_URI)
        mock_ov_instance.server_profiles.get_transformation.assert_called_once_with(
            PROFILE_URI, enclosureGroupUri=ENCLOSURE_GROUP_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI,
            serverHardwareUri=HARDWARE_URI)
        mock_ov_instance.server_profiles.get_compliance_preview.assert_called_once_with(PROFILE_URI)
        mock_ov_instance.server_profiles.get_schema.assert_called_once_with()
        mock_ov_instance.server_profiles.get_profile_ports.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, serverHardwareUri=HARDWARE_URI, )
        mock_ov_instance.server_profiles.get_available_networks.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, serverHardwareUri=HARDWARE_URI, view='FibreChannel')
        mock_ov_instance.server_profiles.get_available_servers.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, profileUri=PROFILE_URI)
        mock_ov_instance.server_profiles.get_available_storage_system.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, storageSystemId=STORAGE_SYSTEM_ID)
        mock_ov_instance.server_profiles.get_available_storage_systems.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI, start=1, count=15,
            filter="\"'status'='OK'\"", sort="name:ascending")
        mock_ov_instance.server_profiles.get_available_targets.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI, profileUri=PROFILE_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_profiles': [{'name': 'Server Profile Name', 'uri': PROFILE_URI}],
                           'server_profile_schema': mock_option_return,
                           'server_profile_compliance_preview': mock_option_return,
                           'server_profile_profile_ports': mock_option_return,
                           'server_profile_messages': mock_option_return,
                           'server_profile_transformation': mock_option_return,
                           'server_profile_available_networks': mock_option_return,
                           'server_profile_available_servers': mock_option_return,
                           'server_profile_available_storage_system': mock_option_return,
                           'server_profile_available_storage_systems': mock_option_return,
                           'server_profile_available_targets': mock_option_return,
                           }
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_get_all_server_profiles_with_options(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_option_return = {'subresource': 'value'}

        params_get_all_options = deepcopy(PARAMS_WITH_OPTIONS)
        del params_get_all_options['name']

        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_all.return_value = [{"name": "Server Profile Name", "uri": PROFILE_URI}]

        mock_ov_instance.server_profiles.get_schema.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_profile_ports.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_networks.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_servers.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_storage_system.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_storage_systems.return_value = mock_option_return
        mock_ov_instance.server_profiles.get_available_targets.return_value = mock_option_return

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(params_get_all_options)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_profiles': [{'name': 'Server Profile Name', 'uri': PROFILE_URI}],
                           'server_profile_schema': mock_option_return,
                           'server_profile_profile_ports': mock_option_return,
                           'server_profile_available_networks': mock_option_return,
                           'server_profile_available_servers': mock_option_return,
                           'server_profile_available_storage_system': mock_option_return,
                           'server_profile_available_storage_systems': mock_option_return,
                           'server_profile_available_targets': mock_option_return,
                           }
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profiles.get_by.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
