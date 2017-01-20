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
import logging

from ansible.module_utils.basic import *

try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.extras.comparators import resource_compare
    from hpOneView.extras.mergers import merge_list_by_key
    from hpOneView.exceptions import HPOneViewTaskError
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound
    from hpOneView.exceptions import HPOneViewValueError

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False
from copy import deepcopy

ASSIGN_HARDWARE_ERROR_CODES = ['AssignProfileToDeviceBayError',
                               'EnclosureBayUnavailableForProfile',
                               'ProfileAlreadyExistsInServer']

KEY_ID = 'id'
KEY_NAME = 'name'
KEY_DEVICE_SLOT = 'deviceSlot'
KEY_CONNECTIONS = 'connections'
KEY_OS_DEPLOYMENT = 'osDeploymentSettings'
KEY_OS_DEPLOYMENT_URI = 'osDeploymentPlanUri'
KEY_ATTRIBUTES = 'osCustomAttributes'
KEY_SAN = 'sanStorage'
KEY_VOLUMES = 'volumeAttachments'
KEY_PATHS = 'storagePaths'
KEY_CONN_ID = 'connectionId'
KEY_BOOT = 'boot'
KEY_BIOS = 'bios'
KEY_BOOT_MODE = 'bootMode'
KEY_LOCAL_STORAGE = 'localStorage'
KEY_SAS_LOGICAL_JBODS = 'sasLogicalJBODs'
KEY_CONTROLLERS = 'controllers'
KEY_LOGICAL_DRIVES = 'logicalDrives'
KEY_SAS_LOGICAL_JBOD_URI = 'sasLogicalJBODUri'
KEY_SAS_LOGICAL_JBOD_ID = 'sasLogicalJBODId'
KEY_DEVICE_SLOT = 'deviceSlot'
KEY_MODE = 'mode'
KEY_MAC_TYPE = 'macType'
KEY_MAC = 'mac'
KEY_SERIAL_NUMBER_TYPE = 'serialNumberType'
KEY_UUID = 'uuid'
KEY_SERIAL_NUMBER = 'serialNumber'
KEY_DRIVE_NUMBER = 'driveNumber'
KEY_WWPN_TYPE = 'wwpnType'
KEY_WWNN = 'wwnn'
KEY_WWPN = 'wwpn'
KEY_LUN_TYPE = 'lunType'
KEY_LUN = 'lun'

TEMPLATE_NOT_FOUND = "Informed Server Profile Template '{}' not found"
HARDWARE_NOT_FOUND = "Informed Server Hardware '{}' not found"
SERVER_PROFILE_CREATED = "Server Profile created."
SERVER_ALREADY_UPDATED = 'Server Profile is already updated.'
SERVER_PROFILE_UPDATED = 'Server profile updated'
SERVER_PROFILE_DELETED = 'Deleted profile'
SERVER_PROFILE_ALREADY_ABSENT = 'Nothing do.'
REMEDIATED_COMPLIANCE = "Remediated compliance issues"
ALREADY_COMPLIANT = "Server Profile is already compliant."
SERVER_PROFILE_NOT_FOUND = "Server Profile is required for this operation."
ERROR_ALLOCATE_SERVER_HARDWARE = 'Could not allocate server hardware'
MAKE_COMPLIANT_NOT_SUPPORTED = "Update from template is not supported for server profile '{}' because it is not " \
                               "associated with a server profile template."
SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND = 'OS Deployment Plan not found: '
SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND = 'Enclosure Group not found: '
SERVER_PROFILE_NETWORK_NOT_FOUND = 'Network not found: '
SERVER_HARDWARE_TYPE_NOT_FOUND = 'Server Hardware Type not found: '
VOLUME_NOT_FOUND = 'Volume not found: '
STORAGE_POOL_NOT_FOUND = 'Storage Pool not found: '
STORAGE_SYSTEM_NOT_FOUND = 'Storage System not found: '

CONCURRENCY_FAILOVER_RETRIES = 25

