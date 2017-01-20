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

from oneview_firmware_bundle import FirmwareBundleModule
from oneview_firmware_bundle import FIRMWARE_BUNDLE_UPLOADED

from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_FIRMWARE_FILE_PATH = '/path/to/file.rpm'

DEFAULT_FIRMWARE_TEMPLATE = dict(
    bundleSize='4837926',
    bundleType='Hotfix',
    category='firmware-drivers',
    description='Provides firmware for the following drive model: MB1000GCWCV and MB4000GCWDC Drives',
    fwComponents=[dict(componentVersion='HPGH',
                       fileName='hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm',
                       name='Supplemental Update',
                       swKeyNameList=['hp-firmware-hdd-a1b08f8a6b'])]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    file_path=DEFAULT_FIRMWARE_FILE_PATH
)


class FirmwareBundleModuleSpec(unittest.TestCase,
                               ModuleContructorTestCase,
                               ErrorHandlingTestCase):

    def setUp(self):
        self.configure_mocks(self, FirmwareBundleModule)
        ErrorHandlingTestCase.configure(self, ansible_params=PARAMS_FOR_PRESENT,
                                        method_to_fire=self.mock_ov_client.firmware_bundles.upload)

    def test_should_upload(self):
        self.mock_ov_client.firmware_drivers.get_by_file_name.return_value = None
        self.mock_ov_client.firmware_bundles.upload.side_effect = [DEFAULT_FIRMWARE_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FIRMWARE_BUNDLE_UPLOADED,
            ansible_facts=dict(firmware_bundle=DEFAULT_FIRMWARE_TEMPLATE)
        )


if __name__ == '__main__':
    unittest.main()
