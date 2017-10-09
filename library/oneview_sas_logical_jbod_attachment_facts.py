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
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_sas_logical_jbod_attachment_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical JBOD Attachments.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the SAS Logical JBOD Attachments from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0"
author: "Abilio Parada (@abiliogp)"
options:
    name:
      description:
        - Name of SAS Logical JBOD Attachment.
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical JBOD Attachment
  oneview_sas_logical_jbod_attachment_facts:
  config: "{{ config_path }}"

- debug: var=sas_logical_jbod_attachments

- name: Gather paginated, filtered and sorted facts about SAS Logical JBOD Attachment
  oneview_sas_logical_jbod_attachment_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "state=Deployed"

- debug: var=sas_logical_jbod_attachments


- name: Gather facts about a SAS Logical JBOD Attachment by name
  oneview_sas_logical_jbod_attachment_facts:
    config: "{{ config_path }}"
    name: "logical-enclosure-SAS-Logical-Interconnect-Group-BDD-1-SLJA-1"

- debug: var=sas_logical_jbod_attachments
'''

RETURN = '''
sas_logical_jbod_attachments:
    description: Has all the OneView facts about the SAS Logical JBOD Attachment.
    returned: Always, but can be null.
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase


class SasLogicalJbodAttachmentFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(SasLogicalJbodAttachmentFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        if self.module.params['name']:
            name = self.module.params['name']
            resources = self.oneview_client.sas_logical_jbod_attachments.get_by('name', name)
        else:
            resources = self.oneview_client.sas_logical_jbod_attachments.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(sas_logical_jbod_attachments=resources))


def main():
    SasLogicalJbodAttachmentFactsModule().run()


if __name__ == '__main__':
    main()
