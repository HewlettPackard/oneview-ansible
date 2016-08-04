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


DOCUMENTATION = '''
---
module: oneview_enclosure_utilization_facts
short_description: Retrieve the facts about the utilization of one enclosure.
description:
    - Retrieve the facts about the historical utilization data, metrics, and time span of the enclosure resource.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Enclosure name.
      required: true
    fields:
      description:
        - "Name of the metric(s) to be retrieved in the format METRIC[,METRIC]... Enclosures support the following
          utilization metrics: AmbientTemperature, AveragePower, PeakPower, PowerCap, DeratedCapacity and RatedCapacity.
          If unspecified, all metrics supported are returned."
      required: false
    startDate:
      description:
        - Start date of requested starting time range in ISO 8601 format.
      required: false
    endDate:
      description:
        - End date of requested starting time range in ISO 8601 format. When omitted the endDate includes
          the latest data sample available.
      required: false
    view:
      description:
        - Specifies the resolution interval length of the samples to be retrieved.
      required: false
      choices: ['native', 'hour', 'day']
    refresh:
      description:
        - Specifies that if necessary an additional request will be queued to obtain the most recent utilization
          data from the enclosure.
      required: false

notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: "Gather facts about the 24 hours of data for all available metrics at a resolution of one sample
         every 5 minutes for the enclosure named 'Test-Enclosure'"
  oneview_enclosure_utilization_facts:
    config: "{{ config }}"
    name: 'Test-Enclosure'
    delegate_to: localhost

- debug: var=oneview_enclosure_utilization

- name: "Gather facts about all temperature data at a resolution of one sample per day for the enclosure
         named 'Test-Enclosure', between two specified dates"
  oneview_enclosure_utilization_facts:
    config: "{{ config }}"
    name: 'Test-Enclosure'
    fields: 'AmbientTemperature
    start_date: '2016-06-30T03:29:42.000Z'
    end_date: '2018-07-01T03:29:42.000Z'
    view: 'day'
    refresh: False
delegate_to: localhost

- debug: var=oneview_enclosure_utilization
'''

RETURN = '''
oneview_enclosure_utilization:
    description: Has all the OneView facts about the utilization of one enclosure.
    returned: always, but can be null
    type: complex
'''


ENCLOSURE_NOT_FOUND = 'Enclosure not found.'


class EnclosureUtilizationFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=True, type='str'),
        fields=dict(required=False, type='str'),
        start_date=dict(required=False, type='str'),
        end_date=dict(required=False, type='str'),
        view=dict(required=False, type='str', choices=['native', 'hour', 'day']),
        refresh=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            enclosure = self.__get_by_name(self.module.params['name'])

            fields = self.module.params['fields']
            view = self.module.params['view']
            refresh = self.module.params['refresh']
            filter = self.__build_filter()

            if enclosure:
                utilization = self.oneview_client.enclosures.get_utilization(enclosure['uri'],
                                                                             fields=fields,
                                                                             filter=filter,
                                                                             view=view,
                                                                             refresh=refresh)
                self.module.exit_json(changed=False,
                                      ansible_facts=dict(oneview_enclosure_utilization=utilization))
            else:
                self.module.exit_json(changed=False,
                                      ansible_facts=dict(oneview_enclosure_utilization=None),
                                      msg=ENCLOSURE_NOT_FOUND)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __get_by_name(self, name):
        result = self.oneview_client.enclosures.get_by('name', name)
        return result[0] if result else None

    def __build_filter(self):
        start_date = self.module.params['start_date']
        end_date = self.module.params['end_date']

        if not start_date and not end_date:
            return None

        start_date_query = ('startDate=' + start_date) if start_date else ''
        end_date_query = ('endDate=' + end_date) if end_date else ''
        separator = ',' if (start_date_query and end_date_query) else ''

        return '{0}{1}{2}'.format(start_date_query, separator, end_date_query)


def main():
    EnclosureUtilizationFactsModule().run()


if __name__ == '__main__':
    main()
