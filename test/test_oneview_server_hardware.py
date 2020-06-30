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
import pytest
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import ServerHardwareModule

FAKE_MSG_ERROR = 'Fake message error'

YAML_SERVER_HARDWARE_PRESENT = """
        config: "{{ config }}"
        state: present
        data:
             hostname : "172.18.6.15"
             username : "dcs"
             password : "dcs"
             force : false
             licensingIntent: "OneView"
             configurationState: "Managed"
          """

YAML_SERVER_HARDWARE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_ADD_MULTIPLE_SERVERS = """
        config: "{{ config }}"
        state: multiple_servers_added
        data:
            mpHostsAndRanges :
              - '172.18.6.15'
            username : 'dcs'
            password : 'dcs'
            initialScopeUris:
              - "/rest/scopes/01SC123456"
            licensingIntent: "OneView"
            configurationState: "Managed"
            """

YAML_SERVER_HARDWARE_POWER_STATE = """
        config: "{{ config }}"
        state: power_state_set
        data:
            name : "172.18.6.15"
            powerStateData:
                powerState: "On"
                powerControl: "MomentaryPress"
"""

YAML_SERVER_HARDWARE_REFRESH_STATE = """
        config: "{{ config }}"
        state: refresh_state_set
        data:
            name : "172.18.6.15"
            refreshStateData:
                refreshState : "RefreshPending"
"""

YAML_SERVER_HARDWARE_ILO_FIRMWARE = """
        config: "{{ config }}"
        state: ilo_firmware_version_updated
        data:
            name : '{{ server_hardware_name }}'
"""

YAML_SERVER_HARDWARE_SET_CALIBRATED_MAX_POWER = """
    config: "{{ config }}"
    state: environmental_configuration_set
    data:
        name : "172.18.6.15"
        environmentalConfigurationData:
            calibratedMaxPower: 2500
"""

YAML_SERVER_HARDWARE_ILO_STATE_RESET = """
        config: config
        state: ilo_state_reset
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_UID_STATE_ON = """
        config: config
        state: uid_state_on
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_UID_STATE_OFF = """
        config: config
        state: uid_state_off
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NORMAL = """
        config: config
        state: one_time_boot_normal
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_CDROM = """
        config: config
        state: one_time_boot_cdrom
        data:
            name : "172.18.6.15"
"""
YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_USB = """
        config: config
        state: one_time_boot_usb
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_HDD = """
        config: config
        state: one_time_boot_hdd
        data:
            name : "172.18.6.15"
"""

YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NETWORK = """
        config: config
        state: one_time_boot_network
        data:
            name : "172.18.6.15"
