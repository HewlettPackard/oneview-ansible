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

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

DOCUMENTATION = '''
---
module: oneview_sas_logical_jbod_attachment_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical JBOD Attachments.
description:
    - Retrieve facts about one or more of the SAS Logical JBOD Attachments from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0"
author: "Abilio Parada (@abiliogp)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
    name:
      description:
        - Name of SAS Logical JBOD Attachment.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json"
    - "Check how to use environment variables for configuration at:
       https://github.com/HewlettPackard/oneview-ansible#environment-variables"
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical JBOD Attachment
    oneview_sas_logical_jbod_attachment_facts:
    config: "{{ config_path }}"

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
    type: complex
'''
HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class SasLogicalJbodAttachmentFactsModule(object):
    argument_spec = dict(
        config=dict(required=False, type='str'),
        name=dict(required=False, type='str')
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
        try:
            if self.module.params['name']:
                name = self.module.params['name']
                resources = self.oneview_client.sas_logical_jbod_attachments.get_by('name', name)
            else:
                resources = self.oneview_client.sas_logical_jbod_attachments.get_all()

            self.module.exit_json(changed=False,
                                  ansible_facts=dict(sas_logical_jbod_attachments=resources))

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


def main():
    SasLogicalJbodAttachmentFactsModule().run()


if __name__ == '__main__':
    main()
