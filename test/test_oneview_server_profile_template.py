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

from test.utils import create_ansible_mock

from hpOneView.oneview_client import OneViewClient
from oneview_server_profile_template import ServerProfileTemplateModule
from oneview_server_profile_template import TEMPLATE_CREATED, TEMPLATE_UPDATED, TEMPLATE_ALREADY_EXIST, \
    TEMPLATE_DELETED, TEMPLATE_ALREADY_ABSENT


FAKE_MSG_ERROR = 'Fake message error'

TEMPLATE_NAME = "ProfileTemplate101"
SHT_URI = "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"

BASIC_TEMPLATE = dict(
    name=TEMPLATE_NAME,
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI
)

BASIC_TEMPLATE_MODIFIED = dict(
    name=TEMPLATE_NAME,
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI,
    serialNumberType="Private"
)

CREATED_BASIC_TEMPLATE = dict(
    affinity="Bay",
    bios=dict(manageBios=False, overriddenSettings=[]),
    boot=dict(manageBoot=False, order=[]),
    bootMode=dict(manageMode=False, mode=None, pxeBootPolicy=None),
    category="server-profile-templates",
    enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
    name="ProfileTemplate101",
    serialNumberType="Virtual",
    serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B",
    status="OK",
    type="ServerProfileTemplateV1",
    uri="/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda",
    wwnType="Virtual"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=BASIC_TEMPLATE
)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='present',
    data=BASIC_TEMPLATE_MODIFIED
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=BASIC_TEMPLATE
)


class ServerProfileTemplatePresentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_create_new_template_when_it_not_exists(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = None
        mock_ov_instance.server_profile_templates.create.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        mock_ov_instance.server_profile_templates.create.assert_called_once_with(BASIC_TEMPLATE)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=TEMPLATE_CREATED,
            ansible_facts=dict(server_profile_templates=CREATED_BASIC_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_not_modify_when_template_already_exists(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_instance.server_profile_templates.create.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=TEMPLATE_ALREADY_EXIST,
            ansible_facts=dict(server_profile_templates=CREATED_BASIC_TEMPLATE)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_instance.server_profile_templates.update.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_UPDATE)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        expected = CREATED_BASIC_TEMPLATE.copy()
        expected.update(BASIC_TEMPLATE_MODIFIED)

        mock_ov_instance.server_profile_templates.update.assert_called_once_with(
            resource=expected, id_or_uri=expected["uri"]
        )

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=TEMPLATE_UPDATED,
            ansible_facts=dict(server_profile_templates=CREATED_BASIC_TEMPLATE)
        )


class ServerProfileTemplateAbsentStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_delete_when_template_exists(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = CREATED_BASIC_TEMPLATE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        mock_ov_instance.server_profile_templates.delete.assert_called_once_with(CREATED_BASIC_TEMPLATE)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=TEMPLATE_DELETED
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_do_nothing_when_templates_not_exists(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = None
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_ABSENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=TEMPLATE_ALREADY_ABSENT
        )


class ServerProfileTemplateErrorHandlingSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.side_effect = Exception(FAKE_MSG_ERROR)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=FAKE_MSG_ERROR)


if __name__ == '__main__':
    unittest.main()
