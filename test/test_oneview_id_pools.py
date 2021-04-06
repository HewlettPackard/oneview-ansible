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
from oneview_module_loader import IdPoolsModule, OneViewModuleValueError

FAKE_MSG_ERROR = 'Fake message error'

URI = '/rest/id-pools/ipv4'

DEFAULT_ID_POOLS = dict(host='127.0.0.1',
                        example_uri='/rest/id-pools',
                        uri='/rest/id-pools/ipv4')

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              idList=['10.1.0.1', '10.1.0.5'])
)

UPDATE_TEMPLATE = dict(uri='/rest/id-pools/vwwn',
                       enabled=True)

PARAMS_FOR_UPDATE = dict(
    config='config.json',
    state='update_pool_type',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              enabled=True)
)

VALIDATE_TEMPLATE = dict(poolType='ipv4',
                         uri='/rest/id-pools',
                         idList=['VCGYOAA023', 'VCGYOAA024'])

PARAMS_WITH_VALIDATE = dict(
    config='config.json',
    state='validate',
    data=dict(uri=DEFAULT_ID_POOLS['example_uri'],
              poolType='vwwn',
              idList=["10:00:2c:6c:28:80:00:00",
                      "10:00:2c:6c:28:80:00:01"])
)

ALLOCATE_TEMPLATE = dict(host='127.0.0.1',
                         uri='/rest/id-pools',
                         poolType='vwwn',
                         count=2)

PARAMS_WITH_ALLOCATE = dict(
    config='config.json',
    state='allocate',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              poolType='vwwn',
              count=2)
)

COLLECTOR_TEMPLATE = dict(host='127.0.0.1',
                          uri='/rest/id-pools',
                          poolType='vwwn',
                          idList=["10:00:2c:6c:28:80:00:00",
                                  "10:00:2c:6c:28:80:00:01"])

PARAMS_WITH_COLLECTOR = dict(
    config='config.json',
    state='collect',
    data=dict(uri=DEFAULT_ID_POOLS['uri'],
              poolType='vwwn',
              idList=["10:00:2c:6c:28:80:00:00",
                      "10:00:2c:6c:28:80:00:01"])
)


@pytest.mark.resource(TestIdPoolsModule='id_pools')
class TestIdPoolsModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_validate(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/validate?idList=VCGYOAA023&idList=VCGYOAA024"

        self.resource.validate.return_value = VALIDATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_VALIDATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_VALIDATED,
            ansible_facts=dict(id_pool=VALIDATE_TEMPLATE)
        )

    def test_validate_should_fail_when_ids_not_valid(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/validate?idList=VCGYOAA023&idList=VCGYOAA024"

        invalid_data = VALIDATE_TEMPLATE.copy()
        invalid_data['idList'] = []
        self.resource.validate.return_value = invalid_data

        self.mock_ansible_module.params = PARAMS_WITH_VALIDATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsModule.MSG_IDS_NOT_AVAILABLE,
            ansible_facts=dict(id_pool=invalid_data)
        )

    def test_should_fail_when_ids_not_available_for_allocation(self):
        self.resource.get.return_value = None
        self.resource.data['uri'] = URI + "/allocator"

        self.resource.allocate.return_value = None
        self.resource.allocate.side_effect = OneViewModuleValueError(IdPoolsModule.MSG_IDS_NOT_AVAILABLE)

        self.mock_ansible_module.params = PARAMS_WITH_ALLOCATE

        IdPoolsModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY,
            msg=IdPoolsModule.MSG_IDS_NOT_AVAILABLE)

    def test_should_update_pool_type(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        update_data = UPDATE_TEMPLATE.copy()
        update_data['enabled'] = False

        self.resource.update_pool_type.return_value = update_data

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_UPDATED,
            ansible_facts=dict(id_pool=update_data)
        )

    def test_should_not_update_pool_type_when_no_changes(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS

        self.resource.update_pool_type.return_value = UPDATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(id_pool=UPDATE_TEMPLATE)
        )

    def test_should_allocate_ids_from_pool(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = URI + "/allocator"
        self.resource.data['count'] = 2

        self.resource.allocate.return_value = ALLOCATE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_ALLOCATE

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_ALLOCATED,
            ansible_facts=dict(id_pool=ALLOCATE_TEMPLATE)
        )

    def test_should_collect_when_ids_allocated(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = URI + "/collector"
        self.resource.data['idList'] = ['10.1.0.1', '10.1.0.5']

        self.resource.collect.return_value = COLLECTOR_TEMPLATE

        self.mock_ansible_module.params = PARAMS_WITH_COLLECTOR

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=IdPoolsModule.MSG_COLLECTED,
            ansible_facts=dict(id_pool=COLLECTOR_TEMPLATE)
        )

    def test_should_not_collect_when_ids_not_allocated(self):
        self.resource.get.return_value = DEFAULT_ID_POOLS
        self.resource.data['uri'] = DEFAULT_ID_POOLS['uri'] + "/collector"

        invalid_data = COLLECTOR_TEMPLATE.copy()
        invalid_data['idList'] = []
        self.resource.collect.return_value = invalid_data

        self.mock_ansible_module.params = PARAMS_WITH_COLLECTOR

        IdPoolsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=IdPoolsModule.MSG_IDS_NOT_AVAILABLE,
            ansible_facts=dict(id_pool=invalid_data)
        )


if __name__ == '__main__':
    pytest.main([__file__])
