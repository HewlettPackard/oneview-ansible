#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_enclosure_facts
short_description: Retrieve facts about one or more Enclosures
description:
    - Retrieve facts about one or more of the Enclosures from OneView.
version_added: "2.5"
requirements:
    - hpeOneView >= 5.0.0
author:
    - Felipe Bulsoni (@fgbulsoni)
    - Thiago Miotto (@tmiotto)
    - Adriane Cardozo (@adriane-cardozo)
options:
    name:
      description:
        - Enclosure name.
    options:
      description:
        - "List with options to gather additional facts about an Enclosure and related resources.
          Options allowed: C(script), C(environmentalConfiguration), and C(utilization). For the option C(utilization),
          you can provide specific parameters."

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Enclosures
  oneview_enclosure_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  no_log: true
  delegate_to: localhost
- debug: var=enclosures

- name: Gather paginated, filtered and sorted facts about Enclosures
  oneview_enclosure_facts:
    params:
      start: 0
      count: 3
      sort: name:descending
      filter: status=OK
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  no_log: true
  delegate_to: localhost
- debug: var=enclosures

- name: Gather facts about an Enclosure by name
  oneview_enclosure_facts:
    name: Enclosure-Name
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  no_log: true
  delegate_to: localhost
- debug: var=enclosures

- name: Gather facts about an Enclosure by name with options
  oneview_enclosure_facts:
    name: Test-Enclosure
    options:
      - script                       # optional
      - environmentalConfiguration   # optional
      - utilization                  # optional
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  no_log: true
  delegate_to: localhost
- debug: var=enclosures
- debug: var=enclosure_script
- debug: var=enclosure_environmental_configuration
- debug: var=enclosure_utilization

- name: "Gather facts about an Enclosure with temperature data at a resolution of one sample per day, between two
         specified dates"
  oneview_enclosure_facts:
    name: Test-Enclosure
    options:
      - utilization:                   # optional
          fields: AmbientTemperature
          filter:
            - startDate=2016-07-01T14:29:42.000Z
            - endDate=2017-07-01T03:29:42.000Z
          view: day
          refresh: false
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
  no_log: true
  delegate_to: localhost
- debug: var=enclosures
- debug: var=enclosure_utilization
'''

RETURN = '''
enclosures:
    description: Has all the OneView facts about the Enclosures.
    returned: Always, but can be null.
    type: dict

enclosure_script:
    description: Has all the OneView facts about the script of an Enclosure.
    returned: When requested, but can be null.
    type: string

enclosure_environmental_configuration:
    description: Has all the OneView facts about the environmental configuration of an Enclosure.
    returned: When requested, but can be null.
    type: dict

enclosure_utilization:
    description: Has all the OneView facts about the utilization of an Enclosure.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class EnclosureFactsModule(OneViewModule):
    argument_spec = dict(name=dict(type='str'), options=dict(type='list'), params=dict(type='dict'))

    def __init__(self):
        super(EnclosureFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.enclosures)

    def execute_module(self):

        ansible_facts = {}

        if self.current_resource:
            enclosures = [self.current_resource.data]
            if self.options:
                ansible_facts = self._gather_optional_facts(self.options)
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            enclosures = self.resource_client.get_all(**self.facts_params)
        else:
            enclosures = []

        ansible_facts['enclosures'] = enclosures

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _gather_optional_facts(self, options):

        ansible_facts = {}

        if options.get('script'):
            ansible_facts['enclosure_script'] = self.current_resource.get_script()
        if options.get('environmentalConfiguration'):
            env_config = self.current_resource.get_environmental_configuration()
            ansible_facts['enclosure_environmental_configuration'] = env_config
        if options.get('utilization'):
            ansible_facts['enclosure_utilization'] = self._get_utilization(options['utilization'])

        return ansible_facts

    def _get_utilization(self, params):
        fields = view = refresh = filter = ''
        if isinstance(params, dict):
            fields = params.get('fields')
            view = params.get('view')
            refresh = params.get('refresh')
            filter = params.get('filter')

        return self.current_resource.get_utilization(fields=fields,
                                                     filter=filter,
                                                     refresh=refresh,
                                                     view=view)


def main():
    EnclosureFactsModule().run()


if __name__ == '__main__':
    main()
