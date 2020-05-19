#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

from copy import deepcopy
from hpe_test_utils import ImageStreamerBaseTest
from oneview_module_loader import ArtifactBundleModule


YAML_ARTIFACT_BUNDLE = """
    config: "{{ config }}"
    state: present
    data:
        uri: /rest/artifact-bundles/4671582d-1746-4122-9cf0-642a59543509
        name: "AB"
    """

YAML_ARTIFACT_BUNDLE_PRESENT = """
        config: "{{ config }}"
        state: present
        data:
            name: "AB"
        """

YAML_ARTIFACT_BUNDLE_UPLOAD = """
        config: "{{ config }}"
        state: present
        data:
            name: "AB"
            localArtifactBundleFilePath: "ab_path"
        """

YAML_ARTIFACT_BUNDLE_RENAME = """
        config: "{{ config }}"
        state: present
        data:
            name: "AB"
            newName: "AB (renamed)"
        """

YAML_ARTIFACT_BUNDLE_NO_RENAME = """
    config: "{{ config }}"
    state: present
    data:
        name: "AB (renamed)"
        newName: "AB"
    """

YAML_ARTIFACT_BUNDLE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: "AB"
        """

YAML_ARTIFACT_BUNDLE_DOWNLOAD = """
        config: "{{ config }}"
        state: download
        data:
            destinationFilePath: "ab_path"
        """

YAML_ARTIFACT_BUNDLE_EXTRACT = """
        config: "{{ config }}"
        state: extract
        data:
            name: "AB"
        """

YAML_ARTIFACT_BUNDLE_BACKUP_CREATE = """
        config: "{{ config }}"
        state: backup_create
        data:
            name: "AB_backup"
        """

YAML_ARTIFACT_BUNDLE_BACKUP_EXTRACT = """
        config: "{{ config }}"
        state: backup_extract
        data:
            name: "AB_backup"
        """

YAML_ARTIFACT_BUNDLE_BACKUP_UPLOAD = """
        config: "{{ config }}"
        state: backup_upload
        data:
            deploymentGroupURI: "/rest/deployment-groups/test"
            localBackupArtifactBundleFilePath: "ab_path"
        """

YAML_ARTIFACT_BUNDLE_BACKUP_DOWNLOAD = """
        config: "{{ config }}"
        state: archive_download
        data:
            destinationFilePath: "ab_backup"
        """

DICT_DEFAULT_ARTIFACT_BUNDLE = yaml.load(YAML_ARTIFACT_BUNDLE)["data"]


@pytest.mark.resource(TestArtifactBundleModule='artifact_bundles')
class TestArtifactBundleModule(ImageStreamerBaseTest):
    """
    ImageStreamerBaseTest has common tests for main function,
    also provides the mocks used in this test case
    """
    def test_should_create_when_resource_not_exist(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_PRESENT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_CREATED,
            ansible_facts=dict(artifact_bundle=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_should_not_update_when_existing_data_is_equals(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_PRESENT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(artifact_bundle=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_should_update_when_data_has_modified_attributes(self):
        data_merged = DICT_DEFAULT_ARTIFACT_BUNDLE.copy()
        data_merged['newName'] = 'New Name'

        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_RENAME)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_UPDATED,
            ansible_facts=dict(artifact_bundle=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_should_upload_when_data_has_destination_path(self):
        self.resource.get_by_name.return_value = None
        self.resource.upload_bundle_from_file.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_UPLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_UPLOADED,
            ansible_facts=dict(artifact_bundle=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_should_delete_hypervisor_cluster_profile_when_resource_exist(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.delete.return_value = True
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_ABSENT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_DELETED,
        )

    def test_should_do_nothing_when_resource_already_absent(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_ABSENT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ALREADY_ABSENT,
        )

    def test_should_download(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.download.return_value = True
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_DOWNLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_DOWNLOADED,
            ansible_facts=dict()
        )

    def test_download_should_fail(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_DOWNLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ArtifactBundleModule.MSG_REQUIRED)

    def test_should_extract(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.extract.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_EXTRACT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_EXTRACTED,
            ansible_facts=dict(artifact_bundle=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_extract_should_fail(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_EXTRACT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ArtifactBundleModule.MSG_REQUIRED)

    def test_should_create_backup(self):
        self.resource.create_backup.return_value = self.resource
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_CREATE)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_BACKUP_CREATED,
            ansible_facts=dict(artifact_bundle_deployment_group=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_should_download_backup(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.get_all_backups.return_value = [DICT_DEFAULT_ARTIFACT_BUNDLE]
        self.resource.get_backup.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.download_archive.return_value = True
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_DOWNLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ArtifactBundleModule.MSG_ARCHIVE_DOWNLOADED,
            ansible_facts=dict()
        )

    def test_backup_download_should_fail(self):
        self.resource.get_all_backups.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_DOWNLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ArtifactBundleModule.MSG_BACKUP_REQUIRED)

    def test_should_extract_backup(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.get_all_backups.return_value = [DICT_DEFAULT_ARTIFACT_BUNDLE]
        self.resource.get_backup.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.extract_backup.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_EXTRACT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_BACKUP_EXTRACTED,
            ansible_facts=dict(artifact_bundle_deployment_group=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )

    def test_backup_extract_should_fail(self):
        self.resource.get_all_backups.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_EXTRACT)

        ArtifactBundleModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=ArtifactBundleModule.MSG_BACKUP_REQUIRED)

    def test_should_upload_backup(self):
        self.resource.data = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.resource.upload_backup_bundle_from_file.return_value = DICT_DEFAULT_ARTIFACT_BUNDLE
        self.mock_ansible_module.params = yaml.load(YAML_ARTIFACT_BUNDLE_BACKUP_UPLOAD)

        ArtifactBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ArtifactBundleModule.MSG_BACKUP_UPLOADED,
            ansible_facts=dict(artifact_bundle_deployment_group=DICT_DEFAULT_ARTIFACT_BUNDLE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
