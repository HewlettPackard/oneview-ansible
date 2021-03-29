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
import mock
import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import IdPoolsFactsModule, OneViewModuleValueError

DEFAULT_ID_POOLS = dict(uri='/rest/id-pools/')

ID_POOLS_SCHEMA = dict(type='Range',
                       name='No name')

PARAMS_WITH_SCHEMA = dict(
    config='config.json',
    state='schema',
    data=dict(type='Range',
              name='No name')
)

GENERATE_TEMPLATE = dict(
    startAddress="BA:FC:D3:A0:00:00",
    endAddress="BA:FC:D3:AF:FF:FF",
    fragmentType="FREE")

PARAMS_WITH_GENERATE = dict(
    config='config.json',
    state='generate',
    data=dict(startAddress="BA:FC:D3:A0:00:00",
              endAddress="BA:FC:D3:AF:FF:FF",
              fragmentType="FREE")
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              idList=['10.1.0.1', '10.1.0.5'])
)

POOL_TYPE_TEMPLATE = dict(uri='/rest/id-pools',
                          poolType='vmac',
                          rangeUris=["/rest/id-pools/vmac/ranges/632f825c-59c8-4f8f-998b-0994d3bde7b3"],
                          enabled=True)

PARAMS_WITH_POOL_TYPE = dict(
    config='config.json',
    state='get_pool_type',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              poolType='ipv4',
              rangeUris=["/rest/id-pools/vmac/ranges/632f825c-59c8-4f8f-998b-0994d3bde7b3"],
              enabled=True)
)

VALIDATE_TEMPLATE = dict(poolType='ipv4',
                         uri='/rest/id-pools',
                         idList=['10.1.0.1', '10.1.0.5'])

PARAMS_WITH_VALIDATE_ID_POOL = dict(
    config='config.json',
    state='validate_id_pool',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              poolType='ipv4',
              idDict=dict(idList=['10.1.0.1', '10.1.0.5']))
)


@pytest.mark.resource(TestIdPoolsFactsModule='id_pools')
class TestIdPoolsFactsModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_get_id_pools_schema(self):
        self.mock_ov_client.id_pools.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + '/schema'
        self.resource.get_schema.return_value = ID_POOLS_SCHEMA

        self.mock_ansible_module.params = PARAMS_WITH_SCHEMA

        IdPoolsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pool=ID_POOLS_SCHEMA)
        )

    def test_should_generate_random_ids(self):
        self.mock_ov_client.id_pools_facts.get.return_value = DEFAULT_ID_POOLS
        self.resource.data = GENERATE_TEMPLATE
        self.resource.data['poolType'] = 'vmac'

        self.mock_ansible_module.check_mode = False
        self.resource.generate.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_GENERATE

        IdPoolsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pool=GENERATE_TEMPLATE)
        )

    def test_should_get_pool_type(self):
        self.mock_ov_client.id_pools_facts.get.return_value = DEFAULT_ID_POOLS
        self.resource.data = POOL_TYPE_TEMPLATE
        self.resource.data['poolType'] = 'vmac'

        self.mock_ansible_module.check_mode = False

        self.resource.get_pool_type.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_POOL_TYPE

        IdPoolsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pool=POOL_TYPE_TEMPLATE)
        )

    def test_should_validate_id_pool(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data = VALIDATE_TEMPLATE
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/validate?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.validate_id_pool.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_VALIDATE_ID_POOL

        IdPoolsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pool=VALIDATE_TEMPLATE)
        )

    def test_should_check_range_availability_with_defaults(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data = VALIDATE_TEMPLATE

        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/checkrangeavailability?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.get_check_range_availability.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        IdPoolsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(id_pool=VALIDATE_TEMPLATE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
