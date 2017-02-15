#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2017) Hewlett Packard Enterprise Development LP
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
    from hpOneView.extras.comparators import resource_compare
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_os_deployment_server
short_description: Manage OneView Deployment Server resources.
description:
    - Provides an interface to manage Deployment Server resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Deployment Server resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with Deployment Server properties.
        required: true
    validate_etag:
        description:
            - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
              for the resource matches the ETag provided in the data.
        default: true
        choices: ['true', 'false']
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - "For the following data, you can provide either a name  or a URI: mgmtNetworkName or mgmtNetworkUri, and
      applianceName or applianceUri"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Ensure that the Deployment Server is present
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Deployment Server'
      description: "OS Deployment Server"
      mgmtNetworkUri: "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"
      applianceUri: "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"

- debug: var=os_deployment_server

- name: Ensure that the Deployment Server is present with name 'Renamed Deployment Server'
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Deployment Server'
      newName: 'Renamed Deployment Server'

- debug: var=os_deployment_server


- name: Ensure that the Deployment Server is absent
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Renamed Deployment Server'
'''

RETURN = '''
os_deployment_server:
    description: Has the facts about the Deployment Servers.
    returned: On state 'present'. Can be null.
    type: complex
'''


class OsDeploymentServerModule(object):
    DEPLOYMENT_SERVER_CREATED = 'Deployment Server created successfully.'
    DEPLOYMENT_SERVER_UPDATED = 'Deployment Server updated successfully.'
    DEPLOYMENT_SERVER_DELETED = 'Deployment Server deleted successfully.'
    DEPLOYMENT_SERVER_ALREADY_EXIST = 'Deployment Server already exists.'
    DEPLOYMENT_SERVER_ALREADY_ABSENT = 'Deployment Server is already absent.'
    HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'
    NETWORK_NOT_FOUND = 'Network "{}" not found.'
    APPLIANCE_NOT_FOUND = 'Appliance "{}" not found.'

    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict'),
        validate_etag=dict(
            required=False,
            type='bool',
            default=True)
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=self.HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):

        try:
            state = self.module.params['state']
            data = self.module.params['data']
            changed, msg, ansible_facts = False, '', {}

            if not self.module.params.get('validate_etag'):
                self.oneview_client.connection.disable_etag_validation()

            resource = self.oneview_client.os_deployment_servers.get_by_name(data['name'])

            if state == 'present':
                changed, msg, ansible_facts = self.__present(resource, data)
            elif state == 'absent':
                changed, msg, ansible_facts = self.__absent(resource)

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, resource, data):

        self.__replace_names_by_uris(data)

        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        if not resource:
            resource = self.oneview_client.os_deployment_servers.add(data)
            changed = True
            msg = self.DEPLOYMENT_SERVER_CREATED
        else:
            appliance_uri = data.pop('applianceUri', '')
            if appliance_uri:
                data['primaryActiveAppliance'] = appliance_uri

            merged_data = resource.copy()
            merged_data.update(data)

            if not resource_compare(resource, merged_data):
                resource = self.oneview_client.os_deployment_servers.update(merged_data)
                changed = True
                msg = self.DEPLOYMENT_SERVER_UPDATED
            else:
                msg = self.DEPLOYMENT_SERVER_ALREADY_EXIST

        return changed, msg, dict(os_deployment_server=resource)

    def __absent(self, resource):
        if resource:
            self.oneview_client.os_deployment_servers.delete(resource)
            return True, self.DEPLOYMENT_SERVER_DELETED, {}

        return False, self.DEPLOYMENT_SERVER_ALREADY_ABSENT, {}

    def __replace_names_by_uris(self, data):
        mgmt_network_name = data.pop("mgmtNetworkName", "")
        if mgmt_network_name:
            data['mgmtNetworkUri'] = self.__get_network_uri_by_name(mgmt_network_name)

        appliance_name = data.pop("applianceName", "")
        if appliance_name:
            data['applianceUri'] = self.__get_appliance_by_name(appliance_name)

    def __get_network_uri_by_name(self, name):
        ethernet_networks = self.oneview_client.ethernet_networks.get_by('name', name)
        if ethernet_networks:
            return ethernet_networks[0]['uri']

        fc_networks = self.oneview_client.fc_networks.get_by('name', name)
        if fc_networks:
            return fc_networks[0]['uri']

        fcoe_networks = self.oneview_client.fcoe_networks.get_by('name', name)
        if not fcoe_networks:
            raise HPOneViewResourceNotFound(self.NETWORK_NOT_FOUND.format(name))

        return fcoe_networks[0]['uri']

    def __get_appliance_by_name(self, name):
        appliances = self.oneview_client.os_deployment_servers.get_appliances()
        if appliances:
            for appliance in appliances:
                if appliance['name'] == name:
                    return appliance['uri']
        raise HPOneViewResourceNotFound(self.APPLIANCE_NOT_FOUND.format(name))


def main():
    OsDeploymentServerModule().run()


if __name__ == '__main__':
    main()
