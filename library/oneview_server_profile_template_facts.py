#!/usr/bin/python

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

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_server_profile_template_facts
short_description: Retrieve facts about the Server Profile Templates from OneView.
description:
    - Retrieve facts about the Server Profile Templates from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Server Profile Template name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Server Profile Template resources.
          Options allowed: new_profile"
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"

- name: Gather facts about a Server Profile Template by name
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    name: "ProfileTemplate101"

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
    returned: always, but can be null
    type: complex

new_profile:
    description: A profile object with the configuration based on this template.
    returned: when requested, but can be null
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerProfileTemplateFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.server_profile_templates

    def run(self):
        try:
            name = self.module.params["name"]

            if name:
                facts = self.__get_by_name(name)
            else:
                facts = self.__get_all()

            self.module.exit_json(changed=False, ansible_facts=facts)
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_by_name(self, name):
        template = self.resource_client.get_by_name(name=name)
        if not template:
            return dict(server_profile_templates=[])

        facts = dict(server_profile_templates=[template])

        options = self.module.params["options"]

        if options and "new_profile" in options:
            profile = self.resource_client.get_new_profile(id_or_uri=template["uri"])
            facts["new_profile"] = profile

        return facts

    def __get_all(self):
        templates = self.resource_client.get_all()
        return dict(server_profile_templates=templates)


def main():
    ServerProfileTemplateFactsModule().run()


if __name__ == '__main__':
    main()
