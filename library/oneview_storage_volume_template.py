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
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_storage_volume_template
short_description: Manage OneView Storage Volume Template resources.
description:
    - "Provides an interface to manage Storage Volume Template resources. Can create, update and delete."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Storage Volume Template resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage Volume Template properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Storage Volume Template
  oneview_storage_volume_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
        name: "Volume Template Name"
        description: "Example Template"
        rootTemplateUri: "/rest/storage-volume-templates/5dbaf127-053b-4988-82fe-a80800eef1f3"
        properties: {}

  delegate_to: localhost

- name: Delete the Storage Volume Template
  oneview_storage_volume_template:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
        name: 'Volume Template Name'
  delegate_to: localhost
'''

RETURN = '''
storage_volume_template:
    description: Has the OneView facts about the Storage Volume Template.
    returned: On 'present' state, but can be null.
    type: dict
'''

import collections

from copy import deepcopy
from six import iteritems

from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError, compare


def _update_dict_with_depth(ov_resource, user_resource):
    for key, value in user_resource.items():
        if isinstance(value, collections.Mapping):
            ov_resource[key] = _update_dict_with_depth(ov_resource.get(key, {}), value)
        else:
            ov_resource[key] = user_resource[key]
    return ov_resource


class StorageVolumeTemplateModule(OneViewModule):
    MSG_CREATED = 'Storage Volume Template created successfully.'
    MSG_UPDATED = 'Storage Volume Template updated successfully.'
    MSG_ALREADY_PRESENT = 'Storage Volume Template is already updated.'
    MSG_DELETED = 'Storage Volume Template deleted successfully.'
    MSG_ALREADY_ABSENT = 'Storage Volume Template is already absent.'
    MSG_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: data.name"

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent']
            ),
            data=dict(required=True, type='dict'),
        )
        super(StorageVolumeTemplateModule, self).__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.storage_volume_templates)

    def execute_module(self):

        if not self.data.get('name'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING)

        if self.state == 'present':
            return self._present()
        elif self.state == 'absent':
            return self.resource_absent()

    def _present(self):
        if not self.current_resource:
            return self.resource_present(fact_name='storage_volume_template')
        else:
            changed = False
            merged_data = _update_dict_with_depth(deepcopy(self.current_resource.data),
                                                  self.data)

            if compare(self.current_resource.data, merged_data):
                msg = self.MSG_ALREADY_PRESENT
            else:
                self.current_resource.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED

            return dict(
                msg=msg,
                changed=changed,
                ansible_facts={'storage_volume_template': self.current_resource.data}
            )


def main():
    StorageVolumeTemplateModule().run()


if __name__ == '__main__':
    main()
