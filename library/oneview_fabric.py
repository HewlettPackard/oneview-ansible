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
    from hpOneView.extras.comparators import resource_compare
    from hpOneView.exceptions import HPOneViewException
    from hpOneView.exceptions import HPOneViewResourceNotFound

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_fabric
short_description: Manage OneView Fabric resources.
description:
    - Provides an interface for managing fabrics in OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Andressa Cruz (@asserdna)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Fabric name.
      required: false
    data:
      description:
        - List with Fabrics properties.
      required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - "This module is only available on HPE Synergy."
'''

EXAMPLES = '''
- name: Update the range of the fabric
  oneview_fabric:
    config: '{{ config }}'
    state: reserved_vlan_range_updated
    data:
      name: '{{ name }}'
      reservedVlanRangeParameters:
        start: '300'
        length: '62'
'''

RETURN = '''
fabric:
    description: Has all the OneView facts about the Fabrics.
    returned: Always, but can be null.
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'
EXCEPTION_NO_RESOURCE = "Resource not found"
NO_CHANGE_FOUND = "No change found"


class FabricModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(required=True,
                   choices=['reserved_vlan_range_updated']),
        data=dict(required=True, type='dict')
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
        state = self.module.params['state']
        data = self.module.params['data']
        try:
            if state == 'reserved_vlan_range_updated':
                self.__reserved_vlan_range_updated(data)
        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __reserved_vlan_range_updated(self, data):
        resource = self.__get_by_name(data)
        if not resource:
            raise HPOneViewResourceNotFound(EXCEPTION_NO_RESOURCE)
        resource_vlan_range = resource.get('reservedVlanRange')
        merged_data = resource_vlan_range.copy()
        merged_data.update(data['reservedVlanRangeParameters'])

        if resource_compare(resource_vlan_range, merged_data):
            self.module.exit_json(changed=False,
                                  msg=NO_CHANGE_FOUND,
                                  ansible_facts=dict(fabric=resource))
        else:
            self.__update_vlan_range(data, resource)

    def __get_by_name(self, data):
        result = self.oneview_client.fabrics.get_by('name', data['name'])
        return result[0] if result else None

    def __update_vlan_range(self, data, resource):
        fabric_update = self.oneview_client.fabrics.update_reserved_vlan_range(
            resource["uri"],
            data["reservedVlanRangeParameters"])
        self.module.exit_json(changed=True,
                              ansible_facts=dict(fabric=fabric_update))


def main():
    FabricModule().run()


if __name__ == '__main__':
    main()
