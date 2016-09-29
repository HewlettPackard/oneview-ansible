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
from hpOneView.common import resource_compare

DOCUMENTATION = '''
---
module: oneview_logical_interconnect
short_description: Manage OneView Logical Interconnect resources.
description:
    - Provides an interface to manage Logical Interconnect resources.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Logical Interconnect resource.
              'compliant' brings the logical interconnect back to a consistent state.
              'ethernet_settings_updated' updates the Ethernet interconnect settings for the logical interconnect.
              'internal_networks_updated' updates the internal networks on the logical interconnect. This operation is
              non-idempotent.
              'settings_updated' updates the Logical Interconnect settings.
              'forwarding_information_base_generated' generates the forwarding information base dump file for the
              logical interconnect. This operation is non-idempotent and asynchronous.
              'qos_aggregated_configuration_updated' updates the QoS aggregated configuration for the logical
              interconnect.
              'snmp_configuration_updated' updates the SNMP configuration for the logical interconnect.
              'port_monitor_updated' updates the port monitor configuration of a logical interconnect.
              'configuration_updated' asynchronously applies or re-applies the logical interconnect configuration
              to all managed interconnects. This operation is non-idempotent.
              'firmware_installed' installs firmware to a logical interconnect. The three operations that are supported
              for the firmware update are Stage (uploads firmware to the interconnect), Activate (installs firmware on
              the interconnect) and Update (which does a Stage and Activate in a sequential manner). All of them are
              non-idempotent.
        choices: ['compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',
                  'forwarding_information_base_generated', 'qos_aggregated_configuration_updated',
                  'snmp_configuration_updated', 'port_monitor_updated', 'configuration_updated', 'firmware_installed']
    data:
      description:
        - List with the options.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Return the Logical Interconnect to a consistent state
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: compliant
  data:
    name: "Name of the Logical Interconnect"

- name: Update the Ethernet interconnect settings for the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: ethernet_settings_updated
  data:
    name: "Name of the Logical Interconnect"
    ethernetSettings:
      macRefreshInterval: 10

- name: Update the internal networks on the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: internal_networks_updated
    data:
      name: "Name of the Logical Interconnect"
      internalNetworks:
        - name: "Name of the Ethernet Network 1"
        - name: "Name of the Ethernet Network 2"
        - uri: "/rest/ethernet-networks/8a58cf7c-d49d-43b1-94ce-da5621be490c"

- name: Update the interconnect settings
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: settings_updated
    data:
      name: "Name of the Logical Interconnect"
      ethernetSettings:
        macRefreshInterval: 10

- name: Generate the forwarding information base dump file for the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: forwarding_information_base_generated
    data:
      name: "{{ logical_interconnect_name }}"  # could also be 'uri'

- name: Update the QoS aggregated configuration for the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: qos_aggregated_configuration_updated
    data:
      name: "Name of the Logical Interconnect"
      qosConfiguration:
      activeQosConfig:
        category: 'qos-aggregated-configuration'
        configType: 'Passthrough'
        downlinkClassificationType: ~
        uplinkClassificationType: ~
        qosTrafficClassifiers: []
        type: 'QosConfiguration'

- name: Update the SNMP configuration for the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: snmp_configuration_updated
  data:
    name: "Name of the Logical Interconnect"
    snmpConfiguration:
      enabled: True

- name: Update the port monitor configuration of the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: port_monitor_updated
    data:
      name: "Name of the Logical Interconnect"
      portMonitor:
        enablePortMonitor: False

- name: Update the configuration on the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: configuration_updated
  data:
    name: "Name of the Logical Interconnect"

- name: Install a firmware to the logical interconnect, running the stage operation to upload the firmware
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: firmware_installed
  data:
    name: "Name of the Logical Interconnect"
    firmware:
      command: Stage
      spp: "filename"  # could also be sppUri: '/rest/firmware-drivers/<filename>'
'''

RETURN = '''
storage_volume_template:
    description: Has the OneView facts about the Logical Interconnect.
    returned: on 'compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated', \
              and 'configuration_updated' states, but can be null.
    type: complex

interconnect_fib:
    description: Has the OneView facts about the Forwarding information Base.
    returned: on 'forwarding_information_base_generated' state, but can be null.
    type: complex

qos_configuration:
    description: Has the OneView facts about the QoS Configuration.
    returned: on 'qos_aggregated_configuration_updated' state, but can be null.
    type: complex

snmp_configuration:
    description: Has the OneView facts about the SNMP Configuration.
    returned: on 'snmp_configuration_updated' state, but can be null.
    type: complex

port_monitor:
    description: Has the OneView facts about the Port Monitor Configuration.
    returned: on 'port_monitor_updated' state, but can be null.
    type: complex

li_firmware:
    description: Has the OneView facts about the installed Firmware.
    returned: on 'firmware_installed' state, but can be null.
    type: complex
'''