DOCUMENTATION = '''
---
module: oneview_server_profile
short_description: Manage OneView Server Profile resources.
description:
    - Manage the servers lifecycle with OneView Server Profiles. On 'present' state, it selects a server hardware
      automatically based on the server profile configuration if no server hardware was provided.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author:
    - "Chakravarthy Racharla"
    - "Camila Balestrin (@balestrinc)"
    - "Mariana Kreisig (@marikrg)"
options:
  config:
    description:
      - Path to a .json configuration file containing the OneView client configuration.
        The configuration file is optional. If the file path is not provided, the configuration will be loaded from
        environment variables.
    required: false
  state:
    description:
      - Indicates the desired state for the Server Profile resource by the end of the playbook execution.
        'present' will ensure data properties are compliant with OneView. This operation will power off the Server
        Hardware before configuring the Server Profile. After it completes, the Server Hardware is powered on.
        For the osDeploymentSettings, you can provide an osDeploymentPlanName instead of osDeploymentPlanUri.
        'absent' will remove the resource from OneView, if it exists.
        'compliant' will make the server profile compliant with its server profile template, when this option was
        specified. If there are Offline updates, the Server Hardware is turned off before remediate compliance issues
        and turned on after that.
    default: present
    choices: ['present', 'absent', 'compliant']
  data:
    description:
      - List with Server Profile properties.
    required: true
  validate_etag:
    description:
      - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for
        the resource matches the ETag provided in the data.
    default: true
    choices: ['true', 'false']
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - "For the following data, you can provide a name instead of a URI: enclosureGroupName instead of enclosureGroupUri,
       osDeploymentPlanName instead of osDeploymentPlanUri (on the osDeploymentSettings), and networkName instead of a
       networkUri (on the connections list)"
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
              # You can choose either volumeStorageSystemUri or volumeStorageSystemName to inform the Volume Storage System
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


# To activate logs, setup the environment var LOGFILE
# e.g.: export LOGFILE=/tmp/ansible-oneview.log
def get_logger(mod_name):
    logger = logging.getLogger(os.path.basename(mod_name))
    global LOGFILE
    LOGFILE = os.environ.get('LOGFILE')
    if not LOGFILE:
        logger.addHandler(logging.NullHandler())
    else:
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            filename=LOGFILE, filemode='a')
    return logger


logger = get_logger(__file__)
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerProfileModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=False,
            choices=[
                'present',
                'absent',
                'compliant'
            ],
            default='present'
        ),
        data=dict(required=True, type='dict'),
        validate_etag=dict(
            required=False,
            type='bool',
            default=True),
    )

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        if not self.module.params.get('validate_etag'):
            self.oneview_client.connection.disable_etag_validation()

    def run(self):
        data = deepcopy(self.module.params['data'])
        server_profile_name = data.get('name')
        state = self.module.params['state']

        try:
            server_profile = self.oneview_client.server_profiles.get_by_name(server_profile_name)

            if state == 'present':
                created, changed, msg, server_profile = self.__present(data, server_profile)
                facts = self.__gather_facts(server_profile)
                facts['created'] = created
                self.module.exit_json(
                    changed=changed, msg=msg, ansible_facts=facts
                )
            elif state == 'absent':
                changed, msg = self.__delete_profile(server_profile)
                self.module.exit_json(
                    changed=changed, msg=msg
                )
            elif state == "compliant":
                changed, msg, server_profile = self.__make_compliant(server_profile)
                self.module.exit_json(
                    changed=changed, msg=msg, ansible_facts=self.__gather_facts(server_profile)
                )
        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, resource):

        server_template_name = data.pop('server_template', '')
        server_hardware_name = data.pop('server_hardware', '')
        server_template = None
        changed = False
        created = False

        self.__replace_names_by_uris(data)

        if server_hardware_name:
            selected_server_hardware = self.__get_server_hardware_by_name(server_hardware_name)
            if not selected_server_hardware:
                raise HPOneViewValueError(HARDWARE_NOT_FOUND.format(server_hardware_name))
            data['serverHardwareUri'] = selected_server_hardware['uri']

        if server_template_name:
            server_template = self.oneview_client.server_profile_templates.get_by_name(server_template_name)
            if not server_template:
                raise HPOneViewValueError(TEMPLATE_NOT_FOUND.format(server_template_name))
            data['serverProfileTemplateUri'] = server_template['uri']
        elif data.get('serverProfileTemplateUri'):
            server_template = self.oneview_client.server_profile_templates.get(data['serverProfileTemplateUri'])

        if not resource:
            resource = self.__create_profile(data, server_template)
            changed = True
            created = True
            msg = SERVER_PROFILE_CREATED
        else:
            merged_data = ServerProfileMerger().merge_data(resource, data)
            resource_for_comparison = self.__prepare_resource_for_comparison(resource)

            if not resource_compare(resource_for_comparison, merged_data):
                resource = self.__update_server_profile(merged_data)
                changed = True
                msg = SERVER_PROFILE_UPDATED
            else:
                msg = SERVER_ALREADY_UPDATED

        return created, changed, msg, resource

    def __prepare_resource_for_comparison(self, resource):
        resource_changed = deepcopy(resource)

        # Order paths from SAN Storage Volumes
        if KEY_SAN in resource_changed and KEY_VOLUMES in resource_changed[KEY_SAN]:
            for volume in resource_changed[KEY_SAN][KEY_VOLUMES]:
                if KEY_PATHS in volume:
                    volume[KEY_PATHS] = sorted(volume[KEY_PATHS], key=lambda k: k[KEY_CONN_ID])

        # Order SAS Logical JBODs from Local Storage
        if KEY_LOCAL_STORAGE in resource_changed and KEY_SAS_LOGICAL_JBODS in resource_changed[KEY_LOCAL_STORAGE]:
            jbods = resource_changed[KEY_LOCAL_STORAGE][KEY_SAS_LOGICAL_JBODS]
            resource_changed[KEY_LOCAL_STORAGE][KEY_SAS_LOGICAL_JBODS] = sorted(jbods, key=lambda k: k[KEY_ID])

        # Order Controllers from Local Storage
        if KEY_LOCAL_STORAGE in resource_changed and KEY_CONTROLLERS in resource_changed[KEY_LOCAL_STORAGE]:
            controllers = resource_changed[KEY_LOCAL_STORAGE][KEY_CONTROLLERS]
            resource_changed[KEY_LOCAL_STORAGE][KEY_CONTROLLERS] = sorted(controllers, key=lambda k: k[KEY_DEVICE_SLOT])

        return resource_changed

    def __update_server_profile(self, profile_with_updates):
        logger.debug(msg="Updating Server Profile")

        if profile_with_updates.get('serverHardwareUri'):
            logger.debug("Power off the server hardware before update")
            self.__set_server_hardware_power_state(profile_with_updates['serverHardwareUri'], 'Off')

        resource = self.oneview_client.server_profiles.update(profile_with_updates, profile_with_updates['uri'])

        if profile_with_updates.get('serverHardwareUri'):
            logger.debug("Power on the server hardware after update")
            self.__set_server_hardware_power_state(profile_with_updates['serverHardwareUri'], 'On')

        return resource

    def __create_profile(self, data, server_profile_template):
        tries = 0
        self.__remove_inconsistent_data(data)

        while tries < CONCURRENCY_FAILOVER_RETRIES:
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
                if task_error.error_code in ASSIGN_HARDWARE_ERROR_CODES:
                    # if this is because the server is already assigned, someone grabbed it before we assigned,
                    # ignore and try again
                    # This waiting time was chosen empirically and it could differ according to the hardware.
                    time.sleep(10)
                else:
                    raise task_error

        raise HPOneViewException(ERROR_ALLOCATE_SERVER_HARDWARE)

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
        mac_type = data.get(KEY_MAC_TYPE, None)
        if mac_type and is_virtual_or_physical(mac_type):
            for conn in data.get(KEY_CONNECTIONS, []):
                conn.pop(KEY_MAC, None)

        # Remove the UUID when Serial Number Type is Virtual or Physical
        serial_number_type = data.get(KEY_SERIAL_NUMBER_TYPE, None)
        if serial_number_type and is_virtual_or_physical(serial_number_type):
            data.pop(KEY_UUID, None)
            data.pop(KEY_SERIAL_NUMBER, None)

        # Remove the WWPN and WWNN when WWPN Type is Virtual or Physical
        for conn in data.get(KEY_CONNECTIONS) or []:
            wwpn_type = conn.get(KEY_WWPN_TYPE, None)
            if is_virtual_or_physical(wwpn_type):
                conn.pop(KEY_WWNN, None)
                conn.pop(KEY_WWPN, None)

        # Remove the driveNumber from the Controllers Drives
        if KEY_LOCAL_STORAGE in data:
            for controller in data[KEY_LOCAL_STORAGE].get(KEY_CONTROLLERS) or []:
                for drive in controller.get(KEY_LOGICAL_DRIVES) or []:
                    drive.pop(KEY_DRIVE_NUMBER, None)

        # Remove the Lun when Lun Type from SAN Storage Volume is Auto
        if KEY_SAN in data and data[KEY_SAN]:
            if KEY_VOLUMES in data[KEY_SAN]:
                for volume in data[KEY_SAN].get(KEY_VOLUMES) or []:
                    if volume.get(KEY_LUN_TYPE) == 'Auto':
                        volume.pop(KEY_LUN, None)

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
            return False, SERVER_PROFILE_ALREADY_ABSENT

        if server_profile.get('serverHardwareUri'):
            self.__set_server_hardware_power_state(server_profile['serverHardwareUri'], 'Off')

        self.oneview_client.server_profiles.delete(server_profile)
        return True, SERVER_PROFILE_DELETED

    def __make_compliant(self, server_profile):

        changed = False
        msg = ALREADY_COMPLIANT

        if not server_profile.get('serverProfileTemplateUri'):
            logger.error("Make the Server Profile compliant is not supported for this profile")
            self.module.fail_json(msg=MAKE_COMPLIANT_NOT_SUPPORTED.format(server_profile['name']))

        elif (server_profile['templateCompliance'] != 'Compliant'):
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
            msg = REMEDIATED_COMPLIANCE

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

    def __replace_names_by_uris(self, data):
        self.__replace_os_deployment_name_by_uri(data)
        self.__replace_enclosure_group_name_by_uri(data)
        self.__replace_networks_name_by_uri(data)
        self.__replace_server_hardware_type_name_by_uri(data)
        self.__replace_volume_attachment_names_by_uri(data)
        self.__replace_enclosure_name_by_uri(data)

    def __replace_os_deployment_name_by_uri(self, data):
        if KEY_OS_DEPLOYMENT in data and data[KEY_OS_DEPLOYMENT]:
            if 'osDeploymentPlanName' in data[KEY_OS_DEPLOYMENT]:
                os_deployment = self.__get_os_deployment_by_name(data[KEY_OS_DEPLOYMENT].pop('osDeploymentPlanName'))
                data[KEY_OS_DEPLOYMENT][KEY_OS_DEPLOYMENT_URI] = os_deployment['uri']

    def __replace_enclosure_group_name_by_uri(self, data):
        if 'enclosureGroupName' in data:
            enclosure_group = self.__get_enclosure_group_by_name(data.pop('enclosureGroupName'))
            data['enclosureGroupUri'] = enclosure_group['uri']

    def __replace_networks_name_by_uri(self, data):
        if KEY_CONNECTIONS in data:
            for connection in data[KEY_CONNECTIONS]:
                if 'networkName' in connection:
                    name = connection.pop('networkName', None)
                    connection['networkUri'] = self.__get_network_by_name(name)['uri']

    def __replace_server_hardware_type_name_by_uri(self, data):
        if 'serverHardwareTypeName' in data:
            name = data.pop('serverHardwareTypeName')
            sh_types = self.oneview_client.server_hardware_types.get_by('name', name)
            if not sh_types:
                raise HPOneViewResourceNotFound(SERVER_HARDWARE_TYPE_NOT_FOUND + name)
            data['serverHardwareTypeUri'] = sh_types[0]['uri']

    def __replace_volume_attachment_names_by_uri(self, data):
        def replace(volume_attachment, attr_name, attr_uri, message, resource_client):
            if attr_name in volume_attachment:
                name = volume_attachment.pop(attr_name)
                resource_by_name = resource_client.get_by('name', name)
                if not resource_by_name:
                    raise HPOneViewResourceNotFound(message + name)
                volume_attachment[attr_uri] = resource_by_name[0]['uri']

        volume_attachments = (data.get('sanStorage') or {}).get('volumeAttachments') or []
        if len(volume_attachments) > 0:
            for volume in volume_attachments:
                replace(volume, 'volumeName', 'volumeUri', VOLUME_NOT_FOUND, self.oneview_client.volumes)
                replace(volume, 'volumeStoragePoolName', 'volumeStoragePoolUri', STORAGE_POOL_NOT_FOUND,
                        self.oneview_client.storage_pools)
                replace(volume, 'volumeStorageSystemName', 'volumeStorageSystemUri', STORAGE_SYSTEM_NOT_FOUND,
                        self.oneview_client.storage_systems)

    def __replace_enclosure_name_by_uri(self, data):
        if 'enclosureName' in data:
            name = data.pop('enclosureName')
            enclsoures = self.oneview_client.enclosures.get_by('name', name)
            if not enclsoures:
                raise HPOneViewResourceNotFound(SERVER_HARDWARE_TYPE_NOT_FOUND + name)
            data['enclosureUri'] = enclsoures[0]['uri']

    def __get_os_deployment_by_name(self, name):
        os_deployment = self.oneview_client.os_deployment_plans.get_by_name(name)
        if not os_deployment:
            raise HPOneViewResourceNotFound(SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND + name)
        return os_deployment

    def __get_enclosure_group_by_name(self, name):
        enclosure_group = self.oneview_client.enclosure_groups.get_by('name', name)
        if not enclosure_group:
            raise HPOneViewResourceNotFound(SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND + name)
        return enclosure_group[0]

    def __get_network_by_name(self, name):
        fc_networks = self.oneview_client.fc_networks.get_by('name', name)
        if fc_networks:
            return fc_networks[0]

        ethernet_networks = self.oneview_client.ethernet_networks.get_by('name', name)
        if not ethernet_networks:
            raise HPOneViewResourceNotFound(SERVER_PROFILE_NETWORK_NOT_FOUND + name)
        return ethernet_networks[0]


class ServerProfileMerger(object):
    def merge_data(self, resource, data):
        merged_data = deepcopy(resource)
        merged_data.update(data)

        merged_data = self._merge_bios_and_boot(merged_data, resource, data)
        merged_data = self._merge_connections(merged_data, resource, data)
        merged_data = self._merge_san_storage(merged_data, data, resource)
        merged_data = self._merge_os_deployment_settings(merged_data, resource, data)
        merged_data = self._merge_local_storage(merged_data, resource, data)

        return merged_data

    def _merge_bios_and_boot(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=KEY_BIOS):
            merged_data = self._merge_dict(merged_data, resource, data, key=KEY_BIOS)
        if self._should_merge(data, resource, key=KEY_BOOT):
            merged_data = self._merge_dict(merged_data, resource, data, key=KEY_BOOT)
        if self._should_merge(data, resource, key=KEY_BOOT_MODE):
            merged_data = self._merge_dict(merged_data, resource, data, key=KEY_BOOT_MODE)
        return merged_data

    def _merge_connections(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=KEY_CONNECTIONS):
            existing_connections = resource[KEY_CONNECTIONS]
            params_connections = data[KEY_CONNECTIONS]
            merged_data[KEY_CONNECTIONS] = merge_list_by_key(existing_connections, params_connections, key=KEY_ID)

            # merge Boot from Connections
            merged_data = self._merge_connections_boot(merged_data, resource)
        return merged_data

    def _merge_connections_boot(self, merged_data, resource):
        existing_connection_map = {x[KEY_ID]: x.copy() for x in resource[KEY_CONNECTIONS]}
        for merged_connection in merged_data[KEY_CONNECTIONS]:
            conn_id = merged_connection[KEY_ID]
            existing_conn_has_boot = conn_id in existing_connection_map and KEY_BOOT in existing_connection_map[conn_id]
            if existing_conn_has_boot and KEY_BOOT in merged_connection:
                current_connection = existing_connection_map[conn_id]
                boot_settings_merged = deepcopy(current_connection[KEY_BOOT])
                boot_settings_merged.update(merged_connection[KEY_BOOT])
                merged_connection[KEY_BOOT] = boot_settings_merged
        return merged_data

    def _merge_san_storage(self, merged_data, data, resource):
        if self._removed_data(data, resource, key=KEY_SAN):
            merged_data[KEY_SAN] = dict(volumeAttachments=[], manageSanStorage=False)
        elif self._should_merge(data, resource, key=KEY_SAN):
            merged_data = self._merge_dict(merged_data, resource, data, key=KEY_SAN)

            # Merge Volumes from SAN Storage
            merged_data = self._merge_san_volumes(merged_data, resource, data)
        return merged_data

    def _merge_san_volumes(self, merged_data, resource, data):
        if self._should_merge(data[KEY_SAN], resource[KEY_SAN], key=KEY_VOLUMES):
            existing_volumes = resource[KEY_SAN][KEY_VOLUMES]
            params_volumes = data[KEY_SAN][KEY_VOLUMES]
            merged_volumes = merge_list_by_key(existing_volumes, params_volumes, key=KEY_ID)
            merged_data[KEY_SAN][KEY_VOLUMES] = merged_volumes

            # Merge Paths from SAN Storage Volumes
            merged_data = self._merge_san_volumes_paths(merged_data, resource, data)
        return merged_data

    def _merge_san_volumes_paths(self, merged_data, resource, data):
        existing_volumes_map = {x[KEY_ID]: x for x in resource[KEY_SAN][KEY_VOLUMES]}  # can't be a copy here
        merged_volumes = merged_data[KEY_SAN][KEY_VOLUMES]
        for merged_volume in merged_volumes:
            volume_id = merged_volume[KEY_ID]
            if volume_id in existing_volumes_map:
                if KEY_PATHS in merged_volume and KEY_PATHS in existing_volumes_map[volume_id]:
                    existent_paths = existing_volumes_map[volume_id][KEY_PATHS]
                    existent_paths = sorted(existent_paths, key=lambda k: k[KEY_CONN_ID])

                    paths_from_merged_volume = merged_volume[KEY_PATHS]
                    paths_from_merged_volume = sorted(paths_from_merged_volume, key=lambda k: k[KEY_CONN_ID])

                    merged_paths = merge_list_by_key(existent_paths, paths_from_merged_volume, key=KEY_CONN_ID)

                    merged_volume[KEY_PATHS] = merged_paths
        return merged_data

    def _merge_os_deployment_settings(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=KEY_OS_DEPLOYMENT):
            merged_data = self._merge_dict(merged_data, resource, data, key=KEY_OS_DEPLOYMENT)

            # Merge Custom Attributes from OS Deployment Settings
            merged_data = self._merge_os_deployment_custom_attr(merged_data, resource, data)
        return merged_data

    def _merge_os_deployment_custom_attr(self, merged_data, resource, data):
        if KEY_ATTRIBUTES in data[KEY_OS_DEPLOYMENT]:
            existing_os_deployment = resource[KEY_OS_DEPLOYMENT]
            params_os_deployment = data[KEY_OS_DEPLOYMENT]
            merged_os_deployment = merged_data[KEY_OS_DEPLOYMENT]

            if self._removed_data(params_os_deployment, existing_os_deployment, key=KEY_ATTRIBUTES):
                merged_os_deployment[KEY_ATTRIBUTES] = params_os_deployment[KEY_ATTRIBUTES]
            else:
                existing_attributes = existing_os_deployment[KEY_ATTRIBUTES]
                params_attributes = params_os_deployment[KEY_ATTRIBUTES]

                if sorted(list(existing_attributes)) == sorted(list(params_attributes)):
                    merged_os_deployment[KEY_ATTRIBUTES] = existing_attributes

        return merged_data

    def _merge_local_storage(self, merged_data, resource, data):
        if self._removed_data(data, resource, key=KEY_LOCAL_STORAGE):
            merged_data[KEY_LOCAL_STORAGE] = dict(sasLogicalJBODs=[], controllers=[])
        elif self._should_merge(data, resource, key=KEY_LOCAL_STORAGE):
            # Merge SAS Logical JBODs from Local Storage
            merged_data = self._merge_sas_logical_jbods(merged_data, resource, data)
            # Merge Controllers from Local Storage
            merged_data = self._merge_controllers(merged_data, resource, data)
        return merged_data

    def _merge_sas_logical_jbods(self, merged_data, resource, data):
        if self._should_merge(data[KEY_LOCAL_STORAGE], resource[KEY_LOCAL_STORAGE], key=KEY_SAS_LOGICAL_JBODS):
            existing_items = resource[KEY_LOCAL_STORAGE][KEY_SAS_LOGICAL_JBODS]
            provided_items = merged_data[KEY_LOCAL_STORAGE][KEY_SAS_LOGICAL_JBODS]
            merged_jbods = merge_list_by_key(existing_items,
                                             provided_items,
                                             key=KEY_ID,
                                             ignore_when_null=[KEY_SAS_LOGICAL_JBOD_URI])
            merged_jbods = sorted(merged_jbods, key=lambda k: k[KEY_ID])
            merged_data[KEY_LOCAL_STORAGE][KEY_SAS_LOGICAL_JBODS] = merged_jbods
        return merged_data

    def _merge_controllers(self, merged_data, resource, data):
        if self._should_merge(data[KEY_LOCAL_STORAGE], resource[KEY_LOCAL_STORAGE], key=KEY_CONTROLLERS):
            existing_items = resource[KEY_LOCAL_STORAGE][KEY_CONTROLLERS]
            provided_items = merged_data[KEY_LOCAL_STORAGE][KEY_CONTROLLERS]
            merged_controllers = merge_list_by_key(existing_items, provided_items, key=KEY_DEVICE_SLOT)
            merged_controllers = sorted(merged_controllers, key=lambda k: k[KEY_DEVICE_SLOT])
            merged_data[KEY_LOCAL_STORAGE][KEY_CONTROLLERS] = merged_controllers

            # Merge Drives from Mezzanine and Embedded controllers
            merged_data = self._merge_controller_drives(merged_data, resource)
        return merged_data

    def _merge_controller_drives(self, merged_data, resource):
        for current_controller in merged_data[KEY_LOCAL_STORAGE][KEY_CONTROLLERS]:
            for existing_controller in resource[KEY_LOCAL_STORAGE][KEY_CONTROLLERS]:
                same_slot = current_controller.get(KEY_DEVICE_SLOT) == existing_controller.get(KEY_DEVICE_SLOT)
                same_mode = existing_controller.get(KEY_MODE) == existing_controller.get(KEY_MODE)
                if same_slot and same_mode and current_controller[KEY_LOGICAL_DRIVES]:

                    key_merge = self._define_key_to_merge_drives(current_controller)

                    if key_merge:
                        merged_drives = merge_list_by_key(existing_controller[KEY_LOGICAL_DRIVES],
                                                          current_controller[KEY_LOGICAL_DRIVES],
                                                          key=key_merge)
                        current_controller[KEY_LOGICAL_DRIVES] = merged_drives
        return merged_data

    def _define_key_to_merge_drives(self, controller):
        has_name = True
        has_logical_jbod_id = True
        for drive in controller[KEY_LOGICAL_DRIVES]:
            if not drive.get(KEY_NAME):
                has_name = False
            if not drive.get(KEY_SAS_LOGICAL_JBOD_ID):
                has_logical_jbod_id = False

        if has_name:
            return KEY_NAME
        elif has_logical_jbod_id:
            return KEY_SAS_LOGICAL_JBOD_ID
        return None

    def _removed_data(self, data, resource, key):
        return key in data and not data[key] and key in resource

    def _should_merge(self, data, resource, key):
        data_has_value = key in data and data[key]
        existing_resource_has_value = key in resource and resource[key]
        return data_has_value and existing_resource_has_value

    def _merge_dict(self, merged_data, resource, data, key):
        if resource[key]:
            merged_dict = deepcopy(resource[key])
            merged_dict.update(deepcopy(data[key]))
        merged_data[key] = merged_dict
        return merged_data


def main():
    ServerProfileModule().run()


if __name__ == '__main__':
    main()
