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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_server_profile
short_description: Manage OneView Server Profile resources.
description:
    - Manage the servers lifecycle with OneView Server Profiles. On C(present) state, it selects a server hardware
      automatically based on the server profile configuration if no server hardware was provided.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 4.0.0"
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
notes:
    - "For the following data, you can provide either a name or a URI: enclosureGroupName or enclosureGroupUri,
       osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the
       connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or
       volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the
       volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri,
       firmwareBaselineName or firmwareBaselineUri (on the firmware), and sasLogicalJBODName or sasLogicalJBODUri (on
       the sasLogicalJBODs list)"
    - "If you define the volumeUri as null in the volumeAttachments list, it will be understood that the volume
       does not exist, so it will be created along with the server profile. Be warned that everytime this option
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
    config: "{{ config }}"
    state: "present"
    data:
        name: Web-Server-L2
        # You can choose either server_template or serverProfileTemplateUri to inform the Server Profile Template
        # serverProfileTemplateUri: "/rest/server-profile-templates/31ade62c-2112-40a0-935c-2f9450a75198"
        server_template: Compute-node-template
        # You can inform a server_hardware or a serverHardwareUri. If any hardware was informed, it will try
        # get one available automatically
        # server_hardware: "Encl1, bay 12"
        # serverHardwareUri: "/rest/server-hardware/30303437-3933-4753-4831-30335835524E"

        # You can choose either serverHardwareTypeUri or serverHardwareTypeName to inform the Server Hardware Type
        # serverHardwareTypeUri: '/rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C'
        # serverHardwareTypeName: 'SY 480 Gen9 1'
        # You can choose either enclosureName or enclosureUri to inform the Enclosure
        # enclosureUri: '/rest/enclosures/09SGH100Z6J1'
        enclosureName: '0000A66102'
        sanStorage:
          hostOSType: 'Windows 2012 / WS2012 R2'
          manageSanStorage: true
          volumeAttachments:
            - id: 1
              # You can choose either volumeName or volumeUri to inform the Volumes
              # volumeName: 'DemoVolume001'
              volumeUri: '/rest/storage-volumes/BCAB376E-DA2E-450D-B053-0A9AE7E5114C'
              # You can choose either volumeStoragePoolUri or volumeStoragePoolName to inform the Volume Storage Pool
              # volumeStoragePoolName: 'FST_CPG2'
              volumeStoragePoolUri: '/rest/storage-pools/30303437-3933-4753-4831-30335835524E'
              # You can choose either volumeStorageSystemUri or volumeStorageSystemName to inform the Volume Storage
              # System
              # volumeStorageSystemName: 'ThreePAR7200-2127'
              volumeStorageSystemUri: '/rest/storage-systems/TXQ1000307'
              lunType: 'Auto'
              storagePaths:
                - isEnabled: true
                  connectionId: 1
                  storageTargetType: 'Auto'
                - isEnabled: true
                  connectionId: 2
                  storageTargetType: 'Auto'
- debug: var=server_profile
- debug: var=serial_number
- debug: var=server_hardware
- debug: var=compliance_preview
- debug: var=created

- name: Create a Server Profile with connections
  oneview_server_profile:
    config: "{{ config }}"
    data:
      name: "server-profile-with-connections"
      connections:
        - id: 1
          name: connection1
          functionType: Ethernet
          portId: Auto
          requestedMbps: 2500
          networkName: eth-demo
  delegate_to: localhost

- name : Remediate compliance issues
  oneview_server_profile:
     config: "{{ config }}"
     state: "compliant"
     data:
        name: Web-Server-L2

- name : Remove the server profile
  oneview_server_profile:
    config: "{{ config }}"
    state: "absent"
    data:
        name: Web-Server-L2
'''

RETURN = '''
server_profile:
    description: Has the OneView facts about the Server Profile.
    returned: On states 'present' and 'compliant'.
    type: complex
serial_number:
    description: Has the Server Profile serial number.
    returned: On states 'present' and 'compliant'.
    type: complex
server_hardware:
    description: Has the OneView facts about the Server Hardware.
    returned: On states 'present' and 'compliant'.
    type: complex
compliance_preview:
    description:
        Has the OneView facts about the manual and automatic updates required to make the server profile
        consistent with its template.
    returned: On states 'present' and 'compliant'.
    type: complex
created:
    description: Indicates if the Server Profile was created.
    returned: On states 'present' and 'compliant'.
    type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import time
