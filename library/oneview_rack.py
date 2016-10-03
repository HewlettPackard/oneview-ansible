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
module: oneview_rack
short_description: Manage OneView Racks resources.
description:
    - Provides an interface to manage Rack resources. Can create, update, delete.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Rack resource.
              'present' will ensure data properties are compliant to OneView. To change the name of the Rack,
               a 'newName' in the data must be provided.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the Rack properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Ensure that a Rack is present using the default configuration
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'

- name: Add rack with custom size and a single mounted enclosure at slot 20
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack101'
      depth: 1500
      height: 2500
      width: 1200
      rackMounts:
        - mountUri: "/rest/enclosures/39SGH102X6J2"
          topUSlot: 20
          uHeight: 10

- name: Rename the Rack to 'Rack101'
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'
      newName: 'Rack101'

- name: Ensure that Rack is absent
  oneview_rack:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Rack Name'
'''

RETURN = '''
rack:
    description: Has the facts about the OneView Racks.
    returned: on state 'present'. Can be null.
    type: complex
'''

RACK_CREATED = 'Rack created successfully.'
RACK_UPDATED = 'Rack updated successfully.'
RACK_DELETED = 'Rack deleted successfully.'
RACK_ALREADY_EXIST = 'Rack already exists.'
RACK_ALREADY_ABSENT = 'Nothing to do.'
RACK_NOT_FOUND = 'Rack was not found for this operation.'
RACK_NEW_NAME_ALREADY_EXISTS = 'Rack with new name already exists.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class RackModule(object):
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
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data']

        try:
            facts = {}
            if state == 'present':
                changed, msg, resource = self.__present(data)
                facts = dict(ansible_facts=dict(rack=resource))
            elif state == 'absent':
                changed, msg = self.__absent(data)

            self.module.exit_json(changed=changed, msg=msg, **facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data['name'])

        self.__check_rename(data, resource)

        if not resource:
            return True, RACK_CREATED, self.oneview_client.racks.add(data)
        else:
            return self.__update(data, resource)

    def __absent(self, data):
        resource = self.__get_by_name(data['name'])

        changed = False
        msg = RACK_ALREADY_ABSENT

        if resource:
            self.oneview_client.racks.remove(resource)
            changed = True
            msg = RACK_DELETED

        return changed, msg

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)

        changed = False
        msg = RACK_ALREADY_EXIST

        if not resource_compare(resource, merged_data):
            resource = self.oneview_client.racks.update(merged_data)
            changed = True
            msg = RACK_UPDATED

        return changed, msg, resource

    def __check_rename(self, data, resource):

        if "newName" not in data:
            return

        resource_new_name = self.__get_by_name(data['newName'])

        if not resource:
            self.module.exit_json(changed=False, msg=RACK_NOT_FOUND)
        elif resource_new_name:
            self.module.exit_json(changed=False, msg=RACK_NEW_NAME_ALREADY_EXISTS)

        data["name"] = data.pop("newName")

    def __get_by_name(self, name):
        result = self.oneview_client.racks.get_by('name', name)
        return result[0] if result else None


def main():
    RackModule().run()


if __name__ == '__main__':
    main()
