#!/usr/bin/python
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
from hpOneView.oneview_client import OneViewClient

PROFILE_NOT_FOUND = "Server Profile not found."
PRESENTATIONS_REMOVED = "Extra presentations removed"

DOCUMENTATION = '''
---
module: oneview_storage_volume_attachment
short_description: Provides an interface to remove extra presentations from a specified server profile.
description:
    - "Provides an interface to remove extra presentations from a specified server profile."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
      description:
        - Indicates the desired state for the Storage Volume Attachment
          'extra_presentations_removed' will remove extra presentations from a specified server profile.
      choices: ['extra_presentations_removed']
      required: true
    server_profile:
      description:
        - Server Profile name or Server Profile URI
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Removes extra presentations from a specified server profile URI
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
  delegate_to: localhost

- debug: var=server_profile


- name: Removes extra presentations from a specified server profile name
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "SV-1001"
  delegate_to: localhost

- debug: var=server_profile
'''

RETURN = '''
server_profile:
    description: Has all the OneView facts about the repaired Server Profile.
    returned: Always.
    type: complex
'''


class StorageVolumeAttachmentModule(object):
    argument_spec = {
        "config": {"required": True, "type": 'str'},
        "state": {"required": True, "type": 'str'},
        "server_profile": {"required": True, "type": 'str'},
    }

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:

            data = {
                "type": "ExtraUnmanagedStorageVolumes",
                "resourceUri": self.__get_server_profile_uri(self.module.params['server_profile'])
            }

            attachment = self.oneview_client.storage_volume_attachments.remove_extra_presentations(data)
            self.module.exit_json(changed=True, msg=PRESENTATIONS_REMOVED,
                                  ansible_facts=dict(server_profile=attachment))

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_server_profile_uri(self, server_profile):
        if "/" in server_profile:
            return server_profile
        else:
            profile = self.oneview_client.server_profiles.get_by_name(server_profile)

            if profile:
                return profile['uri']
            else:
                raise Exception(PROFILE_NOT_FOUND)


def main():
    StorageVolumeAttachmentModule().run()


if __name__ == '__main__':
    main()
