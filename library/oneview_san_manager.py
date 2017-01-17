#!/usr/bin/python
# -*- coding: utf-8 -*-
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
module: oneview_san_manager
short_description: Manage OneView SAN Manager resources.
description:
    - Provides an interface to manage SAN Manager resources. Can create, update, or delete.
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
            - Indicates the desired state for the Uplink Set resource.
              'present' ensures data properties are compliant with OneView.
              'absent' removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with SAN Manager properties.
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
'''

EXAMPLES = '''
- name: Creates a Device Manager for the Brocade SAN provider with the given hostname and credentials
  oneview_san_manager:
    config: "{{ config }}"
    state: present
    data:
      providerDisplayName: 'Brocade Network Advisor'
      connectionInfo:
        - name: Host
          value: '172.18.15.1'
        - name: Port
          value: '5989'
        - name: Username
          value: 'username'
        - name: Password
          value: 'password'
        - name: UseSsl
          value: true

- name: Update the SAN Manager
  oneview_san_manager:
    config: "{{ config_path }}"
    state: present
    data:
      providerDisplayName: 'Brocade Network Advisor'
      refreshState: 'RefreshPending'

- name: Delete the SAN Manager recently created
  oneview_san_manager:
    config: "{{ config_path }}"
    state: absent
    data:
      providerDisplayName: 'Brocade Network Advisor'
'''

RETURN = '''
san_manager:
    description: Has the OneView facts about the SAN Manager.
    returned: On state 'present'. Can be null.
    type: complex
'''

SAN_MANAGER_CREATED = 'SAN Manager created successfully.'
SAN_MANAGER_UPDATED = 'SAN Manager updated successfully.'
SAN_MANAGER_DELETED = 'SAN Manager deleted successfully.'
SAN_MANAGER_ALREADY_EXIST = 'SAN Manager already exists.'
SAN_MANAGER_ALREADY_ABSENT = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SanManagerModule(object):
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
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data'].copy()

        try:
            if not self.module.params.get('validate_etag'):
                self.oneview_client.connection.disable_etag_validation()

            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.oneview_client.san_managers.get_by_provider_display_name(data['providerDisplayName'])
        provider_uri = data.get('providerUri', self.__get_provider_uri_by_display_name(data))

        if not resource:
            self.__add(provider_uri, data)
        else:
            self.__update(resource, data)

    def __add(self, provider_uri, data):
        san_manager = self.oneview_client.san_managers.add(data, provider_uri)

        self.module.exit_json(changed=True,
                              msg=SAN_MANAGER_CREATED,
                              ansible_facts=dict(san_manager=san_manager))

    def __update(self, resource, data):
        merged_data = resource.copy()
        merged_data.update(data)

        # If connectionInfo is not provided, its removed because the password is required for update.
        if 'connectionInfo' not in data:
            merged_data.pop('connectionInfo')

        if resource_compare(resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=SAN_MANAGER_ALREADY_EXIST,
                                  ansible_facts=dict(san_manager=resource))
        else:
            san_manager = self.oneview_client.san_managers.update(resource=merged_data,
                                                                  id_or_uri=resource['uri'])

            self.module.exit_json(changed=True,
                                  msg=SAN_MANAGER_UPDATED,
                                  ansible_facts=dict(san_manager=san_manager))

    def __absent(self, data):
        resource = self.oneview_client.san_managers.get_by_provider_display_name(data['providerDisplayName'])

        if resource:
            self.oneview_client.san_managers.remove(resource)
            self.module.exit_json(changed=True,
                                  msg=SAN_MANAGER_DELETED)
        else:
            self.module.exit_json(changed=False, msg=SAN_MANAGER_ALREADY_ABSENT)

    def __get_provider_uri_by_display_name(self, data):
        return self.oneview_client.san_managers.get_provider_uri(data.get('providerDisplayName'))


def main():
    SanManagerModule().run()


if __name__ == '__main__':
    main()
