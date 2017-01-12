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
try:
    from hpOneView.oneview_client import OneViewClient

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_logical_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnects.
description:
    - Retrieve facts about one or more of the OneView Logical Interconnects.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Bruno Souza (@bsouza)"
    - "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          'start': The first item to return, using 0-based indexing.
          'count': The number of resources to return.
          'filter': A general filter/query string to narrow the list of items returned.
          'sort': The sort order of the returned data set."
      required: false
    name:
      description:
        - Logical Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Logical Interconnect.
          Options allowed:
          'qos_aggregated_configuration' gets the QoS aggregated configuration for the logical interconnect.
          'snmp_configuration' gets the SNMP configuration for a logical interconnect.
          'port_monitor' gets the port monitor configuration of a logical interconnect.
          'internal_vlans' gets the internal VLAN IDs for the provisioned networks on a logical interconnect.
          'forwarding_information_base' gets the forwarding information base data for a logical interconnect.
          'firmware' get the installed firmware for a logical interconnect.
          'unassigned_uplink_ports' gets a collection of uplink ports from the member interconnects which are eligible
          for assignment to an analyzer port.
          'telemetry_configuration' gets the telemetry configuration of the logical interconnect.
        - These options are valid just when a 'name' is provided. Otherwise it will be ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnects
  oneview_logical_interconnect_facts:
  config: "{{ config }}"

- debug: var=logical_interconnects

- name: Gather paginated and sorted facts about Logical Interconnects
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=logical_interconnects

- name: Gather facts about a Logical Interconnect by name with QOS Configuration
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - qos_aggregated_configuration

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration

- name: Gather facts about a Logical Interconnect by name with all options
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - qos_aggregated_configuration
      - snmp_configuration
      - port_monitor
      - internal_vlans
      - forwarding_information_base
      - firmware
      - unassigned_uplink_ports
      - telemetry_configuration

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration
- debug: var=snmp_configuration
- debug: var=port_monitor
- debug: var=internal_vlans
- debug: var=forwarding_information_base
- debug: var=firmware
- debug: var=unassigned_uplink_ports
- debug: var=telemetry_configuration
'''

RETURN = '''
logical_interconnects:
    description: The list of logical interconnects.
    returned: Always, but can be null.
    type: list

qos_aggregated_configuration:
    description: The QoS aggregated configuration for the logical interconnect.
    returned: When requested, but can be null.
    type: complex

snmp_configuration:
    description: The SNMP configuration for a logical interconnect.
    returned: When requested, but can be null.
    type: complex

port_monitor:
    description: The port monitor configuration of a logical interconnect.
    returned: When requested, but can be null.
    type: complex

internal_vlans:
    description: The internal VLAN IDs for the provisioned networks on a logical interconnect.
    returned: When requested, but can be null.
    type: complex

forwarding_information_base:
    description: The forwarding information base data for a logical interconnect.
    returned: When requested, but can be null.
    type: complex

firmware:
    description: The installed firmware for a logical interconnect.
    returned: When requested, but can be null.
    type: complex

unassigned_uplink_ports:
    description: "A collection of uplink ports from the member interconnects which are eligible for assignment to an
                  analyzer port on a logical interconnect."
    returned: When requested, but can be null.
    type: complex

telemetry_configuration:
    description: The telemetry configuration of the logical interconnect.
    returned: When requested, but can be null.
    type: complex
'''

LOGICAL_INTERCONNECT_NOT_FOUND = 'Logical Interconnect not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class LogicalInterconnectFactsModule(object):

    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        if not self.module.params['config']:
            logical_interconnects = OneViewClient.from_environment_variables().logical_interconnects
        else:
            logical_interconnects = OneViewClient.from_json_file(self.module.params['config']).logical_interconnects

        self.resource_client = logical_interconnects
        self.options = dict(
            qos_aggregated_configuration=logical_interconnects.get_qos_aggregated_configuration,
            snmp_configuration=logical_interconnects.get_snmp_configuration,
            port_monitor=logical_interconnects.get_port_monitor,
            internal_vlans=logical_interconnects.get_internal_vlans,
            forwarding_information_base=logical_interconnects.get_forwarding_information_base,
            firmware=logical_interconnects.get_firmware,
            unassigned_uplink_ports=logical_interconnects.get_unassigned_uplink_ports,
            telemetry_configuration=logical_interconnects.get_telemetry_configuration,
        )

    def run(self):
        try:
            name = self.module.params["name"]

            if name:
                facts = self.__get_by_name(name)
            else:
                params = self.module.params.get('params') or {}
                logical_interconnects = self.resource_client.get_all(**params)
                facts = dict(logical_interconnects=logical_interconnects)

            self.module.exit_json(changed=False, ansible_facts=facts)
        except Exception as exception:
            self.module.fail_json(msg=exception.args[0])

    def __get_by_name(self, name):
        logical_interconnect = self.resource_client.get_by_name(name=name)
        if not logical_interconnect:
            raise Exception(LOGICAL_INTERCONNECT_NOT_FOUND)

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
            if option == 'telemetry_configuration':
                telemetry_configuration_uri = logical_interconnect["telemetryConfiguration"]["uri"]
                facts[option] = self.options[option](telemetry_configuration_uri=telemetry_configuration_uri)
            else:
                facts[option] = self.options[option](id_or_uri=uri)

        return facts


def main():
    LogicalInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
