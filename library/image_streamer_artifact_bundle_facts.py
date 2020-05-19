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
module: image_streamer_artifact_bundle_facts
short_description: Retrieve facts about the Artifact Bundle.
description:
    - "Retrieve facts about the Artifact Bundle."
version_added: "2.3"
requirements:
    - "python >= 3.4.2"
    - "hpOneView >= 5.2.0"
author:
    - "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        - Name of the Artifact Bundle.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Artifact Bundle.
          Options allowed:
          C(allBackups) gets the list of backups for the Artifact Bundles.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Artifact Bundles
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather paginated, filtered and sorted facts about Artifact Bundles
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=OK
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather facts about an Artifact Bundle by name
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    name: "Artifact Bundles Test"
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather facts about all Backups for Artifact Bundle
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    options:
      - allBackups
  delegate_to: localhost
- debug: var=artifact_bundle_backups
'''

RETURN = '''
artifact_bundles:
    description: The list of Artifact Bundles.
    returned: Always, but can be also null.
    type: list

artifact_bundle_backups:
    description: The list of backups for the Artifact Bundles.
    returned: When requested, but can also be null.
    type: list
'''

from ansible.module_utils.oneview import OneViewModule


class ArtifactBundleFactsModule(OneViewModule):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ArtifactBundleFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.artifact_bundles

    def execute_module(self):
        ansible_facts = {}

        if self.module.params.get('name'):
            ansible_facts['artifact_bundles'] = self.resource_client.get_by('name', self.module.params['name'])
        elif self.options:
            ansible_facts = self.__gather_optional_facts(self.options)
        else:
            ansible_facts['artifact_bundles'] = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options):

        ansible_facts = {}

        if options.get('allBackups'):
            ansible_facts['artifact_bundle_backups'] = self.resource_client.get_all_backups()

        return ansible_facts


def main():
    ArtifactBundleFactsModule().run()


if __name__ == '__main__':
    main()