LOGICAL_INTERCONNECT_CONSISTENT = 'logical interconnect returned to a consistent state.'
LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED = 'Ethernet settings updated successfully.'
LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED = 'Internal networks updated successfully.'
LOGICAL_INTERCONNECT_SETTINGS_UPDATED = 'Logical Interconnect setttings updated successfully.'
LOGICAL_INTERCONNECT_QOS_UPDATED = 'QoS aggregated configuration updated successfully.'
LOGICAL_INTERCONNECT_SNMP_UPDATED = 'SNMP configuration updated successfully.'
LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED = 'Port Monitor configuration updated successfully.'
LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED = 'Configuration on the logical interconnect updated successfully.'
LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED = 'Firmware updated successfully.'
LOGICAL_INTERCONNECT_NOT_FOUND = 'Logical Interconnect not found.'
LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND = 'Ethernet network not found: '
LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED = 'Nothing to do.'
LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED = 'No options provided.'


class LogicalInterconnectModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',
                     'forwarding_information_base_generated', 'qos_aggregated_configuration_updated',
                     'snmp_configuration_updated', 'port_monitor_updated', 'configuration_updated',
                     'firmware_installed']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            resource = self.__get_by_name(data)

            if not resource:
                raise Exception(LOGICAL_INTERCONNECT_NOT_FOUND)

            uri = resource['uri']

            if state == 'compliant':
                changed, msg, ansible_facts = self.__compliance(uri)
            elif state == 'ethernet_settings_updated':
                changed, msg, ansible_facts = self.__update_ethernet_settings(resource, data)
            elif state == 'internal_networks_updated':
                changed, msg, ansible_facts = self.__update_internal_networks(uri, data)
            elif state == 'settings_updated':
                changed, msg, ansible_facts = self.__update_settings(resource, data)
            elif state == 'forwarding_information_base_generated':
                changed, msg, ansible_facts = self.__generate_forwarding_information_base(uri)
            elif state == 'qos_aggregated_configuration_updated':
                changed, msg, ansible_facts = self.__update_qos_configuration(uri, data)
            elif state == 'snmp_configuration_updated':
                changed, msg, ansible_facts = self.__update_snmp_configuration(uri, data)
            elif state == 'port_monitor_updated':
                changed, msg, ansible_facts = self.__update_port_monitor(uri, data)
            elif state == 'configuration_updated':
                changed, msg, ansible_facts = self.__update_configuration(uri)
            elif state == 'firmware_installed':
                changed, msg, ansible_facts = self.__install_firmware(uri, data)

            if ansible_facts:
                self.module.exit_json(changed=changed, msg=msg, ansible_facts=ansible_facts)
            else:
                self.module.exit_json(changed=changed, msg=msg)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __compliance(self, uri):
        li = self.oneview_client.logical_interconnects.update_compliance(uri)
        return True, LOGICAL_INTERCONNECT_CONSISTENT, dict(logical_interconnect=li)

    def __update_ethernet_settings(self, resource, data):
        self.__validate_options('ethernetSettings', data)

        ethernet_settings_merged = resource['ethernetSettings'].copy()
        ethernet_settings_merged.update(data['ethernetSettings'])

        if resource_compare(resource['ethernetSettings'], ethernet_settings_merged):
            self.module.exit_json(changed=False,
                                  msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)
        else:
            li = self.oneview_client.logical_interconnects.update_ethernet_settings(resource['uri'],
                                                                                    ethernet_settings_merged)
            return True, LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __update_internal_networks(self, uri, data):
        self.__validate_options('internalNetworks', data)

        networks = []
        for network_uri_or_name in data['internalNetworks']:
            if 'name' in network_uri_or_name:
                ethernet_network = self.__get_ethernet_network_by_name(network_uri_or_name['name'])
                if not ethernet_network:
                    raise Exception(LOGICAL_INTERCONNECT_ETH_NETWORK_NOT_FOUND + network_uri_or_name['name'])
                networks.append(ethernet_network['uri'])
            elif 'uri' in network_uri_or_name:
                networks.append(network_uri_or_name['uri'])

        li = self.oneview_client.logical_interconnects.update_internal_networks(uri, networks)

        return True, LOGICAL_INTERCONNECT_INTERNAL_NETWORKS_UPDATED, dict(logical_interconnect=li)

    def __update_settings(self, resource, data):
        self.__validate_settings(data)

        ethernet_settings_merged = self.__merge_network_settings('ethernetSettings', resource, data)
        fcoe_settings_merged = self.__merge_network_settings('fcoeSettings', resource, data)

        if resource_compare(resource['ethernetSettings'], ethernet_settings_merged) and \
                resource_compare(resource['fcoeSettings'], fcoe_settings_merged):

            self.module.exit_json(changed=False,
                                  msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)
        else:
            settings = {
                'ethernetSettings': ethernet_settings_merged,
                'fcoeSettings': fcoe_settings_merged
            }
            li = self.oneview_client.logical_interconnects.update_settings(resource['uri'], settings)
            return True, LOGICAL_INTERCONNECT_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __generate_forwarding_information_base(self, uri):
        result = self.oneview_client.logical_interconnects.create_forwarding_information_base(uri)
        return True, result.get('status'), dict(interconnect_fib=result)

    def __update_qos_configuration(self, uri, data):
        self.__validate_options('qosConfiguration', data)

        qos_config = self.__get_qos_aggregated_configuration(uri)
        qos_config_merged = self.__merge_options(data['qosConfiguration'], qos_config)

        if resource_compare(qos_config_merged, qos_config):

            self.module.exit_json(changed=False,
                                  msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)
        else:
            qos_config_updated = self.oneview_client.logical_interconnects.update_qos_aggregated_configuration(
                uri, qos_config_merged)

            return True, LOGICAL_INTERCONNECT_QOS_UPDATED, dict(qos_configuration=qos_config_updated)

    def __update_snmp_configuration(self, uri, data):
        self.__validate_options('snmpConfiguration', data)

        snmp_config = self.__get_snmp_configuration(uri)
        snmp_config_merged = self.__merge_options(data['snmpConfiguration'], snmp_config)

        if resource_compare(snmp_config_merged, snmp_config):

            return False, LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED, None
        else:
            snmp_config_updated = self.oneview_client.logical_interconnects.update_snmp_configuration(
                uri, snmp_config_merged)

            return True, LOGICAL_INTERCONNECT_SNMP_UPDATED, dict(snmp_configuration=snmp_config_updated)

    def __update_port_monitor(self, uri, data):
        self.__validate_options('portMonitor', data)

        monitor_config = self.__get_port_monitor_configuration(uri)
        monitor_config_merged = self.__merge_options(data['portMonitor'], monitor_config)

        if resource_compare(monitor_config_merged, monitor_config):
            return False, LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED, None
        else:
            monitor_config_updated = self.oneview_client.logical_interconnects.update_port_monitor(
                uri, monitor_config_merged)
            result = dict(port_monitor=monitor_config_updated)
            return True, LOGICAL_INTERCONNECT_PORT_MONITOR_UPDATED, result

    def __install_firmware(self, uri, data):
        self.__validate_options('firmware', data)

        options = data['firmware'].copy()
        if 'spp' in options:
            options['sppUri'] = self.__build_firmware_uri(options.pop('spp'))

        firmware = self.oneview_client.logical_interconnects.install_firmware(options, uri)

        return True, LOGICAL_INTERCONNECT_FIRMWARE_INSTALLED, dict(li_firmware=firmware)

    def __update_configuration(self, uri):
        result = self.oneview_client.logical_interconnects.update_configuration(uri)

        return True, LOGICAL_INTERCONNECT_CONFIGURATION_UPDATED, dict(logical_interconnect=result)

    def __get_by_name(self, data):
        return self.oneview_client.logical_interconnects.get_by_name(data['name'])

    def __get_ethernet_network_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None

    def __get_qos_aggregated_configuration(self, uri):
        return self.oneview_client.logical_interconnects.get_qos_aggregated_configuration(uri)

    def __get_snmp_configuration(self, uri):
        return self.oneview_client.logical_interconnects.get_snmp_configuration(uri)

    def __get_port_monitor_configuration(self, uri):
        return self.oneview_client.logical_interconnects.get_port_monitor(uri)

    def __merge_network_settings(self, settings_type, resource, data):
        settings_merged = {}
        if resource.get(settings_type):
            settings_merged = resource[settings_type].copy()

        if settings_type in data:
            settings_merged.update(data[settings_type])

        return settings_merged

    def __merge_options(self, data, subresource):
        options = data.copy()

        options_merged = subresource.copy()
        options_merged.update(options)

        return options_merged

    def __validate_options(self, subresource_type, data):
        if subresource_type not in data:
            raise Exception(LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED)

    def __validate_settings(self, data):
        if 'ethernetSettings' not in data and 'fcoeSettings' not in data:
            raise Exception(LOGICAL_INTERCONNECT_NO_OPTIONS_PROVIDED)

    def __build_firmware_uri(self, filename):
        return '/rest/firmware-drivers/' + filename


def main():
    LogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
