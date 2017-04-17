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
import unittest

from oneview_module_loader import PowerDeviceModule
from hpe_test_utils import OneViewBaseTestCase


FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_POWER_DEVICE = dict(
    name='PDD name',
    ratedCapacity=40
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_POWER_DEVICE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='PDD new name')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_POWER_DEVICE['name'])
)

PARAMS_FOR_MISSING_ATTRIBUTES = dict(
    config='config.json',
    state='present',
    data=dict(field='invalid')
)

PARAMS_FOR_IPDU = dict(
    config='config.json',
    state='discovered',
    data=dict(
        hostname='10.10.10.10',
        username='username',
        password='password')
)

PARAMS_FOR_POWER_STATE_SET = dict(
    config='config.json',
    state='power_state_set',
    data=dict(
        name='PDD name',
        powerStateData=dict(
            powerState="On"
        )
    )
)

PARAMS_FOR_REFRESH_STATE_SET = dict(
    config='config.json',
    state='refresh_state_set',
    data=dict(
        name='PDD name',
        refreshStateData=dict(
            refreshState="RefreshPending"
        )
    )
)

PARAMS_FOR_UID_STATE_SET = dict(
    config='config.json',
    state='uid_state_set',
    data=dict(
        name='PDD name',
        uidStateData=dict(
            powerState="On"
        )
    )
)


class PowerDeviceModuleSpec(unittest.TestCase,
                            OneViewBaseTestCase):
    """
    OneViewBaseTestCase has common tests for main function,
    also provides the mocks used in this test case.
    """

    def setUp(self):
        self.configure_mocks(self, PowerDeviceModule)
        self.resource = self.mock_ov_client.power_devices

    def test_should_add_new_power_device(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = DEFAULT_POWER_DEVICE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_CREATED,
            ansible_facts=dict(power_device=DEFAULT_POWER_DEVICE)
        )

    def test_should_add_new_ipdu(self):
        self.resource.add_ipdu.return_value = DEFAULT_POWER_DEVICE
        self.mock_ansible_module.params = PARAMS_FOR_IPDU

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_IPDU_ADDED,
            ansible_facts=dict(power_device=DEFAULT_POWER_DEVICE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_POWER_DEVICE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PowerDeviceModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(power_device=DEFAULT_POWER_DEVICE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_POWER_DEVICE.copy()
        data_merged['name'] = 'PDD new name'

        self.resource.get_by.return_value = [DEFAULT_POWER_DEVICE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_UPDATED,
            ansible_facts=dict(power_device=data_merged)
        )

    def test_should_fail_with_missing_required_attributes(self):
        self.mock_ansible_module.params = PARAMS_FOR_MISSING_ATTRIBUTES

        PowerDeviceModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PowerDeviceModule.MSG_MANDATORY_FIELD_MISSING
        )

    def test_should_remove_power_device(self):
        self.resource.get_by.return_value = [DEFAULT_POWER_DEVICE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_DELETED
        )

    def test_should_do_nothing_when_power_device_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PowerDeviceModule.MSG_ALREADY_ABSENT
        )

    def test_should_set_power_state(self):
        self.resource.get_by.return_value = [{"uri": "resourceuri"}]

        self.resource.update_power_state.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_FOR_POWER_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_POWER_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    def test_should_fail_when_the_power_device_was_not_found(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_POWER_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PowerDeviceModule.MSG_NOT_FOUND
        )

    def test_should_set_refresh_state(self):
        self.resource.get_by.return_value = [{"uri": "resourceuri"}]
        self.resource.update_refresh_state.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_REFRESH_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    def test_should_fail_when_the_power_device_was_not_found_for_refresh_state(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PowerDeviceModule.MSG_NOT_FOUND
        )

    def test_should_set_uid_state(self):
        self.resource.get_by.return_value = [{"uri": "resourceuri"}]
        self.resource.update_uid_state.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_FOR_UID_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PowerDeviceModule.MSG_UID_STATE_UPDATED,
            ansible_facts=dict(power_device={"name": "name"})
        )

    def test_should_fail_when_the_power_device_was_not_found_for_uid_state(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_UID_STATE_SET

        PowerDeviceModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PowerDeviceModule.MSG_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
