#!/usr/bin/python
# -*- coding: utf-8 -*-
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
module: oneview_logical_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnects.
description:
    - Retrieve facts about one or more of the OneView Logical Interconnects.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Logical Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Logical Interconnect related resources.
          Options allowed: qos_aggregated_configuration, snmp_configuration"
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnects
  oneview_logical_interconnect_facts:
  config: "{{ config }}"

- debug: var=logical_interconnects

- name: Gather facts about a Logical Interconnect by name with QOS Configuration
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - qos_aggregated_configuration

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration
'''

RETURN = '''
logical_interconnects:
    description: The list of logical interconnects.
    returned: always, but can be null
    type: list

qos_aggregated_configuration:
    description: The QoS aggregated configuration for the logical interconnect.
    returned: when request, but can be null
    type: complex
'''


class LogicalInterconnectFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        logical_interconnects = OneViewClient.from_json_file(self.module.params['config']).logical_interconnects

        self.resource_client = logical_interconnects
        self.options = dict(
            qos_aggregated_configuration=logical_interconnects.get_qos_aggregated_configuration,
            snmp_configuration=logical_interconnects.get_snmp_configuration
        )

    def run(self):
        try:
            name = self.module.params["name"]

            if name:
                facts = self.__get_by_name(name)
            else:
                logical_interconnects = self.resource_client.get_all()
                facts = dict(logical_interconnects=logical_interconnects)

            self.module.exit_json(changed=False, ansible_facts=facts)
        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __get_by_name(self, name):
        logical_interconnect = self.resource_client.get_by_name(name=name)
        facts = dict(logical_interconnects=logical_interconnect)

        options = self.module.params["options"]

        if options:
            options_facts = self.__get_options(logical_interconnect, options)
            facts.update(options_facts)

        return facts

    def __get_options(self, logical_interconnect, options):
        facts = dict()
        uri = logical_interconnect["uri"]

        for option in options:
            facts[option] = self.options[option](id_or_uri=uri)

        return facts


def main():
    LogicalInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
