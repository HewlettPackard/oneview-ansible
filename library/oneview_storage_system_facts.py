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
    from hpOneView.common import transform_list_to_dict

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_storage_system_facts
short_description: Retrieve facts about the OneView Storage Systems.
description:
    - Retrieve facts about the Storage Systems from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    ip_hostname:
      description:
        - Storage System IP or hostname.
      required: false
    name:
      description:
        - Storage System name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Storage System and related resources.
          Options allowed:
          'hostTypes' gets the list of supported host types.
          'storagePools' gets a list of storage pools belonging to the specified storage system."
        - "To gather facts about 'storagePools' it is required to inform either the argument 'name' or 'ip_hostname'.
          Otherwise, this option will be ignored."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_systems


- name: Gather facts about a Storage System by IP
  oneview_storage_system_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_systems


- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System and all options
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
    options:
        - hostTypes
        - storagePools
  delegate_to: localhost

- debug: var=storage_systems
- debug: var=storage_system_host_types
- debug: var=storage_system_pools

'''

RETURN = '''
storage_systems:
    description: Has all the OneView facts about the Storage Systems.
    returned: Always, but can be null.
    type: complex

storage_system_host_types:
    description: Has all the OneView facts about the supported host types.
    returned: When requested, but can be null.
    type: complex

storage_system_pools:
    description: Has all the OneView facts about the Storage Systems - Storage Pools.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class StorageSystemFactsModule(object):
    argument_spec = {
        "config": {
            "required": False,
            "type": 'str'
        },
        "name": {
            "required": False,
            "type": 'str'
        },
        "ip_hostname": {
            "required": False,
            "type": 'str'
        },
        "options": {
            "required": False,
            "type": 'list'
        }}

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            facts = {}
            is_specific_storage_system = True
            if self.module.params.get('ip_hostname'):
                storage_systems = self.oneview_client.storage_systems.get_by_ip_hostname(
                    self.module.params.get('ip_hostname'))
            elif self.module.params.get('name'):
                storage_systems = self.oneview_client.storage_systems.get_by_name(self.module.params['name'])
            else:
                storage_systems = self.oneview_client.storage_systems.get_all()
                is_specific_storage_system = False

            self.__get_options(facts, storage_systems, is_specific_storage_system)

            facts['storage_systems'] = storage_systems

            self.module.exit_json(changed=False, ansible_facts=facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_options(self, facts, storage_system, is_specific_storage_system):

        if self.module.params.get('options'):
            options = transform_list_to_dict(self.module.params['options'])

            if options.get('hostTypes'):
                facts['storage_system_host_types'] = self.oneview_client.storage_systems.get_host_types()

            if storage_system and is_specific_storage_system:
                storage_uri = storage_system['uri']
                if options.get('storagePools'):
                    facts['storage_system_pools'] = self.oneview_client.storage_systems.get_storage_pools(storage_uri)


def main():
    StorageSystemFactsModule().run()


if __name__ == '__main__':
    main()
