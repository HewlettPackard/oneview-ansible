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
module: oneview_interconnect_statistics_facts
short_description: Retrieve the statistics facts about one interconnect from OneView.
description:
    - Retrieve the statistics facts about one interconnect from OneView.
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
        - Interconnect name
      required: true
    port_name:
      description:
        - Interconnect name
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_statistics_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    delegate_to: localhost

- debug: interconnect_statistics
'''

RETURN = '''
interconnect_statistics:
    description: Has all the OneView facts about the Interconnect Statistics.
    returned: If port_name is undefined
    type: dict

port_statistics:
    description: Statistics for the specified port name on an interconnect.
    returned: If port name is defined
    type: dict

subport_statistics:
    description: The subport statistics on an interconnect
    returned: If subport_number is defined
    type: dict
'''


class InterconnectStatisticsFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=True, type='str'),
        port_name=dict(required=False, type='str'),
        subport_number=dict(required=False, type='int')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            interconnect_statistics = None
            port_statistics = None
            subport_statistics = None

            interconnect_uri = self.__get_interconnect_uri()
            port_name = self.module.params['port_name']
            subport_number = self.module.params['subport_number']

            if subport_number:
                subport_statistics = self.oneview_client.interconnects.get_subport_statistics(
                    id_or_uri=interconnect_uri,
                    port_name=port_name,
                    subport_number=subport_number
                )
            elif port_name:
                port_statistics = self.oneview_client.interconnects.get_statistics(
                    id_or_uri=interconnect_uri,
                    port_name=port_name
                )
            else:
                interconnect_statistics = self.oneview_client.interconnects.get_statistics(id_or_uri=interconnect_uri)

            self.module.exit_json(
                changed=False,
                ansible_facts=dict(
                    interconnect_statistics=interconnect_statistics,
                    port_statistics=port_statistics,
                    subport_statistics=subport_statistics
                )
            )
        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_interconnect_uri(self):
        name = self.module.params["name"]
        interconnect = self.oneview_client.interconnects.get_by_name(name)

        if not interconnect:
            raise Exception("There is no interconnect named {}".format(name))

        return interconnect["uri"]


def main():
    InterconnectStatisticsFactsModule().run()


if __name__ == '__main__':
    main()
