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
import unittest

from oneview_module_loader import IdPoolsIpv4SubnetModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SUBNET_TEMPLATE = dict(
    name='Ipv4Subnet',
    uri='rest/subnet/test',
    type='Subnet',
    domain='example.com'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'])
)

PARAMS_FOR_PRESENT_WITH_URI = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_SUBNET_TEMPLATE['uri'])
)

PARAMS_FOR_INVALID = dict(
    config='config.json',
    state='present',
    data=dict(type=DEFAULT_SUBNET_TEMPLATE['type'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'],
              domain='newdomain.com')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'])
)


class IdPoolsIpv4SubnetModuleSpec(unittest.TestCase,
                                  OneViewBaseTestCase):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, IdPoolsIpv4SubnetModule)
        self.resource = self.mock_ov_client.id_pools_ipv4_subnets

    def test_should_create_new_id_pools_ipv4_subnet(self):
        self.resource.get_all.return_value = []
        self.resource.create.return_value = DEFAULT_SUBNET_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_CREATED,
            ansible_facts=dict(id_pools_ipv4_subnets=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_all.return_value = [DEFAULT_SUBNET_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_subnets=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_should_get_the_same_resource_by_uri(self):
        self.resource.get.return_value = DEFAULT_SUBNET_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_WITH_URI

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_subnets=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_should_fail_with_missing_required_attributes(self):
        self.mock_ansible_module.params = PARAMS_FOR_INVALID

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=IdPoolsIpv4SubnetModule.MSG_VALUE_ERROR
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SUBNET_TEMPLATE.copy()
        data_merged['domain'] = 'newdomain.com'

        self.resource.get_all.return_value = [DEFAULT_SUBNET_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_subnets=data_merged)
        )

    def test_should_remove_id_pools_ipv4_subnet(self):
        self.resource.get_all.return_value = [DEFAULT_SUBNET_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_DELETED
        )

    def test_should_do_nothing_when_id_pools_ipv4_subnet_not_exist(self):
        self.resource.get_all.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
