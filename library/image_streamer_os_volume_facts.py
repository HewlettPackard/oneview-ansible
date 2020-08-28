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
module: image_streamer_os_volume_facts
short_description: Retrieve facts about the Image Streamer OS Volumes.
description:
    - Retrieve facts about the Image Streamer OS Volumes.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 3.0.1"
author:
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the OS Volume.
      required: false
    options:
      description:
        - "List with options to gather additional facts about OS volumes.
        Options allowed:
          C(getStorage) gets the storage details of an OS volume
          C(getArchivedLogs) gets the archived logs of an OS volume"
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all OS Volumes
  image_streamer_os_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
  delegate_to: localhost
- debug: var=os_volumes

- name: Gather paginated, filtered and sorted facts about OS Volumes
  image_streamer_os_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: status=OK
  delegate_to: localhost
- debug: var=os_volumes

- name: Gather facts about an OS Volume by name
  image_streamer_os_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    name: "Test Volume"
  delegate_to: localhost
- debug: var=os_volumes

- name: Gather facts about storage of an OS Volume
  image_streamer_os_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    name: "Test Volume"
    options:
      - getStorage
  delegate_to: localhost
- debug: var=storage

- name: Get archived logs of the OS volume
  image_streamer_os_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    name: "Test Volume"
    options:
      - getArchivedLogs:
          file_path: './archived.logs'
  delegate_to: localhost
- debug: var=log_file_path

'''

RETURN = '''
os_volumes:
    description: The list of OS Volumes
    returned: Always, but can be empty.
    type: list
storage:
    description: Storage details of an OS volume.
    type: dict
log_file_path:
    description: OS volume archived log file path
    type: str
'''
from ansible.module_utils.oneview import OneViewModuleBase


class OsVolumeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
        options=dict(required=False, type='list')
    )

    def __init__(self):
        super(OsVolumeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        ansible_facts = {}
        name = self.module.params.get("name")

        if name:
            os_volumes = self.i3s_client.os_volumes.get_by('name', name)
        else:
            os_volumes = self.i3s_client.os_volumes.get_all(**self.facts_params)

        ansible_facts["os_volumes"] = os_volumes

        if self.options:
            ansible_facts.update(self._get_options_facts(os_volumes))

        return dict(changed=False, ansible_facts=ansible_facts)

    def _get_options_facts(self, os_volume):
        options_facts = {}

        if self.options.get("getStorage"):
            options_facts["storage"] = self.i3s_client.os_volumes.get_storage(os_volume[0]["uri"])

        if self.options.get("getArchivedLogs"):
            path = self.options["getArchivedLogs"]["file_path"]
            self.i3s_client.os_volumes.download_archive(os_volume[0]["name"], path)
            options_facts["log_file_path"] = path

        return options_facts


def main():
    OsVolumeFactsModule().run()


if __name__ == '__main__':
    main()
