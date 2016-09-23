###
# Copyright (2016) Hewlett Packard Enterprise Development LP
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
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_managed_san_facts import ManagedSanFactsModule
from utils import create_ansible_mock

ERROR_MSG = 'Fake message error'

MANAGED_SAN_NAME = 'SAN1_0'

MANAGED_SAN_URI = '/rest/fc-sans/managed-sans/028e81d0-831b-4211-931c-8ac63d687ebd'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=MANAGED_SAN_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=MANAGED_SAN_NAME,
    options=['endpoints']
)

MANAGED_SAN = dict(name=MANAGED_SAN_NAME, uri=MANAGED_SAN_URI)

ALL_MANAGED_SANS = [MANAGED_SAN,
                    dict(name='SAN1_1', uri='/rest/fc-sans/managed-sans/928374892-asd-34234234-asd23')]


class ManagedSanFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_get_all(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_all.return_value = ALL_MANAGED_SANS
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=ALL_MANAGED_SANS)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_fail_when_get_all_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_all.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_get_by_name(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ov_instance.managed_sans.get_by_name.assert_called_once_with(MANAGED_SAN_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=[MANAGED_SAN])
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_get_by_name_with_options(self, mock_ansible_module, mock_ov_from_file):
        endpoints = [dict(uri='/rest/fc-sans/endpoints/20:00:00:02:AC:00:08:E2'),
                     dict(uri='/rest/fc-sans/endpoints/20:00:00:02:AC:00:08:FF')]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.get_endpoints.return_value = endpoints
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ov_instance.managed_sans.get_by_name.assert_called_once_with(MANAGED_SAN_NAME)
        mock_ov_instance.managed_sans.get_endpoints.assert_called_once_with(MANAGED_SAN_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(managed_sans=[MANAGED_SAN], managed_san_endpoints=endpoints)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san_facts.AnsibleModule')
    def test_should_fail_when_get_endpoints_raises_exception(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.get_endpoints.side_effect = Exception(ERROR_MSG)
        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_OPTIONS)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
