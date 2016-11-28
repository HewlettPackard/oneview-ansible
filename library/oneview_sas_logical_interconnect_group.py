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
module: oneview_sas_logical_interconnect_group
short_description: Manage OneView SAS Logical Interconnect Group resources.
description:
    - Provides an interface to manage SAS Logical Interconnect Group resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0"
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
            - Indicates the desired state for the SAS Logical Interconnect Group resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the SAS Logical Interconnect Group properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Ensure that the SAS Logical Interconnect Group is present
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    state: present
    data:
      name: "Test SAS Logical Interconnect Group"
      state: "Active"
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "1"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "4"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
      enclosureType: "SY12000"
      enclosureIndexes: [1]
      interconnectBaySet: "1"

- name: Ensure that the SAS Logical Interconnect Group is present with name 'Test'
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New SAS Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the SAS Logical Interconnect Group is absent
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New SAS Logical Interconnect Group'
'''

RETURN = '''
sas_logical_interconnect_group:
    description: Has the facts about the OneView SAS Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

SAS_LIG_CREATED = 'SAS Logical Interconnect Group created successfully.'
SAS_LIG_UPDATED = 'SAS Logical Interconnect Group updated successfully.'
SAS_LIG_DELETED = 'SAS Logical Interconnect Group deleted successfully.'
SAS_LIG_ALREADY_EXIST = 'SAS Logical Interconnect Group already exists.'
SAS_LIG_ALREADY_ABSENT = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasLogicalInterconnectGroupModule(object):
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
        data = self.module.params['data']

        try:
            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                self.__absent(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data.get('name'))

        if "newName" in data:
            data["name"] = data["newName"]
            del data["newName"]

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data):
        name = data.get('name')
        resource = self.__get_by_name(name)

        if resource:
            self.oneview_client.sas_logical_interconnect_groups.delete(resource)
            self.module.exit_json(changed=True, msg=SAS_LIG_DELETED)
        else:
            self.module.exit_json(changed=False, msg=SAS_LIG_ALREADY_ABSENT)

    def __create(self, data):
        new_sas_lig = self.oneview_client.sas_logical_interconnect_groups.create(data)

        self.module.exit_json(changed=True,
                              msg=SAS_LIG_CREATED,
                              ansible_facts=dict(sas_logical_interconnect_group=new_sas_lig))

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)

        if resource_compare(resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=SAS_LIG_ALREADY_EXIST,
                                  ansible_facts=dict(sas_logical_interconnect_group=resource))

        else:
            updated_sas_lig = self.oneview_client.sas_logical_interconnect_groups.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=SAS_LIG_UPDATED,
                                  ansible_facts=dict(sas_logical_interconnect_group=updated_sas_lig))

    def __get_by_name(self, name):
        result = self.oneview_client.sas_logical_interconnect_groups.get_by('name', name)
        return result[0] if result else None


def main():
    SasLogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
