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
module: oneview_storage_volume_template_facts
short_description: Retrieve facts about Storage Volume Templates of the OneView.
description:
    - Retrieve facts about Storage Volume Templates of the OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Storage Volume Template name.
      required: false
    options:
      description:
        - "Retrieve additional facts.
            Options available: C(connectableVolumeTemplates), C(reachableVolumeTemplates), C(compatibleSystems)"
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Volume Templates
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost

- debug: var=storage_volume_templates

- name: Gather paginated, filtered and sorted facts about Storage Volume Templates
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_volume_templates

- name: Gather facts about a Storage Volume Template by name
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "FusionTemplateExample"
  delegate_to: localhost

- debug: var=storage_volume_templates

- name: Gather facts about the connectable Storage Volume Templates
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "FusionTemplateExample"
    options:
      - connectableVolumeTemplates
  delegate_to: localhost

- debug: var=storage_volume_templates
- debug: var=connectable_volume_templates

- name: Gather facts about the reachable Storage Volume Templates
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    options:
      - reachableVolumeTemplates
  delegate_to: localhost

- name: Gather facts about Storage Systems compatible to the SVT
  oneview_storage_volume_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "{{ volume_template_name }}"
    options:
      - compatibleSystems
  delegate_to: localhost
'''

RETURN = '''
storage_volume_templates:
    description: Has all the OneView facts about the Storage Volume Templates.
    returned: Always, but can be null.
    type: dict

connectable_volume_templates:
    description: Has facts about the Connectable Storage Volume Templates. API version <= 300  only.
    returned: When requested, but can be null.
    type: dict

reachable_volume_templates:
    description: Has facts about the Reachable Storage Volume Templates. API version 500+ only.
    returned: When requested, but can be null.
    type: dict

compatible_systems:
    description: Has facts about Storage Systems compatible to the Storage Volume template.
        API version 500+ only.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class StorageVolumeTemplateFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(StorageVolumeTemplateFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.storage_volume_templates)

    def execute_module(self):
        ansible_facts = dict(storage_volume_templates=[])
        networks = self.facts_params.pop('networks', None)

        if 'compatibleSystems' in self.options and self.current_resource:
            ansible_facts['compatible_systems'] = self.current_resource.get_compatible_systems()
            storage_volume_templates = [self.current_resource.data]
        else:
            storage_volume_templates = self.resource_client.get_all(**self.facts_params)

        ansible_facts['storage_volume_templates'] = storage_volume_templates

        self.facts_params['networks'] = networks if networks else None

        if 'connectableVolumeTemplates' in self.options:
            ansible_facts['connectable_volume_templates'] = self.resource_client.get_connectable_volume_templates(
                **self.facts_params)

        if 'reachableVolumeTemplates' in self.options:
            ansible_facts['reachable_volume_templates'] = self.resource_client.get_reachable_volume_templates(
                **self.facts_params)

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    StorageVolumeTemplateFactsModule().run()


if __name__ == '__main__':
    main()