from module_utils.oneview import (OneViewModuleBase,
                                  ServerProfileReplaceNamesByUris,
                                  HPOneViewValueError,
                                  ServerProfileMerger,
                                  ResourceComparator,
                                  HPOneViewTaskError,
                                  SPKeys,
                                  HPOneViewException)
from copy import deepcopy

# To activate logs, setup the environment var LOGFILE
# e.g.: export LOGFILE=/tmp/ansible-oneview.log
logger = OneViewModuleBase.get_logger(__file__)


class ServerProfileModule(OneViewModuleBase):
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
        state=dict(
            required=False,
            choices=[
                'present',
                'absent',
                'compliant'
            ],
            default='present'
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(ServerProfileModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                  validate_etag_support=True)

    def execute_module(self):
        data = deepcopy(self.data)
        server_profile_name = data.get('name')

        server_profile = self.oneview_client.server_profiles.get_by_name(server_profile_name)

        if self.state == 'present':
            created, changed, msg, server_profile = self.__present(data, server_profile)
            facts = self.__gather_facts(server_profile)
            facts['created'] = created
            return dict(
                changed=changed, msg=msg, ansible_facts=facts
            )
        elif self.state == 'absent':
            changed, msg = self.__delete_profile(server_profile)
            return dict(
                changed=changed, msg=msg
            )
        elif self.state == "compliant":
            changed, msg, server_profile = self.__make_compliant(server_profile)
            return dict(
                changed=changed, msg=msg, ansible_facts=self.__gather_facts(server_profile)
            )

    def __present(self, data, resource):

        server_template_name = data.pop('server_template', '')
        server_hardware_name = data.pop('server_hardware', '')
        server_template = None
        changed = False
        created = False

        ServerProfileReplaceNamesByUris().replace(self.oneview_client, data)

        if server_hardware_name:
            selected_server_hardware = self.__get_server_hardware_by_name(server_hardware_name)
            if not selected_server_hardware:
                raise HPOneViewValueError(self.MSG_HARDWARE_NOT_FOUND.format(server_hardware_name))
            data['serverHardwareUri'] = selected_server_hardware['uri']

        if server_template_name:
            server_template = self.oneview_client.server_profile_templates.get_by_name(server_template_name)
            if not server_template:
                raise HPOneViewValueError(self.MSG_TEMPLATE_NOT_FOUND.format(server_template_name))
            data['serverProfileTemplateUri'] = server_template['uri']
        elif data.get('serverProfileTemplateUri'):
            server_template = self.oneview_client.server_profile_templates.get(data['serverProfileTemplateUri'])

        if not resource:
            resource = self.__create_profile(data, server_template)
            changed = True
            created = True
            msg = self.MSG_CREATED
        else:
            merged_data = ServerProfileMerger().merge_data(resource, data)

            self.__validations_for_os_custom_attributes(data, merged_data, resource)

            if not ResourceComparator.compare(resource, merged_data):
                resource = self.__update_server_profile(merged_data, resource)
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return created, changed, msg, resource

    # Removes .mac entries from resource os_custom_attributes if no .mac passed into data params.
    # Swaps True values for 'true' string, and False values for 'false' string to avoid common user errors.
    def __validations_for_os_custom_attributes(self, data, merged_data, resource):
        if not data.get('osDeploymentSettings', {}).get('osCustomAttributes', None):
            return False
        attributes_merged = merged_data.get('osDeploymentSettings', {}).get('osCustomAttributes', None)
        attributes_resource = resource.get('osDeploymentSettings', {}).get('osCustomAttributes', None)
        dp_uri = resource.get('osDeploymentSettings', {}).get('osDeploymentPlanUri', None)
        dp = self.oneview_client.os_deployment_plans.get(dp_uri)
        nics = []
        if dp:
            for parameter in dp['additionalParameters']:
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

    def __update_server_profile(self, profile_with_updates, original_profile):
        logger.debug(msg="Updating Server Profile")

        # These removes are necessary in case SH associated to the SP is being changed
        if self.data.get('enclosureUri') is None:
            profile_with_updates.pop('enclosureUri', None)
        if self.data.get('enclosureBay') is None:
            profile_with_updates.pop('enclosureBay', None)

        # Some specific SP operations require the SH to be powered off. This method attempts
        # the update, and in case of failure mentioning powering off the SH, a Power off on
        # the SH is attempted, followed by the update operation again and a Power On.
        try:
            resource = self.oneview_client.server_profiles.update(profile_with_updates, profile_with_updates['uri'])
        except HPOneViewException as exception:
            error_msg = '; '.join(to_native(e) for e in exception.args)
            power_on_msg = 'Some server profile attributes cannot be changed while the server hardware is powered on.'
            if power_on_msg in error_msg:
                time.sleep(10)
                logger.debug("Update failed due to powered on Server Hardware. Powering off before retrying.")
                self.__set_server_hardware_power_state(original_profile['serverHardwareUri'], 'Off')

                logger.debug("Retrying update operation after server power off")
                resource = self.oneview_client.server_profiles.update(profile_with_updates,
                                                                      profile_with_updates['uri'])

                logger.debug("Powering on the server hardware after update")
                self.__set_server_hardware_power_state(profile_with_updates['serverHardwareUri'], 'On')
            else:
                raise HPOneViewException(error_msg)
        return resource

    def __create_profile(self, data, server_profile_template):
        tries = 0
        self.__remove_inconsistent_data(data)

        while tries < self.CONCURRENCY_FAILOVER_RETRIES:
            try:
                tries += 1

                server_hardware_uri = data.get('serverHardwareUri')

                if not server_hardware_uri:
                    # find servers that have no profile, mathing Server hardware type and enclosure group
                    logger.debug(msg="Get an available Server Hardware for the Profile")
                    server_hardware_uri = self.__get_available_server_hardware_uri(data, server_profile_template)

                if server_hardware_uri:
                    logger.debug(msg="Power off the Server Hardware before create the Server Profile")
                    self.__set_server_hardware_power_state(server_hardware_uri, 'Off')

                # Build the data to create a new server profile based on a template if informed
                server_profile = self.__build_new_profile_data(data, server_profile_template, server_hardware_uri)

                logger.debug(msg="Request Server Profile creation")
                return self.oneview_client.server_profiles.create(server_profile)

            except HPOneViewTaskError as task_error:
                logger.exception("Error code: {} Message: {}".format(str(task_error.error_code), str(task_error.msg)))
                if task_error.error_code in self.ASSIGN_HARDWARE_ERROR_CODES:
                    # if this is because the server is already assigned, someone grabbed it before we assigned,
                    # ignore and try again
                    # This waiting time was chosen empirically and it could differ according to the hardware.
                    time.sleep(10)
                else:
                    raise task_error

        raise HPOneViewException(self.MSG_ERROR_ALLOCATE_SERVER_HARDWARE)

    def __build_new_profile_data(self, data, server_template, server_hardware_uri):

        server_profile_data = deepcopy(data)

        if server_template:
            logger.debug(msg="Get new Profile from template")

            server_profile_template = self.oneview_client.server_profile_templates.get_new_profile(
                server_template['uri'])

            server_profile_template.update(server_profile_data)
            server_profile_data = server_profile_template

        if server_hardware_uri:
            server_profile_data['serverHardwareUri'] = server_hardware_uri

        return server_profile_data

    def __remove_inconsistent_data(self, data):
        def is_virtual_or_physical(defined_type):
            return defined_type == 'Virtual' or defined_type == 'Physical'

        # Remove the MAC from connections when MAC type is Virtual or Physical
        mac_type = data.get(SPKeys.MAC_TYPE, None)
        if mac_type and is_virtual_or_physical(mac_type):
            for conn in data.get(SPKeys.CONNECTIONS) or []:
                conn.pop(SPKeys.MAC, None)

        # Remove the UUID when Serial Number Type is Virtual or Physical
        serial_number_type = data.get(SPKeys.SERIAL_NUMBER_TYPE, None)
        if serial_number_type and is_virtual_or_physical(serial_number_type):
            data.pop(SPKeys.UUID, None)
            data.pop(SPKeys.SERIAL_NUMBER, None)

        # Remove the WWPN and WWNN when WWPN Type is Virtual or Physical
        for conn in data.get(SPKeys.CONNECTIONS) or []:
            wwpn_type = conn.get(SPKeys.WWPN_TYPE, None)
            if is_virtual_or_physical(wwpn_type):
                conn.pop(SPKeys.WWNN, None)
                conn.pop(SPKeys.WWPN, None)

        # Remove the driveNumber from the Controllers Drives
        if SPKeys.LOCAL_STORAGE in data and data[SPKeys.LOCAL_STORAGE]:
            for controller in data[SPKeys.LOCAL_STORAGE].get(SPKeys.CONTROLLERS) or []:
                for drive in controller.get(SPKeys.LOGICAL_DRIVES) or []:
                    drive.pop(SPKeys.DRIVE_NUMBER, None)

        # Remove the Lun when Lun Type from SAN Storage Volume is Auto
        if SPKeys.SAN in data and data[SPKeys.SAN]:
            if SPKeys.VOLUMES in data[SPKeys.SAN]:
                for volume in data[SPKeys.SAN].get(SPKeys.VOLUMES) or []:
                    if volume.get(SPKeys.LUN_TYPE) == 'Auto':
                        volume.pop(SPKeys.LUN, None)

    def __get_available_server_hardware_uri(self, server_profile, server_template):

        if server_template:
            enclosure_group = server_template.get('enclosureGroupUri', '')
            server_hardware_type = server_template.get('serverHardwareTypeUri', '')
        else:
            enclosure_group = server_profile.get('enclosureGroupUri', '')
            server_hardware_type = server_profile.get('serverHardwareTypeUri', '')

        logger.debug(msg="Finding an available server hardware")
        available_server_hardware = self.oneview_client.server_profiles.get_available_targets(
            enclosureGroupUri=enclosure_group,
            serverHardwareTypeUri=server_hardware_type)

        # targets will list empty bays. We need to pick one that has a server
        index = 0
        server_hardware_uri = None
        while not server_hardware_uri and index < len(available_server_hardware['targets']):
            server_hardware_uri = available_server_hardware['targets'][index]['serverHardwareUri']
            index = index + 1

        logger.debug(msg="Found available server hardware: '{}'".format(server_hardware_uri))
        return server_hardware_uri

    def __delete_profile(self, server_profile):
        if not server_profile:
            return False, self.MSG_ALREADY_ABSENT

        if server_profile.get('serverHardwareUri'):
            self.__set_server_hardware_power_state(server_profile['serverHardwareUri'], 'Off')

        self.oneview_client.server_profiles.delete(server_profile)
        return True, self.MSG_DELETED

    def __make_compliant(self, server_profile):

        changed = False
        msg = self.MSG_ALREADY_COMPLIANT

        if not server_profile.get('serverProfileTemplateUri'):
            logger.error("Make the Server Profile compliant is not supported for this profile")
            self.module.fail_json(msg=self.MSG_MAKE_COMPLIANT_NOT_SUPPORTED.format(server_profile['name']))

        elif server_profile['templateCompliance'] != 'Compliant':
            logger.debug(
                "Get the preview of manual and automatic updates required to make the server profile consistent "
                "with its template.")
            compliance_preview = self.oneview_client.server_profiles.get_compliance_preview(server_profile['uri'])

            logger.debug(str(compliance_preview))

            is_offline_update = compliance_preview.get('isOnlineUpdate') is False

            if is_offline_update:
                logger.debug(msg="Power off the server hardware before update from template")
                self.__set_server_hardware_power_state(server_profile['serverHardwareUri'], 'Off')

            logger.debug(msg="Updating from template")

            server_profile = self.oneview_client.server_profiles.patch(
                server_profile['uri'], 'replace', '/templateCompliance', 'Compliant')

            if is_offline_update:
                logger.debug(msg="Power on the server hardware after update from template")
                self.__set_server_hardware_power_state(server_profile['serverHardwareUri'], 'On')

            changed = True
            msg = self.MSG_REMEDIATED_COMPLIANCE

        return changed, msg, server_profile

    def __gather_facts(self, server_profile):

        server_hardware = None
        if server_profile.get('serverHardwareUri'):
            server_hardware = self.oneview_client.server_hardware.get(server_profile['serverHardwareUri'])

        compliance_preview = None
        if server_profile.get('serverProfileTemplateUri'):
            compliance_preview = self.oneview_client.server_profiles.get_compliance_preview(server_profile.get('uri'))

        facts = {
            'serial_number': server_profile.get('serialNumber'),
            'server_profile': server_profile,
            'server_hardware': server_hardware,
            'compliance_preview': compliance_preview,
            'created': False
        }

        return facts

    def __get_server_hardware_by_name(self, server_hardware_name):
        server_hardwares = self.oneview_client.server_hardware.get_by('name', server_hardware_name)
        return server_hardwares[0] if server_hardwares else None

    def __set_server_hardware_power_state(self, hardware_uri, power_state='On'):
        if power_state == 'On':
            self.oneview_client.server_hardware.update_power_state(
                dict(powerState='On', powerControl='MomentaryPress'), hardware_uri)
        else:
            self.oneview_client.server_hardware.update_power_state(
                dict(powerState='Off', powerControl='PressAndHold'), hardware_uri)


def main():
    ServerProfileModule().run()


if __name__ == '__main__':
    main()
