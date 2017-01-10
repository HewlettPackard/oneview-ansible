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
module: oneview_storage_volume_templates_facts
short_description: Retrieve facts about Storage Volume Templates of the OneView.
description:
    - Retrieve facts about Storage Volume Templates of the OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Storage Volume Template name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'connectableVolumeTemplates'."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_volume_templates


- name: Gather facts about a Storage Volume Template by name
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
  delegate_to: localhost

- debug: var=storage_volume_templates


- name: Gather facts about the connectable Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
    options:
      - connectableVolumeTemplates
  delegate_to: localhost

- debug: var=storage_volume_templates
- debug: var=connectable_volume_templates
'''

RETURN = '''
storage_volume_templates:
    description: Has all the OneView facts about the Storage Volume Templates.
    returned: Always, but can be null.
    type: complex

connectable_volume_templates:
    description: Has facts about the Connectable Storage Volume Templates.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class StorageVolumeTemplateFactsModule(object):
    argument_spec = {
        "config": {
            "required": False,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        },
        "options": {
            "required": False,
            "type": 'list'
        }}

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
            client = self.oneview_client.storage_volume_templates

            if self.module.params.get('name'):
                storage_volume_template = client.get_by('name', self.module.params['name'])
            else:
                storage_volume_template = client.get_all()

            ansible_facts = dict(storage_volume_templates=storage_volume_template)

            if self.module.params.get('options') and 'connectableVolumeTemplates' in self.module.params['options']:
                ansible_facts['connectable_volume_templates'] = client.get_connectable_volume_templates()

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    StorageVolumeTemplateFactsModule().run()


if __name__ == '__main__':
    main()
