#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
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
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_server_profile_template
short_description: Manage OneView Server Profile Template resources.
description:
    - Provides an interface to create, modify, and delete server profile templates.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Server Profile Template.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - Dict with Server Profile Template properties.
        required: true
    params:
        description:
            - Dict with query parameters.
        required: false
notes:
    - "For the following data, you can provide either a name  or a URI: enclosureGroupName or enclosureGroupUri,
       osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the
       connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or
       volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the
       volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri,
       firmwareBaselineName or firmwareBaselineUri (on the firmware), sasLogicalJBODName or sasLogicalJBODUri (on
       the sasLogicalJBODs list) and initialScopeNames or initialScopeUris"
    - "If you define the volumeUri as null in the volumeAttachments list, it will be understood that the volume
       does not exist, so it will be created along with the server profile. Be warned that every time this option
       is executed it will always be understood that a new volume needs to be created, so this will not be idempotent.
       It is strongly recommended to ensure volumes with Ansible and then assign them to the desired server profile
       template."

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a basic connection-less server profile template (using URIs)
  oneview_server_profile_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    params:
      force: True
    delegate_to: localhost

- name: Create a basic connection-less server profile template (using names)
  oneview_server_profile_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: "ProfileTemplate102"
      serverHardwareTypeName: "BL460c Gen8 1"
      enclosureGroupName: "EGSAS_3"
    params:
      force: True
  delegate_to: localhost

- name: Delete the Server Profile Template
  oneview_server_profile_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
      name: "ProfileTemplate101"
    params:
      force: True
    delegate_to: localhost
'''

RETURN = '''
server_profile_template:
    description: Has the OneView facts about the Server Profile Template.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, ServerProfileReplaceNamesByUris, ServerProfileMerger, compare


class ServerProfileTemplateModule(OneViewModule):
    MSG_CREATED = 'Server Profile Template created successfully.'
    MSG_UPDATED = 'Server Profile Template updated successfully.'
    MSG_DELETED = 'Server Profile Template deleted successfully.'
    MSG_ALREADY_PRESENT = 'Server Profile Template is already present.'
    MSG_ALREADY_ABSENT = 'Server Profile Template is already absent.'
    MSG_SRV_HW_TYPE_NOT_FOUND = 'Server Hardware Type not found: '
    MSG_ENCLOSURE_GROUP_NOT_FOUND = 'Enclosure Group not found: '

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(ServerProfileTemplateModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                          validate_etag_support=True)

        self.set_resource_object(self.oneview_client.server_profile_templates)
        self.server_profiles = self.oneview_client.server_profiles

    def execute_module(self):
        params = self.module.params.get("params")
        self.params = params if params else {}

        if self.state == 'present':
            result = self.__present()
        else:
            result = self.__absent()

        return result

    def __present(self):
        ServerProfileReplaceNamesByUris().replace(self.oneview_client, self.data)

        data = self.__spt_from_sp() or self.data

        if not self.current_resource:
            changed, msg, resource = self.__create(data)
        else:
            changed, msg, resource = self.__update(data)

        return dict(
            changed=changed,
            msg=msg,
            ansible_facts=dict(server_profile_template=resource)
        )

    def __spt_from_sp(self):
        if self.data.get('serverProfileName'):
            server_profile = self.server_profiles.get_by_name(self.data.pop('serverProfileName'))

            if server_profile:
                spt_from_sp = server_profile.get_new_profile_template()
                copy_of_spt_from_sp = spt_from_sp.copy()

                for key, value in copy_of_spt_from_sp.items():
                    if value is None:
                        del spt_from_sp[key]
                spt_from_sp.update(self.data)

                return spt_from_sp

    def __create(self, data):
        resource = self.resource_client.create(data, **self.params)
        return True, self.MSG_CREATED, resource.data

    def __update(self, data):
        merged_data = ServerProfileMerger().merge_data(self.current_resource.data, data)

        equal = compare(merged_data, self.current_resource.data)

        if equal:
            msg = self.MSG_ALREADY_PRESENT
        else:
            self.current_resource.update(merged_data, **self.params)
            msg = self.MSG_UPDATED

        changed = not equal

        return changed, msg, self.current_resource.data

    def __absent(self):
        if self.current_resource:
            self.current_resource.delete(**self.params)
            msg = self.MSG_DELETED
            changed = True
        else:
            msg = self.MSG_ALREADY_ABSENT
            changed = False

        return dict(changed=changed, msg=msg)


def main():
    ServerProfileTemplateModule().run()


if __name__ == '__main__':
    main()
