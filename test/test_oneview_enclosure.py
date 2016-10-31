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
from oneview_enclosure import EnclosureModule
from oneview_enclosure import ENCLOSURE_ADDED, ENCLOSURE_ALREADY_EXIST, ENCLOSURE_UPDATED, \
    ENCLOSURE_REMOVED, ENCLOSURE_ALREADY_ABSENT, ENCLOSURE_RECONFIGURED, ENCLOSURE_REFRESHED, \
    ENCLOSURE_NOT_FOUND
from test.utils import create_ansible_mock

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_ENCLOSURE_NAME = 'Test-Enclosure'

ENCLOSURE_FROM_ONEVIEW = dict(
    name='Encl1',
    uri='/a/path'
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


class EnclosureClientConfigurationSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_load_config_from_file(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                          mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': 'config.json'})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule()

        mock_ov_client_from_json_file.assert_called_once_with('config.json')
        mock_ov_client_from_env_vars.not_been_called()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch.object(OneViewClient, 'from_environment_variables')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_load_config_from_environment(self, mock_ansible_module, mock_ov_client_from_env_vars,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()

        mock_ov_client_from_env_vars.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock({'config': None})
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule()

        mock_ov_client_from_env_vars.assert_called_once()
        mock_ov_client_from_json_file.not_been_called()


class EnclosurePresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_create_new_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []
        mock_ov_instance.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        mock_ov_instance.enclosures.patch.return_value = ENCLOSURE_FROM_ONEVIEW

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_ADDED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_ALREADY_EXIST,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_update_when_data_has_new_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['name'] = 'Test-Enclosure-Renamed'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.return_value = updated_data

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_UPDATED,
            ansible_facts=dict(enclosure=updated_data)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_update_when_data_has_new_rack_name(self, mock_ansible_module, mock_ov_client_from_json_file):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['rackName'] = 'Another-Rack-Name'

        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.return_value = updated_data

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_RACK_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_UPDATED,
            ansible_facts=dict(enclosure=updated_data)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_replace_name_for_new_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []
        mock_ov_instance.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        mock_ov_instance.enclosures.patch.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ov_instance.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/name", "OneView-Enclosure")

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_replace_name_for_existent_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ov_instance.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/name", "OneView-Enclosure")

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_replace_rack_name_for_new_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []
        mock_ov_instance.enclosures.add.return_value = ENCLOSURE_FROM_ONEVIEW
        mock_ov_instance.enclosures.patch.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_RACK_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ov_instance.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/rackName", "Another-Rack-Name")

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_replace_rack_name_for_existent_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_RACK_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ov_instance.enclosures.patch.assert_called_once_with(
            "/a/path", "replace", "/rackName", "Another-Rack-Name")

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_update_calibrated_max_power_for_existent_enclosure(self, mock_ansible_module,
                                                                mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_CALIBRATED_MAX_POWER)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ov_instance.enclosures.update_environmental_configuration.assert_called_once_with(
            "/a/path", {"calibratedMaxPower": 1750})


class EnclosureAbsentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_remove_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_REMOVED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_do_nothing_when_enclosure_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_ALREADY_ABSENT
        )


class EnclosureReconfiguredStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_reconfigure_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.update_configuration.return_value = ENCLOSURE_FROM_ONEVIEW

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_RECONFIGURED)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=ENCLOSURE_RECONFIGURED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_do_nothing_when_enclosure_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_RECONFIGURED)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_NOT_FOUND
        )


class EnclosureRefreshedStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_refresh_enclosure(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.get.return_value = ENCLOSURE_FROM_ONEVIEW

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=ENCLOSURE_REFRESHED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_do_nothing_when_enclosure_not_exist(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=ENCLOSURE_NOT_FOUND
        )


class EnclosureErrorHandlingSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_fail_when_add_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []
        mock_ov_instance.enclosures.add.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_fail_when_patch_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.patch.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_WITH_NEW_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_fail_when_remove_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = [ENCLOSURE_FROM_ONEVIEW]
        mock_ov_instance.enclosures.remove.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, EnclosureModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

if __name__ == '__main__':
    unittest.main()
