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

import pytest

from hpe_test_utils import OneViewBaseTest
from oneview_module_loader import LoginDetailFactsModule

PARAMS_GET_DETAILS = dict(
    config='config.json'
)

LIST_DEFAULT_LOGIN_DETAIL = [{
    "allowLocalLogin": "true",
    "category": "null",
    "configuredLoginDomains": [
        {
            "authProtocol": "AD",
            "category": "users",
            "created": "Wed Aug 02 15:37:50 UTC 2017",
            "eTag": "Wed Aug 02 15:37:50 UTC 2017",
            "loginDomain": "1",
            "modified": "Wed Aug 02 15:37:50 UTC 2017",
            "name": "wpstad.vse.rdlabs.hpecorp.net",
            "type": "LoginDomainDetails",
            "uri": "/rest/logindetails"
        }
    ]
}]


@pytest.mark.resource(TestLoginDetailFactsModule='login_details')
class TestLoginDetailFactsModule(OneViewBaseTest):
    def test_should_get_all_login_details(self):
        self.resource.get_login_details.return_value = LIST_DEFAULT_LOGIN_DETAIL
        self.mock_ansible_module.params = PARAMS_GET_DETAILS

        LoginDetailFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(login_details=LIST_DEFAULT_LOGIN_DETAIL)
        )


if __name__ == '__main__':
    pytest.main([__file__])
