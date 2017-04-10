#!/usr/bin/python

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


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
module: image_streamer_deployment_group_facts
short_description: Retrieve facts about the Image Streamer Deployment Groups.
description:
    - Retrieve facts about the Image Streamer Deployment Groups.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Abilio Parada (@abiliogp)"
options:
    name:
      description:
        - Name of the Deployment Group.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather paginated, filtered and sorted facts about Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=OK
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather facts about a Deployment Group by name
  image_streamer_deployment_group_facts:
    config: "{{ config_path }}"
    name: "OSS"
  delegate_to: localhost

- debug: var=deployment_groups
'''

RETURN = '''
deployment_groups:
    description: The list of Deployment Groups
    returned: Always, but can be empty.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class DeploymentGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(DeploymentGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            deployment_groups = self.i3s_client.deployment_groups.get_by('name', name)
        else:
            deployment_groups = self.i3s_client.deployment_groups.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(deployment_groups=deployment_groups))


def main():
    DeploymentGroupFactsModule().run()


if __name__ == '__main__':
    main()
