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

from image_streamer_artifact_bundle_facts import ArtifactBundleFactsModule, EXAMPLES
from test.utils import ModuleContructorTestCase, FactsParamsTestCase


ERROR_MSG = 'Fake message error'


class ArtifactBundleFactsSpec(unittest.TestCase,
                              ModuleContructorTestCase,
                              FactsParamsTestCase):
    """
    ModuleContructorTestCase has common tests for the class constructor and the main function, and also provides the
    mocks used in this test class.

    FactsParamsTestCase has common tests for the parameters support.
    """
    def setUp(self):
        self.configure_mocks(self, ArtifactBundleFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.artifact_bundles)

        self.ARTIFACT_BUNDLE_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.ARTIFACT_BUNDLE_EXAMPLES[0]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_BY_NAME = self.ARTIFACT_BUNDLE_EXAMPLES[4]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_ALL_BACKUPS = self.ARTIFACT_BUNDLE_EXAMPLES[6]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_BACKUP = self.ARTIFACT_BUNDLE_EXAMPLES[9]['image_streamer_artifact_bundle_facts']

        self.ARTIFACT_BUNDLE = dict(
            name="HPE-ImageStreamer-Developer-2016-09-12",
            uri="/rest/artifact-bundles/a2f97f20-160c-4c78-8185-1f31f86efaf7")

    def test_get_all_artifact_bundles(self):
        self.i3s.artifact_bundles.get_all.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_an_artifact_bundle_by_name(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_all_backups(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.get_all_backups.return_value = [self.ARTIFACT_BUNDLE]

        self.mock_ansible_module.params = self.TASK_GET_ALL_BACKUPS

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE], artifact_bundle_backups=[self.ARTIFACT_BUNDLE])
        )

    def test_get_backup_for_an_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.get_backup.return_value = [self.ARTIFACT_BUNDLE]

        self.mock_ansible_module.params = self.TASK_GET_BACKUP

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE],
                               backup_for_artifact_bundle=[self.ARTIFACT_BUNDLE])
        )

    def test_should_fail_when_get_all_raises_an_exception(self):
        self.i3s.artifact_bundles.get_all.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.TASK_GET_ALL

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ERROR_MSG)

    def test_should_fail_when_get_by_name_raises_an_exception(self):
        self.i3s.artifact_bundles.get_by.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ERROR_MSG)

    def test_should_fail_when_get_all_backups_raises_an_exception(self):
        self.i3s.artifact_bundles.get_all_backups.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.TASK_GET_ALL_BACKUPS

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ERROR_MSG)

    def test_should_fail_when_get_backup_for_an_artifact_bundle_raises_an_exception(self):
        self.i3s.artifact_bundles.get_backup.side_effect = Exception(ERROR_MSG)
        self.mock_ansible_module.params = self.TASK_GET_BACKUP

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
