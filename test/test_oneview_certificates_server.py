#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
from oneview_module_loader import CertificatesServerModule

server_certificate = dict(
    aliasName='172.18.13.11',
    name='test',
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    name='cert',
    data=dict(aliasName=server_certificate['aliasName'],
              name="test")
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    name='cert',
    data=dict(aliasName=server_certificate['aliasName'],
              name="vcenter renamed")
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    name='cert',
    data=dict(aliasName=server_certificate['aliasName'])
)


@pytest.mark.resource(TestCertificatesServerModule='certificates_server')
class TestCertificatesServerModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_certificate_server(self):
        self.resource.get_by_alias_name = None

        self.resource.data = server_certificate
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        CertificatesServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=CertificatesServerModule.MSG_CREATED,
            ansible_facts=dict(certificate_server=server_certificate)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_alias_name.return_value = server_certificate

        self.resource.data = server_certificate
        self.resource.update = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        CertificatesServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=CertificatesServerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(certificate_server=server_certificate)
        )

    def test_update_when_data_has_modified_attributes(self):
        self.resource.get_by_alias_name.return_value = server_certificate

        data_merged = server_certificate.copy()
        data_merged['name'] = 'vcenter renamed'
        self.resource.data = data_merged
        self.resource.update = self.resource

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        CertificatesServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=CertificatesServerModule.MSG_UPDATED,
            ansible_facts=dict(certificate_server=server_certificate)
        )

    def test_should_remove_certificate_server(self):
        self.resource.data = server_certificate
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        CertificatesServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=CertificatesServerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_certificate_server_not_exist(self):
        self.resource.get_by_alias_name = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        CertificatesServerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=CertificatesServerModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
