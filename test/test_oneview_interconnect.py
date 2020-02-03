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

import mock
import pytest

from copy import deepcopy
from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import InterconnectModule


def create_params_for(power_state):
    return dict(
        config='config.json',
        state=power_state,
        name='Encl1, interconnect 1',
        ip=None
    )


FAKE_URI = "/rest/interconnects/748d4699-62ff-454e-8ec8-773815c4aa2f"

INTERCONNECT_IP = '172.18.1.114'

INTERCONNECT_ID = "748d4699-62ff-454e-8ec8-773815c4aa2f"

PORT_D1 = {
    "type": "port",
    "portName": "d1",
    "bayNumber": 1,
    "enabled": False,
    "portId": "{0}:d1".format(INTERCONNECT_ID)
}

PORT_D2 = {
    "portName": "d2",
    "enabled": False,
    "portId": "{0}:d2".format(INTERCONNECT_ID)
}

PORTS_FOR_UPDATE = [PORT_D1, PORT_D2]

PARAMS_FOR_RESET_DEVICE_BY_IP = dict(
    config='config.json',
    state='device_reset',
    name=None,
    ip=INTERCONNECT_IP
)

PARAMS_FOR_UPDATE_PORTS = dict(
    config='config.json',
    state='update_ports',
    name=None,
    ip=INTERCONNECT_IP,
    ports=PORTS_FOR_UPDATE
)

PARAMS_FOR_RESET_PORT_PROTECTION = dict(
    config='config.json',
    state='reset_port_protection',
    name=None,
    ip=INTERCONNECT_IP
)

PARAMS_FOR_UPDATE_CONFIGURATION = dict(
    config='config.json',
    state='reconfigured',
    name=None,
    ip=INTERCONNECT_IP
)

FAKE_INTERCONNECT = dict(uri=FAKE_URI)


@pytest.mark.resource(TestInterconnectModule='interconnects')
class TestInterconnectModule(OneViewBaseTest):
    def test_should_ensure_powered_on_state(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.data = dict(powerState='Off', uri=FAKE_URI)
        self.resource.get_by_uri.return_value = self.resource

        FAKE_INTERCONNECT_updated = dict(powerState='On')
        obj = self.resource.copy()
        obj.data = FAKE_INTERCONNECT_updated
        self.resource.patch.return_value = obj

        InterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/powerState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_POWERED_ON,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT_updated)
        )

    def test_should_return_changed_false_when_interconnect_is_already_powered_on(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        FAKE_INTERCONNECT = dict(powerState='On')
        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=InterconnectModule.MSG_ALREADY_POWERED_ON,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_ensure_powered_off_state(self):
        ansible_arguments = create_params_for('powered_off')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.data = dict(powerState='On', uri=FAKE_URI)
        self.resource.get_by_uri.return_value = self.resource

        FAKE_INTERCONNECT_updated = dict(powerState='Off')
        obj = self.resource.copy()
        obj.data = FAKE_INTERCONNECT_updated
        self.resource.patch.return_value = obj

        InterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/powerState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_POWERED_OFF,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT_updated)
        )

    def test_should_return_changed_false_when_interconnect_is_already_powered_off(self):
        ansible_arguments = create_params_for('powered_off')
        self.mock_ansible_module.params = ansible_arguments

        FAKE_INTERCONNECT = dict(powerState='Off')
        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=InterconnectModule.MSG_ALREADY_POWERED_OFF,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_ensure_uid_on_state(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        FAKE_INTERCONNECT = dict(uidState='Off', uri=FAKE_URI)
        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        FAKE_INTERCONNECT_updated = dict(uidState='On')
        obj = self.resource.copy()
        obj.data = FAKE_INTERCONNECT_updated
        self.resource.patch.return_value = obj

        InterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/uidState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_UID_STATE_ON,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT_updated)
        )

    def test_should_return_changed_false_when_uid_is_already_on(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        FAKE_INTERCONNECT = dict(uidState='On')
        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=InterconnectModule.MSG_UID_STATE_ALREADY_ON,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_ensure_uid_off_state(self):
        ansible_arguments = create_params_for('uid_off')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.data = dict(uidState='On', uri=FAKE_URI)
        self.resource.get_by_uri.return_value = self.resource

        FAKE_INTERCONNECT_updated = dict(uidState='Off')
        obj = self.resource.copy()
        obj.data = FAKE_INTERCONNECT_updated
        self.resource.patch.return_value = obj

        InterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/uidState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_UID_STATE_OFF,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT_updated)
        )

    def test_should_return_changed_false_when_uid_is_already_off(self):
        ansible_arguments = create_params_for('uid_off')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.data = dict(uidState='Off')
        self.resource.get_by_uri.return_value = self.resource

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=InterconnectModule.MSG_UID_STATE_ALREADY_OFF,
            ansible_facts=dict(interconnect=self.resource.data)
        )

    def test_should_ensure_device_reset(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.patch.return_value = self.resource

        InterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/deviceResetState',
            value='Reset'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_RESET,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_fail_when_interconnect_was_not_found(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        self.resource.get_by_uri.return_value = []
        self.resource.get_by_name.return_value = []

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=InterconnectModule.MSG_INTERCONNECT_NOT_FOUND)

    def test_should_ensure_device_reset_by_ip_address(self):
        self.mock_ansible_module.params = PARAMS_FOR_RESET_DEVICE_BY_IP

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.patch.return_value = self.resource

        InterconnectModule().run()

        self.resource.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_RESET,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_fail_when_no_key_is_provided(self):
        params = PARAMS_FOR_RESET_DEVICE_BY_IP.copy()
        params['ip'] = None

        self.mock_ansible_module.params = params

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=InterconnectModule.MSG_MISSING_KEY)

    def test_should_update_the_interconnect_ports(self):
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_PORTS

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.update_ports.return_value = FAKE_INTERCONNECT

        InterconnectModule().run()

        self.resource.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)
        self.resource.update_ports.assert_called_with(ports=PORTS_FOR_UPDATE)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_PORTS_UPDATED,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_not_update_when_ports_not_provided(self):
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_UPDATE_PORTS)
        self.mock_ansible_module.params['ports'] = []

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.update_ports.return_value = FAKE_INTERCONNECT

        InterconnectModule().run()

        self.resource.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=InterconnectModule.MSG_PORTS_ALREADY_UPDATED,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_reset_port_protection(self):
        self.mock_ansible_module.params = PARAMS_FOR_RESET_PORT_PROTECTION

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.reset_port_protection.return_value = FAKE_INTERCONNECT

        InterconnectModule().run()

        self.resource.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)
        self.resource.reset_port_protection.assert_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_RESET_PORT_PROTECTION,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )

    def test_should_update_configuration(self):
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_CONFIGURATION

        self.resource.data = FAKE_INTERCONNECT
        self.resource.get_by_uri.return_value = self.resource

        self.resource.update_configuration.return_value = FAKE_INTERCONNECT

        InterconnectModule().run()

        self.resource.get_by.assert_called_with("interconnectIP", INTERCONNECT_IP)
        self.resource.update_configuration.assert_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=InterconnectModule.MSG_RECONFIGURED,
            ansible_facts=dict(interconnect=FAKE_INTERCONNECT)
        )


if __name__ == '__main__':
    pytest.main([__file__])
