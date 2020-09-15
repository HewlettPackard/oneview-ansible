#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
    - "hpeOneView >= 5.0.0"
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: compliant
    data:
      name: "Name of the Logical Interconnect"

- name: Update the Ethernet interconnect settings for the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: ethernet_settings_updated
    data:
      name: "Name of the Logical Interconnect"
      ethernetSettings:
        macRefreshInterval: 10

- name: Update the internal networks on the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: internal_networks_updated
    data:
      name: "Name of the Logical Interconnect"
      internalNetworks:
        - name: "Name of the Ethernet Network 1"
        - name: "Name of the Ethernet Network 2"
        - uri: "/rest/ethernet-networks/8a58cf7c-d49d-43b1-94ce-da5621be490c"

- name: Update the interconnect settings
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: settings_updated
    data:
      name: "Name of the Logical Interconnect"
      ethernetSettings:
        macRefreshInterval: 10

- name: Generate the forwarding information base dump file for the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: forwarding_information_base_generated
    data:
      name: "Name of the Logical Interconnect"  # could also be 'uri'

- name: Update the QoS aggregated configuration for the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: snmp_configuration_updated
    data:
      name: "Name of the Logical Interconnect"
      snmpConfiguration:
        enabled: True

- name: Update the port monitor configuration of the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: port_monitor_updated
    data:
      name: "Name of the Logical Interconnect"
      portMonitor:
        enablePortMonitor: False

- name: Update the configuration on the logical interconnect
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: configuration_updated
    data:
      name: "Name of the Logical Interconnect"

- name: Install a firmware to the logical interconnect, running the stage operation to upload the firmware
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: firmware_installed
    data:
      name: "Name of the Logical Interconnect"
      firmware:
        command: Stage
        spp: "filename"  # could also be sppUri: '/rest/firmware-drivers/<filename>'

- name: Updates the telemetry configuration of a logical interconnect.
  oneview_logical_interconnect:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    state: scopes_updated
    data:
      name: "Name of the Logical Interconnect"
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'

- debug: var=scope_uris

- name: Validates the bulk update from group operation and gets the consolidated inconsistency report
  oneview_logical_interconnect:
  config: "{{ config }}"
  state: bulk_inconsistency_validated
  data:
  logicalInterconnectUris:
    -  "/rest/logical-interconnects/d0432852-28a7-4060-ba49-57ca973ef6c2"
  delegate_to: localhost
  when: currentVersion >= '2000' and variant == 'Synergy'
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

from ansible.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError, compare


