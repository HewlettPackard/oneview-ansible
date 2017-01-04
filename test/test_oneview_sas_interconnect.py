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

from oneview_sas_interconnect import SasInterconnectModule, SAS_INTERCONNECT_NOT_FOUND, SAS_INTERCONNECT_NOTHING_TO_DO
from utils import ModuleContructorTestCase

SAS_INTERCONNECT_NAME = "0000A66103, interconnect 4"
SAS_INTERCONNECT_URI = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'

REFRESH_CONFIGURATION = dict(refreshState="RefreshPending")

SAS_INTERCONNECT = dict(
    name=SAS_INTERCONNECT_NAME,
    uri=SAS_INTERCONNECT_URI
)


class StateCheck(object):
    def __init__(self, state_name):
        self.msg = SasInterconnectModule.states_success_message[state_name]
        self.state = SasInterconnectModule.states[state_name]
        self.params = dict(
            config='config.json',
            state=state_name,
            name=SAS_INTERCONNECT_NAME
        )


class SasInterconnectModuleSpec(unittest.TestCase, ModuleContructorTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, SasInterconnectModule)
        self.resource = self.mock_ov_client.sas_interconnects

    def test_should_refresh_the_sas_interconnect(self):
        state_check = StateCheck('refreshed')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.refresh_state.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)

        self.resource.refresh_state.assert_called_once_with(
            id_or_uri=SAS_INTERCONNECT_URI,
            configuration=REFRESH_CONFIGURATION
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_turn_on_the_uid_when_uid_is_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)

        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_INTERCONNECT_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_fail_when_interconnect_not_found(self):
        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SAS_INTERCONNECT_NOT_FOUND,
        )

    def test_should_turn_off_the_uid_when_uid_is_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_INTERCONNECT_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_off_when_the_sas_interconnect_is_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_off(self):
        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_INTERCONNECT_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_on_when_the_sas_interconnect_is_powered_off(self):
        state_check = StateCheck('powered_on')

        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SAS_INTERCONNECT_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_perform_soft_reset(self):
        state_check = StateCheck('soft_reset')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_perform_hard_reset(self):
        state_check = StateCheck('hard_reset')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )


if __name__ == '__main__':
    unittest.main()
