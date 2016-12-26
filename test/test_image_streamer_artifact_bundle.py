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

from image_streamer_artifact_bundle import ArtifactBundleModule, EXAMPLES
from test.utils import ModuleContructorTestCase, PreloadedMocksBaseTestCase


ERROR_MSG = 'Fake message error'


class ArtifactBundleSpec(unittest.TestCase, ModuleContructorTestCase, PreloadedMocksBaseTestCase):

    def setUp(self):
        self.configure_mocks(self, ArtifactBundleModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        self.ARTIFACT_BUNDLE_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_CREATE = self.ARTIFACT_BUNDLE_EXAMPLES[0]['image_streamer_artifact_bundle']
        self.TASK_DOWNLOAD = self.ARTIFACT_BUNDLE_EXAMPLES[1]['image_streamer_artifact_bundle']
        self.TASK_DOWNLOAD_ARCHIVE = self.ARTIFACT_BUNDLE_EXAMPLES[2]['image_streamer_artifact_bundle']
        self.TASK_UPLOAD = self.ARTIFACT_BUNDLE_EXAMPLES[3]['image_streamer_artifact_bundle']
        self.TASK_BACKUP_UPLOAD = self.ARTIFACT_BUNDLE_EXAMPLES[4]['image_streamer_artifact_bundle']
        self.TASK_CREATE_BACKUP = self.ARTIFACT_BUNDLE_EXAMPLES[5]['image_streamer_artifact_bundle']
        self.TASK_EXTRACT = self.ARTIFACT_BUNDLE_EXAMPLES[6]['image_streamer_artifact_bundle']
        self.TASK_BACKUP_EXTRACT = self.ARTIFACT_BUNDLE_EXAMPLES[7]['image_streamer_artifact_bundle']
        self.TASK_UPDATE = self.ARTIFACT_BUNDLE_EXAMPLES[8]['image_streamer_artifact_bundle']
        self.TASK_REMOVE = self.ARTIFACT_BUNDLE_EXAMPLES[9]['image_streamer_artifact_bundle']

        self.BUILD_PLANS = dict(
            resourceUri="/rest/build-plans/ab65bb06-4387-48a0-9a5d-0b0da2888508",
            readOnly="false"
        )

        self.ARTIFACT_BUNDLE = dict(
            name="Artifact Bundle",
            description="Description of Artifact Bundles Test",
            buildPlans=[self.BUILD_PLANS]
        )

    def test_create_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = []
        self.i3s.artifact_bundles.create.return_value = self.ARTIFACT_BUNDLE
        self.mock_ansible_module.params = self.TASK_CREATE

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.create.assert_called_once_with(
            self.ARTIFACT_BUNDLE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(self.ARTIFACT_BUNDLE)
        )

    def test_download_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.i3s.artifact_bundles.get_by.return_value = [artifact_bundle]

        self.mock_ansible_module.params = self.TASK_DOWNLOAD

        ArtifactBundleModule().run()

        download_file = self.TASK_DOWNLOAD['data']['destinationFilePath']
        uri = artifact_bundle['uri']

        self.i3s.artifact_bundles.download_artifact_bundle.assert_called_once_with(uri, download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={})

    def test_download_archives_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.i3s.artifact_bundles.get_by.return_value = [artifact_bundle]

        self.mock_ansible_module.params = self.TASK_DOWNLOAD_ARCHIVE

        ArtifactBundleModule().run()

        download_file = self.TASK_DOWNLOAD_ARCHIVE['data']['destinationFilePath']
        uri = artifact_bundle['uri']

        self.i3s.artifact_bundles.download_archive_artifact_bundle.assert_called_once_with(uri, download_file)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={})

    def test_upload_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = []
        self.i3s.artifact_bundles.upload_bundle_from_file.return_value = True

        self.mock_ansible_module.params = self.TASK_UPLOAD

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.upload_bundle_from_file.assert_called_once_with(
            self.TASK_UPLOAD['data']['localArtifactBundleFilePath'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts={})

    def test_upload_backup_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = []
        self.i3s.artifact_bundles.upload_backup_bundle_from_file.return_value = True

        self.mock_ansible_module.params = self.TASK_BACKUP_UPLOAD

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.upload_backup_bundle_from_file.assert_called_once_with(
            self.TASK_BACKUP_UPLOAD['data']['localBackupArtifactBundleFilePath'],
            self.TASK_BACKUP_UPLOAD['data']['deploymentGroupsUri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts={})

    def test_create_backup_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.i3s.artifact_bundles.create_backup.return_value = artifact_bundle

        self.mock_ansible_module.params = self.TASK_CREATE_BACKUP

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.create_backup.assert_called_once_with(
            self.TASK_CREATE_BACKUP['data']['deploymentGroupsUri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=artifact_bundle)

    def test_extract_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.i3s.artifact_bundles.get_by.return_value = [artifact_bundle]

        self.i3s.artifact_bundles.extract_bundle.return_value = artifact_bundle

        self.mock_ansible_module.params = self.TASK_EXTRACT

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.extract_bundle.assert_called_once_with(
            artifact_bundle['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts={})

    def test_backup_extract_artifact_bundle(self):
        artifact_bundle = self.TASK_CREATE['data']
        artifact_bundle['uri'] = '/rest/artifact-bundles/1'

        self.i3s.artifact_bundles.get_by.return_value = [artifact_bundle]

        self.i3s.artifact_bundles.extract_backup_bundle.return_value = artifact_bundle

        self.mock_ansible_module.params = self.TASK_BACKUP_EXTRACT

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.extract_backup_bundle.assert_called_once_with(
            self.TASK_CREATE_BACKUP['data']['deploymentGroupsUri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=artifact_bundle)

    def test_update_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.update.return_value = self.ARTIFACT_BUNDLE

        self.mock_ansible_module.params = self.TASK_UPDATE

        ArtifactBundleModule().run()

        self.ARTIFACT_BUNDLE['name'] = 'Artifact Bundle Updated'

        self.i3s.artifact_bundles.update.assert_called_once_with(
            self.ARTIFACT_BUNDLE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(self.ARTIFACT_BUNDLE)
        )

    def test_delete_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.delete.return_value = self.ARTIFACT_BUNDLE

        self.mock_ansible_module.params = self.TASK_REMOVE

        ArtifactBundleModule().run()

        self.i3s.artifact_bundles.delete.assert_called_once_with(
            self.ARTIFACT_BUNDLE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts={}
        )

    def test_should_fail_when_create_raises_exception(self):
        self.i3s.artifact_bundles.get_by.return_value = []
        self.i3s.artifact_bundles.create.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = self.TASK_CREATE

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ERROR_MSG
        )

    def test_should_fail_when_delete_raises_exception(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.TASK_CREATE]
        self.i3s.artifact_bundles.delete.side_effect = Exception(ERROR_MSG)

        self.mock_ansible_module.params = self.TASK_REMOVE

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ERROR_MSG
        )


if __name__ == '__main__':
    unittest.main()
