#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_hypervisor_cluster_profile
short_description: Manage OneView Hypervisor Cluster Profiles resources.
description:
    - Provides an interface to manage Hypervisor Cluster Profiles resources. Can create, update, and delete.
version_added: "2.4"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the Hypervisor Cluster Profiles resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with the Hypervisor Cluster Profiles properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Hypervisor Cluster Profile
  oneview_hypervisor_cluster_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'hcp'
      path: 'DC1'
      hypervisorType: 'Vmware'
      hypervisorManagerUri: '/rest/hypervisor-manager/rdy-dfdf12'
      hypervisorHostProfileTemplate:
        serverProfileTemplateUri: '/rest/server-profile-template/2323-32323'
        hostprefix: 'test-host'

- name: Create a Hypervisor Cluster Profile
  oneview_hypervisor_cluster_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      type: "HypervisorClusterProfileV3"
      name: "{{ cluster_profile_name }}"
      hypervisorManagerUri: '/rest/hypervisor-managers/ee73af7a-1775-44ba-8a66-d0479ec85678'
      path: 'DC1'
      hypervisorType: 'Vmware'
      hypervisorHostProfileTemplate:
        serverProfileTemplateUri: '/rest/server-profile-templates/f8e56c43-cfd7-436c-9812-394ecdbd32ed'
        virtualSwitches:
          serverProfileTemplateUri: '/rest/server-profile-templates/f8e56c43-cfd7-436c-9812-394ecdbd32ed'
          hypervisorManagerUri: '/rest/hypervisor-managers/ee73af7a-1775-44ba-8a66-d0479ec85678'
        hostprefix: 'Test-cluster-host'
    params:
      create_vswitch_layout: True

- name: Update the Hypervisor Cluster Profile name to 'hcp Renamed'
  oneview_hypervisor_cluster_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'hcp Renamed'
      path: 'DC1'
      hypervisorType: 'Vmware'
      hypervisorManagerUri: '/rest/hypervisor-manager/rdy-dfdf12'
    params:
      force: True

- name: Ensure that the Hypervisor Cluster Profile is absent
  oneview_hypervisor_cluster_profile:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'hcp'

'''

RETURN = '''
hypervisor_cluster_profile:
    description: Has the facts about the managed OneView Hypervisor Cluster Profile.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, compare


class HypervisorClusterProfileModule(OneViewModule):
    MSG_CREATED = 'Hypervisor Cluster Profile created successfully.'
    MSG_UPDATED = 'Hypervisor Cluster Profile updated successfully.'
    MSG_DELETED = 'Hypervisor Cluster Profile deleted successfully.'
    MSG_ALREADY_PRESENT = 'Hypervisor Cluster Profile is already present.'
    MSG_ALREADY_ABSENT = 'Hypervisor Cluster Profile is already absent.'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   params=dict(type='dict', required=False),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super(HypervisorClusterProfileModule, self).__init__(additional_arg_spec=additional_arg_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.hypervisor_cluster_profiles)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}
        self.create_vswitch_layout = self.facts_params.pop('create_vswitch_layout', None)

        if self.state == 'present':
            changed, msg, ansible_facts = self.__present()
        elif self.state == 'absent':
            changed, msg, ansible_facts = self.__absent()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)

    def __present(self):
        if self.current_resource:
            response = self.__update()
        else:
            response = self.__create(self.data)
        return response

    def __create(self, data):

        self.__create_vswitch_layout()

        self.current_resource = self.resource_client.create(data)
        return True, self.MSG_CREATED, dict(hypervisor_cluster_profile=self.current_resource.data)

    def __absent(self):
        if self.current_resource:
            changed = True
            msg = self.MSG_DELETED
            self.current_resource.delete(**self.facts_params)
        else:
            changed = False
            msg = self.MSG_ALREADY_ABSENT
        return changed, msg, dict(hypervisor_cluster_profile=None)

    def __update(self):
        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        self.__create_vswitch_layout()

        merged_data = self.current_resource.data.copy()
        merged_data.update(self.data)

        if not compare(self.current_resource.data, merged_data):
            self.current_resource.update(merged_data, **self.facts_params)
            return True, self.MSG_UPDATED, dict(hypervisor_cluster_profile=self.current_resource.data)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(hypervisor_cluster_profile=self.current_resource.data)

    # Below code will create the virtual switch layout and modifies the update body if virtualswitches key is present in json data
    def __create_vswitch_layout(self):
        if self.create_vswitch_layout and self.data.get('hypervisorHostProfileTemplate') and \
                self.data.get('hypervisorHostProfileTemplate').get('virtualSwitches'):
            self.data['hypervisorHostProfileTemplate']['virtualSwitches'] = \
                self.resource_client.create_virtual_switch_layout(self.data['hypervisorHostProfileTemplate']['virtualSwitches'])


def main():
    HypervisorClusterProfileModule().run()


if __name__ == '__main__':
    main()
