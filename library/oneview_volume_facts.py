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
try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import transform_list_to_dict

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_volume_facts
short_description: Retrieve facts about the OneView Volumes.
description:
    - Retrieve facts about the Volumes from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Volume name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Volume and related resources.
          Options allowed: attachableVolumes, extraManagedVolumePaths, and snapshots. For the option snapshots, you may
          provide a name."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Volumes
  oneview_volume_facts:
    config: "{{ config_path }}"

- debug: var=storage_volumes


- name: "Gather facts about all Volumes, the attachable volumes managed by the appliance and the extra managed
         storage volume paths"
  oneview_volume_facts:
    config: "{{ config_path }}"
    options:
        - attachableVolumes        # optional
        - extraManagedVolumePaths  # optional

- debug: var=storage_volumes
- debug: var=attachable_volumes
- debug: var=extra_managed_volume_paths


- name: Gather facts about a Volume by name with a list of all snapshots taken
  oneview_volume_facts:
    config: "{{ config }}"
    name: "{{ volume_name }}"
    options:
        - snapshots  # optional

- debug: var=storage_volumes
- debug: var=snapshots


- name: "Gather facts about a Volume with one specific snapshot taken"
  oneview_volume_facts:
    config: "{{ config }}"
    name: "{{ volume_name }}"
    options:
       - snapshots  # optional
           name: "{{ snapshot_name }}"

- debug: var=storage_volumes
- debug: var=snapshots
'''

RETURN = '''
storage_volumes:
    description: Has all the OneView facts about the Volumes.
    returned: Always, but can be null.
    type: complex

attachable_volumes:
    description: Has all the facts about the attachable volumes managed by the appliance.
    returned: When requested, but can be null.
    type: complex

extra_managed_volume_paths:
    description: Has all the facts about the extra managed storage volume paths from the appliance
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class VolumeFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            ansible_facts = {}
            options = self.__get_options()

            if self.module.params.get('name'):
                ansible_facts.update(self.__gather_facts_about_one_volume(options))
            else:
                ansible_facts.update(self.__gather_facts_about_all_volumes())

            ansible_facts.update(self.__gather_facts_from_appliance(options))

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_facts_from_appliance(self, options):
        facts = {}
        extra_managed_volume_paths = None
        attachable_volumes = None

        if options:
            if options.get('extraManagedVolumePaths'):
                extra_managed_volume_paths = self.oneview_client.volumes.get_extra_managed_storage_volume_paths()
                facts['extra_managed_volume_paths'] = extra_managed_volume_paths
            if options.get('attachableVolumes'):
                attachable_volumes = self.oneview_client.volumes.get_attachable_volumes()
                facts['attachable_volumes'] = attachable_volumes

        return facts

    def __gather_facts_about_all_volumes(self):
        facts = {}
        facts['storage_volumes'] = self.oneview_client.volumes.get_all()
        return facts

    def __gather_facts_about_one_volume(self, options):
        facts = {}
        volumes = self.oneview_client.volumes.get_by('name', self.module.params['name'])

        if options.get('snapshots') and len(volumes) > 0:
            options_snapshots = options['snapshots']
            volume_uri = volumes[0]['uri']
            if isinstance(options_snapshots, dict) and 'name' in options_snapshots:
                facts['snapshots'] = self.oneview_client.volumes.get_snapshot_by(volume_uri, 'name',
                                                                                 options_snapshots['name'])
            else:
                facts['snapshots'] = self.oneview_client.volumes.get_snapshots(volume_uri)

        facts['storage_volumes'] = volumes

        return facts

    def __get_options(self):
        if self.module.params.get('options'):
            return transform_list_to_dict(self.module.params['options'])
        else:
            return {}


def main():
    VolumeFactsModule().run()


if __name__ == '__main__':
    main()
