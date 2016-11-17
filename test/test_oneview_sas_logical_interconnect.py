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
import yaml
from test.utils import PreloadedMocksBaseTestCase, ModuleContructorTestCase

from oneview_sas_logical_interconnect import SasLogicalInterconnectModule, \
    SAS_LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED, SAS_LOGICAL_INTERCONNECT_DRIVE_ENCLOSURE_REPLACED, \
    SAS_LOGICAL_INTERCONNECT_CONSISTENT, SAS_LOGICAL_INTERCONNECT_NOT_FOUND, \
    SAS_LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED, SAS_LOGICAL_INTERCONNECT_FIRMWARE_UPDATED

FAKE_MSG_ERROR = 'Fake message error'

SAS_LOGICAL_INTERCONNECT = {
    "name": "SAS Logical Interconnect name",
    "uri": "/rest/sas-logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0"
}


class SasLogicalInterconnectClientConfigurationSpec(unittest.TestCase, ModuleContructorTestCase):
    """
    Test the module constructor
    ModuleContructorTestCase has common tests for class constructor and main function
    """

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectModule)


class SasLogicalInterconnectCompliantStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    YAML_PARAMS_COMPLIANCE_URIS = """
        config: "{{ config }}"
        state: compliant
        data:
          logicalInterconnectUris: ["/rest/resource1", "/rest/resource2"]
    """

    YAML_PARAMS_COMPLIANCE_NAMES = """
            config: "{{ config }}"
            state: compliant
            data:
              logicalInterconnectNames: ["name 1", "name 2"]
        """

    YAML_PARAMS_COMPLIANCE_INVALID = """
        config: "{{ config }}"
        state: compliant
        data:
          logicalInterconnectUris: []
    """

    EXPECTED_UPDATE_COMPLIANCE_CALL = ["/rest/resource1", "/rest/resource2"]

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectModule)
        self.resource = self.mock_ov_client.sas_logical_interconnects

    def test_should_return_to_a_consistent_state_by_uris(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_compliance_all.return_value = [SAS_LOGICAL_INTERCONNECT]

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_PARAMS_COMPLIANCE_URIS)

        SasLogicalInterconnectModule().run()

        self.resource.update_compliance_all.assert_called_once_with(self.EXPECTED_UPDATE_COMPLIANCE_CALL)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_CONSISTENT,
            ansible_facts={}
        )

    def test_should_return_to_a_consistent_state_by_names(self):
        # Mock OneView resource functions
        self.resource.get_by.side_effect = [[{"uri": "/rest/resource1"}], [{"uri": "/rest/resource2"}]]
        self.resource.update_compliance_all.return_value = [SAS_LOGICAL_INTERCONNECT]

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_PARAMS_COMPLIANCE_NAMES)

        SasLogicalInterconnectModule().run()

        self.resource.update_compliance_all.assert_called_once_with(self.EXPECTED_UPDATE_COMPLIANCE_CALL)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_CONSISTENT,
            ansible_facts={}
        )

    def test_should_fail_when_no_uris_provided(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = None

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_PARAMS_COMPLIANCE_INVALID)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SAS_LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED
        )

    def test_should_fail_when_compliance_cannot_resolve_names(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = []

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_PARAMS_COMPLIANCE_NAMES)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SAS_LOGICAL_INTERCONNECT_NOT_FOUND
        )


class SasLogicalInterconnectConfigurationUpdatedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    YAML_CONFIGURATION = """
        config: "config.json"
        state: configuration_updated
        data:
          name: "Name of the SAS Logical Interconnect"
    """

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectModule)
        self.resource = self.mock_ov_client.sas_logical_interconnects

    def test_should_update_configuration(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_configuration.return_value = SAS_LOGICAL_INTERCONNECT

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_CONFIGURATION)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED,
            ansible_facts=dict(sas_logical_interconnect=SAS_LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_sas_logical_interconnect_not_found(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = []

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_CONFIGURATION)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SAS_LOGICAL_INTERCONNECT_NOT_FOUND
        )

    def test_should_fail_when_update_configuration_raises_exception(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_configuration.side_effect = Exception(FAKE_MSG_ERROR)

        # Mock Ansible params
        self.mock_ansible_module.params = yaml.load(self.YAML_CONFIGURATION)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class SasLogicalInterconnectFirmwareInstalledStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    YAML_FIRMWARE_WITH_SPP_NAME = """
        config: "{{ config }}"
        state: firmware_updated
        data:
          name: "Sas Logical Interconnect Name"
          firmware:
            command: Stage
            sppName: "filename-of-the-firmware-to-install"
    """

    YAML_FIRMWARE_WITH_SPP_URI = """
        config: "{{ config }}"
        state: firmware_updated
        data:
          name: "{{ sas_logical_interconnect_name }}"
          firmware:
            command: Stage
            sppUri: '/rest/firmware-drivers/filename-of-the-firmware-to-install'
    """

    expected_data = {
        'command': 'Stage',
        'sppUri': '/rest/firmware-drivers/filename-of-the-firmware-to-install'
    }

    response = {
        "response": "data"
    }

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectModule)
        self.resource = self.mock_ov_client.sas_logical_interconnects

    def test_should_install_firmware_when_spp_name_set(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_firmware.return_value = self.response

        self.mock_ansible_module.params = yaml.load(self.YAML_FIRMWARE_WITH_SPP_NAME)

        SasLogicalInterconnectModule().run()

        self.resource.update_firmware.assert_called_once_with(self.expected_data, SAS_LOGICAL_INTERCONNECT['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_FIRMWARE_UPDATED,
            ansible_facts=dict(li_firmware=self.response))

    def test_should_update_firmware_when_spp_uri_set(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_firmware.return_value = self.response

        self.mock_ansible_module.params = yaml.load(self.YAML_FIRMWARE_WITH_SPP_URI)

        SasLogicalInterconnectModule().run()

        self.resource.update_firmware.assert_called_once_with(self.expected_data, SAS_LOGICAL_INTERCONNECT['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_FIRMWARE_UPDATED,
            ansible_facts=dict(li_firmware=self.response))

    def test_should_fail_when_sas_logical_interconnect_not_found(self):
        self.resource.get_by.return_value = []
        self.resource.update_firmware.return_value = self.response

        self.mock_ansible_module.params = yaml.load(self.YAML_FIRMWARE_WITH_SPP_URI)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SAS_LOGICAL_INTERCONNECT_NOT_FOUND
        )

    def test_should_fail_when_install_firmware_raises_exception(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.update_firmware.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = yaml.load(self.YAML_FIRMWARE_WITH_SPP_URI)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=FAKE_MSG_ERROR)


class SasLogicalInterconnectDriveEnclosureReplacedStateSpec(unittest.TestCase, PreloadedMocksBaseTestCase):
    YAML_REPLACE_DRIVE_ENCLOSURE = """
        config: "{{ config }}"
        state: drive_enclosure_replaced
        data:
          name: "Sas Logical Interconnect Name"
          replace_drive_enclosure:
            oldSerialNumber: "S46016710000J4524YPT"
            newSerialNumber: "S46016710001J4524YPT"
    """

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectModule)
        self.resource = self.mock_ov_client.sas_logical_interconnects

    def test_should_replace_drive_enclosure(self):
        self.resource.get_by.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.resource.replace_drive_enclosure.return_value = {"name": "replaced"}

        self.mock_ansible_module.params = yaml.load(self.YAML_REPLACE_DRIVE_ENCLOSURE)

        SasLogicalInterconnectModule().run()

        self.resource.replace_drive_enclosure.assert_called_once_with(
            self.mock_ansible_module.params['data']['replace_drive_enclosure'],
            SAS_LOGICAL_INTERCONNECT['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SAS_LOGICAL_INTERCONNECT_DRIVE_ENCLOSURE_REPLACED,
            ansible_facts={"sas_logical_interconnect": {"name": "replaced"}})


if __name__ == '__main__':
    unittest.main()
