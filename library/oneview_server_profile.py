#!/usr/bin/python
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_server_profile
short_description: Manage OneView Server Profile resources
description:
    - Manage the servers lifecycle with OneView Server Profiles. On C(present) state, it selects a server hardware
      automatically based on the server profile configuration if no server hardware was provided.
version_added: "2.5"
requirements:
    - hpOneView >= 5.0.0
author:
    - "Chakravarthy Racharla"
    - "Camila Balestrin (@balestrinc)"
    - "Mariana Kreisig (@marikrg)"
options:
  state:
    description:
      - Indicates the desired state for the Server Profile resource by the end of the playbook execution.
        C(present) will ensure data properties are compliant with OneView. This operation will power off the Server
        Hardware before configuring the Server Profile. After it completes, the Server Hardware is powered on.
        C(absent) will remove the resource from OneView, if it exists.
        C(compliant) will make the server profile compliant with its server profile template, when this option was
        specified. If there are Offline updates, the Server Hardware is turned off before remediate compliance issues
        and turned on after that.
    default: present
    choices: ['present', 'absent', 'compliant']
  data:
    description:
      - List with Server Profile properties.
    required: true
  auto_assign_server_hardware:
    description:
      - Bool indicating whether or not a Server Hardware should be automatically retrieved and assigned to the Server Profile.
        When set to true, creates and updates try to ensure that an available Server Hardware is assigned to the Server Profile.
        When set to false, if no Server Hardware is specified during creation, the profile is created as 'unassigned'. If the
        profile already has a Server Hardware assigned to it and a serverHardwareName or serverHardwareUri is specified as None,
        the Server Profile will have its Server Hardware unassigned.
    default: True
    choices: [True, False]
  params:
    description:
      - Dict with query parameters.
    required: False
notes:
    - "For the following data, you can provide either a name or a URI: enclosureGroupName or enclosureGroupUri,
       osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the
       connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or
       volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the
       volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri,
       firmwareBaselineName or firmwareBaselineUri (on the firmware), sasLogicalJBODName or sasLogicalJBODUri (on
       the sasLogicalJBODs list) and initialScopeNames or initialScopeUris"
    - "If you define the volumeUri as null in the volumeAttachments list, it will be understood that the volume
       does not exist, so it will be created along with the server profile. Be warned that every time this option
       is executed it will always be understood that a new volume needs to be created, so this will not be idempotent.
       It is strongly recommended to ensure volumes with Ansible and then assign them to the desired server profile.
       does not exists, so it will be created along with the server profile"

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Server Profile from a Server Profile Template with automatically selected hardware
  oneview_server_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: present
    data:
        name: Web-Server-L2
        # You can choose either server_template or serverProfileTemplateUri to inform the Server Profile Template
        # serverProfileTemplateUri: "/rest/server-profile-templates/31ade62c-2112-40a0-935c-2f9450a75198"
        server_template: Compute-node-template
        # You can inform a server_hardware or a serverHardwareUri. If any hardware was informed, it will try
        # get one available automatically
        # server_hardware: Encl1, bay 12
        # serverHardwareUri: /rest/server-hardware/30303437-3933-4753-4831-30335835524E

        # You can choose either serverHardwareTypeUri or serverHardwareTypeName to inform the Server Hardware Type
        # serverHardwareTypeUri: /rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C
        # serverHardwareTypeName: SY 480 Gen9 1
        # You can choose either enclosureName or enclosureUri to inform the Enclosure
        # enclosureUri: /rest/enclosures/09SGH100Z6J1
        enclosureName: 0000A66102
        sanStorage:
          hostOSType: Windows 2012 / WS2012 R2
          manageSanStorage: true
          volumeAttachments:
            - id: 1
              # You can choose either volumeName or volumeUri to inform the Volumes
              # volumeName: DemoVolume001
              volumeUri: /rest/storage-volumes/BCAB376E-DA2E-450D-B053-0A9AE7E5114C
              # You can choose either volumeStoragePoolUri or volumeStoragePoolName to inform the Volume Storage Pool
              # volumeStoragePoolName: FST_CPG2
              volumeStoragePoolUri: /rest/storage-pools/30303437-3933-4753-4831-30335835524E
              # You can choose either volumeStorageSystemUri or volumeStorageSystemName to inform the Volume Storage
              # System
              # volumeStorageSystemName: ThreePAR7200-2127
              volumeStorageSystemUri: /rest/storage-systems/TXQ1000307
              lunType: 'Auto'
              storagePaths:
                - isEnabled: true
                  connectionId: 1
                  storageTargetType: Auto
                - isEnabled: true
                  connectionId: 2
                  storageTargetType: Auto
  delegate_to: localhost
