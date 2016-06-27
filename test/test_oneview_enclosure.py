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
from oneview_enclosure import ENCLOSURE_ADDED, ENCLOSURE_ALREADY_EXIST, ENCLOSURE_UPDATED
from oneview_enclosure import ENCLOSURE_REMOVED, ENCLOSURE_ALREADY_ABSENT

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

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_ENCLOSURE_NAME)
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


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


class EnclosureErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure.AnsibleModule')
    def test_should_not_add_when_oneview_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
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
    def test_should_not_update_when_oneview_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
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
    def test_should_not_remove_when_oneview_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
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
