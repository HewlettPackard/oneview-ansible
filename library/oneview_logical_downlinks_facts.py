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
module: oneview_logical_downlinks_facts
short_description: Retrieve facts about one or more of the OneView Logical Downlinks.
description:
    - Retrieve facts about one or more of the Logical Downlinks from OneView.
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
        - Logical Downlink name
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Logical Downlinks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather facts about all Logical Downlinks excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather facts about a Logical Downlink by name and excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    name: "LD415a472f-ed77-42cc-9a5e-b9bd5d096923 (HP VC FlexFabric-20/40 F8 Module)"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks
'''

RETURN = '''
logical_interconnects:
    description: The list of logical downlinks.
    returned: Always, but can be null.
    type: list
'''


class LogicalDownlinksFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        excludeEthernet=dict(type='bool', default=False)
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.logical_downlinks

    def run(self):
        try:
            name = self.module.params["name"]
            excludeEthernet = self.module.params["excludeEthernet"]
            logical_downlinks = None

            if name and excludeEthernet:
                logical_downlink = self.__get_by_name(name)[0]
                logical_downlinks = self.resource_client.get_without_ethernet(id_or_uri=logical_downlink["uri"])
            elif name:
                logical_downlinks = self.__get_by_name(name)
            elif excludeEthernet:
                logical_downlinks = self.resource_client.get_all_without_ethernet()
            else:
                logical_downlinks = self.resource_client.get_all()

            self.module.exit_json(changed=False, ansible_facts=dict(logical_downlinks=logical_downlinks))
        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        return self.resource_client.get_by('name', name)


def main():
    LogicalDownlinksFactsModule().run()


if __name__ == '__main__':
    main()