- debug: var=server_profile
- debug: var=serial_number
- debug: var=server_hardware
- debug: var=compliance_preview
- debug: var=created

- name: Create a Server Profile with connections
  oneview_server_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    data:
      name: server-profile-with-connections
      connectionSettings:
        connections:
          - id: 1
            name: connection1
            functionType: Ethernet
            portId: Auto
            requestedMbps: 2500
            networkName: eth-demo
  delegate_to: localhost

- name: Unassign Server Hardware from Server Profile
  oneview_server_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    # This is required for unassigning a SH, or creating a SP and not auto-assigning a SH
    auto_assign_server_hardware: False
    data:
      name: server-profile-with-sh
      # Specify a blank serverHardwareName or serverHardwareUri when auto_assign_server_hardware is False to unassign a SH
      serverHardwareName:
  delegate_to: localhost

- name : Remediate compliance issues
  oneview_server_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: compliant
    data:
        name: Web-Server-L2
  delegate_to: localhost

- name : Remove the server profile
  oneview_server_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: absent
    data:
        name: Web-Server-L2
  delegate_to: localhost
'''

RETURN = '''
server_profile:
    description: Has the OneView facts about the Server Profile.
    returned: On states 'present' and 'compliant'.
    type: dict
serial_number:
    description: Has the Server Profile serial number.
    returned: On states 'present' and 'compliant'.
    type: dict
server_hardware:
    description: Has the OneView facts about the Server Hardware.
    returned: On states 'present' and 'compliant'.
    type: dict
compliance_preview:
    description:
        Has the OneView facts about the manual and automatic updates required to make the server profile
        consistent with its template.
    returned: On states 'present' and 'compliant'.
    type: dict
created:
    description: Indicates if the Server Profile was created.
    returned: On states 'present' and 'compliant'.
    type: bool
