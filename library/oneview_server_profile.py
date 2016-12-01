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
    from hpOneView.common import resource_compare, merge_list_by_key
    from hpOneView.exceptions import HPOneViewTaskError
    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False
from copy import deepcopy


ASSIGN_HARDWARE_ERROR_CODES = ['AssignProfileToDeviceBayError',
                               'EnclosureBayUnavailableForProfile',
                               'ProfileAlreadyExistsInServer']

KEY_ID = 'id'
KEY_CONNECTIONS = 'connections'
KEY_OS_DEPLOYMENT = 'osDeploymentSettings'
KEY_ATTRIBUTES = 'osCustomAttributes'
KEY_SAN = 'sanStorage'
KEY_VOLUMES = 'volumeAttachments'
KEY_PATHS = 'storagePaths'
KEY_CONN_ID = 'connectionId'
KEY_BOOT = 'boot'
KEY_BIOS = 'bios'
KEY_BOOT_MODE = 'bootMode'

TEMPLATE_NOT_FOUND = "Informed Server Profile Template '{}' not found"
HARDWARE_NOT_FOUND = "Informed Server Hardware '{}' not found"
SERVER_PROFILE_CREATED = "Server Profile created."
SERVER_ALREADY_UPDATED = 'Server Profile is already updated.'
SERVER_PROFILE_UPDATED = 'Server profile updated'
SERVER_PROFILE_DELETED = 'Deleted profile'
REMEDIATED_COMPLIANCE = "Remediated compliance issues"
ALREADY_COMPLIANT = "Server Profile is already compliant."
SERVER_PROFILE_NOT_FOUND = "Server Profile is required for this operation."
ERROR_ALLOCATE_SERVER_HARDWARE = 'Could not allocate server hardware'
MAKE_COMPLIANT_NOT_SUPPORTED = "Update from template is not supported for server profile '{}' because it is not " \
                               "associated with a server profile template."

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
    - "hpOneView >= 3.0.0"
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
        'present' will ensure data properties are compliant with OneView.
        'absent' will remove the resource from OneView, if it exists.
        'compliant' will make the server profile complient with its server profile template, when this option was
        specified.
    default: present
    choices: ['present', 'absent', 'compliant']
  data:
    description:
      - List with Server Profile properties.
    required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
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
                self.__delete_profile(server_profile)
                self.module.exit_json(
                    changed=True, msg=SERVER_PROFILE_DELETED
                )
            elif state == "compliant":
                changed, msg, server_profile = self.__make_compliant(server_profile)
                self.module.exit_json(
                    changed=changed, msg=msg, ansible_facts=self.__gather_facts(server_profile)
                )
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, resource):

        server_template_name = data.pop('server_template', '')
        server_hardware_name = data.pop('server_hardware', '')
        server_template = None
        changed = False
        created = False

        if server_hardware_name:
            selected_server_hardware = self.__get_server_hardware_by_name(server_hardware_name)
            if not selected_server_hardware:
                raise ValueError(HARDWARE_NOT_FOUND.format(server_hardware_name))
            data['serverHardwareUri'] = selected_server_hardware['uri']

        if server_template_name:
            server_template = self.oneview_client.server_profile_templates.get_by_name(server_template_name)
            if not server_template:
                raise ValueError(TEMPLATE_NOT_FOUND.format(server_template_name))
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
            resource_for_comparation = self.__resource_with_paths_ordered(resource)

            if not resource_compare(resource_for_comparation, merged_data):
                resource = self.__update_server_profile(merged_data)
                changed = True
                msg = SERVER_PROFILE_UPDATED
            else:
                msg = SERVER_ALREADY_UPDATED

        return created, changed, msg, resource

    def __resource_with_paths_ordered(self, resource):
        resource_changed = deepcopy(resource)
        if KEY_SAN in resource_changed and KEY_VOLUMES in resource_changed[KEY_SAN]:
            for volume in resource_changed[KEY_SAN][KEY_VOLUMES]:
                if KEY_PATHS in volume:
                    volume[KEY_PATHS] = sorted(volume[KEY_PATHS], key=lambda k: k[KEY_CONN_ID])
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

        raise Exception(ERROR_ALLOCATE_SERVER_HARDWARE)

    def __build_new_profile_data(self, data, server_template, server_hardware_uri):

        server_profile_data = deepcopy(data)

        if server_template:
            logger.debug(msg="Get new Profile from template")
            profile_name = server_profile_data['name']
            server_profile_data = self.oneview_client.server_profile_templates.get_new_profile(server_template['uri'])
            server_profile_data['name'] = profile_name

        if server_hardware_uri:
            server_profile_data['serverHardwareUri'] = server_hardware_uri

        return server_profile_data

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
            raise Exception(SERVER_PROFILE_NOT_FOUND)

        if server_profile.get('serverHardwareUri'):
            self.__set_server_hardware_power_state(server_profile['serverHardwareUri'], 'Off')

        self.oneview_client.server_profiles.delete(server_profile)

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


class ServerProfileMerger(object):
    def merge_data(self, resource, data):
        merged_data = deepcopy(resource)
        merged_data.update(data)

        merged_data = self._merge_bios_and_boot(merged_data, resource, data)
        merged_data = self._merge_connections(merged_data, resource, data)
        merged_data = self._merge_san_storage(merged_data, data, resource)
        merged_data = self._merge_os_deployment_settings(merged_data, resource, data)

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
            merged_data[KEY_CONNECTIONS] = merge_list_by_key(existing_connections, params_connections, KEY_ID)

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
            merged_volumes = merge_list_by_key(existing_volumes, params_volumes, KEY_ID)
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

                    merged_paths = merge_list_by_key(existent_paths, paths_from_merged_volume, KEY_CONN_ID)

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

    def _removed_data(self, data, resource, key):
        return key in data and not data[key] and key in resource

    def _should_merge(self, data, resource, key):
        return key in data and data[key] and key in resource

    def _merge_dict(self, merged_data, resource, data, key):
        merged_dict = deepcopy(resource[key])
        merged_dict.update(deepcopy(data[key]))
        merged_data[key] = merged_dict
        return merged_data


def main():
    ServerProfileModule().run()


if __name__ == '__main__':
    main()
