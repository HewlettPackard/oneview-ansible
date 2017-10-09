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
module: oneview_logical_interconnect
short_description: Manage OneView Logical Interconnect resources.
description:
    - Provides an interface to manage Logical Interconnect resources.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Interconnect resource.
              C(compliant) brings the logical interconnect back to a consistent state.
              C(ethernet_settings_updated) updates the Ethernet interconnect settings for the logical interconnect.
              C(internal_networks_updated) updates the internal networks on the logical interconnect. This operation is
              non-idempotent.
              C(settings_updated) updates the Logical Interconnect settings.
              C(forwarding_information_base_generated) generates the forwarding information base dump file for the
              logical interconnect. This operation is non-idempotent and asynchronous.
              C(qos_aggregated_configuration_updated) updates the QoS aggregated configuration for the logical
              interconnect.
              C(snmp_configuration_updated) updates the SNMP configuration for the logical interconnect.
              C(port_monitor_updated) updates the port monitor configuration of a logical interconnect.
              C(configuration_updated) asynchronously applies or re-applies the logical interconnect configuration
              to all managed interconnects. This operation is non-idempotent.
              C(firmware_installed) installs firmware to a logical interconnect. The three operations that are supported
              for the firmware update are Stage (uploads firmware to the interconnect), Activate (installs firmware on
              the interconnect) and Update (which does a Stage and Activate in a sequential manner). All of them are
              non-idempotent.
              C(telemetry_configuration_updated) updates the telemetry configuration of a logical interconnect.
              C(scopes_updated) updates the scopes associated with the logical interconnect.
        choices: ['compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',
                  'forwarding_information_base_generated', 'qos_aggregated_configuration_updated',
                  'snmp_configuration_updated', 'port_monitor_updated', 'configuration_updated', 'firmware_installed',
                  'telemetry_configuration_updated']
    data:
        description:
            - List with the options.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
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

- name: Updates the telemetry configuration of a logical interconnect.
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: telemetry_configuration_updated
  data:
    name: "Name of the Logical Interconnect"
    telemetryConfiguration:
      sampleCount: 12
      enableTelemetry: True
      sampleInterval: 300

- debug: var=telemetry_configuration

- name: Updates the scopes of a logical interconnect.
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: scopes_updated
  data:
    name: "Name of the Logical Interconnect"
    scopeUris:
      - '/rest/scopes/00SC123456'
      - '/rest/scopes/01SC123456'

- debug: var=scope_uris
'''

RETURN = '''
storage_volume_template:
    description: Has the OneView facts about the Logical Interconnect.
    returned: On 'compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated', \
              and 'configuration_updated' states, but can be null.
    type: dict

interconnect_fib:
    description: Has the OneView facts about the Forwarding information Base.
    returned: On 'forwarding_information_base_generated' state, but can be null.
    type: dict

qos_configuration:
    description: Has the OneView facts about the QoS Configuration.
    returned: On 'qos_aggregated_configuration_updated' state, but can be null.
    type: dict

snmp_configuration:
    description: Has the OneView facts about the SNMP Configuration.
    returned: On 'snmp_configuration_updated' state, but can be null.
    type: dict

port_monitor:
    description: Has the OneView facts about the Port Monitor Configuration.
    returned: On 'port_monitor_updated' state, but can be null.
    type: dict

li_firmware:
    description: Has the OneView facts about the installed Firmware.
    returned: On 'firmware_installed' state, but can be null.
    type: dict

telemetry_configuration:
    description: Has the OneView facts about the Telemetry Configuration.
    returned: On 'telemetry_configuration_updated' state, but can be null.
    type: dict

scope_uris:
    description: Has the scope URIs the specified logical interconnect is inserted into.
    returned: On 'scopes_updated' state, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import (OneViewModuleBase,
                                  HPOneViewResourceNotFound,
                                  ResourceComparator,
                                  HPOneViewValueError)


