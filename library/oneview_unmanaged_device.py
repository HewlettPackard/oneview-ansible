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
module: oneview_unmanaged_device
short_description: Manage OneView Unmanaged Device resources.
description:
    - Provides an interface to manage Unmanaged Device resources. Can create, update, or delete.
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
            - Indicates the desired state for the Unmanaged Device resource.
              'present' will ensure data properties are compliant with OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with Unmanaged Device properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
    - "To rename an unamnaged device you must inform a 'newName' in the data argument. The rename is non-idempotent"
'''

EXAMPLES = '''
- name: Ensure that the unmanaged device is present
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      model: 'Procurve 4200VL'
      deviceType: 'Server'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Add another unmanaged device
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'AnotherUnmanagedDevice'
      model: 'Procurve 4200VL'
    delegate_to: localhost

- name: Update the unmanaged device changing the name attribute
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      newName: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Ensure that the unmanaged device is absent
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      name: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- name: Delete all the unmanaged devices
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      filter: "name matches '%'"
    delegate_to: localhost
'''

RETURN = '''
unmanaged_device:
    description: Has the OneView facts about the Unmanaged Device.
    returned: On state 'present'. Can be null.
    type: complex
'''

UNMANAGED_DEVICE_ADDED = 'Unmanaged Device added successfully.'
UNMANAGED_DEVICE_UPDATED = 'Unmanaged Device updated successfully.'
UNMANAGED_DEVICE_REMOVED = 'Unmanaged Device removed successfully.'
UNMANAGED_DEVICE_SET_REMOVED = 'Unmanaged device set deleted successfully.'
NOTHING_TO_DO = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class UnmanagedDeviceModule(object):

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
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.unmanaged_devices

    def run(self):
        try:
            data = self.module.params["data"]
            state = self.module.params["state"]
            facts = dict()

            if state == "present":
                changed, msg, facts = self.__present(data)
            elif state == "absent":
                changed, msg = self.__absent(data)

            self.module.exit_json(changed=changed, msg=msg, **facts)
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data["name"])

        if not resource:
            changed, message, resource = self.__add(data)
        else:
            changed, message, resource = self.__update(data, resource)

        return changed, message, dict(ansible_facts=dict(unmanaged_device=resource))

    def __get_by_name(self, name):
        resources = self.resource_client.get_by('name', name) or [None]
        return resources[0]

    def __add(self, data):
        return True, UNMANAGED_DEVICE_ADDED, self.resource_client.add(data)

    def __update(self, data, resource):
        if "newName" in data:
            data['name'] = data.pop('newName')

        merged_data = resource.copy()
        merged_data.update(data)

        is_equal = resource_compare(resource, merged_data)

        if not is_equal:
            return True, UNMANAGED_DEVICE_UPDATED, self.resource_client.update(merged_data)
        else:
            return False, NOTHING_TO_DO, resource

    def __absent(self, data):
        changed, message = False, NOTHING_TO_DO

        if "name" in data:
            resource = self.__get_by_name(data["name"])

            if resource:
                changed = self.resource_client.remove(resource)

            if changed:
                message = UNMANAGED_DEVICE_REMOVED

        elif "filter" in data:
            self.resource_client.remove_all(**data)
            changed, message = True, UNMANAGED_DEVICE_SET_REMOVED

        return changed, message


def main():
    UnmanagedDeviceModule().run()


if __name__ == '__main__':
    main()
