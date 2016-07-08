# -*- coding: utf-8 -*-
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
import yaml

from hpOneView.oneview_client import OneViewClient
from oneview_logical_enclosure import LogicalEnclosureModule, LOGICAL_ENCLOSURE_UPDATED, \
    LOGICAL_ENCLOSURE_ALREADY_UPDATED, LOGICAL_ENCLOSURE_FIRMWARE_UPDATED, \
    LOGICAL_ENCLOSURE_CONFIGURATION_SCRIPT_UPDATED, \
    LOGICAL_ENCLOSURE_DUMP_GENERATED, LOGICAL_ENCLOSURE_RECONFIGURED, LOGICAL_ENCLOSURE_UPDATED_FROM_GROUP, \
    LOGICAL_ENCLOSURE_REQUIRED

YAML_LOGICAL_ENCLOSURE = """
    config: "{{ config }}"
    state: present
    data:
        uri: rest/logical-enclosures/4671582d-1746-4122-9cf0-642a59543509
        name: "Encl1"
    """

YAML_LOGICAL_ENCLOSURE_FIRMWARE_UPDATE = """
        config: "{{ config }}"
        state: firmware_updated
        data:
            name: "Encl1"
            firmware:
                firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
                firmwareUpdateOn: "EnclosureOnly"
                forceInstallFirmware: "false"
      """

YAML_LOGICAL_ENCLOSURE_UPDATE_SCRIPT = """
        config: "{{ config }}"
        state: script_updated
        data:
            name: "Encl1"
            configurationScript: "# script (updated)"
      """

YAML_LOGICAL_ENCLOSURE_DUMP = """
        config: "{{ config }}"
        state: dumped
        data:
            name: "Encl1"
            dump:
              errorCode: "MyDump16"
              encrypt: "true"
              excludeApplianceDump: "false"
        """

YAML_LOGICAL_ENCLOSURE_CONFIGURE = """
        config: "{{ config }}"
        state: reconfigured
        data:
            name: "Encl1"
    """

YAML_LOGICAL_ENCLOSURE_UPDATE_FROM_GROUP = """
        config: "{{ config }}"
        state: updated_from_group
        data:
            name: "Encl1"
    """

YAML_LOGICAL_ENCLOSURE_RENAME = """
        config: "{{ config }}"
        state: present
        data:
            name: "Encl1"
            newName: "Encl1 (renamed)"
        """

YAML_LOGICAL_ENCLOSURE_NO_RENAME = """
    config: "{{ config }}"
    state: present
    data:
        name: "Encl1 (renamed)"
        newName: "Encl1"
    """

DICT_DEFAULT_LOGICAL_ENCLOSURE = yaml.load(YAML_LOGICAL_ENCLOSURE)["data"]


def create_ansible_mock(yaml_config):
    mock_ansible = mock.Mock()
    mock_ansible.params = yaml.load(yaml_config)
    return mock_ansible


class LogicalEnclosureSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_NO_RENAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=LOGICAL_ENCLOSURE_ALREADY_UPDATED,
            ansible_facts=dict(oneview_logical_enclosure=DICT_DEFAULT_LOGICAL_ENCLOSURE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_raise_error_when_name_not_exists(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = None
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_NO_RENAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=LOGICAL_ENCLOSURE_REQUIRED)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        data_merged = DICT_DEFAULT_LOGICAL_ENCLOSURE.copy()
        data_merged['newName'] = 'New Name'

        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_instance.logical_enclosures.update.return_value = data_merged
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_RENAME)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_UPDATED,
            ansible_facts=dict(oneview_logical_enclosure=data_merged)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_update_firmware(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_instance.logical_enclosures.patch.return_value = {'PATCH', 'EXECUTED'}
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_FIRMWARE_UPDATE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_FIRMWARE_UPDATED,
            ansible_facts=dict(oneview_logical_enclosure={'PATCH', 'EXECUTED'})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_update_script(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_UPDATE_SCRIPT)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_CONFIGURATION_SCRIPT_UPDATED,
            ansible_facts=dict(oneview_configuration_script='# script (updated)')
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_support_dump(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_instance.logical_enclosures.generate_support_dump.return_value = '/rest/appliance/dumpedfile'
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_DUMP)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_DUMP_GENERATED,
            ansible_facts=dict(oneview_generated_dump_uri='/rest/appliance/dumpedfile')
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_reconfigure(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_instance.logical_enclosures.update_configuration.return_value = {'Configuration', 'Updated'}
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_CONFIGURE)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_RECONFIGURED,
            ansible_facts=dict(oneview_logical_enclosure={'Configuration', 'Updated'})
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_logical_enclosure.AnsibleModule')
    def test_update_from_group(self, mock_ansible_module, mock_ov_client_from_json_file):
        # Mock OneView Client
        mock_ov_instance = mock.Mock()
        mock_ov_instance.logical_enclosures.get_by_name.return_value = DICT_DEFAULT_LOGICAL_ENCLOSURE
        mock_ov_instance.logical_enclosures.update_from_group.return_value = {'Updated from group'}
        mock_ov_client_from_json_file.return_value = mock_ov_instance

        # Mock Ansible Module
        mock_ansible_instance = create_ansible_mock(YAML_LOGICAL_ENCLOSURE_UPDATE_FROM_GROUP)
        mock_ansible_module.return_value = mock_ansible_instance

        LogicalEnclosureModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=LOGICAL_ENCLOSURE_UPDATED_FROM_GROUP,
            ansible_facts=dict(oneview_logical_enclosure={'Updated from group'})
        )


if __name__ == '__main__':
    unittest.main()