class LogicalInterconnectModule(OneViewModuleBase):
    MSG_CONSISTENT = 'Logical Interconnect returned to a consistent state.'
    MSG_ETH_SETTINGS_UPDATED = 'Ethernet settings updated successfully.'
    MSG_INTERNAL_NETWORKS_UPDATED = 'Internal networks updated successfully.'
    MSG_SETTINGS_UPDATED = 'Logical Interconnect setttings updated successfully.'
    MSG_QOS_UPDATED = 'QoS aggregated configuration updated successfully.'
    MSG_SNMP_UPDATED = 'SNMP configuration updated successfully.'
    MSG_PORT_MONITOR_UPDATED = 'Port Monitor configuration updated successfully.'
    MSG_CONFIGURATION_UPDATED = 'Configuration on the Logical Interconnect updated successfully.'
    MSG_SCOPES_UPDATED = 'Scopes on the Logical Interconnect updated successfully.'
    MSG_TELEMETRY_CONFIGURATION_UPDATED = 'Telemetry configuration updated successfully.'
    MSG_FIRMWARE_INSTALLED = 'Firmware updated successfully.'
    MSG_NOT_FOUND = 'Logical Interconnect not found.'
    MSG_ETH_NETWORK_NOT_FOUND = 'Ethernet network not found: '
    MSG_NO_CHANGES_PROVIDED = 'Nothing to do.'
    MSG_NO_OPTIONS_PROVIDED = 'No options provided.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',
                     'forwarding_information_base_generated', 'qos_aggregated_configuration_updated',
                     'snmp_configuration_updated', 'port_monitor_updated', 'configuration_updated',
                     'firmware_installed', 'telemetry_configuration_updated', 'scopes_updated']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(LogicalInterconnectModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                        validate_etag_support=True)
        self.resource_client = self.oneview_client.logical_interconnects

    def execute_module(self):

        resource = self.__get_by_name(self.data)

        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)

        changed, msg, ansible_facts = False, '', dict()
        uri = resource['uri']

        if self.state == 'compliant':
            changed, msg, ansible_facts = self.__compliance(uri)
        elif self.state == 'ethernet_settings_updated':
            changed, msg, ansible_facts = self.__update_ethernet_settings(resource, self.data)
        elif self.state == 'internal_networks_updated':
            changed, msg, ansible_facts = self.__update_internal_networks(uri, self.data)
        elif self.state == 'settings_updated':
            changed, msg, ansible_facts = self.__update_settings(resource, self.data)
        elif self.state == 'forwarding_information_base_generated':
            changed, msg, ansible_facts = self.__generate_forwarding_information_base(uri)
        elif self.state == 'qos_aggregated_configuration_updated':
            changed, msg, ansible_facts = self.__update_qos_configuration(uri, self.data)
        elif self.state == 'snmp_configuration_updated':
            changed, msg, ansible_facts = self.__update_snmp_configuration(uri, self.data)
        elif self.state == 'port_monitor_updated':
            changed, msg, ansible_facts = self.__update_port_monitor(uri, self.data)
        elif self.state == 'configuration_updated':
            changed, msg, ansible_facts = self.__update_configuration(uri)
        elif self.state == 'firmware_installed':
            changed, msg, ansible_facts = self.__install_firmware(uri, self.data)
        elif self.state == 'telemetry_configuration_updated':
            changed, msg, ansible_facts = self.__update_telemetry_configuration(resource, self.data)
        elif self.state == 'scopes_updated':
            changed, msg, ansible_facts = self.__update_scopes(resource, self.data)

        if ansible_facts:
            result = dict(changed=changed, msg=msg, ansible_facts=ansible_facts)
        else:
            result = dict(changed=changed, msg=msg)

        return result

    def __compliance(self, uri):
        li = self.oneview_client.logical_interconnects.update_compliance(uri)
        return True, self.MSG_CONSISTENT, dict(logical_interconnect=li)

    def __update_ethernet_settings(self, resource, data):
        self.__validate_options('ethernetSettings', data)

        ethernet_settings_merged = resource['ethernetSettings'].copy()
        ethernet_settings_merged.update(data['ethernetSettings'])

        if ResourceComparator.compare(resource['ethernetSettings'], ethernet_settings_merged):
            return False, self.MSG_NO_CHANGES_PROVIDED, dict()
        else:
            li = self.oneview_client.logical_interconnects.update_ethernet_settings(resource['uri'],
                                                                                    ethernet_settings_merged)
            return True, self.MSG_ETH_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __update_internal_networks(self, uri, data):
        self.__validate_options('internalNetworks', data)

        networks = []
        for network_uri_or_name in data['internalNetworks']:
            if 'name' in network_uri_or_name:
                ethernet_network = self.__get_ethernet_network_by_name(network_uri_or_name['name'])
                if not ethernet_network:
                    msg = self.MSG_ETH_NETWORK_NOT_FOUND + network_uri_or_name['name']
                    raise HPOneViewResourceNotFound(msg)
                networks.append(ethernet_network['uri'])
            elif 'uri' in network_uri_or_name:
                networks.append(network_uri_or_name['uri'])

        li = self.oneview_client.logical_interconnects.update_internal_networks(uri, networks)

        return True, self.MSG_INTERNAL_NETWORKS_UPDATED, dict(logical_interconnect=li)

    def __update_settings(self, resource, data):
        self.__validate_settings(data)

        ethernet_settings_merged = self.__merge_network_settings('ethernetSettings', resource, data)
        fcoe_settings_merged = self.__merge_network_settings('fcoeSettings', resource, data)

        if ResourceComparator.compare(resource['ethernetSettings'], ethernet_settings_merged) and \
                ResourceComparator.compare(resource['fcoeSettings'], fcoe_settings_merged):

            return False, self.MSG_NO_CHANGES_PROVIDED, dict(logical_interconnect=resource)
        else:
            settings = {
                'ethernetSettings': ethernet_settings_merged,
                'fcoeSettings': fcoe_settings_merged
            }
            li = self.oneview_client.logical_interconnects.update_settings(resource['uri'], settings)
            return True, self.MSG_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __generate_forwarding_information_base(self, uri):
        result = self.oneview_client.logical_interconnects.create_forwarding_information_base(uri)
        return True, result.get('status'), dict(interconnect_fib=result)

    def __update_qos_configuration(self, uri, data):
        self.__validate_options('qosConfiguration', data)

        qos_config = self.__get_qos_aggregated_configuration(uri)
        qos_config_merged = self.__merge_options(data['qosConfiguration'], qos_config)

        if ResourceComparator.compare(qos_config_merged, qos_config):
            return False, self.MSG_NO_CHANGES_PROVIDED, dict()
        else:
            qos_config_updated = self.oneview_client.logical_interconnects.update_qos_aggregated_configuration(
                uri, qos_config_merged)

            return True, self.MSG_QOS_UPDATED, dict(qos_configuration=qos_config_updated)

    def __update_snmp_configuration(self, uri, data):
        self.__validate_options('snmpConfiguration', data)

        snmp_config = self.__get_snmp_configuration(uri)
        snmp_config_merged = self.__merge_options(data['snmpConfiguration'], snmp_config)

        if ResourceComparator.compare(snmp_config_merged, snmp_config):

            return False, self.MSG_NO_CHANGES_PROVIDED, None
        else:
            snmp_config_updated = self.oneview_client.logical_interconnects.update_snmp_configuration(
                uri, snmp_config_merged)

            return True, self.MSG_SNMP_UPDATED, dict(snmp_configuration=snmp_config_updated)

    def __update_port_monitor(self, uri, data):
        self.__validate_options('portMonitor', data)

        monitor_config = self.__get_port_monitor_configuration(uri)
        monitor_config_merged = self.__merge_options(data['portMonitor'], monitor_config)

        if ResourceComparator.compare(monitor_config_merged, monitor_config):
            return False, self.MSG_NO_CHANGES_PROVIDED, None
        else:
            monitor_config_updated = self.oneview_client.logical_interconnects.update_port_monitor(
                uri, monitor_config_merged)
            result = dict(port_monitor=monitor_config_updated)
            return True, self.MSG_PORT_MONITOR_UPDATED, result

    def __install_firmware(self, uri, data):
        self.__validate_options('firmware', data)

        options = data['firmware'].copy()
        if 'spp' in options:
            options['sppUri'] = self.__build_firmware_uri(options.pop('spp'))

        firmware = self.oneview_client.logical_interconnects.install_firmware(options, uri)

        return True, self.MSG_FIRMWARE_INSTALLED, dict(li_firmware=firmware)

    def __update_configuration(self, uri):
        result = self.oneview_client.logical_interconnects.update_configuration(uri)

        return True, self.MSG_CONFIGURATION_UPDATED, dict(logical_interconnect=result)

    def __update_telemetry_configuration(self, resource, data):
        config = data.get('telemetryConfiguration')
        telemetry_config_uri = resource['telemetryConfiguration']['uri']

        result = self.oneview_client.logical_interconnects.update_telemetry_configurations(telemetry_config_uri, config)

        return True, self.MSG_TELEMETRY_CONFIGURATION_UPDATED, dict(
            telemetry_configuration=result.get('telemetryConfiguration'))

    def __update_scopes(self, resource, data):

        scope_uris = self.data.pop('scopeUris', None)
        result = dict(changed=False,
                      msg=self.MSG_NO_CHANGES_PROVIDED,
                      ansible_facts=dict(scope_uris=resource))
        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'scope_uris', scope_uris)
            if result['changed']:
                result['msg'] = self.MSG_SCOPES_UPDATED

        result['ansible_facts']['scope_uris'] = result['ansible_facts']['scope_uris'].pop('scopeUris', None)

        return result['changed'], result['msg'], result['ansible_facts']

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
            raise HPOneViewValueError(self.MSG_NO_OPTIONS_PROVIDED)

    def __validate_settings(self, data):
        if 'ethernetSettings' not in data and 'fcoeSettings' not in data:
            raise HPOneViewValueError(self.MSG_NO_OPTIONS_PROVIDED)

    def __build_firmware_uri(self, filename):
        return '/rest/firmware-drivers/' + filename


def main():
    LogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
