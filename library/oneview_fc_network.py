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
module: oneview_fc_network
short_description: Manage OneView Fibre Channel Network resources.
description:
    - Provides an interface to manage Fibre Channel Network resources. Can create, update, delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Fibre Channel Network resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the Fibre Channel Network properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Ensure that a Fibre Channel Network is present using the default configuration
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New FC Network'

- name: Ensure that the Fibre Channel Network is present with fabricType 'DirectAttach'
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New FC Network'
      fabricType: 'DirectAttach'

- name: Ensure that Fibre Channel Network is absent
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FC Network'
'''

RETURN = '''
fc_network:
    description: Has the facts about the OneView FC Networks.
    returned: on state 'present'. Can be null.
    type: complex
'''

FC_NETWORK_CREATED = 'FC Network created successfully.'
FC_NETWORK_UPDATED = 'FC Network updated successfully.'
FC_NETWORK_DELETED = 'FC Network deleted successfully.'
FC_NETWORK_ALREADY_EXIST = 'FC Network already exists.'
FC_NETWORK_ALREADY_ABSENT = 'Nothing to do.'


class FcNetworkModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
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
            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __present(self, data):
        resource = self.__get_by_name(data)

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.fc_networks.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=FC_NETWORK_DELETED)
        else:
            self.module.exit_json(changed=False, msg=FC_NETWORK_ALREADY_ABSENT)

    def __create(self, data):
        new_fc_network = self.oneview_client.fc_networks.create(data)

        self.module.exit_json(changed=True,
                              msg=FC_NETWORK_CREATED,
                              ansible_facts=dict(fc_network=new_fc_network))

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)

        if resource_compare(resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=FC_NETWORK_ALREADY_EXIST,
                                  ansible_facts=dict(fc_network=resource))

        else:
            updated_fc_network = self.oneview_client.fc_networks.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=FC_NETWORK_UPDATED,
                                  ansible_facts=dict(fc_network=updated_fc_network))

    def __get_by_name(self, data):
        result = self.oneview_client.fc_networks.get_by('name', data['name'])
        return result[0] if result else None


def main():
    FcNetworkModule().run()


if __name__ == '__main__':
    main()
