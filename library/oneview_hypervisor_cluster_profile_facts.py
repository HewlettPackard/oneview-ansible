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
module: oneview_hypervisor_cluster_profile_facts
short_description: Retrieve facts about the OneView Hypervisor Cluster Profiles.
description:
    - Retrieve facts about the Hypervisor Cluster Profile from OneView.
version_added: "2.3"
requirements:
    - "python >= 3.4.2"
    - "hpOneView >= 5.1.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        - Hypervisor Cluster Profile name.
    uri:
      description:
        - Hypervisor Cluster Profile uri.
    options:
      description:
        - "List with options to gather additional facts about Hypervisor Cluster Profile related resources.
          Options allowed: C(compliancePreview)"
        - "To gather facts about C(compliancePreview), a Hypervisor Cluster Profile name is required.
          Otherwise, these options will be ignored."

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Hypervisor Cluster Profiles
  oneview_hypervisor_cluster_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost

- debug: var=hypervisor_cluster_profiles

- name: Gather paginated, filtered and sorted facts about Hypervisor Cluster Profiles
  oneview_hypervisor_cluster_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
  delegate_to: localhost

- debug: var=hypervisor_cluster_profiles


- name: Gather facts about a Hypervisor Cluster Profile by name
  oneview_hypervisor_cluster_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: ClusterProfile-1
  delegate_to: localhost

- debug: var=hypervisor_cluster_profiles


- name: Gather facts about a Hypervisor Cluster Profile by uri
  oneview_hypervisor_cluster_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    uri: /rest/hypervisor-cluster-profiles/e23d9fa4-f926-4447-b971-90116ca3e61e
  delegate_to: localhost

- debug: var=hypervisor_cluster_profiles

- name: Gather all facts about a Hypervisor Cluster Profile
  oneview_hypervisor_cluster_profile_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name : "ClusterProfile-1"
    options:
        - compliancePreview

  delegate_to: localhost

- debug: var=hypervisor_cluster_profiles
- debug: var=hypervisor_cluster_profile_compliance_preview
'''

RETURN = '''
hypervisor_cluster_profiles:
    description: Has all the OneView facts about the Hypervisor Cluster Profiles.
    returned: Always, but can be null.
    type: dict

hypervisor_cluster_profile_compliance_preview:
    description:
        Has all the facts about the manual and automatic updates required to make the hypervisor cluster profile compliant
        with its template.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class HypervisorClusterProfileFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(type='str'),
        uri=dict(type='str'),
        options=dict(type='list'),
        params=dict(type='dict')
    )

    def __init__(self):
        super(HypervisorClusterProfileFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.hypervisor_cluster_profiles)

    def execute_module(self):
        ansible_facts = {}
        hypervisor_cluster_profiles = []

        if self.current_resource:
            hypervisor_cluster_profiles = [self.current_resource.data]
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            hypervisor_cluster_profiles = self.resource_client.get_all(**self.facts_params)

        if self.options:
            ansible_facts = self.__gather_option_facts()

        ansible_facts["hypervisor_cluster_profiles"] = hypervisor_cluster_profiles

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_option_facts(self):
        facts = {}

        if self.current_resource:
            if self.options.get('compliancePreview'):
                facts['hypervisor_cluster_profile_compliance_preview'] = self.current_resource.get_compliance_preview()

        return facts


def main():
    HypervisorClusterProfileFactsModule().run()


if __name__ == '__main__':
    main()
