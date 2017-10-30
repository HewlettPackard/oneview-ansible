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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_version
short_description: Returns the range of possible API versions supported by the appliance
description:
    - Provides an interface to return the range of possible API versions supported by the appliance.
version_added: "2.5"
requirements:
    - "hpOneView >= 4.3.0"
author: "Priyanka Sood (@soodpr)"
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Ensure that the Appliance Current and minimum version is present with version '500'
  oneview_version_facts:
    config: "{{ config_file_path }}"

- debug: var=version
'''

RETURN = '''
appliance_version:
    description: Has the facts about the OneView current and minimum version.
    returned: When requested, but can not be null
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class VersionFactsModule(OneViewModuleBase):
    def __init__(self):
        super(VersionFactsModule, self).__init__(additional_arg_spec=dict())

    def execute_module(self):
        version = self.oneview_client.versions.get_version()
        return dict(changed=False,
                    ansible_facts=dict(version=version))


def main():
    VersionFactsModule().run()


if __name__ == '__main__':
    main()
