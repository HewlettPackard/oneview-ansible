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
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_fabric_facts
short_description: Retrieve the facts about one or more of the OneView Fabrics.
description:
    - Retrieve the facts about one or more of the Fabrics from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Fabric name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics
'''

RETURN = '''
fabrics:
    description: Has all the OneView facts about the Fabrics.
    returned: always, but can be null
    type: complex
'''


class FabricFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            name = self.module.params['name']
            if name:
                fabrics = self.oneview_client.fabrics.get_by('name', name)
            else:
                fabrics = self.oneview_client.fabrics.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(fabrics=fabrics))

        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])


def main():
    FabricFactsModule().run()


if __name__ == '__main__':
    main()