'''

import time

from copy import deepcopy

from ansible.module_utils.oneview import (OneViewModule,
                                          ServerProfileReplaceNamesByUris,
                                          OneViewModuleValueError,
                                          ServerProfileMerger,
                                          OneViewModuleTaskError,
                                          SPKeys,
                                          OneViewModuleException,
                                          compare)


class ServerProfileModule(OneViewModule):
    ASSIGN_HARDWARE_ERROR_CODES = ['AssignProfileToDeviceBayError',
                                   'EnclosureBayUnavailableForProfile',
                                   'ProfileAlreadyExistsInServer']

    MSG_TEMPLATE_NOT_FOUND = "Informed Server Profile Template '{}' not found"
    MSG_HARDWARE_NOT_FOUND = "Informed Server Hardware '{}' not found"
    MSG_CREATED = "Server Profile created."
    MSG_ALREADY_PRESENT = 'Server Profile is already present.'
    MSG_UPDATED = 'Server profile updated'
    MSG_DELETED = 'Deleted profile'
    MSG_ALREADY_ABSENT = 'Nothing do.'
    MSG_REMEDIATED_COMPLIANCE = "Remediated compliance issues"
    MSG_ALREADY_COMPLIANT = "Server Profile is already compliant."
    MSG_NOT_FOUND = "Server Profile is required for this operation."
    MSG_ERROR_ALLOCATE_SERVER_HARDWARE = 'Could not allocate server hardware'
    MSG_MAKE_COMPLIANT_NOT_SUPPORTED = "Update from template is not supported for server profile '{}' because it is" \
                                       " not associated with a server profile template."

    CONCURRENCY_FAILOVER_RETRIES = 25

    argument_spec = dict(
        state=dict(choices=['present', 'absent', 'compliant'], default='present'),
        data=dict(type='dict', required=True),
        params=dict(type='dict', required=False),
        auto_assign_server_hardware=dict(type='bool', default=True)
    )

    def __init__(self):
        super(ServerProfileModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                  validate_etag_support=True)

        self.set_resource_object(self.oneview_client.server_profiles)

        self.server_profile_templates = self.oneview_client.server_profile_templates
        self.server_hardware = self.oneview_client.server_hardware
        self.os_deployment_plans = self.oneview_client.os_deployment_plans
        self.server_template = None

    def execute_module(self):
        self.auto_assign_server_hardware = self.module.params.get('auto_assign_server_hardware')
        params = self.module.params.get("params")
        self.params = params if params else {}

        if self.state == 'present':
            created, changed, msg, server_profile = self.__present()
            facts = self.__gather_facts()
            facts['created'] = created
            return dict(
                changed=changed, msg=msg, ansible_facts=facts
            )
        elif self.state == 'absent':
            changed, msg = self.__delete_profile()
            return dict(
                changed=changed, msg=msg
            )
        elif self.state == "compliant":
            changed, msg, server_profile = self.__make_compliant()
            return dict(
                changed=changed, msg=msg, ansible_facts=self.__gather_facts()
            )

    def __present(self):
        server_template_name = self.data.pop('serverProfileTemplateName', '')
        server_hardware_name = self.data.pop('serverHardwareName', '')
        changed = False
        created = False

        ServerProfileReplaceNamesByUris().replace(self.oneview_client, self.data)

        if server_hardware_name:
            selected_server_hardware = self.__get_server_hardware_by_name(server_hardware_name)
            if not selected_server_hardware:
                raise OneViewModuleValueError(self.MSG_HARDWARE_NOT_FOUND.format(server_hardware_name))
            self.data['serverHardwareUri'] = selected_server_hardware['uri']

        if server_template_name:
            self.server_template = self.server_profile_templates.get_by_name(server_template_name)
            if not self.server_template:
                raise OneViewModuleValueError(self.MSG_TEMPLATE_NOT_FOUND.format(server_template_name))
            self.data['serverProfileTemplateUri'] = self.server_template.data['uri']
        elif self.data.get('serverProfileTemplateUri'):
            self.server_template = self.server_profile_templates.get_by_uri(self.data['serverProfileTemplateUri'])

        if not self.current_resource:
            self.current_resource = self.__create_profile()
            changed = True
            created = True
            msg = self.MSG_CREATED
        else:
            # This allows unassigning a profile if a SH key is specifically passed in as None
            if not self.auto_assign_server_hardware:
                server_hardware_uri_exists = False
                if 'serverHardwareUri' in self.module.params['data'].keys() or 'serverHardwareName' in self.module.params['data'].keys():
                    server_hardware_uri_exists = True
                if self.data.get('serverHardwareUri') is None and server_hardware_uri_exists:
                    self.data['serverHardwareUri'] = None

            # Auto assigns a Server Hardware to Server Profile if auto_assign_server_hardware is True and no SH uris/enclosure uri and bay exist
            if not self.current_resource.data.get('serverHardwareUri') and not self.data.get('serverHardwareUri') and self.auto_assign_server_hardware \
                and not self.current_resource.data.get('enclosureUri') and not self.current_resource.data.get('enclosureBay') \
                    and not self.data.get('enclosureUri') and not self.data.get('enclosureBay'):
                self.data['serverHardwareUri'] = self._auto_assign_server_profile()

            merged_data = ServerProfileMerger().merge_data(self.current_resource.data, self.data)

            self.__validations_for_os_custom_attributes(merged_data, self.current_resource.data)

            if not compare(self.current_resource.data, merged_data):
                self.__update_server_profile(merged_data)
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return created, changed, msg, self.current_resource.data

    # Removes .mac entries from resource os_custom_attributes if no .mac passed into data params.
    # Swaps True values for 'true' string, and False values for 'false' string to avoid common user errors.
    def __validations_for_os_custom_attributes(self, merged_data, resource):
        if self.data.get('osDeploymentSettings') is None or resource.get('osDeploymentSettings') is None:
            return
        elif self.data.get('osDeploymentSettings', {}).get('osCustomAttributes') is None:
            return
        elif resource.get('osDeploymentSettings', {}).get('osCustomAttributes') is None:
            return

        attributes_merged = merged_data.get('osDeploymentSettings', {}).get('osCustomAttributes', None)
        attributes_resource = resource.get('osDeploymentSettings', {}).get('osCustomAttributes', None)

        dp_uri = resource.get('osDeploymentSettings', {}).get('osDeploymentPlanUri', None)
        dp = self.os_deployment_plans.get_by_uri(dp_uri)
        nics = []
        if dp:
            for parameter in dp.data['additionalParameters']:
                if parameter['caType'] == 'nic':
                    nics.append(parameter['name'])

        mac_positions_in_merged_data = self.__find_in_array_of_hashes(attributes_merged, '.mac', -4)
        mac_positions_in_resource = self.__find_in_array_of_hashes(attributes_resource, '.mac', -4)

        if not mac_positions_in_merged_data:
            for index in sorted(mac_positions_in_resource, reverse=True):
                if attributes_resource[index].get('name').split('.')[0] in nics:
                    del attributes_resource[index]

        if attributes_merged:
            for attribute in attributes_merged:
                if attribute['value'] is True:
                    attribute['value'] = 'true'
                elif attribute['value'] is False:
                    attribute['value'] = 'false'

    # Searches for a key or suffix of a key inside an array of hashes. The search looks for {'name': <key>} pairs
    # inside the array.
    # Returns an array containing the positions of matches.
    def __find_in_array_of_hashes(self, array_of_hashes, key, part=None):
        matches = []
        for position in range(0, len(array_of_hashes)):
            attribute_name = array_of_hashes[position].get('name', None)
            if attribute_name and attribute_name[part:] == key:
                matches.append(position)
        return matches

    def __update_server_profile(self, profile_with_updates):
        self.module.log(msg="Updating Server Profile")

        # These removes are necessary in case SH associated to the SP is being changed
        if self.data.get('enclosureUri') is None:
            profile_with_updates.pop('enclosureUri', None)
        if self.data.get('enclosureBay') is None:
            profile_with_updates.pop('enclosureBay', None)

        # Some specific SP operations require the SH to be powered off. This method attempts
        # the update, and in case of failure mentioning powering off the SH, a Power off on
        # the SH is attempted, followed by the update operation again and a Power On.
        try:
            self.current_resource.update(profile_with_updates)
        except OneViewModuleException as exception:
            error_msg = '; '.join(str(e) for e in exception.args)
            power_on_msg = 'Some server profile attributes cannot be changed while the server hardware is powered on.'
            if power_on_msg in error_msg:
                self.module.log("Update failed due to powered on Server Hardware. Powering off before retrying.")
                time.sleep(10)  # sleep timer to avoid timing issues after update operation failed

                # When reassigning Server Hardwares, both the original and the new SH should be set to OFF
                self.__set_server_hardware_power_state(self.current_resource.data['serverHardwareUri'], 'Off')
                self.__set_server_hardware_power_state(profile_with_updates['serverHardwareUri'], 'Off')

                self.module.log("Retrying update operation after server power off")
                self.current_resource.update(profile_with_updates)

                self.module.log("Powering on the server hardware after update")
                self.__set_server_hardware_power_state(self.current_resource.data['serverHardwareUri'], 'On')
            else:
                raise OneViewModuleException(error_msg)

    def __create_profile(self):
        tries = 0
        self.__remove_inconsistent_data()
        while tries < self.CONCURRENCY_FAILOVER_RETRIES:
            try:
                tries += 1

                server_hardware_uri = self._auto_assign_server_profile()

                if server_hardware_uri:
                    self.module.log(msg="Power off the Server Hardware before create the Server Profile")
                    self.__set_server_hardware_power_state(server_hardware_uri, 'Off')

                # Build the data to create a new server profile based on a template if informed
                server_profile = self.__build_new_profile_data(server_hardware_uri)

                self.module.log(msg="Request Server Profile creation")
                return self.resource_client.create(server_profile, **self.params)

            except OneViewModuleTaskError as task_error:
                self.module.log("Error code: {} Message: {}".format(str(task_error.error_code), str(task_error.msg)))
                if task_error.error_code in self.ASSIGN_HARDWARE_ERROR_CODES:
                    # if this is because the server is already assigned, someone grabbed it before we assigned,
                    # ignore and try again
                    # This waiting time was chosen empirically and it could differ according to the hardware.
                    time.sleep(10)
                else:
                    raise task_error

        raise OneViewModuleException(self.MSG_ERROR_ALLOCATE_SERVER_HARDWARE)

    def __build_new_profile_data(self, server_hardware_uri):
        server_profile_data = deepcopy(self.data)

        if self.server_template:
            self.module.log(msg="Get new Profile from template")

            server_profile_template = self.server_template.get_new_profile()

            server_profile_template.update(server_profile_data)
            server_profile_data = server_profile_template

        if server_hardware_uri:
            server_profile_data['serverHardwareUri'] = server_hardware_uri

        return server_profile_data

    def __remove_inconsistent_data(self):
        def is_virtual_or_physical(defined_type):
            return defined_type == 'Virtual' or defined_type == 'Physical'

        # Remove the MAC from connections when MAC type is Virtual or Physical
        mac_type = self.data.get(SPKeys.MAC_TYPE, None)
        if mac_type and is_virtual_or_physical(mac_type):
            for conn in self.data.get(SPKeys.CONNECTIONS) or []:
                conn.pop(SPKeys.MAC, None)

        # Remove the UUID when Serial Number Type is Virtual or Physical
        serial_number_type = self.data.get(SPKeys.SERIAL_NUMBER_TYPE, None)
        if serial_number_type and is_virtual_or_physical(serial_number_type):
            self.data.pop(SPKeys.UUID, None)
            self.data.pop(SPKeys.SERIAL_NUMBER, None)

        # Remove the WWPN and WWNN when WWPN Type is Virtual or Physical
        for conn in self.data.get(SPKeys.CONNECTIONS) or []:
            wwpn_type = conn.get(SPKeys.WWPN_TYPE, None)
            if is_virtual_or_physical(wwpn_type):
                conn.pop(SPKeys.WWNN, None)
                conn.pop(SPKeys.WWPN, None)

        # Remove the driveNumber from the Controllers Drives
        if SPKeys.LOCAL_STORAGE in self.data and self.data[SPKeys.LOCAL_STORAGE]:
            for controller in self.data[SPKeys.LOCAL_STORAGE].get(SPKeys.CONTROLLERS) or []:
                for drive in controller.get(SPKeys.LOGICAL_DRIVES) or []:
                    drive.pop(SPKeys.DRIVE_NUMBER, None)

        # Remove the Lun when Lun Type from SAN Storage Volume is Auto
        if SPKeys.SAN in self.data and self.data[SPKeys.SAN]:
            if SPKeys.VOLUMES in self.data[SPKeys.SAN]:
                for volume in self.data[SPKeys.SAN].get(SPKeys.VOLUMES) or []:
                    if volume.get(SPKeys.LUN_TYPE) == 'Auto':
                        volume.pop(SPKeys.LUN, None)

    def __get_available_server_hardware_uri(self):
        scope_uris = self.data.get('initialScopeUris', [])
        scope_uri = '%20OR%20'.join(scope_uris)

        if self.server_template:
            enclosure_group = self.server_template.data.get('enclosureGroupUri', '')
            server_hardware_type = self.server_template.data.get('serverHardwareTypeUri', '')
        else:
            enclosure_group = self.data.get('enclosureGroupUri', '')
            server_hardware_type = self.data.get('serverHardwareTypeUri', '')

        # This change is made to handle auto assign for rack mount servers, because there is no EG for rack servers
        if enclosure_group is None:
            enclosure_group = ''

        if not enclosure_group and not server_hardware_type:
            return

        self.module.log(msg="Finding an available server hardware")
        if self.oneview_client.api_version >= 1600:
            # To get available targets for scoped user
            if scope_uri:
                available_server_hardware = self.resource_client.get_available_targets(
                    enclosureGroupUri=enclosure_group,
                    serverHardwareTypeUri=server_hardware_type,
                    scopeUris=scope_uri)['targets']
            else:
                available_server_hardware = self.resource_client.get_available_targets(
                    enclosureGroupUri=enclosure_group,
                    serverHardwareTypeUri=server_hardware_type)['targets']
        else:
            available_server_hardware = self.resource_client.get_available_servers(
                enclosureGroupUri=enclosure_group,
                serverHardwareTypeUri=server_hardware_type)

        # targets will list empty bays. We need to pick one that has a server
        index = 0
        server_hardware_uri = None
        while not server_hardware_uri and index < len(available_server_hardware):
            server_hardware_uri = available_server_hardware[index]['serverHardwareUri']
            index = index + 1

        self.module.log(msg="Found available server hardware: '{}'".format(server_hardware_uri))
        return server_hardware_uri

    def __delete_profile(self):
        if not self.current_resource:
            return False, self.MSG_ALREADY_ABSENT

        if self.current_resource.data.get('serverHardwareUri'):
            self.__set_server_hardware_power_state(self.current_resource.data['serverHardwareUri'],
                                                   'Off')

        self.current_resource.delete()
        return True, self.MSG_DELETED

    def __make_compliant(self):

        changed = False
        msg = self.MSG_ALREADY_COMPLIANT

        if not self.current_resource.data.get('serverProfileTemplateUri'):
            self.module.log("Make the Server Profile compliant is not supported for this profile")
            self.module.fail_json(msg=self.MSG_MAKE_COMPLIANT_NOT_SUPPORTED.format(
                self.current_resource.data['name']))

        elif self.current_resource.data['templateCompliance'] != 'Compliant':
            self.module.log(
                "Get the preview of manual and automatic updates required to make the server profile consistent "
                "with its template.")
            compliance_preview = self.current_resource.get_compliance_preview()

            self.module.log(str(compliance_preview))

            is_offline_update = compliance_preview.get('isOnlineUpdate') is False

            if is_offline_update:
                self.module.log(msg="Power off the server hardware before update from template")
                self.__set_server_hardware_power_state(
                    self.current_resource.data['serverHardwareUri'], 'Off')

            self.module.log(msg="Updating from template")

            self.current_resource.patch('replace', '/templateCompliance', 'Compliant')

            if is_offline_update:
                self.module.log(msg="Power on the server hardware after update from template")
                self.__set_server_hardware_power_state(
                    self.current_resource.data['serverHardwareUri'], 'On')

            changed = True
            msg = self.MSG_REMEDIATED_COMPLIANCE

        return changed, msg, self.current_resource.data

    def __gather_facts(self):

        server_hardware = None
        if self.current_resource.data.get('serverHardwareUri'):
            server_hardware_by_uri = self.server_hardware.get_by_uri(
                self.current_resource.data['serverHardwareUri'])
            if server_hardware_by_uri:
                server_hardware = server_hardware_by_uri.data

        compliance_preview = None
        if self.current_resource.data.get('serverProfileTemplateUri'):
            compliance_preview = self.current_resource.get_compliance_preview()

        facts = {
            'serial_number': self.current_resource.data.get('serialNumber'),
            'server_profile': self.current_resource.data,
            'server_hardware': server_hardware,
            'compliance_preview': compliance_preview,
            'created': False
        }

        return facts

    def __get_server_hardware_by_name(self, server_hardware_name):
        server_hardwares = self.server_hardware.get_by('name', server_hardware_name)
        return server_hardwares[0] if server_hardwares else None

    def __set_server_hardware_power_state(self, hardware_uri, power_state='On'):
        if hardware_uri is not None:
            hardware = self.server_hardware.get_by_uri(hardware_uri)
            if power_state in ['On']:
                hardware.update_power_state(
                    dict(powerState='On', powerControl='MomentaryPress'))
            else:
                hardware.update_power_state(
                    dict(powerState='Off', powerControl='PressAndHold'))

    def _auto_assign_server_profile(self):
        server_hardware_uri = self.data.get('serverHardwareUri')
        enclosure_uri = self.data.get('enclosureUri')
        enclosure_bay = self.data.get('enclosureBay')
        if not server_hardware_uri and self.auto_assign_server_hardware and not enclosure_uri and not enclosure_bay:
            # find servers that have no profile, matching Server hardware type and enclosure group
            self.module.log(msg="Get an available Server Hardware for the Profile")
            server_hardware_uri = self.__get_available_server_hardware_uri()

        return server_hardware_uri


def main():
    ServerProfileModule().run()


if __name__ == '__main__':
    main()
