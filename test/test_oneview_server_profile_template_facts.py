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

from test.utils import FactsParamsTestCase
from test.utils import ModuleContructorTestCase
from test.utils import ErrorHandlingTestCase

from oneview_server_profile_template_facts import ServerProfileTemplateFactsModule

ERROR_MSG = 'Fake message error'

TEMPLATE_NAME = "ProfileTemplate101"

TEMPLATE_URI = "/rest/server-profile-templates/0d02350a-8ac1-40b9-8b7e-5ee9a78c8f0e"

ENCLOSURE_GROUP_FOR_TRANSFORMATION = "/rest/enclosure-groups/34e4af48-f57d-45d6-a0a3-e9c18d69bc90"
SERVER_HARDWARE_TYPE_FOR_TRANSFORMATION = "/rest/server-hardware-types/172D9A28-7F63-479E-BBCD-A91C7F7848DB"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=TEMPLATE_NAME,
    options=None
)

PARAMS_GET_BY_NAME_WITH_NEW_PROFILE = dict(
    config='config.json',
    name=TEMPLATE_NAME,
    options=["new_profile"]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=TEMPLATE_NAME,
    options=[
        'new_profile',
        {'transformation': {
            'enclosure_group_uri': ENCLOSURE_GROUP_FOR_TRANSFORMATION,
            'server_hardware_type_uri': SERVER_HARDWARE_TYPE_FOR_TRANSFORMATION}}
    ]
)

BASIC_TEMPLATE = dict(
    name=TEMPLATE_NAME,
    uri=TEMPLATE_URI,
    enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
    serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
)

TRANSFORMATION_TEMPLATE = dict(
    name=TEMPLATE_NAME,
    uri=TEMPLATE_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_FOR_TRANSFORMATION,
    serverHardwareTypeUri=SERVER_HARDWARE_TYPE_FOR_TRANSFORMATION
)

PROFILE = dict(
    name=None,
    type="ServerProfileV5"
)

TEMPLATES = [BASIC_TEMPLATE]


class ServerProfileTemplateFactsSpec(unittest.TestCase,
                                     ModuleContructorTestCase,
                                     FactsParamsTestCase,
                                     ErrorHandlingTestCase):
    """
    ModuleContructorTestCase has common tests for the class constructor and the main function, and also provides the
    mocks used in this test class.

    FactsParamsTestCase has common tests for the parameters support.
    """
    def setUp(self):
        self.configure_mocks(self, ServerProfileTemplateFactsModule)

        FactsParamsTestCase.configure_client_mock(self, self.mock_ov_client.server_profile_templates)
        ErrorHandlingTestCase.configure(self, method_to_fire=self.mock_ov_client.server_profile_templates.get_by_name)

    def test_should_get_all_templates(self):
        self.mock_ov_client.server_profile_templates.get_all.return_value = TEMPLATES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ServerProfileTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profile_templates=TEMPLATES)
        )

    def test_should_get_template_by_name(self):
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ServerProfileTemplateFactsModule().run()

        self.mock_ov_client.server_profile_templates.get_by_name.assert_called_once_with(name=TEMPLATE_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_profile_templates=[BASIC_TEMPLATE])
        )

    def test_should_get_template_by_name_with_new_profile(self):
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        self.mock_ov_client.server_profile_templates.get_new_profile.return_value = PROFILE

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_NEW_PROFILE

        ServerProfileTemplateFactsModule().run()

        self.mock_ov_client.server_profile_templates.get_by_name.assert_called_once_with(name=TEMPLATE_NAME)
        self.mock_ov_client.server_profile_templates.get_new_profile.assert_called_once_with(id_or_uri=TEMPLATE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                server_profile_templates=[BASIC_TEMPLATE],
                new_profile=PROFILE
            )
        )

    def test_should_get_template_by_name_with_options(self):
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        self.mock_ov_client.server_profile_templates.get_new_profile.return_value = PROFILE
        self.mock_ov_client.server_profile_templates.get_transformation.return_value = TRANSFORMATION_TEMPLATE

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        ServerProfileTemplateFactsModule().run()

        self.mock_ov_client.server_profile_templates.get_by_name.assert_called_once_with(name=TEMPLATE_NAME)
        self.mock_ov_client.server_profile_templates.get_new_profile.assert_called_once_with(id_or_uri=TEMPLATE_URI)
        self.mock_ov_client.server_profile_templates.get_transformation.assert_called_once_with(
            id_or_uri=TEMPLATE_URI,
            server_hardware_type_uri=SERVER_HARDWARE_TYPE_FOR_TRANSFORMATION,
            enclosure_group_uri=ENCLOSURE_GROUP_FOR_TRANSFORMATION
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                server_profile_templates=[BASIC_TEMPLATE],
                new_profile=PROFILE,
                transformation=TRANSFORMATION_TEMPLATE
            )
        )


if __name__ == '__main__':
    unittest.main()
