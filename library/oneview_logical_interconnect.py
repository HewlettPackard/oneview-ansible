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
from hpOneView.common import resource_compare


DOCUMENTATION = '''
---
module: oneview_logical_interconnect
short_description: Manage OneView Logical Interconnect resources.
description:
    - Provides an interface to manage Logical Interconnect resources.
      Have support to return logical interconnects to a consistent state and update the Ethernet interconnect settings
      for the logical interconnect.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Logical Interconnect resource.
              'compliant' brings the logical interconnect back to a consistent state.
              'ethernet_settings_updated' updates the Ethernet interconnect settings for the logical interconnect.
        choices: ['compliant', 'ethernet_settings_updated']
    data:
      description:
        - List with the options.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
'''

EXAMPLES = '''
- name: Return the logical interconnect to a consistent state
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: compliant
    data:
      name: 'Name of the Logical Interconnect'
'''

LOGICAL_INTERCONNECT_CONSISTENT = 'logical interconnect returned to a consistent state.'
LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED = 'Ethernet settings updated successfully.'
LOGICAL_INTERCONNECT_NOT_FOUND = 'Logical Interconnect not found.'
LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED = 'Nothing to do.'


class LogicalInterconnectModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['compliant', 'ethernet_settings_updated']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):

        state = self.module.params['state']
        data = self.module.params['data']

        try:
            resource = self.__get_by_name(data)
            if state == 'compliant':
                self.__compliance(resource)
            if state == 'ethernet_settings_updated':
                self.__update_ethernet_settings(resource, data)

        except Exception as exception:
            self.module.fail_json(msg=exception.message)

    def __compliance(self, resource):
        if resource:
            li = self.oneview_client.logical_interconnects.update_compliance(resource['uri'])
            self.module.exit_json(changed=True,
                                  msg=LOGICAL_INTERCONNECT_CONSISTENT,
                                  ansible_facts=dict(logical_interconnect=li))
        else:
            raise Exception(LOGICAL_INTERCONNECT_NOT_FOUND)

    def __update_ethernet_settings(self, resource, data):
        if resource:
            ethernet_settings_merged = resource['ethernetSettings'].copy()
            ethernet_settings_merged.update(data['ethernetSettings'])

            if resource_compare(resource['ethernetSettings'], ethernet_settings_merged):
                self.module.exit_json(changed=False,
                                      msg=LOGICAL_INTERCONNECT_NO_CHANGES_PROVIDED)
            else:
                li = self.oneview_client.logical_interconnects.update_ethernet_settings(resource['uri'],
                                                                                        ethernet_settings_merged)
                self.module.exit_json(changed=True,
                                      msg=LOGICAL_INTERCONNECT_ETH_SETTINGS_UPDATED,
                                      ansible_facts=dict(logical_interconnect=li))
        else:
            raise Exception(LOGICAL_INTERCONNECT_NOT_FOUND)

    def __get_by_name(self, data):
        return self.oneview_client.logical_interconnects.get_by_name(data['name'])


def main():
    LogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
