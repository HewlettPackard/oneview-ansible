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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: image_streamer_artifact_bundle_facts
short_description: Retrieve facts about the Artifact Bundle.
description:
    - "Retrieve facts about the Artifact Bundle."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Abilio Parada (@abiliogp)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Name of the Artifact Bundle.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Artifact Bundle.
          Options allowed:
          'allBackups' gets the list of backups for the Artifact Bundles.
          'backupForAnArtifactBundle' gets the list of backups for the Artifact Bundle."
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           'start': The first item to return, using 0-based indexing.
           'count': The number of resources to return.
           'filter': A general filter/query string to narrow the list of items returned.
           'sort': The sort order of the returned data set."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
    name: "Artifact Bundles Test"
    options:
      - allBackups
  delegate_to: localhost
- debug: var=artifact_bundles
- debug: var=artifact_bundle_backups

- name: Gather facts about Backup for an Artifact Bundle
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    name: "Artifact Bundles Test"
    options:
      - backupForAnArtifactBundle
  delegate_to: localhost
- debug: var=artifact_bundles
- debug: var=backup_for_artifact_bundle
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

backup_for_artifact_bundle:
    description: The backup for an Artifact Bundle.
    returned: When requested, but can also be null.
    type: list
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ArtifactBundleFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def run(self):
        try:
            ansible_facts = {}

            if self.module.params.get('name'):
                artifact_bundles = self.__get_by_name(self.module.params['name'])

                if self.module.params.get('options') and artifact_bundles:
                    ansible_facts = self.__gather_optional_facts(self.module.params['options'], artifact_bundles[0])
            else:
                artifact_bundles = self.__get_all()

            ansible_facts['artifact_bundles'] = artifact_bundles

            self.module.exit_json(changed=False, ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_optional_facts(self, options, artifact_bundle):
        options = transform_list_to_dict(options)

        ansible_facts = {}

        if options.get('allBackups'):
            ansible_facts['artifact_bundle_backups'] = self.__get_backups()
        if options.get('backupForAnArtifactBundle'):
            ansible_facts['backup_for_artifact_bundle'] = self.__get_backup_for_an_artifact_bundle(artifact_bundle)

        return ansible_facts

    def __get_all(self):
        params = self.module.params.get('params') or {}
        return self.i3s_client.artifact_bundles.get_all(**params)

    def __get_by_name(self, name):
        return self.i3s_client.artifact_bundles.get_by('name', name)

    def __get_backups(self):
        return self.i3s_client.artifact_bundles.get_all_backups()

    def __get_backup_for_an_artifact_bundle(self, artifact_bundle):
        return self.i3s_client.artifact_bundles.get_backup(artifact_bundle['uri'])


def main():

    ArtifactBundleFactsModule().run()


if __name__ == '__main__':
    main()
