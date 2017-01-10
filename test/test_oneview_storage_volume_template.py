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

from oneview_storage_volume_template import StorageVolumeTemplateModule, STORAGE_VOLUME_TEMPLATE_CREATED, \
    STORAGE_VOLUME_TEMPLATE_DELETED, STORAGE_VOLUME_TEMPLATE_ALREADY_ABSENT, \
    STORAGE_VOLUME_TEMPLATE_ALREADY_UPDATED, STORAGE_VOLUME_TEMPLATE_UPDATED

from utils import ModuleContructorTestCase, ValidateEtagTestCase

FAKE_MSG_ERROR = 'Fake message error'

STORAGE_VOLUME_TEMPLATE = dict(
    name='StorageVolumeTemplate Test',
    state='Configured',
    description='Example Template',
    provisioning=dict(
         shareable='true',
         provisionType='Thin',
         capacity='235834383322',
         storagePoolUri='{{storage_pool_uri}}'),
    stateReason='None',
    storageSystemUri='{{ storage_system_uri }}',
    snapshotPoolUri='{{storage_pool_uri}}',
    type='StorageVolumeTemplateV3'
)

STORAGE_VOLUME_TEMPLATE_WITH_NEW_DESCRIPTION = dict(
    STORAGE_VOLUME_TEMPLATE, description='Example Template with a new description')


PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=STORAGE_VOLUME_TEMPLATE
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=STORAGE_VOLUME_TEMPLATE_WITH_NEW_DESCRIPTION
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=STORAGE_VOLUME_TEMPLATE['name'])
)


class StorageVolumeTemplatePresentStateSpec(unittest.TestCase, ModuleContructorTestCase, ValidateEtagTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    ValidateEtagTestCase has common tests for the validate_etag attribute.
    """

    def setUp(self):
        self.configure_mocks(self, StorageVolumeTemplateModule)
        self.resource = self.mock_ov_client.storage_volume_templates

    def test_should_create_new_storage_volume_template(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_CREATED,
            ansible_facts=dict(storage_volume_template={"name": "name"})
        )

    def test_should_update_the_storage_volume_template(self):
        self.resource.get_by.return_value = [STORAGE_VOLUME_TEMPLATE]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_UPDATED,
            ansible_facts=dict(storage_volume_template={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [STORAGE_VOLUME_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=STORAGE_VOLUME_TEMPLATE_ALREADY_UPDATED,
            ansible_facts=dict(storage_volume_template=STORAGE_VOLUME_TEMPLATE)
        )


class StorageVolumeTemplateAbsentStateSpec(unittest.TestCase, ModuleContructorTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, StorageVolumeTemplateModule)
        self.resource = self.mock_ov_client.storage_volume_templates

    def test_should_remove_storage_volume_template(self):
        self.resource.get_by.return_value = [STORAGE_VOLUME_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=True,
            msg=STORAGE_VOLUME_TEMPLATE_DELETED
        )

    def test_should_do_nothing_when_storage_volume_template_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            ansible_facts={},
            changed=False,
            msg=STORAGE_VOLUME_TEMPLATE_ALREADY_ABSENT
        )


class StorageVolumeTemplateErrorHandlingSpec(unittest.TestCase, ModuleContructorTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, StorageVolumeTemplateModule)
        self.resource = self.mock_ov_client.storage_volume_templates

    def test_should_fail_when_create_raises_exception(self):
        self.resource.get_by.return_value = []
        self.resource.create.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_update_raises_exception(self):
        self.resource.get_by.return_value = [STORAGE_VOLUME_TEMPLATE]
        self.resource.update.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.resource.get_by.return_value = [STORAGE_VOLUME_TEMPLATE]
        self.resource.delete.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        self.assertRaises(Exception, StorageVolumeTemplateModule().run())

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
