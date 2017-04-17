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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_os_deployment_server
short_description: Manage OneView Deployment Server resources.
description:
    - Provides an interface to manage Deployment Server resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Deployment Server resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with Deployment Server properties.
        required: true
notes:
    - "For the following data, you can provide either a name or a URI: C(mgmtNetworkName) or C(mgmtNetworkUri), and
      C(applianceName) or C(applianceUri)"
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
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

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound, ResourceComparator


class OsDeploymentServerModule(OneViewModuleBase):
    MSG_CREATED = 'Deployment Server created successfully.'
    MSG_UPDATED = 'Deployment Server updated successfully.'
    MSG_DELETED = 'Deployment Server deleted successfully.'
    MSG_ALREADY_PRESENT = 'Deployment Server is already present.'
    MSG_ALREADY_ABSENT = 'Deployment Server is already absent.'
    MSG_NETWORK_NOT_FOUND = 'Network "{}" not found.'
    MSG_APPLIANCE_NOT_FOUND = 'Appliance "{}" not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(OsDeploymentServerModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                       validate_etag_support=True)
        self.resource_client = self.oneview_client.os_deployment_servers

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            return self.__present(resource, self.data)
        elif self.state == 'absent':
            return self.resource_absent(resource)

    def __present(self, resource, data):

        self.__replace_names_by_uris(data)

        changed = False

        if "newName" in data:
            data["name"] = data.pop("newName")

        if not resource:
            resource = self.oneview_client.os_deployment_servers.add(data)
            changed = True
            msg = self.MSG_CREATED
        else:
            appliance_uri = data.pop('applianceUri', '')
            if appliance_uri:
                data['primaryActiveAppliance'] = appliance_uri

            merged_data = resource.copy()
            merged_data.update(data)

            if not ResourceComparator.compare(resource, merged_data):
                resource = self.oneview_client.os_deployment_servers.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED
            else:
                msg = self.MSG_ALREADY_PRESENT

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(os_deployment_server=resource))

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
            raise HPOneViewResourceNotFound(self.MSG_NETWORK_NOT_FOUND.format(name))

        return fcoe_networks[0]['uri']

    def __get_appliance_by_name(self, name):
        appliance = self.oneview_client.os_deployment_servers.get_appliance_by_name(name)

        if not appliance:
            raise HPOneViewResourceNotFound(self.MSG_APPLIANCE_NOT_FOUND.format(name))

        return appliance['uri']


def main():
    OsDeploymentServerModule().run()


if __name__ == '__main__':
    main()
