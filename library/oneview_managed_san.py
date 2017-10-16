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
module: oneview_managed_san
short_description: Manage OneView Managed SAN resources.
description:
    - "Provides an interface to manage Managed SAN resources. Can update the Managed SAN, set the refresh state, create
       a SAN endpoints CSV file, and create an unexpected zoning issue report."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Managed SAN resource.
              C(present) ensures data properties are compliant with OneView.
              C(refresh_state_set) updates the refresh state of the Managed SAN.
              C(endpoints_csv_file_created) creates a SAN endpoints CSV file.
              C(issues_report_created) creates an unexpected zoning report for a SAN.
        choices: ['present', 'refresh_state_set', 'endpoints_csv_file_created', 'issues_report_created']
        required: true
    data:
        description:
            - "List with Managed SAN properties and its associated states.
               Warning: For the 'present' state, the contents of the publicAttributes will replace the existing list, so
               leaving out a public attribute from the given list will effectively delete it."
        required: true

extends_documentation_fragment:
    - oneview
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
    type: dict

managed_san_endpoints:
    description: Has the OneView facts about the Endpoints CSV File created.
    returned: On state 'endpoints_csv_file_created'. Can be null.
    type: dict

managed_san_issues:
    description: Has the OneView facts about the unexpected zoning report created.
    returned: On state 'issues_report_created'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound, ResourceComparator


class ManagedSanModule(OneViewModuleBase):
    MSG_UPDATED = 'Managed SAN updated successfully.'
    MSG_REFRESH_STATE_UPDATED = 'Managed SAN\'s refresh state changed successfully.'
    MSG_NOT_FOUND = 'Managed SAN was not found for this operation.'
    MSG_NO_CHANGES_PROVIDED = 'The Managed SAN is already compliant.'
    MSG_ENDPOINTS_CSV_FILE_CREATED = 'SAN endpoints CSV file created successfully.'
    MSG_ISSUES_REPORT_CREATED = 'Unexpected zoning report created successfully.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'refresh_state_set', 'endpoints_csv_file_created', 'issues_report_created']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(ManagedSanModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        resource = self.__get_resource(self.data)

        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)

        if self.state == 'present':
            exit_status = self.__update(self.data, resource)
        elif self.state == 'refresh_state_set':
            exit_status = self.__set_refresh_state(self.data, resource)
        elif self.state == 'endpoints_csv_file_created':
            exit_status = self.__create_endpoints_csv_file(resource)
        elif self.state == 'issues_report_created':
            exit_status = self.__create_issue_report(resource)

        return dict(exit_status)

    def __get_resource(self, data):
        return self.oneview_client.managed_sans.get_by_name(data['name'])

    def __update(self, data, resource):
        merged_data = resource.copy()
        merged_data.update(data)

        if ResourceComparator.compare(resource, merged_data):
            changed = False
            msg = self.MSG_NO_CHANGES_PROVIDED
        else:
            changed = True
            resource = self.oneview_client.managed_sans.update(resource['uri'], data)
            msg = self.MSG_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(managed_san=resource))

    def __set_refresh_state(self, data, resource):
        resource = self.oneview_client.managed_sans.update(resource['uri'], data['refreshStateData'])

        return dict(changed=True,
                    msg=self.MSG_REFRESH_STATE_UPDATED,
                    ansible_facts=dict(managed_san=resource))

    def __create_endpoints_csv_file(self, resource):
        resource = self.oneview_client.managed_sans.create_endpoints_csv_file(resource['uri'])

        return dict(changed=True,
                    msg=self.MSG_ENDPOINTS_CSV_FILE_CREATED,
                    ansible_facts=dict(managed_san_endpoints=resource))

    def __create_issue_report(self, resource):
        resource = self.oneview_client.managed_sans.create_issues_report(resource['uri'])

        return dict(changed=True,
                    msg=self.MSG_ISSUES_REPORT_CREATED,
                    ansible_facts=dict(managed_san_issues=resource))


def main():
    ManagedSanModule().run()


if __name__ == '__main__':
    main()
