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
module: oneview_volume_facts
short_description: Retrieve facts about the OneView Volumes.
description:
    - Retrieve facts about the Volumes from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Volume name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Volume and related resources.
          Options allowed: C(attachableVolumes), C(extraManagedVolumePaths), and C(snapshots). For the option
          C(snapshots), you may provide a name."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Volumes
  oneview_volume_facts:
    config: "{{ config_path }}"

- debug: var=storage_volumes

- name: Gather paginated, filtered and sorted facts about Volumes
  oneview_volume_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "provisionType='Thin'"

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
       - snapshots:  # optional
           name: "{{ snapshot_name }}"

- debug: var=storage_volumes
- debug: var=snapshots
'''

RETURN = '''
storage_volumes:
    description: Has all the OneView facts about the Volumes.
    returned: Always, but can be null.
    type: dict

attachable_volumes:
    description: Has all the facts about the attachable volumes managed by the appliance.
    returned: When requested, but can be null.
    type: dict

extra_managed_volume_paths:
    description: Has all the facts about the extra managed storage volume paths from the appliance.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class VolumeFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )

        super(VolumeFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.volumes

    def execute_module(self):
        ansible_facts = {}
        networks = self.facts_params.pop('networks', None)
        if self.module.params.get('name'):
            ansible_facts['storage_volumes'] = self.resource_client.get_by('name', self.module.params['name'])
            ansible_facts.update(self.__gather_facts_about_one_volume(ansible_facts['storage_volumes']))
        else:
            ansible_facts['storage_volumes'] = self.resource_client.get_all(**self.facts_params)

        if networks:
            self.facts_params['networks'] = networks

        ansible_facts.update(self.__gather_facts_from_appliance())

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_facts_from_appliance(self):
        facts = {}

        if self.options:
            if self.options.get('extraManagedVolumePaths'):
                extra_managed_volume_paths = self.resource_client.get_extra_managed_storage_volume_paths()
                facts['extra_managed_volume_paths'] = extra_managed_volume_paths
            if self.options.get('attachableVolumes'):
                attachable_volumes = self.resource_client.get_attachable_volumes()
                facts['attachable_volumes'] = attachable_volumes

        return facts

    def __gather_facts_about_one_volume(self, volumes):
        facts = {}

        if self.options.get('snapshots') and len(volumes) > 0:
            options_snapshots = self.options['snapshots']
            volume_uri = volumes[0]['uri']
            if isinstance(options_snapshots, dict) and 'name' in options_snapshots:
                facts['snapshots'] = self.resource_client.get_snapshot_by(volume_uri, 'name', options_snapshots['name'])
            else:
                facts['snapshots'] = self.resource_client.get_snapshots(volume_uri)

        return facts


def main():
    VolumeFactsModule().run()


if __name__ == '__main__':
    main()
