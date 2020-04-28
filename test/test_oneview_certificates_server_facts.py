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

from hpe_test_utils import OneViewBaseFactsTest
from oneview_module_loader import CertificatesServerFactsModule

FAKE_MSG_ERROR = "No matching certificate found for the specified alias"

PARAMS_GET_REMOTE = dict(
    config='config.json',
    remote="172.18.13.11",
    aliasName=None
)

PARAMS_GET_BY_ALIASNAME = dict(
    config='config.json',
    aliasName="172.18.13.11",
    remote=None
)

PRESENT_CERTIFICATES = {
    "aliasName": "172.18.13.11",
    "uri": "/rest/certificates/servers/172.18.13.11"
}


class Exception(Exception):
    def __init__(self, message):
        self.msg=message


@pytest.mark.resource(TestCertificatesServerFactsModule='certificates_server')
class TestCertificatesServerFactsModule(OneViewBaseFactsTest):
    def test_should_get_remote_certificate(self):
        self.resource.get_remote.return_value = PRESENT_CERTIFICATES
        self.mock_ansible_module.params = PRESENT_CERTIFICATES

        CertificatesServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(remote_certificate=PRESENT_CERTIFICATES)
        )

    def test_should_get_certificate_server_by_aliasname(self):
        self.resource.get_by_aliasName.return_value = PRESENT_CERTIFICATES
        self.mock_ansible_module.params = PRESENT_CERTIFICATES

        CertificatesServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(certificates_server=PRESENT_CERTIFICATES)
        )

    def test_should_return_none_when_certificate_not_present(self):
        self.resource.get_by_aliasName.side_effect = Exception(FAKE_MSG_ERROR)
        self.mock_ansible_module.params = None

        CertificatesServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(certificates_server=None)
        )


if __name__ == '__main__':
    pytest.main([__file__])
