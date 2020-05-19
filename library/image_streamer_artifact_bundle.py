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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: image_streamer_artifact_bundle
short_description: Manage the Artifact Bundle resource.
description:
    - "Provides an interface to manage the Artifact Bundle. Can create, update, remove, and download, upload, extract"
version_added: "2.3"
requirements:
    - "python >= 3.4.2"
    - "hpOneView >= 5.2.0"
author:
    - "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
      description:
        - Indicates the desired state for the Artifact Bundle resource.
          C(present) will ensure data properties are compliant with OneView. When the artifact bundle already exists,
          only the name is updated. Changes in any other attribute value is ignored.
          C(absent) will remove the resource from OneView, if it exists.
          C(download) will download the Artifact Bundle to the file path provided.
          C(archive_download) will download the Artifact Bundle archive to the file path provided.
          C(backup_upload) will upload the Backup for the Artifact Bundle from the file path provided.
          C(backup_create) will create a Backup for the Artifact Bundle.
          C(extract) will extract an Artifact Bundle.
          C(backup_extract) will extract an Artifact Bundle from the Backup.
      choices: ['present', 'absent', 'download', 'archive_download',
                'backup_upload', 'backup_create', 'extract', 'backup_extract']
      required: true
    data:
      description:
        - List with Artifact Bundle properties and its associated states.
      required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      name: 'Artifact Bundle'
      description: 'Description of Artifact Bundles Test'
      buildPlans:
        - resourceUri: '/rest/build-plans/ab65bb06-4387-48a0-9a5d-0b0da2888508'
          readOnly: 'false'
  delegate_to: localhost

- name: Download the Artifact Bundle to the file path provided
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: download
    data:
      name: 'Artifact Bundle'
      destinationFilePath: '~/downloaded_artifact.zip'
  delegate_to: localhost

- name: Download the Archive for Artifact Bundle to the file path provided
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: archive_download
    data:
      name: 'Artifact Bundle'
      destinationFilePath: '~/downloaded_archive.zip'
  delegate_to: localhost

- name: Upload an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      localArtifactBundleFilePath: '~/uploaded_artifact.zip'
  delegate_to: localhost

- name: Upload Backup an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_upload
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
      localBackupArtifactBundleFilePath: '~/uploaded_backup.zip'
  delegate_to: localhost

- name: Create Backup for Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_create
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
  delegate_to: localhost

- name: Extract an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: extract
    data:
      name: 'Artifact Bundle'
  delegate_to: localhost

- name: Extract Backup an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_extract
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
  delegate_to: localhost

- name: Update an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      name: 'Artifact Bundle'
      newName: 'Artifact Bundle Updated'
  delegate_to: localhost

- name: Remove an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: absent
    data:
      name: 'Artifact Bundle'
  delegate_to: localhost
'''

RETURN = '''
artifact_bundle:
    description: Has the OneView facts about the Artifact Bundles.
    returned: On state 'present' and 'extract'.
    type: dict

artifact_bundle_deployment_group:
    description: Has the OneView facts about the Deployment Group.
    returned: On state 'backup_extract', 'backup_upload', and 'backup_create'.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, compare


