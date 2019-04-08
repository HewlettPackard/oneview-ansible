#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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

import mock
import pytest
import yaml

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import SasLogicalInterconnectModule

FAKE_MSG_ERROR = 'Fake message error'

SAS_LOGICAL_INTERCONNECT = {
    "name": "SAS Logical Interconnect name",
    "uri": "/rest/sas-logical-interconnects/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0"
}

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

YAML_CONFIGURATION = """
    config: "config.json"
    state: configuration_updated
    data:
      name: "Name of the SAS Logical Interconnect"
"""

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

YAML_REPLACE_DRIVE_ENCLOSURE = """
    config: "{{ config }}"
    state: drive_enclosure_replaced
    data:
      name: "Sas Logical Interconnect Name"
      replace_drive_enclosure:
        oldSerialNumber: "S46016710000J4524YPT"
        newSerialNumber: "S46016710001J4524YPT"
"""

EXPECTED_UPDATE_COMPLIANCE_CALL = ["/rest/resource1", "/rest/resource2"]

expected_data = {
    'command': 'Stage',
    'sppUri': '/rest/firmware-drivers/filename-of-the-firmware-to-install'
}

response = {
    "response": "data"
}


@pytest.mark.resource(TestSasLogicalInterconnectModule='sas_logical_interconnects')
class TestSasLogicalInterconnectModule(OneViewBaseTest):
    def test_should_return_to_a_consistent_state_by_uris(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT
        self.resource.update_compliance_all.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_COMPLIANCE_URIS)

        SasLogicalInterconnectModule().run()

        self.resource.update_compliance_all.assert_called_once_with(EXPECTED_UPDATE_COMPLIANCE_CALL)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_CONSISTENT,
            ansible_facts={}
        )

    def test_should_return_to_a_consistent_state_by_names(self):
        self.resource.get_by.side_effect = [[{"uri": "/rest/resource1"}], [{"uri": "/rest/resource2"}]]
        self.resource.update_compliance_all.return_value = [SAS_LOGICAL_INTERCONNECT]
        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_COMPLIANCE_NAMES)

        SasLogicalInterconnectModule().run()

        self.resource.update_compliance_all.assert_called_once_with(EXPECTED_UPDATE_COMPLIANCE_CALL)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_CONSISTENT,
            ansible_facts={}
        )

    def test_should_fail_when_no_uris_provided(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_COMPLIANCE_INVALID)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasLogicalInterconnectModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_fail_when_compliance_cannot_resolve_names(self):
        self.resource.get_by.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_PARAMS_COMPLIANCE_NAMES)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasLogicalInterconnectModule.MSG_NOT_FOUND)

    def test_should_update_configuration(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT
        self.resource.update_configuration.return_value = SAS_LOGICAL_INTERCONNECT
        self.mock_ansible_module.params = yaml.load(YAML_CONFIGURATION)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_CONFIGURATION_UPDATED,
            ansible_facts=dict(sas_logical_interconnect=SAS_LOGICAL_INTERCONNECT)
        )

    def test_should_fail_when_sas_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_CONFIGURATION)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasLogicalInterconnectModule.MSG_NOT_FOUND)

    def test_should_install_firmware_when_spp_name_set(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT
        self.resource.update_firmware.return_value = response
        self.mock_ansible_module.params = yaml.load(YAML_FIRMWARE_WITH_SPP_NAME)

        SasLogicalInterconnectModule().run()

        self.resource.update_firmware.assert_called_once_with(expected_data)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_FIRMWARE_UPDATED,
            ansible_facts=dict(li_firmware=response))

    def test_should_update_firmware_when_spp_uri_set(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT
        self.resource.update_firmware.return_value = response
        self.mock_ansible_module.params = yaml.load(YAML_FIRMWARE_WITH_SPP_URI)

        SasLogicalInterconnectModule().run()

        self.resource.update_firmware.assert_called_once_with(expected_data)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_FIRMWARE_UPDATED,
            ansible_facts=dict(li_firmware=response))

    def test_should_fail_when_firmware_sas_logical_interconnect_not_found(self):
        self.resource.get_by_name.return_value = None
        self.resource.update_firmware.return_value = response
        self.mock_ansible_module.params = yaml.load(YAML_FIRMWARE_WITH_SPP_URI)

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasLogicalInterconnectModule.MSG_NOT_FOUND)

    def test_should_replace_drive_enclosure(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT
        self.resource.replace_drive_enclosure.return_value = {"name": "replaced"}
        self.mock_ansible_module.params = yaml.load(YAML_REPLACE_DRIVE_ENCLOSURE)

        SasLogicalInterconnectModule().run()

        self.resource.replace_drive_enclosure.assert_called_once_with(
            self.mock_ansible_module.params['data']['replace_drive_enclosure'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectModule.MSG_DRIVE_ENCLOSURE_REPLACED,
            ansible_facts={"sas_logical_interconnect": {"name": "replaced"}})


if __name__ == '__main__':
    pytest.main([__file__])
