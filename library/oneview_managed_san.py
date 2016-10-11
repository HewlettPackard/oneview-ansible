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
    from hpOneView.common import resource_compare

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_managed_san
short_description: Manage OneView Managed SAN resources.
description:
    - "Provides an interface to manage Managed SAN resources. Can update the Managed SAN, set the refresh state, create
       a SAN endpoints CSV file, and create an unexpected zoning issue report."
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
        description:
            - Path to a .json configuration file containing the OneView client configuration.
        required: true
    state:
        description:
            - Indicates the desired state for the Managed SAN resource.
              'present' ensures data properties are compliant with OneView.
              'refresh_state_set' updates the refresh state of the Managed SAN.
              'endpoints_csv_file_created' creates a SAN endpoints CSV file.
              'issues_report_created' creates an unexpected zoning report for a SAN.
        choices: ['present', 'refresh_state_set', 'endpoints_csv_file_created', 'issues_report_created']
        required: true
    data:
        description:
            - "List with Managed SAN properties and its associated states.
               Warning: For the 'present' state, the contents of the publicAttributes will replace the existing list, so
               leaving out a public attribute from the given list will effectively delete it."
        required: true
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
  - name: Refresh the Managed SAN
    oneview_managed_san:
      config: '{{ config_path }}'
      state: refresh_state_set
      data:
          name: 'SAN1_0'
          refreshStateData:
              refreshState: 'RefreshPending'
    delegate_to: localhost

  - name: Update the Managed SAN
    oneview_managed_san:
      config: '{{ config_path }}'
      state: present
      data:
          name: 'SAN1_0'
          publicAttributes:
            - name: 'MetaSan'
              value: 'Neon SAN'
              valueType: 'String'
              valueFormat: 'None'
          sanPolicy:
            zoningPolicy: 'SingleInitiatorAllTargets'
            zoneNameFormat: '{hostName}_{initiatorWwn}'
            enableAliasing: True
            initiatorNameFormat: '{hostName}_{initiatorWwn}'
            targetNameFormat: '{storageSystemName}_{targetName}'
            targetGroupNameFormat: '{storageSystemName}_{targetGroupName}'
    delegate_to: localhost

  - name: Create an endpoints CSV file for the SAN
    oneview_managed_san:
      config: '{{ config }}'
      state: endpoints_csv_file_created
      data:
          name: '{{ name }}'
    delegate_to: localhost

  - name: Create an unexpected zoning report for the SAN
    oneview_managed_san:
      config: '{{ config }}'
      state: issues_report_created
      data:
          name: '{{ name }}'
    delegate_to: localhost
'''

RETURN = '''
managed_san:
    description: Has the OneView facts about the Managed SAN.
    returned: On states 'present' and 'refresh_state_set'. Can be null.
    type: complex

managed_san_endpoints:
    description: Has the OneView facts about the Endpoints CSV File created.
    returned: On state 'endpoints_csv_file_created'. Can be null.
    type: complex

managed_san_issues:
    description: Has the OneView facts about the unexpected zoning report created.
    returned: On state 'issues_report_created'. Can be null.
    type: complex
'''

MANAGED_SAN_UPDATED = 'Managed SAN updated successfully.'
MANAGED_SAN_REFRESH_STATE_UPDATED = 'Managed SAN\'s refresh state changed successfully.'
MANAGED_SAN_NOT_FOUND = 'Managed SAN was not found for this operation.'
MANAGED_SAN_NO_CHANGES_PROVIDED = 'The Managed SAN is already compliant.'
MANAGED_SAN_ENDPOINTS_CSV_FILE_CREATED = 'SAN endpoints CSV file created successfully.'
MANAGED_SAN_ISSUES_REPORT_CREATED = 'Unexpected zoning report created successfully.'
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ManagedSanModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'refresh_state_set', 'endpoints_csv_file_created', 'issues_report_created']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=HPE_ONEVIEW_SDK_REQUIRED)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        try:
            state = self.module.params['state']
            data = self.module.params['data']

            resource = self.__get_resource(data)

            if not resource:
                raise Exception(MANAGED_SAN_NOT_FOUND)

            if state == 'present':
                exit_status = self.__update(data, resource)
            elif state == 'refresh_state_set':
                exit_status = self.__set_refresh_state(data, resource)
            elif state == 'endpoints_csv_file_created':
                exit_status = self.__create_endpoints_csv_file(resource)
            elif state == 'issues_report_created':
                exit_status = self.__create_issue_report(resource)

            self.module.exit_json(**exit_status)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __get_resource(self, data):
        return self.oneview_client.managed_sans.get_by_name(data['name'])

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)
        changed = False

        if resource_compare(resource, merged_data):
            changed = False
            msg = MANAGED_SAN_NO_CHANGES_PROVIDED
        else:
            changed = True
            resource = self.oneview_client.managed_sans.update(resource['uri'], data)
            msg = MANAGED_SAN_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(managed_san=resource))

    def __set_refresh_state(self, data, resource):
        resource = self.oneview_client.managed_sans.update(resource['uri'], data['refreshStateData'])

        return dict(changed=True,
                    msg=MANAGED_SAN_REFRESH_STATE_UPDATED,
                    ansible_facts=dict(managed_san=resource))

    def __create_endpoints_csv_file(self, resource):
        resource = self.oneview_client.managed_sans.create_endpoints_csv_file(resource['uri'])

        return dict(changed=True,
                    msg=MANAGED_SAN_ENDPOINTS_CSV_FILE_CREATED,
                    ansible_facts=dict(managed_san_endpoints=resource))

    def __create_issue_report(self, resource):
        resource = self.oneview_client.managed_sans.create_issues_report(resource['uri'])

        return dict(changed=True,
                    msg=MANAGED_SAN_ISSUES_REPORT_CREATED,
                    ansible_facts=dict(managed_san_issues=resource))


def main():
    ManagedSanModule().run()


if __name__ == '__main__':
    main()
