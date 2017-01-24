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
    from hpOneView.common import transform_list_to_dict
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_power_device_facts
short_description: Retrieve facts about the OneView Power Devices.
description:
    - Retrieve facts about the Power Delivery Devices from OneView.
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
    name:
      description:
        - Power Device name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Power Device.
          Options allowed: powerState, uidState, utilization"
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           'start': The first item to return, using 0-based indexing.
           'count': The number of resources to return.
           'filter': A general filter/query string to narrow the list of items returned.
           'query': A general query string to narrow the list of resources returned.
           'sort': The sort order of the returned data set."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all Power Devices
  oneview_power_device_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: msg="{{power_devices | map(attribute='name') | list }}"

- name:  Gather paginated, filtered and sorted facts about Power Devices
  oneview_power_device_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state='Unmanaged'
      query: feedIdentifier eq 'A'
  delegate_to: localhost
- debug: var=power_devices

- name: Gather facts about a Power Device by name
  oneview_power_device_facts:
    config: "{{ config }}"
    name: "Power Device Name"
  delegate_to: localhost
- debug: var=power_devices

- name: Gather facts about the power state of a Power Device
  oneview_power_device_facts:
    config: "{{ config }}"
    name: "Power Device Name"
    options:
      - powerState            # optional
  delegate_to: localhost
- debug: msg="{{power_devices | map(attribute='name') | list }}"
- debug: var=power_device_power_state

- name: Gather all facts about a Power Device with all options
  oneview_power_device_facts:
   config: "{{ config }}"
   name : "Power Device Name"
   options:
       - powerState             # optional
       - uidState               # optional
       - utilization:           # optional
                fields : 'AveragePower'
                filter : ['startDate=2016-05-30T03:29:42.000Z']
                view : 'day'
  delegate_to: localhost

- debug: msg="{{power_devices | map(attribute='name') | list }}"
- debug: var=power_device_power_state
- debug: var=power_device_uid_state
- debug: var=power_device_utilization
'''

RETURN = '''
power_devices:
    description: Has all the OneView facts about the Power Device.
    returned: Always, but can be null.
    type: complex

power_device_power_state:
    description: Has all the facts about the Power state of the Power Device.
    returned: When requested, but can be null.
    type: complex

power_device_uid_state:
    description: Has all the facts about the Power Device UID state.
    returned: When requested, but can be null.
    type: complex

power_device_utilization:
    description: Has all the facts about the Power Device utilization.
    returned: When requested, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class PowerDeviceFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

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

            ansible_facts = {}

            if self.module.params.get('name'):
                power_devices = self.oneview_client.power_devices.get_by("name", self.module.params['name'])

                if self.module.params.get('options') and power_devices:
                    ansible_facts = self.gather_option_facts(self.module.params['options'], power_devices[0])
            else:
                params = self.module.params.get('params') or {}
                power_devices = self.oneview_client.power_devices.get_all(**params)

            ansible_facts["power_devices"] = power_devices

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def gather_option_facts(self, options, power_device):

        options = transform_list_to_dict(options)

        srv_hw_client = self.oneview_client.power_devices
        ansible_facts = {}

        if options.get('powerState'):
            ansible_facts['power_device_power_state'] = srv_hw_client.get_power_state(power_device['uri'])
        if options.get('uidState'):
            ansible_facts['power_device_uid_state'] = srv_hw_client.get_uid_state(power_device['uri'])
        if options.get('utilization'):
            ansible_facts['power_device_utilization'] = self.get_utilization(power_device, options['utilization'])

        return ansible_facts

    def get_utilization(self, power_device, data):

        fields = view = refresh = filter = ''

        if isinstance(data, dict):
            fields = data.get('fields')
            view = data.get('view')
            refresh = data.get('refresh')
            filter = data.get('filter')

        return self.oneview_client.power_devices.get_utilization(power_device['uri'],
                                                                 fields=fields,
                                                                 filter=filter,
                                                                 refresh=refresh,
                                                                 view=view)


def main():
    PowerDeviceFactsModule().run()


if __name__ == '__main__':
    main()
