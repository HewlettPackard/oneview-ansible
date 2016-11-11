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
from test.utils import PreloadedMocksTestCase, ModuleContructorTestCase
from copy import deepcopy
import yaml

from oneview_enclosure import EnclosureModule
from oneview_enclosure import ENCLOSURE_ADDED, ENCLOSURE_ALREADY_EXIST, ENCLOSURE_UPDATED, \
    ENCLOSURE_REMOVED, ENCLOSURE_ALREADY_ABSENT, ENCLOSURE_RECONFIGURED, ENCLOSURE_REFRESHED, \
    ENCLOSURE_NOT_FOUND, APPLIANCE_BAY_POWERED_ON, APPLIANCE_BAY_ALREADY_POWERED_ON, APPLIANCE_BAY_NOT_FOUND, \
    UID_ALREADY_POWERED_ON, UID_POWERED_ON, UID_POWERED_OFF, UID_ALREADY_POWERED_OFF, MANAGER_BAY_UID_ALREADY_ON, \
    MANAGER_BAY_UID_ON, MANAGER_BAY_NOT_FOUND, MANAGER_BAY_UID_OFF, MANAGER_BAY_UID_ALREADY_OFF

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_ENCLOSURE_NAME = 'Test-Enclosure'

ENCLOSURE_FROM_ONEVIEW = dict(
    name='Encl1',
    uri='/a/path',
    applianceBayCount=2,
    uidState='Off',
    applianceBays=[
        dict(bayNumber=1, poweredOn=True),
        dict(bayNumber=2, poweredOn=False)
    ],
    managerBays=[
        dict(bayNumber=1, uidState='On'),
        dict(bayNumber=2, uidState='Off')
    ]

)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name='OneView-Enclosure')
)

PARAMS_WITH_NEW_NAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              newName='OneView-Enclosure')
)

PARAMS_WITH_NEW_RACK_NAME = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1',
              rackName='Another-Rack-Name')
)

PARAMS_WITH_CALIBRATED_MAX_POWER = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1',
              calibratedMaxPower=1750)
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_ENCLOSURE_NAME)
)

PARAMS_FOR_RECONFIGURED = dict(
    config='config.json',
    state='reconfigured',
    data=dict(name=DEFAULT_ENCLOSURE_NAME)
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              refreshState='Refreshing')
)

PARAMS_FOR_BAY_POWER_ON = dict(
    config='config.json',
    state='appliance_bays_power_on',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              applianceBay=2)
)


class EnclosureClientConfigurationSpec(unittest.TestCase, ModuleContructorTestCase):
    """
    Test the module constructor
    ModuleContructorTestCase has common tests for class constructor and main function
    """

    def setUp(self):
        self.configure_mocks(self, EnclosureModule)


class EnclosurePresentStateSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_create_new_enclosure(self):
        self.enclosures.get_by.return_value = []
        self.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        self.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_ADDED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_ALREADY_EXIST,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_update_when_data_has_new_name(self):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['name'] = 'Test-Enclosure-Renamed'

        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = updated_data

        self.mock_ansible_module.params = PARAMS_WITH_NEW_NAME

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_UPDATED,
            ansible_facts=dict(enclosure=updated_data)
        )

    def test_update_when_data_has_new_rack_name(self):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['rackName'] = 'Another-Rack-Name'

        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = updated_data

        self.mock_ansible_module.params = PARAMS_WITH_NEW_RACK_NAME

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_UPDATED,
            ansible_facts=dict(enclosure=updated_data)
        )

    def test_replace_name_for_new_enclosure(self):
        self.enclosures.get_by.return_value = []
        self.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        self.enclosures.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/name", "OneView-Enclosure")

    def test_replace_name_for_existent_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_NEW_NAME

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/name", "OneView-Enclosure")

    def test_replace_rack_name_for_new_enclosure(self):
        self.enclosures.get_by.return_value = []
        self.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        self.enclosures.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_NEW_RACK_NAME

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/rackName", "Another-Rack-Name")

    def test_replace_rack_name_for_existent_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_NEW_RACK_NAME

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/rackName", "Another-Rack-Name")

    def test_update_calibrated_max_power_for_existent_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_CALIBRATED_MAX_POWER

        EnclosureModule().run()

        self.enclosures.update_environmental_configuration.assert_called_once_with(
            "/a/path", {"calibratedMaxPower": 1750})


class EnclosureAbsentStateSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_remove_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_REMOVED
        )

    def test_should_do_nothing_when_enclosure_not_exist(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_ALREADY_ABSENT
        )


class EnclosureReconfiguredStateSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_reconfigure_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.update_configuration.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_RECONFIGURED
        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_RECONFIGURED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_fail_when_enclosure_not_exist(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_RECONFIGURED
        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureRefreshedStateSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_refresh_enclosure(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.get.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=ENCLOSURE_REFRESHED
        )

    def test_should_fail_when_enclosure_not_exist(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH
        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureErrorHandlingSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_fail_when_add_raises_exception(self):
        self.enclosures.get_by.return_value = []
        self.enclosures.add.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        self.assertRaises(Exception, EnclosureModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_patch_raises_exception(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_WITH_NEW_NAME
        self.assertRaises(Exception, EnclosureModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_remove_raises_exception(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.remove.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        self.assertRaises(Exception, EnclosureModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class EnclosureApplianceBaysPowerOnStateSpec(PreloadedMocksTestCase):
    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_power_on_appliance_bays(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_BAY_POWER_ON

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            ENCLOSURE_FROM_ONEVIEW['uri'], operation='replace', path='/applianceBays/2/power', value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=APPLIANCE_BAY_POWERED_ON
        )

    def test_should_not_power_on_when_already_on(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_BAY_POWER_ON)
        params_power_on_do_nothing['data']['applianceBay'] = 1
        self.mock_ansible_module.params = params_power_on_do_nothing

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=APPLIANCE_BAY_ALREADY_POWERED_ON
        )

    def test_should_fail_when_appliance_bay_not_found(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_power_on_not_found_bay = deepcopy(PARAMS_FOR_BAY_POWER_ON)
        params_power_on_not_found_bay['data']['applianceBay'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=APPLIANCE_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_appliance_bays(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, applianceBays=[])
        self.enclosures.get_by.return_value = [enclosure_without_appliance_bays]

        self.mock_ansible_module.params = PARAMS_FOR_BAY_POWER_ON

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=APPLIANCE_BAY_NOT_FOUND)

    def test_should_fail_when_enclosure_not_found(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_BAY_POWER_ON

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureUidOnStateSpec(PreloadedMocksTestCase):
    PARAMS_FOR_UID_ON = """
        config: "{{ config_file_path }}"
        state: uid_on
        data:
          name: 'Test-Enclosure'
    """

    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_turn_on_uid(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_ON)

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            ENCLOSURE_FROM_ONEVIEW['uri'], operation='replace', path='/uidState', value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=UID_POWERED_ON
        )

    def test_should_not_set_to_on_when_already_on(self):
        enclosure_uid_on = dict(ENCLOSURE_FROM_ONEVIEW, uidState='On')
        self.enclosures.get_by.return_value = [enclosure_uid_on]

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_ON)

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=enclosure_uid_on),
            msg=UID_ALREADY_POWERED_ON
        )

    def test_should_fail_when_enclosure_not_found(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_ON)

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureUidOffStateSpec(PreloadedMocksTestCase):
    PARAMS_FOR_UID_OFF = """
        config: "{{ config_file_path }}"
        state: uid_off
        data:
          name: 'Test-Enclosure'
    """

    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_turn_off_uid(self):
        enclosure_uid_on = dict(ENCLOSURE_FROM_ONEVIEW, uidState='On')

        self.enclosures.get_by.return_value = [enclosure_uid_on]
        self.enclosures.patch.return_value = enclosure_uid_on

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_OFF)

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            ENCLOSURE_FROM_ONEVIEW['uri'], operation='replace', path='/uidState', value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=enclosure_uid_on),
            msg=UID_POWERED_OFF
        )

    def test_should_not_set_to_off_when_already_off(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_OFF)

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=UID_ALREADY_POWERED_OFF
        )

    def test_should_fail_when_enclosure_not_found(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_UID_OFF)

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureManagerBaysUidOnStateSpec(PreloadedMocksTestCase):
    PARAMS_FOR_MANAGER_BAY_UID_ON = """
        config: "{{ config_file_path }}"
        state: manager_bays_uid_on
        data:
          name: 'Test-Enclosure'
          managerBay: 2
    """

    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_turn_on_uid(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_ON)

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            ENCLOSURE_FROM_ONEVIEW['uri'], operation='replace', path='/managerBays/2/uidState', value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=MANAGER_BAY_UID_ON
        )

    def test_should_not_set_to_on_when_already_on(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_manager_bay_uid = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_ON)
        params_manager_bay_uid['data']['managerBay'] = '1'

        self.mock_ansible_module.params = params_manager_bay_uid

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=MANAGER_BAY_UID_ALREADY_ON
        )

    def test_should_fail_when_manager_bay_not_found(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_power_on_not_found_bay = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_ON)
        params_power_on_not_found_bay['data']['managerBay'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MANAGER_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.enclosures.get_by.return_value = [enclosure_without_appliance_bays]

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_ON)

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MANAGER_BAY_NOT_FOUND)

    def test_should_fail_when_enclosure_not_found(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_ON)

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


class EnclosureManagerBaysUidOffStateSpec(PreloadedMocksTestCase):
    PARAMS_FOR_MANAGER_BAY_UID_OFF = """
        config: "{{ config_file_path }}"
        state: manager_bays_uid_off
        data:
          name: 'Test-Enclosure'
          managerBay: 1
    """

    def setUp(self):
        self.configure_mocks(EnclosureModule)
        self.enclosures = self.mock_ov_client.enclosures

    def test_should_turn_off_uid(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        self.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_OFF)

        EnclosureModule().run()

        self.enclosures.patch.assert_called_once_with(
            ENCLOSURE_FROM_ONEVIEW['uri'], operation='replace', path='/managerBays/1/uidState', value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=MANAGER_BAY_UID_OFF
        )

    def test_should_not_set_to_off_when_already_off(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_manager_bay_uid = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_OFF)
        params_manager_bay_uid['data']['managerBay'] = '2'

        self.mock_ansible_module.params = params_manager_bay_uid

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=MANAGER_BAY_UID_ALREADY_OFF
        )

    def test_should_fail_when_manager_bay_not_found(self):
        self.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        params_power_on_not_found_bay = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_OFF)
        params_power_on_not_found_bay['data']['managerBay'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MANAGER_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.enclosures.get_by.return_value = [enclosure_without_appliance_bays]

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_OFF)

        EnclosureModule().run()

        self.enclosures.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MANAGER_BAY_NOT_FOUND)

    def test_should_fail_when_enclosure_not_found(self):
        self.enclosures.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(self.PARAMS_FOR_MANAGER_BAY_UID_OFF)

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ENCLOSURE_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
