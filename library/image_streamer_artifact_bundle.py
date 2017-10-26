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
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author:
    - "Abilio Parada (@abiliogp)"
options:
    state:
      description:
        - Indicates the desired state for the Artifact Bundle resource.
          C(present) will ensure data properties are compliant with OneView. When the artifact bundle already exists,
          only the name is updated. Changes in any other attribute value is ignored.
          C(absent) will remove the resource from OneView, if it exists.
          C(downloaded) will download the Artifact Bundle to the file path provided.
          C(archive_downloaded) will download the Artifact Bundle archive to the file path provided.
          C(backup_uploaded) will upload the Backup for the Artifact Bundle from the file path provided.
          C(backup_created) will create a Backup for the Artifact Bundle.
          C(extracted) will extract an Artifact Bundle.
          C(backup_extracted) will extract an Artifact Bundle from the Backup.
      choices: ['present', 'absent', 'downloaded', 'archive_downloaded',
                'backup_uploaded', 'backup_created', 'extracted', 'backup_extracted']
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
    state: downloaded
    data:
      name: 'Artifact Bundle'
      destinationFilePath: '~/downloaded_artifact.zip'
  delegate_to: localhost

- name: Download the Archive for Artifact Bundle to the file path provided
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: archive_downloaded
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
    state: backup_uploaded
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
      localBackupArtifactBundleFilePath: '~/uploaded_backup.zip'
  delegate_to: localhost

- name: Create Backup for Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_created
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
  delegate_to: localhost

- name: Extract an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: extracted
    data:
      name: 'Artifact Bundle'
  delegate_to: localhost

- name: Extract Backup an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_extracted
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
    returned: On state 'present' and 'extracted'.
    type: dict

artifact_bundle_deployment_group:
    description: Has the OneView facts about the Deployment Group.
    returned: On state 'backup_extracted', 'backup_uploaded', and 'backup_created'.
    type: dict
'''

import os
from ansible.module_utils.oneview import OneViewModuleBase, compare


class ArtifactBundleModule(OneViewModuleBase):
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

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'downloaded', 'archive_downloaded', 'backup_created',
                     'backup_uploaded', 'extracted', 'backup_extracted']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(ArtifactBundleModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.artifact_bundles

    def execute_module(self):
        ansible_facts = {}

        resource = self.__get_by_name(self.data.get('name'))

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present(self.data, resource)
        elif self.state == 'absent':
            return self.resource_absent(resource)
        elif self.state == 'downloaded':
            changed, msg, ansible_facts = self.__download(self.data, resource)
        elif self.state == 'archive_downloaded':
            changed, msg, ansible_facts = self.__download_archive(self.data, resource)
        elif self.state == 'backup_uploaded':
            changed, msg, ansible_facts = self.__upload_backup(self.data)
        elif self.state == 'backup_created':
            changed, msg, ansible_facts = self.__create_backup(self.data)
        elif self.state == 'extracted':
            changed, msg, ansible_facts = self.__extract(resource)
        elif self.state == 'backup_extracted':
            changed, msg, ansible_facts = self.__extract_backup(self.data)

        return dict(msg=msg, changed=changed, ansible_facts=ansible_facts)

    def __get_by_name(self, name):
        if name is None:
            return None
        return self.get_by_name(name)

    def __present(self, data, resource):
        if data.get('newName'):
            changed, msg, facts = self.__update(data, resource)
        elif data.get('localArtifactBundleFilePath'):
            changed, msg, facts = self.__upload(data)
        elif not resource:
            changed, msg, facts = self.__create(data)
        else:
            changed = False
            msg = self.MSG_ALREADY_PRESENT
            facts = dict(artifact_bundle=resource)
        return changed, msg, facts

    def __create(self, data):
        resource = self.i3s_client.artifact_bundles.create(data)
        return True, self.MSG_CREATED, dict(artifact_bundle=resource)

    def __update(self, data, resource):
        if resource is None:
            resource = self.__get_by_name(data['newName'])
        data["name"] = data.pop("newName")
        merged_data = resource.copy()
        merged_data.update(data)

        if not compare(resource, merged_data):
            resource = self.i3s_client.artifact_bundles.update(merged_data)
            changed = True
            msg = self.MSG_UPDATED
        else:
            changed = False
            msg = self.MSG_ALREADY_PRESENT
        return changed, msg, dict(artifact_bundle=resource)

    def __download(self, data, resource):
        self.i3s_client.artifact_bundles.download_artifact_bundle(resource['uri'], data['destinationFilePath'])
        return False, self.MSG_DOWNLOADED, {}

    def __download_archive(self, data, resource):
        self.i3s_client.artifact_bundles.download_archive_artifact_bundle(resource['uri'], data['destinationFilePath'])
        return False, self.MSG_ARCHIVE_DOWNLOADED, {}

    def __upload(self, data):
        file_name = data['localArtifactBundleFilePath']
        file_name_path = os.path.basename(file_name)
        file_name_wo_ext = os.path.splitext(file_name_path)[0]
        artifact_bundle = self.__get_by_name(file_name_wo_ext)
        if artifact_bundle is None:
            artifact_bundle = self.i3s_client.artifact_bundles.upload_bundle_from_file(file_name)
            changed = True
            msg = self.MSG_UPLOADED
        else:
            changed = False
            msg = self.MSG_ALREADY_PRESENT
        return changed, msg, dict(artifact_bundle=artifact_bundle)

    def __upload_backup(self, data):
        deployment_group = self.i3s_client.artifact_bundles.upload_backup_bundle_from_file(
            data['localBackupArtifactBundleFilePath'], data['deploymentGroupURI'])
        return True, self.MSG_BACKUP_UPLOADED, dict(artifact_bundle_deployment_group=deployment_group)

    def __create_backup(self, data):
        resource = self.i3s_client.artifact_bundles.create_backup(data)
        return False, self.MSG_BACKUP_CREATED, dict(artifact_bundle_deployment_group=resource)

    def __extract(self, resource):
        resource = self.i3s_client.artifact_bundles.extract_bundle(resource)
        return True, self.MSG_EXTRACTED, dict(artifact_bundle=resource)

    def __extract_backup(self, data):
        resource = self.i3s_client.artifact_bundles.extract_backup_bundle(data)
        return True, self.MSG_BACKUP_EXTRACTED, dict(artifact_bundle_deployment_group=resource)


def main():
    ArtifactBundleModule().run()


if __name__ == '__main__':
    main()
