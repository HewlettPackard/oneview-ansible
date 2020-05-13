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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_volume_facts
short_description: Retrieve facts about the OneView Volumes.
description:
    - Retrieve facts about the Volumes from OneView.
version_added: "2.5"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Volume name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Volume and related resources.
          Options allowed:
            - C(attachableVolumes)
            - C(extraManagedVolumePaths)
            - C(snapshots). For this option, you may provide a name."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Volumes
  oneview_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
- debug: var=storage_volumes

- name: Gather paginated, filtered and sorted facts about Volumes
  oneview_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "provisionType='Thin'"
- debug: var=storage_volumes

- name: "Gather facts about all Volumes, the attachable volumes managed by the appliance and the extra managed
         storage volume paths"
  oneview_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    options:
        - attachableVolumes        # optional
        - extraManagedVolumePaths  # optional
- debug: var=storage_volumes
- debug: var=attachable_volumes
- debug: var=extra_managed_volume_paths


- name: Gather facts about a Volume by name with a list of all snapshots taken
  oneview_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "{{ volume_name }}"
    options:
        - snapshots  # optional
- debug: var=storage_volumes
- debug: var=snapshots


- name: "Gather facts about a Volume with one specific snapshot taken"
  oneview_volume_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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

from ansible.module_utils.oneview import OneViewModule


class VolumeFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(name=dict(type='str'), options=dict(type='list'), params=dict(type='dict'))
        super(VolumeFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.volumes)

    def execute_module(self):
        ansible_facts = {}
        networks = self.facts_params.pop('networks', None)
        if self.module.params.get('name'):
            ansible_facts['storage_volumes'] = self.resource_client.get_by('name', self.module.params['name'])
            ansible_facts.update(self._gather_facts_about_one_volume(ansible_facts['storage_volumes']))
        else:
            ansible_facts['storage_volumes'] = self.resource_client.get_all(**self.facts_params)

        if networks:
            self.facts_params['networks'] = networks

        ansible_facts.update(self._gather_facts_from_appliance())

        return dict(changed=False, ansible_facts=ansible_facts)

    def _gather_facts_from_appliance(self):
        facts = {}
        if self.options:
            if self.options.get('extraManagedVolumePaths'):
                extra_managed_volume_paths = self.resource_client.get_extra_managed_storage_volume_paths()
                facts['extra_managed_volume_paths'] = extra_managed_volume_paths
            if self.options.get('attachableVolumes'):
                query_params = self.options['attachableVolumes']
                query_params = {} if type(query_params) is not dict else query_params
                if 'connections' in query_params:
                    query_params['connections'] = str(query_params['connections'])
                attachable_volumes = self.resource_client.get_attachable_volumes(**query_params)
                facts['attachable_volumes'] = attachable_volumes

        return facts

    def _gather_facts_about_one_volume(self, volumes):
        facts = {}
        
        if self.options.get('snapshots') and len(volumes) > 0:
            options_snapshots = self.options['snapshots']
            if isinstance(options_snapshots, dict) and 'name' in options_snapshots:
                facts['snapshots'] = self.current_resource.get_snapshot_by('name', options_snapshots['name'])
            else:
                facts['snapshots'] = self.current_resource.get_snapshots()

        return facts


def main():
    VolumeFactsModule().run()


if __name__ == '__main__':
    main()
