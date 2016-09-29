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
from oneview_server_profile_template_facts import ServerProfileTemplateFactsModule

ERROR_MSG = 'Fake message error'

TEMPLATE_NAME = "ProfileTemplate101"

TEMPLATE_URI = "/rest/server-profile-templates/0d02350a-8ac1-40b9-8b7e-5ee9a78c8f0e"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=TEMPLATE_NAME,
    options=None
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=TEMPLATE_NAME,
    options=["new_profile"]
)

BASIC_TEMPLATE = dict(
    name=TEMPLATE_NAME,
    uri=TEMPLATE_URI,
    enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
    serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
)

PROFILE = dict(
    name=None,
    type="ServerProfileV5"
)

TEMPLATES = [BASIC_TEMPLATE]


class ServerProfileTemplateFactsSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template_facts.AnsibleModule')
    def test_should_get_all_templates(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_all.return_value = TEMPLATES
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profile_templates=TEMPLATES)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template_facts.AnsibleModule')
    def test_should_get_template_by_name(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateFactsModule().run()

        mock_ov_instance.server_profile_templates.get_by_name.assert_called_once_with(name=TEMPLATE_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profile_templates=[BASIC_TEMPLATE])
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template_facts.AnsibleModule')
    def test_should_get_template_by_name_with_options(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        mock_ov_instance.server_profile_templates.get_new_profile.return_value = PROFILE
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateFactsModule().run()

        mock_ov_instance.server_profile_templates.get_by_name.assert_called_once_with(name=TEMPLATE_NAME)
        mock_ov_instance.server_profile_templates.get_new_profile.assert_called_once_with(id_or_uri=TEMPLATE_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                server_profile_templates=[BASIC_TEMPLATE],
                new_profile=PROFILE
            )
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_server_profile_template_facts.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_an_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.server_profile_templates.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ServerProfileTemplateFactsModule().run()
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
