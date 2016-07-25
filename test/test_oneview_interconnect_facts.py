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
from oneview_interconnect_facts import InterconnectFactsModule


ERROR_MSG = 'Fake message error'

INTERCONNECT_NAME = "0000A66102, interconnect 2"

PARAMS_FOR_GET_ALL = dict(
    config='config.json',
    name=None,
    gather_name_servers=False
)

PARAMS_FOR_GET_BY_NAME = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    gather_name_servers=False
)

PARAMS_FOR_GET_NAME_SERVERS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    gather_name_servers=True
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params

    return mock_ansible


class InterconnectFactsSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_all_interconnects(self, mock_ansible_module, mock_ov_from_file):
        fake_interconnects = [dict(uidState='On', name=INTERCONNECT_NAME)]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_all.return_value = fake_interconnects

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_all.assert_called_once()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=fake_interconnects)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_fail_when_oneview_client_raises_error(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_all.side_effect = Exception(ERROR_MSG)

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_ALL)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, InterconnectFactsModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MSG)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_interconnects_by_interconnect_name(self, mock_ansible_module, mock_ov_from_file):
        fake_interconnects = [dict(uidState='On', name=INTERCONNECT_NAME)]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = fake_interconnects

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_by.assert_called_once_with('name', INTERCONNECT_NAME)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=fake_interconnects)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_facts.AnsibleModule')
    def test_should_get_interconnect_name_servers(self, mock_ansible_module, mock_ov_from_file):
        fake_uri = '/rest/interconnects/9b8f7ec0-52b3-475e-84f4-c4eac51c2c20'
        fake_interconnects = [dict(uidState='On', name=INTERCONNECT_NAME, uri=fake_uri)]
        fake_name_servers = [dict(t=1)]

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by.return_value = fake_interconnects
        mock_ov_instance.interconnects.get_name_servers.return_value = fake_name_servers

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_GET_NAME_SERVERS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectFactsModule().run()

        mock_ov_instance.interconnects.get_by.assert_called_once_with('name', INTERCONNECT_NAME)
        mock_ov_instance.interconnects.get_name_servers.assert_called_once_with(fake_uri)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=fake_interconnects, name_servers=fake_name_servers)
        )


if __name__ == '__main__':
    unittest.main()
