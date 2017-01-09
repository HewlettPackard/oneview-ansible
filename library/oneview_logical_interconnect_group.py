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
module: oneview_logical_interconnect_group
short_description: Manage OneView Logical Interconnect Group resources.
description:
    - Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
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
            - Indicates the desired state for the Logical Interconnect Group resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Logical Interconnect Group properties.
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
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalDownlinkUri: ~
            logicalLocation:
                locationEntries:
                    - relativeValue: "1"
                      type: "Bay"
                    - relativeValue: 1
                      type: "Enclosure"
            permittedInterconnectTypeName: 'HP VC Flex-10/10D Module'
            # Alternatively you can inform permittedInterconnectTypeUri

- name: Ensure that the Logical Interconnect Group is present with name 'Test'
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the Logical Interconnect Group is absent
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New Logical Interconnect Group'
'''

RETURN = '''
logical_interconnect_group:
    description: Has the facts about the OneView Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

LIG_CREATED = 'Logical Interconnect Group created successfully.'
LIG_UPDATED = 'Logical Interconnect Group updated successfully.'
LIG_DELETED = 'Logical Interconnect Group deleted successfully.'
LIG_ALREADY_EXIST = 'Logical Interconnect Group already exists.'
LIG_ALREADY_ABSENT = 'Nothing to do.'
INTERCONNECT_TYPE_NOT_FOUND = 'Interconnect Type was not found.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class LogicalInterconnectGroupModule(object):
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
        data = self.module.params['data']

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
        resource = self.__get_by_name(data)

        if "newName" in data:
            data["name"] = data["newName"]
            del data["newName"]

        self.__replace_name_by_uris(data)

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __replace_name_by_uris(self, resource):
        map_template = resource.get('interconnectMapTemplate')

        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name).get('uri')

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.interconnect_types.get_by('name', name)
        if i_type:
            return i_type[0]
        else:
            raise Exception(INTERCONNECT_TYPE_NOT_FOUND)

    def __absent(self, data):
        resource = self.__get_by_name(data)

        if resource:
            self.oneview_client.logical_interconnect_groups.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=LIG_DELETED)
        else:
            self.module.exit_json(changed=False, msg=LIG_ALREADY_ABSENT)

    def __create(self, data):
        new_lig = self.oneview_client.logical_interconnect_groups.create(data)

        self.module.exit_json(changed=True,
                              msg=LIG_CREATED,
                              ansible_facts=dict(logical_interconnect_group=new_lig))

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)

        if resource_compare(resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=LIG_ALREADY_EXIST,
                                  ansible_facts=dict(logical_interconnect_group=resource))

        else:
            updated_lig = self.oneview_client.logical_interconnect_groups.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=LIG_UPDATED,
                                  ansible_facts=dict(logical_interconnect_group=updated_lig))

    def __get_by_name(self, data):
        result = self.oneview_client.logical_interconnect_groups.get_by('name', data['name'])
        return result[0] if result else None


def main():
    LogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
