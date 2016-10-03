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
from hpOneView.oneview_client import OneViewClient
from hpOneView.common import transform_list_to_dict


DOCUMENTATION = '''
---
module: oneview_enclosure_facts
short_description: Retrieve facts about one or more Enclosures.
description:
    - Retrieve facts about one or more of the Enclosures from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an Enclosure and related resources.
          Options allowed: script, environmentalConfiguration, and utilization. For the option utilization, you can
          provide specific parameters."
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Enclosures
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"

- debug: var=enclosures

- name: Gather facts about an Enclosure by name
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Enclosure-Name"
  delegate_to: localhost

- debug: var=enclosures

- name: Gather facts about an Enclosure by name with options
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: 'Test-Enclosure'
    options:
      - script                       # optional
      - environmentalConfiguration   # optional
      - utilization                  # optional
  delegate_to: localhost

- debug: var=enclosures
- debug: var=enclosure_script
- debug: var=enclosure_environmental_configuration
- debug: var=enclosure_utilization

- name: "Gather facts about an Enclosure with temperature data at a resolution of one sample per day, between two
         specified dates"
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: 'Test-Enclosure'
    options:
      - utilization                  # optional
          fields: 'AmbientTemperature'
          filter:
            - "startDate=2016-07-01T14:29:42.000Z"
            - "endDate=2017-07-01T03:29:42.000Z"
          view: 'day'
          refresh: False
  delegate_to: localhost

- debug: var=enclosures
- debug: var=enclosure_utilization
'''

RETURN = '''
enclosures:
    description: Has all the OneView facts about the Enclosures.
    returned: always, but can be null
    type: complex

enclosure_script:
    description: Has all the OneView facts about the script of an Enclosure.
    returned: when requested, but can be null
    type: complex

enclosure_environmental_configuration:
    description: Has all the OneView facts about the environmental configuration of an Enclosure.
    returned: when requested, but can be null
    type: complex

enclosure_utilization:
    description: Has all the OneView facts about the utilization of an Enclosure.
    returned: when requested, but can be null
    type: complex
'''


class EnclosureFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            ansible_facts = {}

            if self.module.params['name']:
                enclosures = self.__get_by_name(self.module.params['name'])

                if self.module.params.get('options') and enclosures:
                    ansible_facts = self.__gather_optional_facts(self.module.params['options'], enclosures[0])
            else:
                enclosures = self.__get_all()

            ansible_facts['enclosures'] = enclosures

            self.module.exit_json(changed=False,
                                  ansible_facts=ansible_facts)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __gather_optional_facts(self, options, enclosure):

        options = transform_list_to_dict(options)

        enclosure_client = self.oneview_client.enclosures
        ansible_facts = {}

        if options.get('script'):
            ansible_facts['enclosure_script'] = enclosure_client.get_script(enclosure['uri'])
        if options.get('environmentalConfiguration'):
            env_config = enclosure_client.get_environmental_configuration(enclosure['uri'])
            ansible_facts['enclosure_environmental_configuration'] = env_config
        if options.get('utilization'):
            ansible_facts['enclosure_utilization'] = self.__get_utilization(enclosure, options['utilization'])

        return ansible_facts

    def __get_utilization(self, enclosure, params):
        fields = view = refresh = filter = ''

        if isinstance(params, dict):
            fields = params.get('fields')
            view = params.get('view')
            refresh = params.get('refresh')
            filter = params.get('filter')

        return self.oneview_client.enclosures.get_utilization(enclosure['uri'],
                                                              fields=fields,
                                                              filter=filter,
                                                              refresh=refresh,
                                                              view=view)

    def __get_by_name(self, name):
        return self.oneview_client.enclosures.get_by('name', name)

    def __get_all(self):
        return self.oneview_client.enclosures.get_all()


def main():
    EnclosureFactsModule().run()


if __name__ == '__main__':
    main()
