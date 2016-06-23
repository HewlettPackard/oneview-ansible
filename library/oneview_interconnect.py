#!/usr/bin/python

###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient


DOCUMENTATION = '''
---
module: oneview_interconnect
short_description: Manage the OneView Interconnects resources.
description:
    - Provides an interface to manage the Interconnects power state and the UID light state. Can change power state,
    UID light state and perform device reset.
requirements:
    - "python 2.7.11"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Interconnect resource.
              'powered_on' turns the power on.
              'powered_off' turns the power off.
        choices: ['powered_on', 'powered_off']
    id:
      description:
        - Interconnect ID.
      required: true
notes:
    - A sample configuration file for the config parameter can be found at&colon;
      https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json
'''

EXAMPLES = '''
- name: Turn the power off for Interconnect e542bdab-c75f-4cf2-b89e-9a566849e292
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'powered_off'
    id: 'd9583219-2f06-4908-979f-66bde4b51294'
'''


class InterconnectModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['powered_on', 'powered_off']
        ),
        id=dict(required=True, type='str')
    )

    power_state_values = {
        'powered_on': 'On',
        'powered_off': 'Off'
    }

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        interconnect_id = self.module.params['id']

        try:
            resource = self.oneview_client.interconnects.patch(
                id_or_uri=interconnect_id,
                operation='replace',
                path='/powerState',
                value=self.power_state_values[state]
            )
            self.module.exit_json(
                changed=True,
                ansible_facts=dict(resource=resource)
            )
        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    InterconnectModule().run()


if __name__ == '__main__':
    main()