class ArtifactBundleModule(OneViewModule):
    MSG_CREATED = 'Artifact Bundle created successfully.'
    MSG_UPDATED = 'Artifact Bundle updated successfully.'
    MSG_DELETED = 'Artifact Bundle deleted successfully.'
    MSG_ALREADY_ABSENT = 'Artifact Bundle is already absent.'
    MSG_ALREADY_PRESENT = 'Artifact Bundle is already present.'
    MSG_DOWNLOADED = 'Artifact Bundle downloaded successfully.'
    MSG_UPLOADED = 'Artifact Bundle uploaded successfully.'
    MSG_BACKUP_UPLOADED = 'Backup for Artifact Bundle uploaded successfully.'
    MSG_ARCHIVE_DOWNLOADED = 'Archive of Artifact Bundle downloaded successfully.'
    MSG_BACKUP_CREATED = 'Backup of Artifact Bundle created successfully.'
    MSG_EXTRACTED = 'Artifact Bundle extracted successfully.'
    MSG_BACKUP_EXTRACTED = 'Artifact Bundle extracted successfully.'
    MSG_REQUIRED = "An existing Artifact Bundle is required."
    MSG_BACKUP_REQUIRED = "An existing Backup is required"

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'download', 'archive_download', 'backup_create',
                     'backup_upload', 'extract', 'backup_extract']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(ArtifactBundleModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.set_resource_object(self.i3s_client.artifact_bundles)

    def execute_module(self):
        ansible_facts = {}

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present()
        elif self.state == 'absent':
            return self.resource_absent()
        elif self.state == 'download':
            changed, msg, ansible_facts = self.__download()
        elif self.state == 'archive_download':
            changed, msg, ansible_facts = self.__download_archive()
        elif self.state == 'backup_upload':
            changed, msg, ansible_facts = self.__upload_backup()
        elif self.state == 'backup_create':
            changed, msg, ansible_facts = self.__create_backup()
        elif self.state == 'extract':
            changed, msg, ansible_facts = self.__extract()
        elif self.state == 'backup_extract':
            changed, msg, ansible_facts = self.__extract_backup()

        return dict(msg=msg, changed=changed, ansible_facts=ansible_facts)

    def __present(self):
        if not self.current_resource:
            if self.data.get('localArtifactBundleFilePath'):
                changed, msg, facts = self.__upload()
            else:
                changed, msg, facts = self.__create()
        else:
            changed, msg, facts = self.__update()
        return changed, msg, facts

    def __upload(self):
        file_name = self.data['localArtifactBundleFilePath']
        artifact_bundle = self.resource_client.upload_bundle_from_file(file_name)
        return True, self.MSG_UPLOADED, dict(artifact_bundle=artifact_bundle)

    def __create(self):
        self.current_resource = self.resource_client.create(self.data)
        return True, self.MSG_CREATED, dict(artifact_bundle=self.current_resource.data)

    def __update(self):
        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        merged_data = self.current_resource.data.copy()
        merged_data.update(self.data)

        if not compare(self.current_resource.data, merged_data):
            self.current_resource.update(merged_data)
            return True, self.MSG_UPDATED, dict(artifact_bundle=self.current_resource.data)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(artifact_bundle=self.current_resource.data)

    def __download(self):
        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_REQUIRED)

        self.current_resource.download(self.data['destinationFilePath'])
        return False, self.MSG_DOWNLOADED, {}

    def __extract(self):
        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_REQUIRED)
        resource = self.current_resource.extract()
        return True, self.MSG_EXTRACTED, dict(artifact_bundle=resource)

    def __create_backup(self):
        self.current_resource = self.resource_client.create_backup(self.data)
        return True, self.MSG_BACKUP_CREATED, dict(artifact_bundle_deployment_group=self.current_resource.data)

    def __download_archive(self):
        self.allbackups = self.resource_client.get_all_backups()
        if len(self.allbackups) == 0:
            raise OneViewModuleResourceNotFound(self.MSG_BACKUP_REQUIRED)

        self.current_resource = self.resource_client.get_backup(self.allbackups[0]['uri'])
        self.current_resource.download_archive(self.data['destinationFilePath'])
        return False, self.MSG_ARCHIVE_DOWNLOADED, {}

    def __extract_backup(self):
        self.allbackups = self.resource_client.get_all_backups()
        if len(self.allbackups) == 0:
            raise OneViewModuleResourceNotFound(self.MSG_BACKUP_REQUIRED)

        self.current_resource = self.resource_client.get_backup(self.allbackups[0]['uri'])
        resource = self.current_resource.extract_backup(self.data)
        return True, self.MSG_BACKUP_EXTRACTED, dict(artifact_bundle_deployment_group=resource)

    def __upload_backup(self):
        if self.data.get('localBackupArtifactBundleFilePath') and self.data.get('deploymentGroupURI'):
            deployment_group = self.resource_client.upload_backup_bundle_from_file(
                self.data['localBackupArtifactBundleFilePath'], self.data['deploymentGroupURI'])
        return True, self.MSG_BACKUP_UPLOADED, dict(artifact_bundle_deployment_group=deployment_group)


def main():
    ArtifactBundleModule().run()


if __name__ == '__main__':
    main()
