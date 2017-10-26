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


from ansible.compat.tests import unittest, mock
from oneview_module_loader import SwitchModule
from hpe_test_utils import OneViewBaseTestCase

SWITCH_NAME = "172.18.16.2"

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    name=SWITCH_NAME,
    data=dict(scopeUris=['/rest/scopes/fake'])
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    name=SWITCH_NAME
)

PARAMS_PORTS_UPDATED = dict(
    config='config.json',
    state='ports_updated',
    name=SWITCH_NAME,
    data=dict(
        ports=[dict(
               portId="ca520119-1329-496b-8e44-43092e937eae:1.21",
               portName="1.21",
               enabled=True
               )
               ]
    )
)

SWITCH = dict(
    name=SWITCH_NAME,
    uri="/rest/switches/ca520119-1329-496b-8e44-43092e937eae",
    scopeUris=[]
)


class SwitchModuleSpec(unittest.TestCase,
                       OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, SwitchModule)
        self.resource = self.mock_ov_client.switches

    def test_should_remove_switch(self):
        self.resource.get_by.return_value = [SWITCH]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SwitchModule.MSG_DELETED
        )

    def test_should_do_nothing_when_switch_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SwitchModule.MSG_ALREADY_ABSENT
        )

    def test_should_update_switch_ports(self):
        self.resource.get_by.return_value = [SWITCH]
        self.mock_ansible_module.params = PARAMS_PORTS_UPDATED

        SwitchModule().run()

        self.resource.update_ports.assert_called_once_with(
            id_or_uri=SWITCH["uri"],
            ports=PARAMS_PORTS_UPDATED["data"]['ports']
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SwitchModule.MSG_PORTS_UPDATED
        )

    def test_should_fail_when_switch_not_found_on_update_ports(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_PORTS_UPDATED

        SwitchModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SwitchModule.MSG_NOT_FOUND)

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = SWITCH.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/switches/fake'
        self.resource.get_by.return_value = [resource_data]

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        self.resource.patch.return_value = patch_return

        SwitchModule().run()

        self.resource.patch.assert_called_once_with('rest/switches/fake',
                                                    operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(switch=patch_return),
            msg=SwitchModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = SWITCH.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.get_by.return_value = [resource_data]

        SwitchModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switch=resource_data),
            msg=SwitchModule.MSG_ALREADY_PRESENT
        )


if __name__ == '__main__':
    unittest.main()
