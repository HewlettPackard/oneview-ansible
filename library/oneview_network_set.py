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
try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_network_set
short_description: Manage OneView Network Set resources.
description:
    - Provides an interface to manage Network Set resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    state:
        description:
            - Indicates the desired state for the Network Set resource.
              'present' ensures data properties are compliant with OneView.
              'absent' removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the Network Set properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Create a Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      networkUris:
        - 'Test Ethernet Network_1'                                       # can be a name
        - '/rest/ethernet-networks/e4360c9d-051d-4931-b2aa-7de846450dd8'  # or a URI

- name: Update the Network Set name to 'OneViewSDK Test Network Set - Renamed' and change the associated networks
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      newName: 'OneViewSDK Test Network Set - Renamed'
      networkUris:
        - 'Test Ethernet Network_1'

- name: Delete the Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: absent
    data:
        name: 'OneViewSDK Test Network Set - Renamed'
'''

RETURN = '''
network_set:
    description: Has the facts about the Network Set.
    returned: On state 'present', but can be null.
    type: complex
'''

NETWORK_SET_CREATED = 'Network Set created successfully.'
NETWORK_SET_UPDATED = 'Network Set updated successfully.'
NETWORK_SET_DELETED = 'Network Set deleted successfully.'
NETWORK_SET_ALREADY_EXIST = 'Network Set already exists.'
NETWORK_SET_ALREADY_ABSENT = 'Nothing to do.'
NETWORK_SET_NEW_NAME_INVALID = 'Rename failed: the new name provided is being used by another Network Set.'
NETWORK_SET_ENET_NETWORK_NOT_FOUND = 'Ethernet network not found: '
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class NetworkSetModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data'].copy()

        try:
            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data['name'])

        self.__replace_network_name_by_uri(data)

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data['name'])

        if resource:
            self.oneview_client.network_sets.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=NETWORK_SET_DELETED)
        else:
            self.module.exit_json(changed=False, msg=NETWORK_SET_ALREADY_ABSENT)

    def __create(self, data):
        created_network_set = self.oneview_client.network_sets.create(data)

        self.module.exit_json(changed=True,
                              msg=NETWORK_SET_CREATED,
                              ansible_facts=dict(network_set=created_network_set))

    def __update(self, data, resource):
        if 'newName' in data:
            if self.__get_by_name(data['newName']):
                raise Exception(NETWORK_SET_NEW_NAME_INVALID)
            data['name'] = data.pop('newName')

        merged_data = resource.copy()
        merged_data.update(data)

        if resource_compare(resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=NETWORK_SET_ALREADY_EXIST,
                                  ansible_facts=dict(network_set=resource))

        else:
            updated_network_set = self.oneview_client.network_sets.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=NETWORK_SET_UPDATED,
                                  ansible_facts=dict(network_set=updated_network_set))

    def __get_by_name(self, name):
        result = self.oneview_client.network_sets.get_by('name', name)
        return result[0] if result else None

    def __get_ethernet_network_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None

    def __get_network_uri(self, network_name_or_uri):
        if network_name_or_uri.startswith('/rest/ethernet-networks'):
            return network_name_or_uri
        else:
            enet_network = self.__get_ethernet_network_by_name(network_name_or_uri)
            if enet_network:
                return enet_network['uri']
            else:
                raise Exception(NETWORK_SET_ENET_NETWORK_NOT_FOUND + network_name_or_uri)

    def __replace_network_name_by_uri(self, data):
        if 'networkUris' in data:
            data['networkUris'] = [self.__get_network_uri(x) for x in data['networkUris']]


def main():
    NetworkSetModule().run()


if __name__ == '__main__':
    main()
