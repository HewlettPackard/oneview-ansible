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
from oneview_managed_san import ManagedSanModule
from oneview_managed_san import MANAGED_SAN_UPDATED, MANAGED_SAN_REFRESH_STATE_UPDATED, MANAGED_SAN_NOT_FOUND, \
    MANAGED_SAN_NO_CHANGES_PROVIDED, MANAGED_SAN_ENDPOINTS_CSV_FILE_CREATED, MANAGED_SAN_ISSUES_REPORT_CREATED

FAKE_MSG_ERROR = 'Fake message error'

MANAGED_SAN = dict(
    name='SAN1_0',
    uri='/rest/fc-sans/managed-sans/a374d517-0369-4c48-b34e-409213642978',
    sanPolicy=dict(zoningPolicy='SingleInitiatorAllTargets',
                   zoneNameFormat='{hostName}_{initiatorWwn}',
                   enableAliasing=True,
                   initiatorNameFormat='{hostName}_{initiatorWwn}',
                   targetNameFormat='{storageSystemName}_{targetName}',
                   targetGroupNameFormat='{storageSystemName}_{targetGroupName}'))

PARAMS_FOR_PRESENT_WITHOUT_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='SAN1_0',
              sanPolicy=dict(MANAGED_SAN['sanPolicy']))
)

PARAMS_FOR_PRESENT_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name='SAN1_0',
              sanPolicy=dict(zoningPolicy='SingleInitiatorSingleTarget'))
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refresh_state_set',
    data=dict(name='SAN1_0',
              refreshStateData=dict(refreshState='RefreshPending'))
)

PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE = dict(
    config='config.json',
    state='endpoints_csv_file_created',
    data=dict(name='SAN1_0')
)

PARAMS_TO_CREATE_ISSUES_REPORT = dict(
    config='config.json',
    state='issues_report_created',
    data=dict(name='SAN1_0')
)


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class ManagedSanPresentStateSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_not_update_when_data_is_equals(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT_WITHOUT_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=MANAGED_SAN_NO_CHANGES_PROVIDED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_update_when_data_has_modified_attributes(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.update.return_value = MANAGED_SAN

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=MANAGED_SAN_UPDATED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_managed_san_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=MANAGED_SAN_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT_WITH_CHANGES)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class ManagedSanRefreshStateSetSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_update_refresh_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.update.return_value = MANAGED_SAN

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=MANAGED_SAN_REFRESH_STATE_UPDATED,
            ansible_facts=dict(managed_san=MANAGED_SAN)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_managed_san_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=MANAGED_SAN_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_update_raises_exception(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.update.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_REFRESH)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class ManagedSanEndpointsCsvFileCreatedSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_create_endpoints_csv_file(self, mock_ansible_module, mock_ov_client_from_json_file):
        endpoints_csv_file = {"csvFileName": "ci-005056a65f14-172.18.15.1-SAN1_0-endpoints-2016_09_21_05_55_24.csv.gz"}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.create_endpoints_csv_file.return_value = endpoints_csv_file

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=MANAGED_SAN_ENDPOINTS_CSV_FILE_CREATED,
            ansible_facts=dict(managed_san_endpoints=endpoints_csv_file)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_managed_san_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=MANAGED_SAN_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_create_endpoints_csv_file_raises_exception(self, mock_ansible_module,
                                                                         mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.create_endpoints_csv_file.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ENDPOINTS_CSV_FILE)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


class ManagedSanIssuesReportCreatedSpec(unittest.TestCase):
    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_create_issues_report(self, mock_ansible_module, mock_ov_client_from_json_file):
        issues_report = {"status": "report status"}

        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.create_issues_report.return_value = issues_report

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ISSUES_REPORT)
        mock_ansible_module.return_value = mock_ansible_instance

        ManagedSanModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=MANAGED_SAN_ISSUES_REPORT_CREATED,
            ansible_facts=dict(managed_san_issues=issues_report)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_managed_san_not_found(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = None

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ISSUES_REPORT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=MANAGED_SAN_NOT_FOUND
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_managed_san.AnsibleModule')
    def test_should_fail_when_create_issues_report_raises_exception(self, mock_ansible_module,
                                                                    mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.managed_sans.get_by_name.return_value = MANAGED_SAN
        mock_ov_instance.managed_sans.create_issues_report.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_TO_CREATE_ISSUES_REPORT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, ManagedSanModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )
