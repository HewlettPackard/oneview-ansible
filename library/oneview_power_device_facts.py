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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_power_device_facts
short_description: Retrieve facts about the OneView Power Devices.
description:
    - Retrieve facts about the Power Delivery Devices from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Power Device name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Power Device.
          Options allowed: C(powerState), C(uidState), C(utilization)"
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           C(start): The first item to return, using 0-based indexing.
           C(count): The number of resources to return.
           C(filter): A general filter/query string to narrow the list of items returned.
           C(query): A general query string to narrow the list of resources returned.
           C(sort): The sort order of the returned data set."
      required: false

extends_documentation_fragment:
    - oneview
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
    type: dict

power_device_power_state:
    description: Has all the facts about the Power state of the Power Device.
    returned: When requested, but can be null.
    type: dict

power_device_uid_state:
    description: Has all the facts about the Power Device UID state.
    returned: When requested, but can be null.
    type: dict

power_device_utilization:
    description: Has all the facts about the Power Device utilization.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase


class PowerDeviceFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(PowerDeviceFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        ansible_facts = {}

        if self.module.params.get('name'):
            power_devices = self.oneview_client.power_devices.get_by("name", self.module.params['name'])

            if self.options and power_devices:
                ansible_facts = self.gather_option_facts(self.options, power_devices[0])
        else:
            power_devices = self.oneview_client.power_devices.get_all(**self.facts_params)

        ansible_facts["power_devices"] = power_devices

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def gather_option_facts(self, options, power_device):

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
