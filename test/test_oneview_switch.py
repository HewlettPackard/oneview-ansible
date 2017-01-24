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

from oneview_switch import SwitchModule, SWITCH_DELETED, SWITCH_ALREADY_ABSENT, SWITCH_PORTS_UPDATED
from utils import ModuleContructorTestCase
from utils import ErrorHandlingTestCase

SWITCH_NAME = "172.18.16.2"

PARAMS_ABSENT = dict(
    config='config.json',
    state='absent',
    name=SWITCH_NAME
)

PARAMS_PORTS_UPDATED = dict(
    config='config.json',
    state='ports_updated',
    name=SWITCH_NAME,
    data=[
        dict(
            portId="ca520119-1329-496b-8e44-43092e937eae:1.21",
            portName="1.21",
            enabled=True
        )
    ]
)

SWITCH = dict(
    name=SWITCH_NAME,
    uri="/rest/switches/ca520119-1329-496b-8e44-43092e937eae"
)


class SwitchModuleSpec(unittest.TestCase,
                       ModuleContructorTestCase,
                       ErrorHandlingTestCase):
    def setUp(self):
        self.configure_mocks(self, SwitchModule)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.mock_ov_client.switches.get_by)

    def test_should_remove_switch(self):
        switches = [SWITCH]
        self.mock_ov_client.switches.get_by.return_value = switches
        self.mock_ansible_module.params = PARAMS_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SWITCH_DELETED
        )

    def test_should_do_nothing_when_switch_not_exist(self):
        self.mock_ov_client.switches.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SWITCH_ALREADY_ABSENT
        )

    def test_should_update_switch_ports(self):
        switches = [SWITCH]
        self.mock_ov_client.switches.get_by.return_value = switches
        self.mock_ansible_module.params = PARAMS_PORTS_UPDATED

        SwitchModule().run()

        self.mock_ov_client.switches.update_ports.assert_called_once_with(
            id_or_uri=SWITCH["uri"],
            ports=PARAMS_PORTS_UPDATED["data"]
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SWITCH_PORTS_UPDATED
        )


if __name__ == '__main__':
    unittest.main()