"""

SERVER_HARDWARE_HOSTNAME = "172.18.6.15"

DICT_DEFAULT_SERVER_HARDWARE = yaml.load(YAML_SERVER_HARDWARE_PRESENT)["data"]


@pytest.mark.resource(TestServerHardwareModule='server_hardware')
class TestServerHardwareModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_add_new_server_hardware(self):
        self.resource.get_by_name.return_value = []
        self.resource.data = {"name": "name"}
        self.resource.add.return_value = self.resource

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_PRESENT)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ADDED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_not_add_when_it_already_exists(self):
        self.resource.data = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_PRESENT)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_add_multiple_servers(self):
        self.resource.get_by_name.return_value = None
        self.resource.data = {'name': 'name'}

        self.resource.add_multiple_servers.return_value = self.resource

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ADD_MULTIPLE_SERVERS)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_MULTIPLE_RACK_MOUNT_SERVERS_ADDED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_calibrate_max_power_server_hardware(self):
        self.resource.data = [{"name": "name", "uri": "uri"}]

        self.resource.update_environmental_configuration.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_SET_CALIBRATED_MAX_POWER)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ENV_CONFIG_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_present_should_fail_with_missing_hostname_attribute(self):
        self.mock_ansible_module.params = {"state": "present",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid"}}

        ServerHardwareModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=ServerHardwareModule.MSG_MANDATORY_FIELD_MISSING.format('data.hostname'))

    def test_should_fail_with_missing_name_attribute(self):
        self.mock_ansible_module.params = {"state": "absent",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid"}}

        ServerHardwareModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=ServerHardwareModule.MSG_MANDATORY_FIELD_MISSING.format(
                                                                       'data.name'))

    def test_should_remove_server_hardware(self):
        self.resource.data = {'name': 'name'}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ABSENT)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_DELETED
        )

    def test_should_do_nothing_when_server_hardware_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ABSENT)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_ALREADY_ABSENT
        )

    def test_should_set_power_state(self):
        self.resource.data = {"uri": "resourceuri"}
        self.resource.update_power_state.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_POWER_STATE)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_POWER_STATE_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_fail_when_set_power_state_and_server_hardware_was_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_POWER_STATE)

        ServerHardwareModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=ServerHardwareModule.MSG_SERVER_HARDWARE_NOT_FOUND)

    def test_should_set_refresh_state(self):
        self.resource.data = {"uri": "resourceuri"}
        self.resource.refresh_state.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_REFRESH_STATE)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_REFRESH_STATE_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_fail_when_set_refresh_state_and_server_hardware_was_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_REFRESH_STATE)

        ServerHardwareModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=ServerHardwareModule.MSG_SERVER_HARDWARE_NOT_FOUND)

    def test_should_set_ilo_firmware(self):
        self.resource.data = {"uri": "resourceuri"}
        self.resource.update_mp_firware_version.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ILO_FIRMWARE)

        ServerHardwareModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ILO_FIRMWARE_VERSION_UPDATED,
            ansible_facts=dict(server_hardware={"name": "name"})
        )

    def test_should_fail_when_set_ilo_firmware_and_server_hardware_was_not_found(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ILO_FIRMWARE)

        ServerHardwareModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=ServerHardwareModule.MSG_SERVER_HARDWARE_NOT_FOUND)

    def test_should_reset_ilo_state(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ILO_STATE_RESET)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['ilo_state_reset']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ILO_STATE_RESET,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_set_on_the_uid_state(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "uidState": "Off"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_UID_STATE_ON)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['uid_state_on']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_UID_STATE_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_the_uid_state_is_already_on(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "uidState": "On"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_UID_STATE_ON)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_should_set_off_the_uid_state(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "uidState": "On"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_UID_STATE_OFF)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['uid_state_off']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_UID_STATE_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_the_uid_state_is_already_off(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "uidState": "Off"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_UID_STATE_OFF)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_update_scopes_when_different(self):
        params_to_scope = yaml.load(YAML_SERVER_HARDWARE_PRESENT).copy()
        params_to_scope['data']['scopeUris'] = ['/fake/test']
        get_results = params_to_scope['data'].copy()
        get_results['password'] = None
        get_results['scopeUris'] = []
        get_results['uri'] = '/rest/server-hardware/fake'
        self.mock_ansible_module.params = params_to_scope

        self.resource.data = get_results
        obj = mock.Mock()
        obj.data = params_to_scope['data']
        self.resource.patch.return_value = obj

        ServerHardwareModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['/fake/test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(server_hardware=params_to_scope['data']),
            msg=ServerHardwareModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = yaml.load(YAML_SERVER_HARDWARE_PRESENT).copy()
        params_to_scope['data']['scopeUris'] = ['/fake/test']
        get_results = params_to_scope['data'].copy()
        get_results['password'] = None
        self.mock_ansible_module.params = params_to_scope

        self.resource.data = get_results

        ServerHardwareModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardware=get_results),
            msg=ServerHardwareModule.MSG_ALREADY_PRESENT
        )

    def test_should_set_one_time_boot_to_normal(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "oneTimeBoot": "NETWORK"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NORMAL)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['one_time_boot_normal']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ONE_TIME_BOOT_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_one_time_boot_is_already_normal(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "oneTimeBoot": "NORMAL"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NORMAL)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_should_set_one_time_boot_to_cdrom(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "oneTimeBoot": "NORMAL"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_CDROM)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['one_time_boot_cdrom']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ONE_TIME_BOOT_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_one_time_boot_is_already_cdrom(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "oneTimeBoot": "CDROM"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_CDROM)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_should_set_one_time_boot_to_usb(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "oneTimeBoot": "NORMAL"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_USB)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['one_time_boot_usb']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ONE_TIME_BOOT_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_one_time_boot_is_already_usb(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "oneTimeBoot": "USB"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_USB)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_should_set_one_time_boot_to_hdd(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "oneTimeBoot": "NORMAL"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_HDD)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['one_time_boot_hdd']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ONE_TIME_BOOT_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_one_time_boot_is_already_hdd(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "oneTimeBoot": "HDD"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_HDD)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )

    def test_should_set_one_time_boot_to_network(self):
        server_hardware_uri = "resourceuri"

        self.resource.data = {"uri": server_hardware_uri, "oneTimeBoot": "NORMAL"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NETWORK)

        ServerHardwareModule().run()

        patch_params = ServerHardwareModule.patch_params['one_time_boot_network']
        self.resource.patch.assert_called_once_with(**patch_params)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareModule.MSG_ONE_TIME_BOOT_CHANGED,
            ansible_facts=dict(server_hardware=self.resource.data)
        )

    def test_should_not_set_when_one_time_boot_is_already_network(self):
        server_hardware_uri = "resourceuri"
        server_hardware = {"uri": server_hardware_uri, "oneTimeBoot": "NETWORK"}

        self.resource.data = server_hardware

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_ONE_TIME_BOOT_AS_NETWORK)

        ServerHardwareModule().run()

        self.resource.patch.assert_not_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(server_hardware=server_hardware)
        )


if __name__ == '__main__':
    pytest.main([__file__])
