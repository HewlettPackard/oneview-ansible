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

class ModuleDocFragment(object):
    # OneView doc fragment
    DOCUMENTATION = '''
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false

notes:
    - "A sample configuration file for the config parameter can be found at:
       U(https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json)"
    - "Check how to use environment variables for configuration at:
       U(https://github.com/HewlettPackard/oneview-ansible#environment-variables)"
    - "Additional Playbooks for the HPE OneView Ansible modules can be found at:
       U(https://github.com/HewlettPackard/oneview-ansible/tree/master/examples)"
    '''

    VALIDATEETAG = '''
options:
    validate_etag:
        description:
            - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
                for the resource matches the ETag provided in the data.
        default: true
        choices: ['true', 'false']
'''

    FACTSPARAMS = '''
options:
    params:
        description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
            C(start): The first item to return, using 0-based indexing.
            C(count): The number of resources to return.
            C(filter): A general filter/query string to narrow the list of items returned.
            C(sort): The sort order of the returned data set."
        required: false
'''
