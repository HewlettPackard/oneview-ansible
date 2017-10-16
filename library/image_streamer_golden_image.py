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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: image_streamer_golden_image
short_description: Manage Image Streamer Golden Image resources.
description:
    - "Provides an interface to manage Image Streamer Golden Image. Can create, add, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Golden Image resource.
              C(present) will ensure data properties are compliant with Synergy Image Streamer.
              C(absent) will remove the resource from Synergy Image Streamer, if it exists.
              C(downloaded) will download the Golden Image to the file path provided.
              C(archive_downloaded) will download the Golden Image archive to the file path provided.
        choices: ['present', 'absent', 'downloaded', 'archive_downloaded']
        required: true
    data:
        description:
            - List with Golden Image properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Add a Golden Image from OS Volume
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image creation'
      description: "Test Description"
      imageCapture: "true"
      osVolumeName: 'OSVolume-20'
      buildPlanName: 'Buld Plan name'
  delegate_to: localhost

- name: Create a Golden Image uploading from a local file
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image upload'
      description: "Test"
      localImageFilePath: '~/image_file.zip'
  delegate_to: localhost

- name: Update the Golden Image description and name
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image upload'
      description: "New description"
      newName: 'Golden Image Renamed'
  delegate_to: localhost

- name: Download the Golden Image to the file path provided
  image_streamer_golden_image:
    config: "{{ config }}"
    state: downloaded
    data:
      name: 'Demo Golden Image'
      destination_file_path: '~/downloaded_image.zip'
  delegate_to: localhost

- name: Download the Golden Image archive log to the file path provided
  image_streamer_golden_image:
    config: "{{ config }}"
    state: archive_downloaded
    data:
      name: 'Demo Golden Image'
      destination_file_path: '~/archive.log'
  delegate_to: localhost

- name: Remove a Golden Image
  image_streamer_golden_image:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Golden Image name'
  delegate_to: localhost
'''

RETURN = '''
golden_image:
    description: Has the OneView facts about the Golden Image.
    returned: On state 'present'.
    type: dict
'''

from ansible.module_utils.oneview import (OneViewModuleBase, HPOneViewValueError, HPOneViewResourceNotFound, ResourceComparator)


class GoldenImageModule(OneViewModuleBase):
    MSG_CREATED = 'Golden Image created successfully.'
    MSG_UPLOADED = 'Golden Image uploaded successfully.'
    MSG_UPDATED = 'Golden Image updated successfully.'
    MSG_ALREADY_PRESENT = 'Golden Image is already present.'
    MSG_DELETED = 'Golden Image deleted successfully.'
    MSG_DOWNLOADED = 'Golden Image downloaded successfully.'
    MSG_ARCHIVE_DOWNLOADED = 'Golden Image archive downloaded successfully.'
    MSG_ALREADY_ABSENT = 'Golden Image is already absent.'
    MSG_WAS_NOT_FOUND = 'Golden Image was not found.'
    MSG_CANT_CREATE_AND_UPLOAD = "You can use an existent OS Volume or upload an Image, you cannot do both."
    MSG_MISSING_MANDATORY_ATTRIBUTES = 'Mandatory field is missing: osVolumeURI or localImageFilePath are required.'
    MSG_OS_VOLUME_WAS_NOT_FOUND = 'OS Volume was not found.'
    MSG_BUILD_PLAN_WAS_NOT_FOUND = 'OS Build Plan was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'downloaded', 'archive_downloaded']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(GoldenImageModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.golden_images

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present(self.data, resource)
        elif self.state == 'absent':
            return self.resource_absent(resource)
        else:
            if not resource:
                raise HPOneViewResourceNotFound(self.MSG_WAS_NOT_FOUND)

            if self.state == 'downloaded':
                changed, msg, ansible_facts = self.__download(self.data, resource)
            elif self.state == 'archive_downloaded':
                changed, msg, ansible_facts = self.__download_archive(self.data, resource)

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __check_present_consistency(self, data):
        if data.get('osVolumeURI') and data.get('localImageFilePath'):
            raise HPOneViewValueError(self.MSG_CANT_CREATE_AND_UPLOAD)

    def __present(self, data, resource):

        changed = False
        msg = ''

        if "newName" in data:
            data["name"] = data.pop("newName")

        self.__replace_name_by_uris(data)
        self.__check_present_consistency(data)

        file_path = data.pop('localImageFilePath', None)

        if not resource:
            if data.get('osVolumeURI'):
                resource = self.i3s_client.golden_images.create(data)
                msg = self.MSG_CREATED
                changed = True
            elif file_path:
                resource = self.i3s_client.golden_images.upload(file_path, data)
                msg = self.MSG_UPLOADED
                changed = True
            else:
                raise HPOneViewValueError(self.MSG_MISSING_MANDATORY_ATTRIBUTES)
        else:
            merged_data = resource.copy()
            merged_data.update(data)

            if not ResourceComparator.compare(resource, merged_data):
                resource = self.i3s_client.golden_images.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return changed, msg, dict(golden_image=resource)

    def __replace_name_by_uris(self, data):
        vol_name = data.pop('osVolumeName', None)
        if vol_name:
            data['osVolumeURI'] = self.__get_os_voume_by_name(vol_name)['uri']

        build_plan_name = data.pop('buildPlanName', None)
        if build_plan_name:
            data['buildPlanUri'] = self.__get_build_plan_by_name(build_plan_name)['uri']

    def __get_os_voume_by_name(self, name):
        os_volume = self.i3s_client.os_volumes.get_by_name(name)
        if not os_volume:
            raise HPOneViewResourceNotFound(self.MSG_OS_VOLUME_WAS_NOT_FOUND)
        return os_volume

    def __get_build_plan_by_name(self, name):
        build_plan = self.i3s_client.build_plans.get_by('name', name)
        if build_plan:
            return build_plan[0]
        else:
            raise HPOneViewResourceNotFound(self.MSG_BUILD_PLAN_WAS_NOT_FOUND)

    def __download(self, data, resource):
        self.i3s_client.golden_images.download(resource['uri'], data['destination_file_path'])
        return True, self.MSG_DOWNLOADED, {}

    def __download_archive(self, data, resource):
        self.i3s_client.golden_images.download_archive(resource['uri'], data['destination_file_path'])
        return True, self.MSG_ARCHIVE_DOWNLOADED, {}


def main():
    GoldenImageModule().run()


if __name__ == '__main__':
    main()
