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
module: oneview_fc_network_facts
short_description: Retrieve the facts about one or more of the OneView Fibre Channel Networks.
description:
    - Retrieve the facts about one or more of the Fibre Channel Networks from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Fibre Channel Network name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Fibre Channel Networks
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fc_networks

- name: Gather facts about a Fibre Channel Network by name
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"
    name: network name

- debug: var=fc_networks
'''

RETURN = '''
fc_networks:
    description: Has all the OneView facts about the Fibre Channel Networks.
    returned: Always, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class FcNetworkFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if self.module.params['name']:
                self.__get_by_name(self.module.params['name'])
            else:
                self.__get_all()

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_by_name(self, name):
        fc_network = self.oneview_client.fc_networks.get_by('name', name)

        self.module.exit_json(changed=False,
                              ansible_facts=dict(fc_networks=fc_network))

    def __get_all(self):
        fc_networks = self.oneview_client.fc_networks.get_all()

        self.module.exit_json(changed=False,
                              ansible_facts=dict(fc_networks=fc_networks))


def main():
    FcNetworkFactsModule().run()


if __name__ == '__main__':
    main()
