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
from oneview_interconnect_statistics_facts import InterconnectStatisticsFactsModule


INTERCONNECT_NAME = "0000A66102, interconnect 2"

INTERCONNECT_URI = "/rest/interconnects/53fa7d35-1cc8-46c1-abf0-6af091a1aed3"

PARAMS = dict(
    config='config.json',
    name=INTERCONNECT_NAME
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


class InterconnectStatisticsFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_statistics_facts.AnsibleModule')
    def test_should_get_interconnect_statistics_by_interconnect_name(self, mock_ansible_module,
                                                                     mock_ov_from_file):

        fake_interconnect = dict(uidState='On', uri=INTERCONNECT_URI)

        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by_name.return_value = fake_interconnect

        fake_statistics = dict()
        mock_ov_instance.interconnects.get_statistics.return_value = fake_statistics

        mock_ov_from_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectStatisticsFactsModule().run()

        mock_ov_instance.interconnects.get_statistics.assert_called_once_with(INTERCONNECT_URI)

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_statistics=fake_statistics)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect_statistics_facts.AnsibleModule')
    def test_should_do_nothing_when_interconnect_is_absent(self, mock_ansible_module, mock_ov_from_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.get_by_name.return_value = None

        mock_ov_from_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, InterconnectStatisticsFactsModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=AnyStringWith("There is no interconnect named")
        )


if __name__ == '__main__':
    unittest.main()
