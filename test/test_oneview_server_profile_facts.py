#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import ServerProfileFactsModule

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

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/fake"
)
PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Server Profile",
    options=[
        'schema',
        'compliancePreview',
        'newProfileTemplate',
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


@pytest.mark.resource(TestServerProfileFactsModule='server_profiles')
class TestServerProfileFactsModule(OneViewBaseFactsTest):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def test_should_get_all_servers(self):
        server_profiles = [
            {"name": "Server Profile Name 1"},
            {"name": "Server Profile Name 2"}
        ]
        self.mock_ov_client.server_profiles.get_all.return_value = server_profiles

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_ALL)

        ServerProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profiles=server_profiles)
        )

    def test_should_get_by_name(self):
        servers = {"name": "Server Profile Name", 'uri': '/rest/test/123'}
        obj = mock.Mock()
        obj.data = servers
        self.mock_ov_client.server_profiles.get_by_name.return_value = obj

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_BY_NAME)

        ServerProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profiles=[servers])
        )

    def test_should_get_by_uri(self):
        server_profile = {"name": "Server Profile Name", 'uri': '/rest/test/123'}
        obj = mock.Mock()
        obj.data = server_profile
        self.mock_ov_client.server_profiles.get_by_uri.return_value = obj

        self.mock_ansible_module.params = deepcopy(PARAMS_GET_BY_URI)

        ServerProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profiles=[server_profile])
        )

    def test_should_get_server_profile_by_name_with_all_options(self):
        mock_option_return = {'subresource': 'value'}
        self.mock_ov_client.server_profiles.data =  {"name": "Server Profile Name", "uri": PROFILE_URI}
        self.mock_ov_client.server_profiles.get_by_name.return_value = self.mock_ov_client.server_profiles
        self.mock_ov_client.server_profiles.get_messages.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_transformation.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_compliance_preview.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_new_profile_template.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_schema.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_profile_ports.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_networks.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_servers.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_storage_system.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_storage_systems.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_targets.return_value = mock_option_return

        self.mock_ansible_module.params = deepcopy(PARAMS_WITH_OPTIONS)

        ServerProfileFactsModule().run()

        self.mock_ov_client.server_profiles.get_messages.assert_called_once_with()
        self.mock_ov_client.server_profiles.get_transformation.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI,
            serverHardwareUri=HARDWARE_URI)
        self.mock_ov_client.server_profiles.get_compliance_preview.assert_called_once_with()
        self.mock_ov_client.server_profiles.get_new_profile_template.assert_called_once_with()
        self.mock_ov_client.server_profiles.get_schema.assert_called_once_with()
        self.mock_ov_client.server_profiles.get_profile_ports.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, serverHardwareUri=HARDWARE_URI, )
        self.mock_ov_client.server_profiles.get_available_networks.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, serverHardwareUri=HARDWARE_URI, view='FibreChannel')
        self.mock_ov_client.server_profiles.get_available_servers.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, profileUri=PROFILE_URI)
        self.mock_ov_client.server_profiles.get_available_storage_system.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI,
            serverHardwareTypeUri=HARDWARE_TYPE_URI, storageSystemId=STORAGE_SYSTEM_ID)
        self.mock_ov_client.server_profiles.get_available_storage_systems.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI, start=1, count=15,
            filter="\"'status'='OK'\"", sort="name:ascending")
        self.mock_ov_client.server_profiles.get_available_servers.assert_called_once_with(
            enclosureGroupUri=ENCLOSURE_GROUP_URI, profileUri=PROFILE_URI, serverHardwareTypeUri=HARDWARE_TYPE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_profiles': [{'name': 'Server Profile Name', 'uri': PROFILE_URI}],
                           'server_profile_schema': mock_option_return,
                           'server_profile_compliance_preview': mock_option_return,
                           'server_profile_new_profile_template': mock_option_return,
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

    def test_should_get_all_server_profiles_with_options(self):
        mock_option_return = {'subresource': 'value'}

        params_get_all_options = deepcopy(PARAMS_WITH_OPTIONS)
        del params_get_all_options['name']

        self.mock_ov_client.server_profiles.get_all.return_value = [{"name": "Server Profile Name", "uri": PROFILE_URI}]

        self.mock_ov_client.server_profiles.get_schema.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_profile_ports.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_networks.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_servers.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_storage_system.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_storage_systems.return_value = mock_option_return
        self.mock_ov_client.server_profiles.get_available_targets.return_value = mock_option_return

        self.mock_ansible_module.params = deepcopy(params_get_all_options)

        ServerProfileFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
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

    def test_should_get_server_profiles_with_invalid_profile_ports_option(self):
        mock_option_return = {'subresource': 'value'}

        obj = mock.Mock()
        obj.data = {"name": "Server Profile Name", "uri": PROFILE_URI}
        self.mock_ov_client.server_profiles.get_by_name.return_value = obj
        self.mock_ov_client.server_profiles.get_profile_ports.return_value = mock_option_return

        self.mock_ansible_module.params = dict(
            config='config.json',
            name="Test Server Profile",
            options=[
                {'profilePorts': [1]}
            ])

        ServerProfileFactsModule().run()

        self.mock_ov_client.server_profiles.get_profile_ports.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_profiles': [{'name': 'Server Profile Name', 'uri': PROFILE_URI}],
                           'server_profile_profile_ports': mock_option_return,
                           }
        )


if __name__ == '__main__':
    pytest.main([__file__])