class LogicalInterconnectModule(OneViewModule):
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
        self.set_resource_object(self.oneview_client.logical_interconnects)

    def execute_module(self):

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

        changed, msg, ansible_facts = False, '', dict()

        if self.state == 'compliant':
            changed, msg, ansible_facts = self.__compliance()
        elif self.state == 'ethernet_settings_updated':
            changed, msg, ansible_facts = self.__update_ethernet_settings()
        elif self.state == 'internal_networks_updated':
            changed, msg, ansible_facts = self.__update_internal_networks()
        elif self.state == 'settings_updated':
            changed, msg, ansible_facts = self.__update_settings()
        elif self.state == 'forwarding_information_base_generated':
            changed, msg, ansible_facts = self.__generate_forwarding_information_base()
        elif self.state == 'qos_aggregated_configuration_updated':
            changed, msg, ansible_facts = self.__update_qos_configuration()
        elif self.state == 'snmp_configuration_updated':
            changed, msg, ansible_facts = self.__update_snmp_configuration()
        elif self.state == 'port_monitor_updated':
            changed, msg, ansible_facts = self.__update_port_monitor()
        elif self.state == 'configuration_updated':
            changed, msg, ansible_facts = self.__update_configuration()
        elif self.state == 'firmware_installed':
            changed, msg, ansible_facts = self.__install_firmware()
        elif self.state == 'telemetry_configuration_updated':
            changed, msg, ansible_facts = self.__update_telemetry_configuration()
        elif self.state == 'scopes_updated':
            changed, msg, ansible_facts = self.__update_scopes()
        elif self.state == 'bulk_inconsistency_validated':
                changed, msg, ansible_facts = self.__bulk_inconsistency_validate()

        if ansible_facts:
            result = dict(changed=changed, msg=msg, ansible_facts=ansible_facts)
        else:
            result = dict(changed=changed, msg=msg)

        return result

    def __compliance(self):
        li = self.current_resource.update_compliance()
        return True, self.MSG_CONSISTENT, dict(logical_interconnect=li)

    def __update_ethernet_settings(self):
        self.__validate_options('ethernetSettings', self.data)

        ethernet_settings_merged = self.current_resource.data['ethernetSettings'].copy()
        ethernet_settings_merged.update(self.data['ethernetSettings'])

        if compare(self.current_resource.data['ethernetSettings'], ethernet_settings_merged):
            return False, self.MSG_NO_CHANGES_PROVIDED, dict()
        else:
            li = self.current_resource.update_ethernet_settings(ethernet_settings_merged)
            return True, self.MSG_ETH_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __update_internal_networks(self):
        self.__validate_options('internalNetworks', self.data)

        networks = []
        for network_uri_or_name in self.data['internalNetworks']:
            if 'name' in network_uri_or_name:
                ethernet_network = self.__get_ethernet_network_by_name(
                    network_uri_or_name['name'])

                if not ethernet_network:
                    msg = self.MSG_ETH_NETWORK_NOT_FOUND + network_uri_or_name['name']
                    raise OneViewModuleResourceNotFound(msg)

                networks.append(ethernet_network['uri'])
            elif 'uri' in network_uri_or_name:
                networks.append(network_uri_or_name['uri'])

        li = self.current_resource.update_internal_networks(networks)

        return True, self.MSG_INTERNAL_NETWORKS_UPDATED, dict(logical_interconnect=li)

    def __update_settings(self):
        self.__validate_settings(self.data)

        ethernet_settings_merged = self.__merge_network_settings(
            'ethernetSettings', self.current_resource.data, self.data)
        fcoe_settings_merged = self.__merge_network_settings(
            'fcoeSettings', self.current_resource.data, self.data)

        if compare(self.current_resource.data['ethernetSettings'], ethernet_settings_merged) and \
                compare(self.current_resource.data['fcoeSettings'], fcoe_settings_merged):

            return False, self.MSG_NO_CHANGES_PROVIDED, dict(
                logical_interconnect=self.current_resource.data)
        else:
            settings = {
                'ethernetSettings': ethernet_settings_merged,
                'fcoeSettings': fcoe_settings_merged
            }
            li = self.current_resource.update_settings(settings)
            return True, self.MSG_SETTINGS_UPDATED, dict(logical_interconnect=li)

    def __generate_forwarding_information_base(self):
        result = self.current_resource.create_forwarding_information_base()
        return True, result.get('status'), dict(interconnect_fib=result)

    def __update_qos_configuration(self):
        self.__validate_options('qosConfiguration', self.data)

        qos_config = self.__get_qos_aggregated_configuration()
        qos_config_merged = self.__merge_options(self.data['qosConfiguration'], qos_config)

        if compare(qos_config_merged, qos_config):
            return False, self.MSG_NO_CHANGES_PROVIDED, dict()
        else:
            qos_config_updated = self.current_resource.update_qos_aggregated_configuration(
                qos_config_merged)

            return True, self.MSG_QOS_UPDATED, dict(qos_configuration=qos_config_updated)

    def __update_snmp_configuration(self):
        self.__validate_options('snmpConfiguration', self.data)

        snmp_config = self.__get_snmp_configuration()
        snmp_config_merged = self.__merge_options(self.data['snmpConfiguration'], snmp_config)

        if compare(snmp_config_merged, snmp_config):
            return False, self.MSG_NO_CHANGES_PROVIDED, None
        else:
            snmp_config_updated = self.current_resource.update_snmp_configuration(
                snmp_config_merged)

            return True, self.MSG_SNMP_UPDATED, dict(snmp_configuration=snmp_config_updated)

    def __update_port_monitor(self):
        self.__validate_options('portMonitor', self.data)

        monitor_config = self.__get_port_monitor_configuration()
        monitor_config_merged = self.__merge_options(self.data['portMonitor'], monitor_config)

        if compare(monitor_config_merged, monitor_config):
            return False, self.MSG_NO_CHANGES_PROVIDED, None
        else:
            monitor_config_updated = self.current_resource.update_port_monitor(
                monitor_config_merged)
            result = dict(port_monitor=monitor_config_updated)
            return True, self.MSG_PORT_MONITOR_UPDATED, result

    def __install_firmware(self):
        self.__validate_options('firmware', self.data)

        options = self.data['firmware'].copy()
        if 'spp' in options:
            options['sppUri'] = self.__build_firmware_uri(options.pop('spp'))

        firmware = self.current_resource.install_firmware(options)

        return True, self.MSG_FIRMWARE_INSTALLED, dict(li_firmware=firmware)

    def __update_configuration(self):
        result = self.current_resource.update_configuration()

        return True, self.MSG_CONFIGURATION_UPDATED, dict(logical_interconnect=result)

    def __update_telemetry_configuration(self):
        config = self.data.get('telemetryConfiguration')
        result = self.current_resource.update_telemetry_configurations(config)

        return True, self.MSG_TELEMETRY_CONFIGURATION_UPDATED, dict(
            telemetry_configuration=result.get('telemetryConfiguration'))

    def __update_scopes(self):

        scope_uris = self.data.pop('scopeUris', None)
        result = dict(changed=False,
                      msg=self.MSG_NO_CHANGES_PROVIDED,
                      ansible_facts=dict(scope_uris=self.current_resource.data))
        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'scope_uris', scope_uris)
            if result['changed']:
                result['msg'] = self.MSG_SCOPES_UPDATED

        result['ansible_facts']['scope_uris'] = result['ansible_facts']['scope_uris'].pop('scopeUris', None)

        return result['changed'], result['msg'], result['ansible_facts']

    def __bulk_inconsistency_validate(self):
        result = self.current_resource.bulk_inconsistency_validate(self.data)
        return True, result.get('allowUpdateFromGroup'), dict(bulk_inconsistency_validation_result=result)

    def __get_ethernet_network_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None

    def __get_qos_aggregated_configuration(self):
        return self.current_resource.get_qos_aggregated_configuration()

    def __get_snmp_configuration(self):
        return self.current_resource.get_snmp_configuration()

    def __get_port_monitor_configuration(self):
        return self.current_resource.get_port_monitor()

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
            raise OneViewModuleValueError(self.MSG_NO_OPTIONS_PROVIDED)

    def __validate_settings(self, data):
        if 'ethernetSettings' not in data and 'fcoeSettings' not in data:
            raise OneViewModuleValueError(self.MSG_NO_OPTIONS_PROVIDED)

    def __build_firmware_uri(self, filename):
        return '/rest/firmware-drivers/' + filename


def main():
    LogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
