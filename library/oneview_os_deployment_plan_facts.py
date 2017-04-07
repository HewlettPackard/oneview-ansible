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
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_os_deployment_plan_facts
short_description: Retrieve facts about one or more Os Deployment Plans.
description:
    - Retrieve facts about one or more of the Os Deployment Plans from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author:
    - Abilio Parada (@abiliogp)
    - Gustavo Hennig (@GustavoHennig)
options:
    name:
      description:
        - Os Deployment Plan name.
      required: false
    options:
      description:
        - "List with options to gather facts about OS Deployment Plan.
          Option allowed: C(osCustomAttributesForServerProfile)
          The option C(osCustomAttributesForServerProfile) retrieves the list of editable OS Custom Atributes, prepared
          for Server Profile use."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all OS Deployment Plans
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather paginated, filtered and sorted facts about OS Deployment Plans
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: deploymentApplianceIpv4='15.212.171.216'
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather facts about an OS Deployment Plan by name
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    name: "Deployment Plan"
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather facts about an OS Deployment Plan by name with OS Custom Attributes option
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    name: "Deployment Plan"
    options:
      # This option will generate an os_deployment_plan_custom_attributes facts in the Server Profile format.
      - osCustomAttributesForServerProfile
  delegate_to: localhost
- debug: var=os_deployment_plans
- debug: var=os_deployment_plan_custom_attributes
'''

RETURN = '''
os_deployment_plans:
    description: Has all the OneView facts about the Os Deployment Plans.
    returned: Always, but can be null.
    type: complex

os_deployment_plan_custom_attributes:
    description: Has the editable Custom Attribute facts of the Os Deployment Plans in the Server Profiles format.
    returned: When requested, but can be empty.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from module_utils.oneview import OneViewModuleBase
from six import iteritems


class OsDeploymentPlanFactsModule(OneViewModuleBase):
    argument_spec = {
        "name": {"required": False, "type": 'str'},
        "options": {"required": False, "type": 'list'},
        "params": {"required": False, "type": 'dict'},
    }

    def __init__(self):
        super(OsDeploymentPlanFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        ansible_facts = {}
        if self.module.params.get('name'):
            os_deployment_plans = self.oneview_client.os_deployment_plans.get_by('name', self.module.params['name'])

            if self.options and os_deployment_plans:
                option_facts = self._gather_option_facts(self.options, os_deployment_plans[0])
                ansible_facts.update(option_facts)

        else:
            os_deployment_plans = self.oneview_client.os_deployment_plans.get_all(**self.facts_params)

        ansible_facts['os_deployment_plans'] = os_deployment_plans

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _gather_option_facts(self, options, resource):

        ansible_facts = {}
        custom_attributes = []

        nic_names = []
        expected_attr_for_nic = {
            "connectionid": "",
            "dhcp": False,
            "ipv4disable": False,
            "networkuri": "",
            "constraint": "auto",
        }

        # It's just a cache to avoid iterate custom_attributes
        names_added_to_ca = {}

        if options.get('osCustomAttributesForServerProfile'):
            for item in resource['additionalParameters']:
                if item.get("caType") == "nic":
                    nic_names.append(item.get('name'))
                    continue

                if item.get("caEditable"):
                    custom_attributes.append({
                        "name": item.get('name'),
                        "value": item.get('value')
                    })
                    names_added_to_ca[item.get('name')] = item.get('value')

        for nic_name in nic_names:
            expected_attr_for_nic.pop("parameters", None)
            for ckey, cvalue in iteritems(expected_attr_for_nic):

                if ckey not in names_added_to_ca:
                    custom_attributes.append({
                        "name": nic_name + "." + ckey,
                        "value": cvalue
                    })

        ansible_facts['os_deployment_plan_custom_attributes'] = {
            "os_custom_attributes_for_server_profile": custom_attributes}

        return ansible_facts


def main():
    OsDeploymentPlanFactsModule().run()


if __name__ == '__main__':
    main()
