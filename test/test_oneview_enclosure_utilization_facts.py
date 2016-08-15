##
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
from oneview_enclosure_utilization_facts import EnclosureUtilizationFactsModule
from oneview_enclosure_utilization_facts import ENCLOSURE_NOT_FOUND

ERROR_MSG = 'Fake message error'

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name='Test-Enclosure'
)

PARAMS_GET_BY_NAME_WITH_FILTERS = dict(
    config='config.json',
    name='Test-Enclosure',
    fields='AveragePower',
    start_date='2016-06-30T03:29:42.000Z',
    end_date='2016-07-01T03:29:42.000Z',
    view='day',
    refresh=True
)

PRESENT_ENCLOSURES = [{
    "name": "Test-Enclosure",
    "uri": "/rest/enclosures/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

UTILIZATION = {
    "isFresh": "True"
}


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name] if name in params else None)

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class EnclosureUtiilizationFactsSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization(self, mock_ansible_module,
                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_utilization=UTILIZATION)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_all_utilization_data(self, mock_ansible_module,
                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(PRESENT_ENCLOSURES[0]['uri'],
                                                                            fields=None,
                                                                            filter=None,
                                                                            view=None,
                                                                            refresh=None)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_by_field(self, mock_ansible_module,
                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_FILTERS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields='AveragePower',
                                                                            filter=mock.ANY,
                                                                            view=mock.ANY,
                                                                            refresh=mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_between_dates(self, mock_ansible_module,
                                                  mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_FILTERS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        filter = "startDate=2016-06-30T03:29:42.000Z,endDate=2016-07-01T03:29:42.000Z"

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields=mock.ANY,
                                                                            filter=filter,
                                                                            view=mock.ANY,
                                                                            refresh=mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_with_start_date(self, mock_ansible_module,
                                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        params = PARAMS_GET_BY_NAME_WITH_FILTERS.copy()
        params.pop('end_date')

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields=mock.ANY,
                                                                            filter='startDate=2016-06-30T03:29:42.000Z',
                                                                            view=mock.ANY,
                                                                            refresh=mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_with_end_date(self, mock_ansible_module,
                                                  mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        params = PARAMS_GET_BY_NAME_WITH_FILTERS.copy()
        params.pop('start_date')

        mock_ansible_instance = create_ansible_mock(params)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields=mock.ANY,
                                                                            filter='endDate=2016-07-01T03:29:42.000Z',
                                                                            view=mock.ANY,
                                                                            refresh=mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_with_resolution_interval(self, mock_ansible_module,
                                                             mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_FILTERS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields=mock.ANY,
                                                                            filter=mock.ANY,
                                                                            view='day',
                                                                            refresh=mock.ANY)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_get_utilization_with_refresh(self, mock_ansible_module,
                                                 mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.return_value = UTILIZATION

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME_WITH_FILTERS)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ov_instance.enclosures.get_utilization.assert_called_once_with(mock.ANY,
                                                                            fields=mock.ANY,
                                                                            filter=mock.ANY,
                                                                            view=mock.ANY,
                                                                            refresh=True)

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_fail_when_get_utilization_raises_error(self, mock_ansible_module,
                                                           mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = PRESENT_ENCLOSURES
        mock_ov_instance.enclosures.get_utilization.side_effect = Exception(ERROR_MSG)

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_fail_when_get_by_name_raises_error(self,
                                                       mock_ansible_module,
                                                       mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.side_effect = Exception(ERROR_MSG)
        mock_ov_instance.enclosures.get_utilization.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ansible_instance.fail_json.assert_called_once()

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_enclosure_utilization_facts.AnsibleModule')
    def test_should_do_nothing_when_enclosure_not_exist(self,
                                                        mock_ansible_module,
                                                        mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.enclosures.get_by.return_value = []
        mock_ov_instance.enclosures.get_utilization.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance

        mock_ansible_instance = create_ansible_mock(PARAMS_GET_BY_NAME)
        mock_ansible_module.return_value = mock_ansible_instance

        EnclosureUtilizationFactsModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_utilization=None),
            msg=ENCLOSURE_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
