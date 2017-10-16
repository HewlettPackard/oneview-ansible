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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_logical_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnects.
description:
    - Retrieve facts about one or more of the OneView Logical Interconnects.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author:
    - "Bruno Souza (@bsouza)"
    - "Mariana Kreisig (@marikrg)"
    - "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Logical Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Logical Interconnect.
          Options allowed:
          C(qos_aggregated_configuration) gets the QoS aggregated configuration for the logical interconnect.
          C(snmp_configuration) gets the SNMP configuration for a logical interconnect.
          C(port_monitor) gets the port monitor configuration of a logical interconnect.
          C(internal_vlans) gets the internal VLAN IDs for the provisioned networks on a logical interconnect.
          C(forwarding_information_base) gets the forwarding information base data for a logical interconnect.
          C(firmware) get the installed firmware for a logical interconnect.
          C(unassigned_uplink_ports) gets a collection of uplink ports from the member interconnects which are eligible
          for assignment to an analyzer port.
          C(telemetry_configuration) gets the telemetry configuration of the logical interconnect.
          C(ethernet_settings) gets the Ethernet interconnect settings for the Logical Interconnect.
        - These options are valid just when a C(name) is provided. Otherwise it will be ignored."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
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
      - ethernet_settings

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration
- debug: var=snmp_configuration
- debug: var=port_monitor
- debug: var=internal_vlans
- debug: var=forwarding_information_base
- debug: var=firmware
- debug: var=unassigned_uplink_ports
- debug: var=telemetry_configuration
- debug: var=ethernet_settings
'''

RETURN = '''
logical_interconnects:
    description: The list of logical interconnects.
    returned: Always, but can be null.
    type: list

qos_aggregated_configuration:
    description: The QoS aggregated configuration for the logical interconnect.
    returned: When requested, but can be null.
    type: dict

snmp_configuration:
    description: The SNMP configuration for a logical interconnect.
    returned: When requested, but can be null.
    type: dict

port_monitor:
    description: The port monitor configuration of a logical interconnect.
    returned: When requested, but can be null.
    type: dict

internal_vlans:
    description: The internal VLAN IDs for the provisioned networks on a logical interconnect.
    returned: When requested, but can be null.
    type: dict

forwarding_information_base:
    description: The forwarding information base data for a logical interconnect.
    returned: When requested, but can be null.
    type: dict

firmware:
    description: The installed firmware for a logical interconnect.
    returned: When requested, but can be null.
    type: dict

unassigned_uplink_ports:
    description: "A collection of uplink ports from the member interconnects which are eligible for assignment to an
                  analyzer port on a logical interconnect."
    returned: When requested, but can be null.
    type: dict

telemetry_configuration:
    description: The telemetry configuration of the logical interconnect.
    returned: When requested, but can be null.
    type: dict

ethernet_settings:
    description: The Ethernet Interconnect Settings.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class LogicalInterconnectFactsModule(OneViewModuleBase):
    MSG_NOT_FOUND = 'Logical Interconnect not found.'

    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(LogicalInterconnectFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

        self.resource_client = self.oneview_client.logical_interconnects
        self.options = dict(
            qos_aggregated_configuration=self.resource_client.get_qos_aggregated_configuration,
            snmp_configuration=self.resource_client.get_snmp_configuration,
            port_monitor=self.resource_client.get_port_monitor,
            internal_vlans=self.resource_client.get_internal_vlans,
            forwarding_information_base=self.resource_client.get_forwarding_information_base,
            firmware=self.resource_client.get_firmware,
            unassigned_uplink_ports=self.resource_client.get_unassigned_uplink_ports,
            telemetry_configuration=self.resource_client.get_telemetry_configuration,
            ethernet_settings=self.resource_client.get_ethernet_settings,
        )

    def execute_module(self):
        name = self.module.params["name"]

        if name:
            facts = self.__get_by_name(name)
        else:
            logical_interconnects = self.resource_client.get_all(**self.facts_params)
            facts = dict(logical_interconnects=logical_interconnects)

        return dict(changed=False, ansible_facts=facts)

    def __get_by_name(self, name):
        logical_interconnect = self.resource_client.get_by_name(name=name)
        if not logical_interconnect:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)

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
