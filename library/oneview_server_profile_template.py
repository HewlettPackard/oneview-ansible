#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
    - "hpOneView >= 3.1.0"
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
notes:
    - "For the following data, you can provide either a name  or a URI: enclosureGroupName or enclosureGroupUri,
       osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the
       connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or
       volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the
       volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri,
       firmwareBaselineName or firmwareBaselineUri (on the firmware), and sasLogicalJBODName or sasLogicalJBODUri (on
       the sasLogicalJBODs list)"
    - "If you define the volumeUri as null in the volumeAttachments list, it will be understood that the volume
       does not exist, so it will be created along with the server profile. Be warned that everytime this option
       is executed it will always be understood that a new volume needs to be created, so this will not be idempotent.
       It is strongly recommended to ensure volumes with ansible and then assign them to the desired server profile
       template."

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a basic connection-less server profile template (using URIs)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    delegate_to: localhost

- name: Create a basic connection-less server profile template (using names)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate102"
      serverHardwareTypeName: "BL460c Gen8 1"
      enclosureGroupName: "EGSAS_3"
  delegate_to: localhost

- name: Delete the Server Profile Template
  oneview_server_profile_template:
    config: "{{ config }}"
    state: absent
    data:
      name: "ProfileTemplate101"
    delegate_to: localhost
'''

RETURN = '''
server_profile_template:
    description: Has the OneView facts about the Server Profile Template.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import (OneViewModuleBase,
                                  ServerProfileReplaceNamesByUris,
                                  ServerProfileMerger,
                                  ResourceComparator)

# To activate logs, setup the environment var LOGFILE
# e.g.: export LOGFILE=/tmp/ansible-oneview.log
logger = OneViewModuleBase.get_logger(__file__)


class ServerProfileTemplateModule(OneViewModuleBase):
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
        data=dict(required=True, type='dict')
    )

    def __init__(self):

        super(ServerProfileTemplateModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                          validate_etag_support=True)

        self.resource_client = self.oneview_client.server_profile_templates

    def execute_module(self):

        template = self.resource_client.get_by_name(self.data["name"])

        if self.state == 'present':
            result = self.__present(self.data, template)
        else:
            result = self.__absent(template)

        return result

    def __present(self, data, template):

        ServerProfileReplaceNamesByUris().replace(self.oneview_client, data)

        data = self.__spt_from_sp(data) or data

        if not template:
            changed, msg, resource = self.__create(data)
        else:
            changed, msg, resource = self.__update(data, template)

        return dict(
            changed=changed,
            msg=msg,
            ansible_facts=dict(server_profile_template=resource)
        )

    def __spt_from_sp(self, data):
        if data.get('serverProfileName'):
            server_profiles = self.oneview_client.server_profiles.get_by('name', data.pop('serverProfileName'))
            if server_profiles:
                spt_from_sp = self.oneview_client.server_profiles.get_new_profile_template(server_profiles[0]['uri'])
                copy_of_spt_from_sp = spt_from_sp.copy()
                for key, value in copy_of_spt_from_sp.items():
                    if value is None:
                        del spt_from_sp[key]
                spt_from_sp.update(data)
                return spt_from_sp

    def __create(self, data):
        resource = self.resource_client.create(data)
        return True, self.MSG_CREATED, resource

    def __update(self, data, template):
        resource = template.copy()

        merged_data = ServerProfileMerger().merge_data(resource, data)

        equal = ResourceComparator.compare(merged_data, resource)

        if equal:
            msg = self.MSG_ALREADY_PRESENT
        else:
            resource = self.resource_client.update(resource=merged_data, id_or_uri=merged_data["uri"])
            msg = self.MSG_UPDATED

        changed = not equal

        return changed, msg, resource

    def __absent(self, template):
        msg = self.MSG_ALREADY_ABSENT

        if template:
            self.resource_client.delete(template)
            msg = self.MSG_DELETED

        changed = template is not None
        return dict(changed=changed, msg=msg)


def main():
    ServerProfileTemplateModule().run()


if __name__ == '__main__':
    main()
