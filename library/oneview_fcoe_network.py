#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient
from hpOneView.common import resource_compare

DOCUMENTATION = '''
---
module: oneview_fcoe_network
short_description: Manage OneView FCoE Network resources.
description:
    - Provides an interface to manage FCoE Network resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the FCoE Network resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with FCoE Network properties
      required: true
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Ensure that FCoE Network is present using the default configuration
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test FCoE Network'
      vlanId: '201'

- name: Ensure that FCoE Network is absent
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FCoE Network'
'''

FCOE_NETWORK_CREATED = 'FCoE Network created sucessfully.'
FCOE_NETWORK_UPDATED = 'FCoE Network updated sucessfully.'
FCOE_NETWORK_DELETED = 'FCoE Network deleted sucessfully.'
FCOE_NETWORK_ALREADY_EXIST = 'FCoE Network already exists.'
FCOE_NETWORK_ALREADY_ABSENT = 'Nothing to do.'


class FcoeNetworkModule(object):
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

        if "newName" in data:
            data["name"] = data["newName"]
            del data["newName"]

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.fcoe_networks.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=FCOE_NETWORK_DELETED)
        else:
            self.module.exit_json(changed=False, msg=FCOE_NETWORK_ALREADY_ABSENT)

    def __create(self, data):
        new_fcoe_network = self.oneview_client.fcoe_networks.create(data)

        self.module.exit_json(changed=True,
                              msg=FCOE_NETWORK_CREATED,
                              ansible_facts=dict(fcoe_network=new_fcoe_network))

    def __update(self, new_data, existent_resource):
        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if resource_compare(existent_resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=FCOE_NETWORK_ALREADY_EXIST,
                                  ansible_facts=dict(fcoe_network=existent_resource))

        else:
            updated_fcoe_network = self.oneview_client.fcoe_networks.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=FCOE_NETWORK_UPDATED,
                                  ansible_facts=dict(fcoe_network=updated_fcoe_network))

    def __get_by_name(self, data):
        result = self.oneview_client.fcoe_networks.get_by('name', data['name'])
        return result[0] if result else None


def main():
    FcoeNetworkModule().run()


if __name__ == '__main__':
    main()
