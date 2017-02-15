#!/usr/bin/python

###
# Copyright (2017) Hewlett Packard Enterprise Development LP
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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_os_deployment_server_facts
short_description: Retrieve facts about one or more OS Deployment Servers.
description:
    - Retrieve facts about one or more of the OS Deployment Servers from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author: "Camila Balestrin (@balestrinc)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          'start': The first item to return, using 0-based indexing.
          'count': The number of resources to return.
          'filter': A general filter/query string to narrow the list of items returned.
          'sort': The sort order of the returned data set.
          'query': A general query string to narrow the list of resources returned.
          'fields': Specifies which fields should be returned in the result set.
          'view': Return a specific subset of the attributes of the resource or collection, by
          specifying the name of a predefined view."
      required: false
    name:
      description:
        - OS Deployment Server name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an OS Deployment Server and related resources.
          Options allowed: networks, appliances, and appliance."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is only available on HPE Synergy
'''

EXAMPLES = '''
- name: Gather facts about all OS Deployment Servers
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: "OS Deployment Server-Name"
  delegate_to: localhost

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name with options
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: 'Test-OS Deployment Server'
    options:
      - networks                    # optional
      - appliances                  # optional
      - appliance: 'Appliance name' # optional
  delegate_to: localhost

- debug: var=os_deployment_servers
- debug: var=os_deployment_server_networks
- debug: var=os_deployment_server_appliances
- debug: var=os_deployment_server_appliance
'''

RETURN = '''
os_deployment_servers:
    description: Has all the OneView facts about the OS Deployment Servers.
    returned: Always, but can be null.
    type: complex

os_deployment_server_networks:
    description: Has all the OneView facts about the OneView networks.
    returned: When requested, but can be null.
    type: complex

os_deployment_server_appliances:
    description: Has all the OneView facts about all the Image Streamer resources.
    returned: When requested, but can be null.
    type: complex

os_deployment_server_appliance:
    description: Has the facts about the particular Image Streamer resource.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class OsDeploymentServerFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            ansible_facts = {}

            if self.module.params.get('name'):
                os_deployment_servers = self.oneview_client.os_deployment_servers.get_by('name',
                                                                                         self.module.params['name'])
            else:
                os_deployment_servers = self.__get_all()

            if self.module.params.get('options'):
                ansible_facts = self.__gather_optional_facts(self.module.params['options'])

            ansible_facts['os_deployment_servers'] = os_deployment_servers

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_optional_facts(self, options):

        options = transform_list_to_dict(options)

        facts = {}

        if options.get('networks'):
            facts['os_deployment_server_networks'] = self.oneview_client.os_deployment_servers.get_networks()
        if options.get('appliances'):
            facts['os_deployment_server_appliances'] = self.oneview_client.os_deployment_servers.get_appliances()
        if options.get('appliance'):
            facts['os_deployment_server_appliance'] = self.oneview_client.os_deployment_servers.get_appliance_by_name(
                options.get('appliance'))

        return facts

    def __get_all(self):
        params = self.module.params.get('params') or {}
        return self.oneview_client.os_deployment_servers.get_all(**params)


def main():
    OsDeploymentServerFactsModule().run()


if __name__ == '__main__':
    main()
