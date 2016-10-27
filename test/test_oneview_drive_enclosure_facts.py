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
from oneview_drive_enclosure_facts import DriveEnclosureFactsModule
from utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

DRIVE_ENCLOSURE_URI = '/rest/drive-enclosures/SN123101'
DRIVE_ENCLOSURE_NAME = '0000A66102, bay 1'

DICT_DEFAULT_DRIVE_ENCLOSURE = {
    'name': DRIVE_ENCLOSURE_NAME,
    'powerState': 'On',
    'status': 'OK',
    'type': 'drive-enclosure',
    'uidState': 'Off',
    'uri': DRIVE_ENCLOSURE_URI
}

MOCK_DRIVE_ENCLOSURES = [
    DICT_DEFAULT_DRIVE_ENCLOSURE,
    DICT_DEFAULT_DRIVE_ENCLOSURE
]

MOCK_PORT_MAP = {
    "type": "DriveEnclosurePortMap"
}

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=['portMap']
)


class DriveEnclosureFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_get_all(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_all.return_value = MOCK_DRIVE_ENCLOSURES

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=(MOCK_DRIVE_ENCLOSURES))
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_all.side_effect = Exception(ERROR_MSG)

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_get_by_name(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE])
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.side_effect = Exception(ERROR_MSG)

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_get_by_name_with_options(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        mock_ov_instance.drive_enclosures.get_port_map.return_value = MOCK_PORT_MAP

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE],
                               drive_enclosure_port_map=MOCK_PORT_MAP)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_drive_enclosure_facts.AnsibleModule')
    def test_should_fail_when_get_port_map_raises_exception(self, mock_ansible_module, mock_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.drive_enclosures.get_by.return_value = MOCK_DRIVE_ENCLOSURES
        mock_ov_instance.drive_enclosures.get_port_map.side_effect = Exception(ERROR_MSG)

        mock_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        DriveEnclosureFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
