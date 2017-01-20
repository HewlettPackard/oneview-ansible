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
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_unmanaged_device_facts
short_description: Retrieve facts about one or more of the OneView Unmanaged Device.
description:
    - Retrieve facts about one or more of the Unmanaged Device from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
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
          'sort': The sort order of the returned data set."
      required: false
    name:
      description:
        - Unmanaged Device name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Unmanaged Device.
          Options allowed:
          'environmental_configuration' gets a description of the environmental configuration for the Unmnaged Device."
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Unmanaged Devices
  oneview_unmanaged_device_facts:
    config: "{{ config }}"

- debug: var=unmanaged_devices

- name: Gather paginated, filtered and sorted facts about Unmanaged Devices
  oneview_unmanaged_device_facts:
  config: "{{ config }}"
  params:
    start: 0
    count: 2
    sort: 'name:descending'
    filter: "status='Disabled'"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name with environmental configuration
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - environmental_configuration

- debug: var=unmanaged_device_environmental_configuration
'''

RETURN = '''
unmanaged_devices:
    description: The list of unmanaged devices.
    returned: Always, but can be null.
    type: list

unmanaged_device_environmental_configuration:
    description: The description of the environmental configuration for the logical interconnect.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class UnmanagedDeviceFactsModule(object):

    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type="list"),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            oneview_client = OneViewClient.from_environment_variables()
        else:
            oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.resource_client = oneview_client.unmanaged_devices

    def run(self):
        try:
            name = self.module.params["name"]
            facts = dict()

            if name:
                unmanaged_devices = self.resource_client.get_by('name', name)
                environmental_configuration = self.__get_environmental_configuration(unmanaged_devices)

                if environmental_configuration is not None:
                    facts["unmanaged_device_environmental_configuration"] = environmental_configuration
            else:
                params = self.module.params.get('params') or {}
                unmanaged_devices = self.resource_client.get_all(**params)

            facts["unmanaged_devices"] = unmanaged_devices
            self.module.exit_json(ansible_facts=facts)
        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_environmental_configuration(self, unmanaged_devices):
        environmental_configuration = None
        options = self.module.params["options"] or []

        if unmanaged_devices and "environmental_configuration" in options:
            unmanaged_device_uri = unmanaged_devices[0]["uri"]
            environmental_configuration = self.resource_client.get_environmental_configuration(
                id_or_uri=unmanaged_device_uri
            )

        return environmental_configuration


def main():
    UnmanagedDeviceFactsModule().run()


if __name__ == '__main__':
    main()
