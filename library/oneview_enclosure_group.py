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
module: oneview_enclosure_group
short_description: Manage OneView Enclosure Group resources.
description:
    - Provides an interface to manage Enclosure Group resources. Can create, update, or delete.
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
            - Indicates the desired state for the Enclosure Group resource.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with Enclosure Group properties
      required: true
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Ensure that Enclosure Group is present using the default configuration
  oneview_enclosure_group:
    config: "{{ config }}"
    state: present
    data:
        name: "Enclosure Group 1"
        stackingMode: "Enclosure"
        interconnectBayMappings:
            - interconnectBay: 1
            - interconnectBay: 2
            - interconnectBay: 3
            - interconnectBay: 4
            - interconnectBay: 5
            - interconnectBay: 6
            - interconnectBay: 7
            - interconnectBay: 8
  delegate_to: localhost

- name: Ensure that Enclosure Group is absent
  oneview_enclosure_group:
    config: "{{ config }}"
    state: absent
    data:
      name: "Enclosure Group 1 (renamed)"
  delegate_to: localhost
'''

ENCLOSURE_GROUP_CREATED = 'Enclosure Group created sucessfully.'
ENCLOSURE_GROUP_UPDATED = 'Enclosure Group updated sucessfully.'
ENCLOSURE_GROUP_DELETED = 'Enclosure Group deleted sucessfully.'
ENCLOSURE_GROUP_ALREADY_EXIST = 'Enclosure Group already exists.'
ENCLOSURE_GROUP_ALREADY_ABSENT = 'Nothing to do.'


class EnclosureGroupModule(object):
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
            self.oneview_client.enclosure_groups.delete(resource)
            self.module.exit_json(changed=True,
                                  msg=ENCLOSURE_GROUP_DELETED)
        else:
            self.module.exit_json(changed=False, msg=ENCLOSURE_GROUP_ALREADY_ABSENT)

    def __create(self, data):
        new_enclosure_group = self.oneview_client.enclosure_groups.create(data)

        self.module.exit_json(changed=True,
                              msg=ENCLOSURE_GROUP_CREATED,
                              ansible_facts=dict(enclosure_group=new_enclosure_group))

    def __update(self, new_data, existent_resource):
        merged_data = existent_resource.copy()
        merged_data.update(new_data)

        if resource_compare(existent_resource, merged_data):

            self.module.exit_json(changed=False,
                                  msg=ENCLOSURE_GROUP_ALREADY_EXIST,
                                  ansible_facts=dict(enclosure_group=existent_resource))

        else:
            updated_enclosure_group = self.oneview_client.enclosure_groups.update(merged_data)

            self.module.exit_json(changed=True,
                                  msg=ENCLOSURE_GROUP_UPDATED,
                                  ansible_facts=dict(enclosure_group=updated_enclosure_group))

    def __get_by_name(self, data):
        result = self.oneview_client.enclosure_groups.get_by('name', data['name'])
        return result[0] if result else None


def main():
    EnclosureGroupModule().run()


if __name__ == '__main__':
    main()
