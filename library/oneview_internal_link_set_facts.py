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

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_internal_link_set_facts
short_description: Retrieve facts about the OneView Internal Link Sets.
description:
    - Retrieve facts about the Internal Link Sets from OneView. It is possible get all Internal Link Sets or filter
      by name.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
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
          'view': Return a specific subset of the attributes of the resource or collection, by specifying the name
          of a predefined view."
      required: false
    name:
      description:
        - Name of the Internal Link Set.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
    - This resource is available for API version 300 or later
'''

EXAMPLES = '''
- name: Gather facts about all Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"

- debug: var=internal_link_sets

- name: Gather paginated and sorted facts about Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    params:
      - start: 0
      - count: 3
      - sort: 'name:ascending'

- debug: var=internal_link_sets

- name: Gather facts about an Internal Link Set by name
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    name: "Internal Link Set Name"

- debug: var=internal_link_sets
'''

RETURN = '''
internal_link_sets:
    description: Has all the OneView facts about the Internal Link Sets.
    returned: Always, but can be null.
    type: complex
'''

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class InternalLinkSetFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        params=dict(required=False, type='list')

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
            if self.module.params.get('name'):
                internal_links = self.oneview_client.internal_link_sets.get_by('name', self.module.params.get('name'))
            else:
                params = self.module.params.get('params')
                get_all_params = transform_list_to_dict(params) if params else {}

                internal_links = self.oneview_client.internal_link_sets.get_all(**get_all_params)

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(internal_link_sets=internal_links))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    InternalLinkSetFactsModule().run()


if __name__ == '__main__':
    main()
