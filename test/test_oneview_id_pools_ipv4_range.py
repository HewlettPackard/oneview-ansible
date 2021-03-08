#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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

import pytest
import mock

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import IdPoolsIpv4RangeModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_RANGE_TEMPLATE = dict(
    name='Ipv4Range',
    uri='rest/range/test',
    subnetUri='rest/subnet/test',
    type='Range',
    enabled=True,
    gateway='10.10.0.1'
)

DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector = dict(
    name='Ipv4Range',
    uri='rest/range/test',
    subnetUri='rest/subnet/test',
    idList=['10.0.0.0', '10.1.1.1'],
    type='Range',
    enabled=True,
    gateway='10.10.0.1'
)

DEFAULT_NOT_RANGE_TEMPLATE = dict(
    name='NOTIpv4Range',
    uri='rest/range/useless',
    subnetUri='rest/subnet/test',
    type='Range',
    gateway='10.3.3.1'
)

DEFAULT_SUBNET_TEMPLATE = dict(
    name='Ipv4Range',
    uri='rest/subnet/test',
    type='Subnet',
    rangeUris=['rest/range/useless', 'rest/range/test']
)

PARAMS_FOR_PRESENT_WITH_URI = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE['uri'])
)

PARAMS_FOR_PRESENT_NAME_SUBNET = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_RANGE_TEMPLATE['name'], subnetUri=DEFAULT_RANGE_TEMPLATE['subnetUri'])
)

PARAMS_FOR_INVALID = dict(
    config='config.json',
    state='present',
    data=dict(type=DEFAULT_RANGE_TEMPLATE['type'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE['uri'],
              newName='newRangeName')
)

PARAMS_FOR_ENABLE_NO_CHANGE = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE['uri'],
              enabled=True)
)

PARAMS_FOR_COLLECTOR = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector['uri'],
              idList=['10.0.0.0', '10.1.1.1'],
              update_collector=True)
)

PARAMS_FOR_ALLOCATOR = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector['uri'],
              idList=['10.0.0.0', '10.1.1.1'],
              count=2,
              update_allocator=True)
)

PARAMS_FOR_ENABLE_EDIT = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_RANGE_TEMPLATE['uri'],
              enabled=False)
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_RANGE_TEMPLATE['name'], subnetUri=DEFAULT_RANGE_TEMPLATE['subnetUri'])
)


@pytest.mark.resource(TestIdPoolsIpv4RangeModule='id_pools_ipv4_ranges')
class TestIdPoolsIpv4RangeModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_id_pools_ipv4_range(self):

        self.mock_ov_client.id_pools_ipv4_subnets.get.return_value = DEFAULT_SUBNET_TEMPLATE
        self.mock_ov_client.id_pools_ipv4_ranges.get_by_uri().data = DEFAULT_NOT_RANGE_TEMPLATE
        self.resource.data = DEFAULT_RANGE_TEMPLATE
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_NAME_SUBNET

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_CREATED,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE)
        )

    def test_should_not_update_when_data_is_the_same(self):
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE
        self.resource.data = DEFAULT_RANGE_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_WITH_URI

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4RangeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE)
        )

    def test_should_update_when_data_is_different(self):
        new_data = DEFAULT_RANGE_TEMPLATE.copy()
        new_data['name'] = 'newRangeName'
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE
        self.resource.data = new_data
        self.resource.update.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE)
        )

    def test_should_not_enable_when_it_is_already_enabled(self):
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ENABLE_NO_CHANGE

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4RangeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE)
        )

    def test_should_disable_when_it_is_enabled(self):
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE

        new_data = DEFAULT_RANGE_TEMPLATE.copy()
        new_data['enabled'] = False

        self.resource.enable.return_value = new_data

        self.mock_ansible_module.params = PARAMS_FOR_ENABLE_EDIT

        IdPoolsIpv4RangeModule().run()

        self.resource.enable.assert_called_once_with(dict(type='Range', enabled=False), DEFAULT_RANGE_TEMPLATE['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_range=new_data)
        )

    def test_should_collect_id_back_from_ip_range(self):
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector
        self.resource.update_collector.return_value = DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector
        self.mock_ansible_module.params = PARAMS_FOR_COLLECTOR

        IdPoolsIpv4RangeModule().run()

        self.resource.update_collector.assert_called_once_with(dict(idList=['10.0.0.0', '10.1.1.1']), DEFAULT_RANGE_TEMPLATE['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector)
        )

    def test_should_allocate_id_to_ip_range(self):
        self.resource.get_by_uri().data = DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector
        self.resource.update_allocator.return_value = DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector
        self.mock_ansible_module.params = PARAMS_FOR_ALLOCATOR

        IdPoolsIpv4RangeModule().run()

        self.resource.update_allocator.assert_called_once_with(dict(idList=['10.0.0.0', '10.1.1.1'], count=2), DEFAULT_RANGE_TEMPLATE['uri'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_UPDATED,
            ansible_facts=dict(id_pools_ipv4_range=DEFAULT_RANGE_TEMPLATE_Alocator_and_Collector)
        )

    def test_should_delete_the_ipv4_range_when_it_exists(self):
        self.resource.get_by_uri.return_value = self.resource
        self.resource.data = DEFAULT_SUBNET_TEMPLATE
        obj = mock.Mock()
        obj.data = DEFAULT_RANGE_TEMPLATE
        self.mock_ov_client.id_pools_ipv4_subnets.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsIpv4RangeModule.MSG_DELETED
        )

    def test_should_not_delete_when_id_pools_ipv4_range_do_not_exist(self):
        self.resource.get_by_uri.return_value = DEFAULT_SUBNET_TEMPLATE
        self.resource.data = DEFAULT_SUBNET_TEMPLATE
        self.resource.get_by_uri.side_effect = [DEFAULT_NOT_RANGE_TEMPLATE, DEFAULT_NOT_RANGE_TEMPLATE]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        IdPoolsIpv4RangeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsIpv4RangeModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
