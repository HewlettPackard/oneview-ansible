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
module: oneview_server_profile_template
short_description: Manage OneView Server Profile Template resources.
description:
    - Provides an interface to create, modify, and delete server profile templates.
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
            - Indicates the desired state for the Server Profile Template.
              'present' will ensure data properties are compliant to OneView.
              'absent' will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - Dict with Server Profile Template properties
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
      https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Create a basic connection-less server profile template
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
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
    type: complex
'''

TEMPLATE_CREATED = 'Server Profile Template created successfully.'
TEMPLATE_UPDATED = 'Server Profile Template updated successfully.'
TEMPLATE_DELETED = 'Server Profile Template deleted successfully.'
TEMPLATE_ALREADY_EXIST = 'Server Profile Template already exists.'
TEMPLATE_ALREADY_ABSENT = 'Nothing to do.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerProfileTemplateModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.server_profile_templates

    def run(self):
        try:
            state = self.module.params["state"]
            data = self.module.params["data"]
            template = self.resource_client.get_by_name(data["name"])

            if state == 'present':
                result = self.__present(data, template)
            else:
                result = self.__absent(template)

            self.module.exit_json(**result)
        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data, template):
        if not template:
            changed, msg, resource = self.__create(data)
        else:
            changed, msg, resource = self.__update(data, template)

        return dict(
            changed=changed,
            msg=msg,
            ansible_facts=dict(server_profile_template=resource)
        )

    def __create(self, data):
        resource = self.resource_client.create(data)
        return True, TEMPLATE_CREATED, resource

    def __update(self, data, template):
        resource = template.copy()
        resource.update(data)
        equal = resource_compare(template, resource)

        if equal:
            msg = TEMPLATE_ALREADY_EXIST
        else:
            resource = self.resource_client.update(resource=resource, id_or_uri=resource["uri"])
            msg = TEMPLATE_UPDATED

        changed = not equal

        return changed, msg, resource

    def __absent(self, template):
        msg = TEMPLATE_ALREADY_ABSENT

        if template:
            self.resource_client.delete(template)
            msg = TEMPLATE_DELETED

        changed = template is not None
        return dict(changed=changed, msg=msg)


def main():
    ServerProfileTemplateModule().run()


if __name__ == '__main__':
    main()
