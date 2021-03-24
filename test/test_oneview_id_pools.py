# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import IDPoolsModule

FAKE_MSG_ERROR = 'Fake message error'

URI = '/rest/id-pools/ipv4'

DEFAULT_ID_POOLS = dict(host='127.0.0.1',
                        example_uri='/rest/id-pools',
                        uri='/rest/id-pools/ipv4')

ID_POOLS_SCHEMA = dict(type='Range',
                       name='No name')

PARAMS_WITH_SCHEMA = dict(
    config='config.json',
    state='present',
    data=dict(type='Range',
              name='No name')
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              idList=['10.1.0.1', '10.1.0.5'])
)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              enabled=True)
)

GENERATE_TEMPLATE = dict(idList=['10.1.0.1', '10.1.0.5'])

POOL_TYPE_TEMPLATE = dict(host='127.0.0.1',
                          uri='/rest/id-pools',
                          poolType='ipv4',
                          rangeUris=['10.1.0.1', '10.1.0.5'])

VALIDATE_TEMPLATE = dict(poolType='ipv4',
                         uri='/rest/id-pools',
                         rangeUris=['10.1.0.1', '10.1.0.5'])

VALIDATE_TEMPLATE = dict(poolType='ipv4',
                         uri='/rest/id-pools',
                         idList=['VCGYOAA023', 'VCGYOAA024'])

ALLOCATE_TEMPLATE = dict(host='127.0.0.1',
                         uri='/rest/id-pools',
                         poolType='ipv4',
                         count=2)

COLLECTOR_TEMPLATE = dict(host='127.0.0.1',
                          uri='/rest/id-pools',
                          poolType='ipv4',
                          rangeUris=['10.1.0.1', '10.1.0.5'])


@pytest.mark.resource(TestIdPoolsModule='id_pools')
class TestIdPoolsModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_get_id_pools_schema(self):
        self.mock_ov_client.id_pools.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['example_uri'] + '/schema'
        self.resource.get_schema.return_value = ID_POOLS_SCHEMA

        self.mock_ansible_module.params = PARAMS_WITH_SCHEMA

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pools=ID_POOLS_SCHEMA)
        )

    def test_should_generate_random_ids(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + '/generate'

        self.resource.generate.return_value = GENERATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pools=GENERATE_TEMPLATE)
        )

    def test_should_get_pool_type(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS

        self.resource.get_pool_type.return_value = POOL_TYPE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pools=POOL_TYPE_TEMPLATE)
        )

    def test_should_validate_id_pool(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/validate?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.validate_id_pool.return_value = VALIDATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_VALIDATED,
            ansible_facts=dict(id_pools=VALIDATE_TEMPLATE)
        )

    def test_should_validate(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/validate?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.validate.return_value = VALIDATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_VALIDATED,
            ansible_facts=dict(id_pools=VALIDATE_TEMPLATE)
        )

    def test_should_update_pool_type(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['enabled'] = True

        self.resource.update_pool_type.return_value = self.resource.data

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pools=self.resource.data)
        )

    def test_should_check_range_availability_with_defaults(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/checkrangeavailability?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.get_check_range_availability.return_value = VALIDATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pools=VALIDATE_TEMPLATE)
        )

    def test_should_allocate_ids_from_pool(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = URI + "/allocator"
        self.resource.data['count'] = 2

        self.resource.allocate.return_value = ALLOCATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_ALLOCATED,
            ansible_facts=dict(id_pools=ALLOCATE_TEMPLATE)
        )

    def test_should_fail_when_ids_not_available_for_allocation(self):
        self.resource.get.return_value = []
        self.resource.data['uri'] = URI + "/allocator"
        self.resource.data['count'] = 2

        self.resource.allocate.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_IDS_NOT_AVAILABLE
        )

    def test_should_collect_when_ids_allocated(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = URI + "/collector"
        self.resource.data['rangeUris'] = ['10.1.0.1', '10.1.0.5']

        self.resource.collect.return_value = COLLECTOR_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pools=COLLECTOR_TEMPLATE)
        )
