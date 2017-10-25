#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from ansible.compat.tests import unittest
from oneview_module_loader import StorageVolumeTemplateFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="FusionTemplateExample"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_CONNECTED = dict(
    config='config.json',
    options=['connectableVolumeTemplates']
)

PARAMS_GET_REACHABLE = dict(
    config='config.json',
    options=['reachableVolumeTemplates']
)

PARAMS_GET_COMPATIBLE = dict(
    config='config.json',
    name="SVT1",
    options=['compatibleSystems']
)

DEFAULT_VOLUME_TEMPLATES_RETURN = [{"name": "Storage Volume Template 1"}]


class StorageVolumeTemplatesFactsSpec(unittest.TestCase,
                                      FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageVolumeTemplateFactsModule)
        self.storage_volume_templates = self.mock_ov_client.storage_volume_templates
        FactsParamsTestCase.configure_client_mock(self, self.storage_volume_templates)

    def test_should_get_all_storage_volume_templates(self):
        self.storage_volume_templates.get_all.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN

        self.mock_ansible_module.params = PARAMS_GET_ALL

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_templates=(DEFAULT_VOLUME_TEMPLATES_RETURN))
        )

    def test_should_get_storage_volume_template_by_name(self):
        self.storage_volume_templates.get_by.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_templates=(DEFAULT_VOLUME_TEMPLATES_RETURN))
        )

    def test_should_get_connectable_storage_volume_templates(self):
        self.storage_volume_templates.get_all.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN
        self.storage_volume_templates.get_connectable_volume_templates.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN

        self.mock_ansible_module.params = PARAMS_GET_CONNECTED

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'connectable_volume_templates': DEFAULT_VOLUME_TEMPLATES_RETURN,
                           'storage_volume_templates': DEFAULT_VOLUME_TEMPLATES_RETURN}
        )

    def test_should_get_reachable_storage_volume_templates(self):
        self.storage_volume_templates.get_all.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN
        self.storage_volume_templates.get_reachable_volume_templates.return_value = DEFAULT_VOLUME_TEMPLATES_RETURN

        self.mock_ansible_module.params = PARAMS_GET_REACHABLE

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'reachable_volume_templates': DEFAULT_VOLUME_TEMPLATES_RETURN,
                           'storage_volume_templates': DEFAULT_VOLUME_TEMPLATES_RETURN}
        )

    def test_should_get_compatible_systems(self):
        self.storage_volume_templates.get_by.return_value = [{'name': 'SVT1', 'uri': '/rest/fake'}]
        self.storage_volume_templates.get_compatible_systems.return_value = {
            "name": "Storage System Name"}

        self.mock_ansible_module.params = PARAMS_GET_COMPATIBLE

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'compatible_systems': {'name': 'Storage System Name'},
                           'storage_volume_templates': [{'name': 'SVT1', 'uri': '/rest/fake'}]}
        )


if __name__ == '__main__':
    unittest.main()
