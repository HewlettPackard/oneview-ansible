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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_login_detail_facts
short_description: Retrieve the facts about login details
description:
    - Retrieve the facts about login details from oneview.
version_added: "2.5"
requirements:
    - hpOneView >= 4.3.0
author: Madhav Bharadwaj(@madhav-bharadwaj)

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about login details
  oneview_login_detail_facts:
    config: "{{ config }}"
    delegate_to: localhost

- debug: var=login_details
'''

RETURN = '''
login_details:
    description: Lists all the login details
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class LoginDetailFactsModule(OneViewModuleBase):
    def __init__(self):
        super(LoginDetailFactsModule, self).__init__()

    def execute_module(self):
        login_details = self.oneview_client.login_details.get_login_details()
        return dict(changed=False, ansible_facts=dict(login_details=login_details))


def main():
    LoginDetailFactsModule().run()


if __name__ == '__main__':
    main()
