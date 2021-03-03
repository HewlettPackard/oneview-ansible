#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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

import mock
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import IdPoolsIpv4SubnetModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SUBNET_TEMPLATE = dict(
    name='Ipv4Subnet',
    uri='/rest/subnet/test',
    type='Subnet',
    domain='example.com'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'])
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

PARAMS_FOR_COLLECT = dict(
    config='config.json',
    state='collect',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'],
              idList=['10.1.1.1', '10.1.1.2'],
              allocatorUri='/rest/fake')
)

PARAMS_FOR_ALLOCATE = dict(
    config='config.json',
    state='allocate',
    data=dict(name=DEFAULT_SUBNET_TEMPLATE['name'],
              count=2)
)


@pytest.mark.resource(TestIdPoolsIpv4SubnetModule='id_pools_ipv4_subnets')
class TestIdPoolsIpv4SubnetModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """
    def test_should_create_new_id_pools_ipv4_subnet(self):
        self.resource.get_by_name.return_value = None
        self.resource.create.return_value = self.resource
        self.resource.data = DEFAULT_SUBNET_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_CREATED,
            ansible_facts=dict(id_pools_ipv4_subnet=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_SUBNET_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_subnet=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_should_get_the_same_resource_by_name(self):
        self.resource.data = DEFAULT_SUBNET_TEMPLATE
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_subnet=DEFAULT_SUBNET_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SUBNET_TEMPLATE.copy()
        data_merged['domain'] = 'diffdomain.com'

        self.resource.data = data_merged
        self.resource.update.return_value = self.resource
        self.mock_ansible_module.check_mode = False

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_subnet=data_merged)
        )

    def test_should_allocate_when_valid_ids_present(self):
        data_merged = DEFAULT_SUBNET_TEMPLATE.copy()

        data_merged['count'] = 2
        self.resource.data = data_merged
        self.resource.get_by_name.return_value = self.resource
        self.resource.allocate.return_value = {'idList': ['172.9.0.1', '172.9.0.2']}

        self.mock_ansible_module.params = PARAMS_FOR_ALLOCATE

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_ALLOCATE,
            ansible_facts=dict(id_pools_ipv4_subnet={'idList': ['172.9.0.1', '172.9.0.2']})
        )

    def test_should_collect_when_valid_ids_allocated(self):
        data_merged = DEFAULT_SUBNET_TEMPLATE.copy()
        
        data_merged['idList'] = ['10.1.1.1', '10.1.1.2']
        data_merged['allocatorUri'] = '/rest/fake'
        self.resource.data = data_merged
        self.resource.get_by_name.return_value = self.resource
        self.resource.collect.return_value = {'idList': ['10.1.1.1', '10.1.1.1']}

        self.mock_ansible_module.params = PARAMS_FOR_COLLECT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_COLLECT,
            ansible_facts=dict(id_pools_ipv4_subnet=data_merged)
        )

    def test_should_remove_id_pools_ipv4_subnet(self):
        self.resource.data = DEFAULT_SUBNET_TEMPLATE
        self.resource.get_all.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4SubnetModule.MSG_DELETED
        )

    def test_should_do_nothing_when_id_pools_ipv4_subnet_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT
        self.mock_ansible_module.check_mode = True

        IdPoolsIpv4SubnetModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4SubnetModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
