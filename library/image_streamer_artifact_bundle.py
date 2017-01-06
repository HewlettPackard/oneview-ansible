#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from ansible.module_utils.basic import *
import os.path

try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: image_streamer_artifact_bundle
short_description: Manage Artifact Bundle resource.
description:
    - "Provides an interface to manage Artifact Bundle. Can create, update, remove, and also, download, upload, extract"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Abilio Parada (@abiliogp)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
      description:
        - Indicates the desired state for the Artifact Bundle resource.
          'present' will ensure data properties are compliant with OneView.
          'absent' will remove the resource from OneView, if it exists.
          'downloaded' will download the Artifact Bundle to the file path provided.
          'archive_downloaded' will download the Artifact Bundle archive to the file path provided.
          'backup_uploaded' will upload the Backup of Artifact Bundle from the file path provided.
          'backup_created' will create a Backup for Artifact Bundle.
          'extracted' will extract an Artifact Bundle.
          'backup_extracted' will extract an Artifact Bundle from Backup.
      choices: ['present', 'absent', 'downloaded', 'archive_downloaded',
                'backup_uploaded', 'backup_created', 'extracted','backup_extracted']
      required: true
    data:
      description:
        - List with Artifact Bundle properties and its associated states.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
        resourceUri: '/rest/build-plans/ab65bb06-4387-48a0-9a5d-0b0da2888508'
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
    type: complex

artifact_bundle_deployment_group:
    description: Has the OneView facts about the Deployment Group.
    returned: On state 'backup_extracted', 'backup_uploaded', and 'backup_created'.
    type: complex
'''

ARTIFACT_BUNDLE_CREATED = 'Artifact Bundle created successfully.'
ARTIFACT_BUNDLE_UPDATED = 'Artifact Bundle updated successfully.'
ARTIFACT_BUNDLE_DELETED = 'Artifact Bundle deleted successfully.'
ARTIFACT_BUNDLE_ABSENT = 'Artifact Bundle is already absent.'
ARTIFACT_BUNDLE_ALREADY_EXIST = 'Artifact Bundle already exists.'
ARTIFACT_BUNDLE_DOWNLOADED = 'Artifact Bundle downloaded successfully.'
ARTIFACT_BUNDLE_UPLOADED = 'Artifact Bundle uploaded successfully.'
BACKUP_UPLOADED = 'Backup for Artifact Bundle uploaded successfully.'
ARCHIVE_DOWNLOADED = 'Archive of Artifact Bundle downloaded successfully.'
BACKUP_CREATED = 'Backup of Artifact Bundle created successfully.'
ARTIFACT_BUNDLE_EXTRACTED = 'Artifact Bundle extracted successfully.'
BACKUP_EXTRACTED = 'Artifact Bundle extracted successfully.'

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ArtifactBundleModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'downloaded', 'archive_downloaded', 'backup_created',
                     'backup_uploaded', 'extracted', 'backup_extracted']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def run(self):
        try:
            ansible_facts = {}

            state = self.module.params.get('state')
            data = self.module.params.get('data')
            name = data.get('name')

            resource = self.__get_by_name(name)

            if state == 'present':
                changed, msg, ansible_facts = self.__present(data, resource)

            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)

            elif state == 'downloaded':
                changed, msg, ansible_facts = self.__download(data, resource)
            elif state == 'archive_downloaded':
                changed, msg, ansible_facts = self.__download_archive(data, resource)

            elif state == 'backup_uploaded':
                changed, msg, ansible_facts = self.__upload_backup(data)

            elif state == 'backup_created':
                changed, msg, ansible_facts = self.__create_backup(data)

            elif state == 'extracted':
                changed, msg, ansible_facts = self.__extract(resource)
            elif state == 'backup_extracted':
                changed, msg, ansible_facts = self.__extract_backup(data)

            self.module.exit_json(msg=msg, changed=changed, ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_by_name(self, name):
        if name is None:
            return None
        return (self.i3s_client.artifact_bundles.get_by('name', name) or [None])[0]

    def __present(self, data, resource):
        if data.get('newName'):
            changed, msg, facts = self.__update(data, resource)
        elif data.get('localArtifactBundleFilePath'):
            changed, msg, facts = self.__upload(data)
        elif not resource:
            changed, msg, facts = self.__create(data)
        else:
            changed = False
            msg = ARTIFACT_BUNDLE_ALREADY_EXIST
            facts = dict(artifact_bundle=resource)
        return changed, msg, facts

    def __absent(self, resource):
        if resource:
            self.i3s_client.artifact_bundles.delete(resource)
            changed = True
            msg = ARTIFACT_BUNDLE_DELETED
        else:
            changed = False
            msg = ARTIFACT_BUNDLE_ABSENT
        return changed, msg, {}

    def __create(self, data):
        data['buildPlans'] = [data['buildPlans']]
        resource = self.i3s_client.artifact_bundles.create(data)
        return True, ARTIFACT_BUNDLE_CREATED, dict(artifact_bundle=resource)

    def __update(self, data, resource):
        if resource is None:
            resource = self.__get_by_name(data['newName'])
        data["name"] = data.pop("newName")
        merged_data = resource.copy()
        merged_data.update(data)

        if not resource_compare(resource, merged_data):
            resource = self.i3s_client.artifact_bundles.update(merged_data)
            changed = True
            msg = ARTIFACT_BUNDLE_UPDATED
        else:
            changed = False
            msg = ARTIFACT_BUNDLE_ALREADY_EXIST
        return changed, msg, dict(artifact_bundle=resource)

    def __download(self, data, resource):
        self.i3s_client.artifact_bundles.download_artifact_bundle(resource['uri'], data['destinationFilePath'])
        return False, ARTIFACT_BUNDLE_DOWNLOADED, {}

    def __download_archive(self, data, resource):
        self.i3s_client.artifact_bundles.download_archive_artifact_bundle(resource['uri'], data['destinationFilePath'])
        return False, ARCHIVE_DOWNLOADED, {}

    def __upload(self, data):
        file_name = data['localArtifactBundleFilePath']
        file_name_path = os.path.basename(file_name)
        file_name_wo_ext = os.path.splitext(file_name_path)[0]
        artifact_bundle = self.__get_by_name(file_name_wo_ext)
        if artifact_bundle is None:
            artifact_bundle = self.i3s_client.artifact_bundles.upload_bundle_from_file(file_name)
            changed = True
            msg = ARTIFACT_BUNDLE_UPLOADED
        else:
            changed = False
            msg = ARTIFACT_BUNDLE_ALREADY_EXIST
        return changed, msg, dict(artifact_bundle=artifact_bundle)

    def __upload_backup(self, data):
        deployment_group = self.i3s_client.artifact_bundles.upload_backup_bundle_from_file(
            data['localBackupArtifactBundleFilePath'], data['deploymentGroupURI'])
        return True, BACKUP_UPLOADED, dict(artifact_bundle_deployment_group=deployment_group)

    def __create_backup(self, data):
        resource = self.i3s_client.artifact_bundles.create_backup(data)
        return False, BACKUP_CREATED, dict(artifact_bundle_deployment_group=resource)

    def __extract(self, resource):
        resource = self.i3s_client.artifact_bundles.extract_bundle(resource)
        return True, ARTIFACT_BUNDLE_EXTRACTED, dict(artifact_bundle=resource)

    def __extract_backup(self, data):
        resource = self.i3s_client.artifact_bundles.extract_backup_bundle(data)
        return True, BACKUP_EXTRACTED, dict(artifact_bundle_deployment_group=resource)


def main():
    ArtifactBundleModule().run()


if __name__ == '__main__':
    main()
