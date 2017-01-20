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

from oneview_interconnect import InterconnectModule, MISSING_KEY_MSG, INTERCONNECT_WAS_NOT_FOUND

from utils import ModuleContructorTestCase
from utils import ErrorHandlingTestCase

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


def create_params_for(power_state):
    return dict(
        config='config.json',
        state=power_state,
        name='Encl1, interconnect 1',
        ip=None
    )


class InterconnectModuleSpec(unittest.TestCase,
                             ModuleContructorTestCase,
                             ErrorHandlingTestCase):

    def setUp(self):
        self.configure_mocks(self, InterconnectModule)
        ErrorHandlingTestCase.configure(self, ansible_params=PARAMS_FOR_UPDATE_PORTS,
                                        method_to_fire=self.mock_ov_client.interconnects.get_by)

    def test_should_ensure_powered_on_state(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(powerState='Off', uri=FAKE_URI)]

        fake_interconnect_updated = dict(powerState='On')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=FAKE_URI,
            operation='replace',
            path='/powerState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_return_changed_false_when_interconnect_is_already_powered_on(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(powerState='On')
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_ensure_powered_off_state(self):
        ansible_arguments = create_params_for('powered_off')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(powerState='On', uri=FAKE_URI)]

        fake_interconnect_updated = dict(powerState='Off')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=FAKE_URI,
            operation='replace',
            path='/powerState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_ensure_uid_on_state(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(uidState='Off', uri=FAKE_URI)]

        fake_interconnect_updated = dict(uidState='On')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=FAKE_URI,
            operation='replace',
            path='/uidState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_return_changed_false_when_uid_is_already_on(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(uidState='On')
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_ensure_uid_off_state(self):
        ansible_arguments = create_params_for('uid_off')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(uidState='On', uri=FAKE_URI)]

        fake_interconnect_updated = dict(uidState='Off')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=FAKE_URI,
            operation='replace',
            path='/uidState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_ensure_device_reset(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(uri=FAKE_URI)

        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=FAKE_URI,
            operation='replace',
            path='/deviceResetState',
            value='Reset'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_fail_when_interconnect_was_not_found(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = []

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=INTERCONNECT_WAS_NOT_FOUND
        )

    def test_should_ensure_device_reset_by_ip_address(self):
        self.mock_ansible_module.params = PARAMS_FOR_RESET_DEVICE_BY_IP

        fake_interconnect = dict(uri=FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_fail_when_no_key_is_provided(self):
        params = PARAMS_FOR_RESET_DEVICE_BY_IP.copy()
        params['ip'] = None

        self.mock_ansible_module.params = params

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MISSING_KEY_MSG)

    def test_should_update_the_interconnect_ports(self):
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_PORTS

        fake_interconnect = dict(uri=FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.update_ports.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)
        self.mock_ov_client.interconnects.update_ports.assert_called_with(ports=PORTS_FOR_UPDATE, id_or_uri=FAKE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_reset_port_protection(self):
        self.mock_ansible_module.params = PARAMS_FOR_RESET_PORT_PROTECTION

        fake_interconnect = dict(uri=FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.reset_port_protection.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', INTERCONNECT_IP)
        self.mock_ov_client.interconnects.reset_port_protection.assert_called_with(id_or_uri=FAKE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )


if __name__ == '__main__':
    unittest.main()
