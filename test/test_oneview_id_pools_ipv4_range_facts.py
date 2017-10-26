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

from ansible.compat.tests import unittest
from oneview_module_loader import IdPoolsIpv4RangeFactsModule
from hpe_test_utils import OneViewBaseTestCase

ERROR_MSG = 'Fake message error'

DEFAULT_RANGE_TEMPLATE = dict(
    name='Ipv4Range',
    uri='rest/range/test',
    subnetUri='rest/subnet/test',
    type='Range',
    enabled=True,
    gateway='10.10.0.1'
)

DEFAULT_NOT_RANGE_TEMPLATE = dict(
    name='NOTIpv4Range',
    uri='rest/range/not',
    subnetUri='rest/subnet/test',
    type='Range',
    gateway='10.3.3.1'
)

DEFAULT_SUBNET_TEMPLATE_1 = dict(
    name='Ipv4Subnet1',
    uri='rest/subnet/test1',
    type='Subnet',
    rangeUris=['rest/range/not2', 'rest/range/not3']
)

DEFAULT_SUBNET_TEMPLATE_2 = dict(
    name='Ipv4Subnet2',
    uri='rest/subnet/test2',
    type='Subnet',
    rangeUris=['rest/range/test', 'rest/range/not4']
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_ALL_FROM_SUBNET = dict(
    config='config.json',
    subnetUri='rest/subnet/test2'
)

PARAMS_GET_BY_NAME_AND_SUBNET_URI = dict(
    config='config.json',
    name="Ipv4Range",
    subnetUri='rest/subnet/test2'
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri='/rest/ipv4-range/test'
)

PARAMS_GET_ALLOCATED_FRAGMENTS = dict(
    config='config.json',
    options=['allocatedFragments'],
    uri='/rest/ipv4-range/test'
)

PARAMS_GET_FREE_FRAGMENTS = dict(
    config='config.json',
    options=['freeFragments'],
    uri='/rest/ipv4-range/test'
)

ALL_SUBNETS = [DEFAULT_SUBNET_TEMPLATE_1.copy(), DEFAULT_SUBNET_TEMPLATE_2.copy()]


class IdPoolsIpv4RangeFactsSpec(unittest.TestCase,
                                OneViewBaseTestCase):

    def setUp(self):
        self.configure_mocks(self, IdPoolsIpv4RangeFactsModule)
        self.ranges = self.mock_ov_client.id_pools_ipv4_ranges
        self.subnets = self.mock_ov_client.id_pools_ipv4_subnets

    def test_should_get_all_id_pools_ipv4_ranges(self):
        self.subnets.get_all.return_value = ALL_SUBNETS
        range_1 = DEFAULT_RANGE_TEMPLATE.copy()
        range_2 = DEFAULT_NOT_RANGE_TEMPLATE.copy()
        range_2['name'] = range_2['name'] + '2'
        range_2['uri'] = range_2['uri'] + '2'
        range_3 = DEFAULT_NOT_RANGE_TEMPLATE.copy()
        range_3['name'] = range_3['name'] + '3'
        range_3['uri'] = range_3['uri'] + '3'
        range_4 = DEFAULT_NOT_RANGE_TEMPLATE.copy()
        range_4['name'] = range_4['name'] + '4'
        range_4['uri'] = range_4['uri'] + '4'
        ranges = [range_2, range_3, range_1, range_4]

        self.ranges.get.side_effect = ranges

        self.mock_ansible_module.params = PARAMS_GET_ALL

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=ranges)
        )

    def test_should_get_all_id_pools_ipv4_ranges_from_subnet(self):
        self.subnets.get.return_value = DEFAULT_SUBNET_TEMPLATE_2
        range_1 = DEFAULT_RANGE_TEMPLATE.copy()
        range_4 = DEFAULT_NOT_RANGE_TEMPLATE.copy()
        range_4['name'] = range_4['name'] + '4'
        range_4['uri'] = range_4['uri'] + '4'
        ranges = [range_1, range_4]

        self.ranges.get.side_effect = ranges

        self.mock_ansible_module.params = PARAMS_GET_ALL_FROM_SUBNET

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=ranges)
        )

    def test_should_get_id_pools_ipv4_range_from_subnet_and_name(self):
        self.subnets.get.return_value = DEFAULT_SUBNET_TEMPLATE_2

        range_1 = DEFAULT_RANGE_TEMPLATE.copy()
        range_4 = DEFAULT_NOT_RANGE_TEMPLATE.copy()
        range_4['name'] = range_4['name'] + '4'
        range_4['uri'] = range_4['uri'] + '4'
        ranges = [range_1, range_4]
        self.ranges.get.side_effect = ranges

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_AND_SUBNET_URI

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=[range_1])
        )

    def test_should_get_id_pools_ipv4_range_from_uri(self):
        self.ranges.get.return_value = DEFAULT_RANGE_TEMPLATE.copy()

        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=[DEFAULT_RANGE_TEMPLATE.copy()])
        )

    def test_should_get_id_pools_ipv4_ranges_allocated_fragments(self):
        self.ranges.get.return_value = DEFAULT_RANGE_TEMPLATE.copy()
        self.ranges.get_allocated_fragments.return_value = [{'frag': 'test'}]

        self.mock_ansible_module.params = PARAMS_GET_ALLOCATED_FRAGMENTS

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=[DEFAULT_RANGE_TEMPLATE.copy()],
                               id_pools_ipv4_ranges_allocated_fragments=[{'frag': 'test'}])
        )

    def test_should_get_id_pools_ipv4_ranges_free_fragments(self):
        self.ranges.get.return_value = DEFAULT_RANGE_TEMPLATE.copy()
        self.ranges.get_free_fragments.return_value = [{'frag': 'testfree'}]

        self.mock_ansible_module.params = PARAMS_GET_FREE_FRAGMENTS

        IdPoolsIpv4RangeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pools_ipv4_ranges=[DEFAULT_RANGE_TEMPLATE.copy()],
                               id_pools_ipv4_ranges_free_fragments=[{'frag': 'testfree'}])
        )


if __name__ == '__main__':
    unittest.main()
