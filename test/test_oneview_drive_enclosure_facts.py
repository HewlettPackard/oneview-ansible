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

from oneview_drive_enclosure_facts import DriveEnclosureFactsModule
from test.utils import ParamsTestCase
from test.utils import ModuleContructorTestCase

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


class DriveEnclosureFactsSpec(unittest.TestCase, ModuleContructorTestCase, ParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, DriveEnclosureFactsModule)
        self.drive_enclosures = self.mock_ov_client.drive_enclosures
        ParamsTestCase.configure_client_mock(self, self.drive_enclosures)

    def test_should_get_all(self):
        self.drive_enclosures.get_all.return_value = MOCK_DRIVE_ENCLOSURES

        self.mock_ansible_module.params = PARAMS_GET_ALL

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=(MOCK_DRIVE_ENCLOSURES))
        )

    def test_should_fail_when_get_all_raises_exception(self):
        self.drive_enclosures.get_all.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_ALL

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_by_name(self):
        self.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE])
        )

    def test_should_fail_when_get_by_name_raises_exception(self):
        self.drive_enclosures.get_by.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()

    def test_should_get_by_name_with_options(self):
        self.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        self.drive_enclosures.get_port_map.return_value = MOCK_PORT_MAP

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE],
                               drive_enclosure_port_map=MOCK_PORT_MAP)
        )

    def test_should_fail_when_get_port_map_raises_exception(self):
        self.drive_enclosures.get_by.return_value = MOCK_DRIVE_ENCLOSURES
        self.drive_enclosures.get_port_map.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
