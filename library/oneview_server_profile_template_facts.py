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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_server_profile_template_facts
short_description: Retrieve facts about the Server Profile Templates from OneView.
description:
    - Retrieve facts about the Server Profile Templates from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Server Profile Template name.
    uri:
      description:
        - Server Profile Template uri.
    options:
      description:
        - "List with options to gather additional facts about Server Profile Template resources.
          Options allowed: C(new_profile) and C(transformation)."
notes:
    - The option C(transformation) is only available for API version 300 or later.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"

- debug: var=server_profile_templates

- name: Gather paginated, filtered and sorted facts about Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
  delegate_to: localhost

- debug: var=server_profile_templates

- name: Gather facts about a Server Profile Template by name
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    name: "ProfileTemplate101"

- name: Gather facts about a Server Profile by uri
  oneview_server_profile_facts:
    config: "{{ config }}"
    uri: /rest/server-profile-templates/c0868397-eff6-49ed-8151-4338702792d3
  delegate_to: localhost

- name: Gather facts about a template and a profile with the configuration based on this template
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    name: "ProfileTemplate101"
    options:
      - new_profile
'''

RETURN = '''
server_profile_templates:
    description: Has all the OneView facts about the Server Profile Templates.
    returned: Always, but can be null.
    type: complex

new_profile:
    description: A profile object with the configuration based on this template.
    returned: When requested, but can be null.
    type: complex
'''
from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class ServerProfileTemplateFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(type='str'),
        options=dict(type='list'),
        params=dict(type='dict'),
        uri=dict(type='str')
    )

    def __init__(self):
        super(ServerProfileTemplateFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

        self.resource_client = self.oneview_client.server_profile_templates

    def execute_module(self):
        name = self.module.params.get("name")
        uri = self.module.params.get("uri")

        if name:
            facts = self.__get_by_attribute(name, 'name')
        elif uri:
            facts = self.__get_by_attribute(uri, 'uri')
        else:
            facts = self.__get_all()

        return dict(changed=False, ansible_facts=facts)

    def __get_by_attribute(self, attribute_value, attribute_name):
        if attribute_name == 'name':
            template = self.resource_client.get_by_name(name=attribute_value)
        else:
            template = self.resource_client.get(attribute_value)
        if not template:
            return dict(server_profile_templates=[])

        facts = dict(server_profile_templates=[template])

        if self.options:

            if "new_profile" in self.options:
                facts["new_profile"] = self.resource_client.get_new_profile(id_or_uri=template["uri"])

            if "transformation" in self.options:
                tranformation_data = self.options.get('transformation')
                facts["transformation"] = self.resource_client.get_transformation(
                    id_or_uri=template["uri"],
                    **tranformation_data
                )

        return facts

    def __get_all(self):
        templates = self.resource_client.get_all(**self.facts_params)
        return dict(server_profile_templates=templates)


def main():
    ServerProfileTemplateFactsModule().run()


if __name__ == '__main__':
    main()
