#!/usr/bin/python

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

DOCUMENTATION = '''
---
module: oneview_logical_interconnect_group_facts
short_description: Retrieve facts about one or more of the OneView Logical Interconnect Groups.
description:
    - Retrieve facts about one or more of the Logical Interconnect Groups from OneView.
requirements:
    - "python 2.7.11"
    - "hpOneView"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Logical Interconnect Group name.
      required: false
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=logical_interconnect_groups
'''

RETURN = '''
ligs:
    description: Has all the OneView facts about the Logical Interconnect Groups.
    returned: always, but can be null
    type: complex
'''


class LogicalInterconnectGroupFactsModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            if self.module.params['name']:
                self.__get_by_name(self.module.params['name'])
            else:
                self.__get_all()

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        logical_interconnect_groups = self.oneview_client.logical_interconnect_groups.get_by('name', name)

        self.module.exit_json(changed=False,
                              ansible_facts=dict(logical_interconnect_groups=logical_interconnect_groups))

    def __get_all(self):
        logical_interconnect_groups = self.oneview_client.logical_interconnect_groups.get_all()

        self.module.exit_json(changed=False,
                              ansible_facts=dict(logical_interconnect_groups=logical_interconnect_groups))


def main():
    LogicalInterconnectGroupFactsModule().run()


if __name__ == '__main__':
    main()
