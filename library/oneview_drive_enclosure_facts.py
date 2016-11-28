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
    from hpOneView.common import transform_list_to_dict

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_drive_enclosure_facts
short_description: Retrieve the facts about one or more of the OneView Drive Enclosures.
description:
    - Retrieve the facts about one or more of the Drive Enclosures from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Drive Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Drive Enclosure related resources.
          Options allowed: portMap"
        - "To gather additional facts it is required inform the Drive Enclosure name. Otherwise, these options will be
          ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - This resource is only available on HPE Synergy.
'''

EXAMPLES = '''
- name: Gather facts about all Drive Enclosures
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure by name
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure and the Port Map
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure
    options:
        - portMap

- debug: var=drive_enclosures
- debug: var=drive_enclosure_port_map
'''

RETURN = '''
drive_enclosures:
    description: Has all the OneView facts about the Drive Enclosures.
    returned: Always, but can be null.
    type: complex

drive_enclosure_port_map:
    description: Has all the OneView facts about the Drive Enclosure Port Map.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class DriveEnclosureFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list')
    )

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
            name = self.module.params['name']
            options = self.module.params.get('options')
            facts = {}

            if name:
                drive_enclosures = self.oneview_client.drive_enclosures.get_by('name', name)
                if drive_enclosures:
                    drive_enclosures_uri = drive_enclosures[0]['uri']
                    if options:
                        options = transform_list_to_dict(options)
                        if options.get('portMap'):
                            facts['drive_enclosure_port_map'] = \
                                self.oneview_client.drive_enclosures.get_port_map(drive_enclosures_uri)
            else:
                drive_enclosures = self.oneview_client.drive_enclosures.get_all()

            facts['drive_enclosures'] = drive_enclosures

            self.module.exit_json(changed=False, ansible_facts=facts)

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])


def main():
    DriveEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
