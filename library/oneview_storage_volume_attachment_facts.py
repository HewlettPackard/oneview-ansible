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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_storage_volume_attachment_facts
short_description: Retrieve facts about the OneView Storage Volume Attachments.
description:
    - "Retrieve facts about the OneView Storage Volume Attachments. To gather facts about a specific Storage Volume
      Attachment it is required to inform the option I(storageVolumeAttachmentUri). It is also possible to retrieve a
      specific Storage Volume Attachment by the Server Profile and the Volume. For this option, it is required to inform
      the option I(serverProfileName) and the param I(storageVolumeName) or I(storageVolumeUri)."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    storageVolumeAttachmentUri:
      description:
        - Storage Volume Attachment uri.
      required: false
    storageVolumeUri:
      description:
        - Storage Volume uri.
      required: false
    storageVolumeName:
      description:
        - Storage Volume name.
      required: false
    serverProfileName:
      description:
        - Server Profile name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available:
          C(extraUnmanagedStorageVolumes) retrieve the list of extra unmanaged storage volumes.
          C(paths) retrieve all paths or a specific attachment path for the specified volume attachment. To retrieve a
           specific path a C(pathUri) or a C(pathId) must be informed"
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Volume Attachments
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_volume_attachments

- name: Gather paginated, filtered and sorted facts about Storage Volume Attachments
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "storageVolumeUri='/rest/storage-volumes/E5B84BC8-75CF-4305-8DB5-7585A2979351'"

- debug: var=storage_volume_attachments

- name: Gather facts about a Storage Volume Attachment by Server Profile and Volume
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeName: "volume-test" # You could inform either the volume name or the volume uri
    # storageVolumeUri: "volume-test"
  delegate_to: localhost

- debug: var=storage_volume_attachments


- name: Gather facts about extra unmanaged storage volumes
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    options:
      - extraUnmanagedStorageVolumes:
            start: 0     # optional
            count: '-1'  # optional
            filter: ''   # optional
            sort: ''     # optional
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=extra_unmanaged_storage_volumes

- name: Gather facts about all paths for the specified volume attachment
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeUri: "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"
    options:
      - paths
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=storage_volume_attachment_paths

- name: Gather facts about a specific attachment path
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeUri: "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"
    options:
      - paths:
            # You could inform either the path id or the path uri
            pathId: '9DFC8953-15A4-4EA9-AB65-23AB12AB23' # optional
            # pathUri: '/rest/storage-volume-attachments/123-123-123/paths/123-123-123'
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=storage_volume_attachment_paths
'''

RETURN = '''
storage_volume_attachments:
    description: Has all the OneView facts about the Storage Volume Attachments.
    returned: Always, but can be null.
    type: complex

extra_unmanaged_storage_volumes:
    description: Has facts about the extra unmanaged storage volumes.
    returned: When requested, but can be null.
    type: complex

storage_volume_attachment_paths:
    description: Has facts about all paths or a specific attachment path for the specified volume attachment.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewValueError

SPECIFIC_ATTACHMENT_OPTIONS = ['storageVolumeAttachmentUri', 'storageVolumeUri', 'storageVolumeName',
                               'serverProfileName']


class StorageVolumeAttachmentFactsModule(OneViewModuleBase):
    ATTACHMENT_KEY_REQUIRED = "Server Profile Name and Volume Name or Volume Uri are required."

    def __init__(self):
        argument_spec = dict(
            serverProfileName=dict(required=False, type='str'),
            storageVolumeAttachmentUri=dict(required=False, type='str'),
            storageVolumeUri=dict(required=False, type='str'),
            storageVolumeName=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(StorageVolumeAttachmentFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_volume_attachments

        resource_uri = self.oneview_client.storage_volume_attachments.URI
        self.__search_attachment_uri = str(resource_uri) + "?filter=storageVolumeUri='{}'"

    def execute_module(self):
        facts = {}
        client = self.oneview_client.storage_volume_attachments
        params = self.module.params

        param_specific_attachment = [entry for entry in SPECIFIC_ATTACHMENT_OPTIONS if params.get(entry)]

        if param_specific_attachment:
            attachments = self.__get_specific_attachment(params)
            self.__get_paths(attachments, self.options, facts)
        else:
            attachments = client.get_all(**self.facts_params)

        facts['storage_volume_attachments'] = attachments

        if self.options.get('extraUnmanagedStorageVolumes'):
            volumes_options = self.__get_sub_options(self.options['extraUnmanagedStorageVolumes'])
            facts['extra_unmanaged_storage_volumes'] = client.get_extra_unmanaged_storage_volumes(**volumes_options)

        return dict(changed=False, ansible_facts=facts)

    def __get_specific_attachment(self, params):

        attachment_uri = params.get('storageVolumeAttachmentUri')

        if attachment_uri:
            return [self.oneview_client.storage_volume_attachments.get(attachment_uri)]
        else:
            volume_uri = params.get('storageVolumeUri')
            profile_name = params.get('serverProfileName')

            if not profile_name or not (volume_uri or params.get('storageVolumeName')):
                raise HPOneViewValueError(self.ATTACHMENT_KEY_REQUIRED)

            if not volume_uri and params.get('storageVolumeName'):
                volumes = self.oneview_client.volumes.get_by('name', params.get('storageVolumeName'))
                if volumes:
                    volume_uri = volumes[0]['uri']

            uri = self.__search_attachment_uri.format(volume_uri, profile_name)
            attachments = self.oneview_client.storage_volume_attachments.get(uri) or {}

            return attachments.get('members')

    def __get_paths(self, attachments, options, facts):

        if attachments and 'paths' in options:

            attachment_uri = attachments[0]['uri']
            paths_options = self.__get_sub_options(options['paths'])
            path_id_or_uri = paths_options.get('pathId') or paths_options.get('pathUri')

            if path_id_or_uri:
                paths = [self.oneview_client.storage_volume_attachments.get_paths(attachment_uri, path_id_or_uri)]
            else:
                paths = self.oneview_client.storage_volume_attachments.get_paths(attachment_uri)

            facts['storage_volume_attachment_paths'] = paths

    def __get_sub_options(self, option):
        return option if isinstance(option, dict) else {}


def main():
    StorageVolumeAttachmentFactsModule().run()


if __name__ == '__main__':
    main()
