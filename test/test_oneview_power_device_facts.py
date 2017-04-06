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

from oneview_module_loader import PowerDeviceFactsModule
from hpe_test_utils import FactsParamsTestCase


class PowerDeviceFactsModuleSpec(unittest.TestCase,
                                 FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """
    ERROR_MSG = 'Fake message error'

    PARAMS_GET_ALL = dict(
        config='config.json',
        name=None
    )

    PARAMS_GET_BY_NAME = dict(
        config='config.json',
        name="Test Power Device"
    )

    PARAMS_WITH_OPTIONS = dict(
        config='config.json',
        name="Test Power Device",
        options=[
            'powerState', 'uidState',
            {"utilization": {"fields": 'AveragePower',
                             "filter": 'startDate=2016-05-30T03:29:42.000Z',
                             "view": 'day'}}]
    )

    def setUp(self):
        self.configure_mocks(self, PowerDeviceFactsModule)
        self.power_devices = self.mock_ov_client.power_devices
        FactsParamsTestCase.configure_client_mock(self, self.power_devices)

    def test_should_get_all_power_devices(self):
        self.power_devices.get_all.return_value = {"name": "Power Device Name"}
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(power_devices=({"name": "Power Device Name"}))
        )

    def test_should_get_power_device_by_name(self):
        self.power_devices.get_by.return_value = {"name": "Power Device Name"}
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(power_devices=({"name": "Power Device Name"}))
        )

    def test_should_get_power_device_by_name_with_options(self):
        self.power_devices.get_by.return_value = [{"name": "Power Device Name", "uri": "resuri"}]
        self.power_devices.get_power_state.return_value = {'subresource': 'ps'}
        self.power_devices.get_uid_state.return_value = {'subresource': 'uid'}
        self.power_devices.get_utilization.return_value = {'subresource': 'util'}
        self.mock_ansible_module.params = self.PARAMS_WITH_OPTIONS

        PowerDeviceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'power_devices': [{'name': 'Power Device Name', 'uri': 'resuri'}],
                           'power_device_power_state': {'subresource': 'ps'},
                           'power_device_uid_state': {'subresource': 'uid'},
                           'power_device_utilization': {'subresource': 'util'},
                           }
        )


if __name__ == '__main__':
    unittest.main()
