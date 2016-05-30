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

FC_NETWORK_CREATED = 'FC Network created sucessfully.'
FC_NETWORK_ALREADY_EXIST = 'FC Network already exists.'


class FcNetworkModule(object):

    argument_spec = dict(
        oneview_host=dict(required=True, type='str'),
        username=dict(required=True, type='str'),
        password=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        template=dict(required=True, type='dict')
    )


    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec,
                                    supports_check_mode=False)
        self.oneview_client = OneViewClient(self.__get_config())


    def __get_config(self):
        return dict(
            ip=self.module.params['oneview_host'],
            credentials=dict(
                userName=self.module.params['username'],
                password=self.module.params['password']
            )
        )


    def run(self):
        state = self.module.params['state']
        template = self.module.params['template']

        if state != 'present':
            self.module.exit_json(changed=False)
        else:
            try:
                changed, message, facts = self.__present(template)
                self.module.exit_json(changed=changed,
                                      msg=message,
                                      ansible_facts=facts)
            except Exception as exception:
                self.module.fail_json(msg=exception.message)


    def __present(self, template):
        result = self.__get_by_name(template)

        if not result:
            msg, fc_network = self.__create(template)
            changed = True
        else:
            msg = FC_NETWORK_ALREADY_EXIST
            fc_network = result[0]
            changed = False

        facts = dict(fc_network=fc_network)

        return changed, msg, facts


    def __create(self, template):
        new_fc_network = self.oneview_client.fc_networks.create(template)
        return FC_NETWORK_CREATED, new_fc_network


    def __get_by_name(self, template):
        return self.oneview_client.fc_networks.get_by('name', template['name'])


def main():
    FcNetworkModule().run()


if __name__ == '__main__':
    main()
