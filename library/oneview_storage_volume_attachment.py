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
module: oneview_storage_volume_attachment
short_description: Provides an interface to remove extra presentations from a specified server profile.
description:
    - "Provides an interface to remove extra presentations from a specified server profile."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
      description:
        - Indicates the desired state for the Storage Volume Attachment
          C(extra_presentations_removed) will remove extra presentations from a specified server profile.
      choices: ['extra_presentations_removed']
      required: true
    server_profile:
      description:
        - Server Profile name or Server Profile URI
      required: true
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Removes extra presentations from a specified server profile URI
  oneview_storage_volume_attachment:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: extra_presentations_removed
    server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
  delegate_to: localhost

- debug: var=server_profile


- name: Removes extra presentations from a specified server profile name
  oneview_storage_volume_attachment:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: extra_presentations_removed
    server_profile: "SV-1001"
  delegate_to: localhost

- debug: var=server_profile
'''

RETURN = '''
server_profile:
    description: Has all the OneView facts about the repaired Server Profile.
    returned: Always.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class StorageVolumeAttachmentModule(OneViewModule):
    PROFILE_NOT_FOUND = "Server Profile not found."
    PRESENTATIONS_REMOVED = "Extra presentations removed"

    def __init__(self):
        argument_spec = {
            "state": {"required": True, "type": 'str'},
            "server_profile": {"required": True, "type": 'str'},
        }

        super(StorageVolumeAttachmentModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.storage_volume_attachments)

    def execute_module(self):

        data = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": self.__get_server_profile_uri(self.module.params['server_profile'])
        }

        attachment = self.resource_client.remove_extra_presentations(data)
        return dict(changed=True, msg=self.PRESENTATIONS_REMOVED,
                    ansible_facts=dict(server_profile=attachment))

    def __get_server_profile_uri(self, server_profile):
        if "/" in server_profile:
            return server_profile
        else:
            profile = self.oneview_client.server_profiles.get_by_name(server_profile)

            if profile:
                return profile.data['uri']
            else:
                raise OneViewModuleResourceNotFound(self.PROFILE_NOT_FOUND)


def main():
    StorageVolumeAttachmentModule().run()


if __name__ == '__main__':
    main()
