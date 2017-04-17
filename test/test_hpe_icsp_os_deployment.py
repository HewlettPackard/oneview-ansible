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

import unittest
import mock
import hpe_icsp_os_deployment
from test.utils import create_ansible_mock
from copy import deepcopy

TASK_OS_DEPLOYMENT = {
    "icsp_host": "16.124.133.251",
    "username": "Administrator",
    "password": "admin",
    "server_id": "VCGYZ33007",
    "os_build_plan": "RHEL 7.2 x64",
    "personality_data": None,
    "custom_attributes": None
}

DEFAULT_SERVER = {"name": "SP-01",
                  "uri": "/uri/239",
                  "ilo": {"ipAddress": "16.124.135.239"},
                  "state": "",
                  "customAttributes": []}

DEFAULT_SERVER_UPDATED = {"name": "SP-01",
                          "uri": "/uri/239",
                          "ilo": {"ipAddress": "16.124.135.239"},
                          "state": "OK",
                          "customAttributes":
                              [{'values': [{'scope': 'server', 'value': "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}],
                                'key': 'SSH_CERT'}]}

DEFAULT_BUILD_PLAN = {"name": "BuildPlanName2", "uri": "/rest/os-deployment-build-plans/222"}


class IcspServerSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch('hpe_icsp_os_deployment.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.patcher_icsp_service = mock.patch('hpe_icsp_os_deployment.hpICsp')
        self.mock_icsp = self.patcher_icsp_service.start()

        self.patcher_time_sleep = mock.patch('time.sleep', return_value=None)
        self.mock_time_sleep = self.patcher_time_sleep.start()

        self.patcher_get_server_by_serial = mock.patch('hpe_icsp_os_deployment.get_server_by_serial')
        self.mock_get_server_by_serial = self.patcher_get_server_by_serial.start()

        self.patcher_get_build_plan = mock.patch('hpe_icsp_os_deployment.get_build_plan')
        self.mock_get_build_plan = self.patcher_get_build_plan.start()

        self.mock_connection = mock.Mock()
        self.mock_connection.login.return_value = {}
        self.mock_icsp.connection.return_value = self.mock_connection

        self.mock_icsp_common = mock.Mock()
        self.mock_icsp.common.return_value = self.mock_icsp_common

        self.mock_icsp_jobs = mock.Mock()
        self.mock_icsp.jobs.return_value = self.mock_icsp_jobs

        self.mock_server_service = mock.Mock()
        self.mock_icsp.servers.return_value = self.mock_server_service

        self.mock_build_plans_service = mock.Mock()
        self.mock_icsp.buildPlans.return_value = self.mock_build_plans_service

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_icsp_service.stop()
        self.patcher_get_build_plan.stop()
        self.patcher_get_server_by_serial.stop()
        self.patcher_time_sleep.stop()

    def test_should_not_add_server_when_already_present(self):
        server_already_deployed = dict(DEFAULT_SERVER, state="OK")
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.return_value = {'uri': '/rest/os-deployment-servers/123456'}
        self.mock_server_service.get_server.return_value = server_already_deployed

        mock_ansible_instance = create_ansible_mock(TASK_OS_DEPLOYMENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        self.mock_time_sleep.assert_not_called()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False, msg="Server already deployed.", ansible_facts={'icsp_server': server_already_deployed}
        )

    def test_should_fail_after_try_get_server_by_serial_21_times(self):
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.return_value = None
        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        mock_ansible_instance = create_ansible_mock(TASK_OS_DEPLOYMENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(21, times_sleep_called)

        mock_ansible_instance.fail_json.assert_called_once_with(msg='Cannot find server in ICSP.')

    def test_should_deploy_server(self):
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.side_effect = [DEFAULT_SERVER]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]

        mock_ansible_instance = create_ansible_mock(TASK_OS_DEPLOYMENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(0, times_sleep_called)

        mock_ansible_instance.exit_json.assert_called_once_with(changed=True, msg='OS Deployed Successfully.',
                                                                ansible_facts={'icsp_server': DEFAULT_SERVER_UPDATED})

    def test_should_try_deploy_server_3_times(self):
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.side_effect = [None, None, DEFAULT_SERVER]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]

        mock_ansible_instance = create_ansible_mock(TASK_OS_DEPLOYMENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(2, times_sleep_called)

        mock_ansible_instance.exit_json.assert_called_once_with(changed=True, msg='OS Deployed Successfully.',
                                                                ansible_facts={'icsp_server': DEFAULT_SERVER_UPDATED})

    def test_should_fail_when_os_build_plan_not_found(self):
        self.mock_get_build_plan.return_value = None
        self.mock_get_server_by_serial.side_effect = [None, None, DEFAULT_SERVER]
        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        mock_ansible_instance = create_ansible_mock(TASK_OS_DEPLOYMENT)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        mock_ansible_instance.fail_json.assert_called_once_with(msg='Cannot find OS Build plan: RHEL 7.2 x64')

    def test_should_update_server_when_task_include_network_personalization(self):
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.return_value = DEFAULT_SERVER
        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]
        self.mock_icsp.common.monitor_execution.return_value = {}
        self.mock_icsp_jobs.add_job.return_value = {"job mock return"}

        task_with_network_personalization = deepcopy(TASK_OS_DEPLOYMENT)
        network_config = {"network_config": {"hostname": "test-web.io.fc.hpe.com", "domain": "demo.com"}}
        task_with_network_personalization['personality_data'] = network_config
        mock_ansible_instance = create_ansible_mock(task_with_network_personalization)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        server_data = {"serverUri": DEFAULT_SERVER['uri'], "personalityData": None}
        network_config = {"serverData": [server_data]}
        build_plan_body = {"osbpUris": [DEFAULT_BUILD_PLAN['uri']], "serverData": [server_data], "stepNo": 1}

        monitor_build_plan = mock.call(self.mock_icsp_jobs.add_job(build_plan_body), self.mock_icsp_jobs)
        monitor_update_server = mock.call(self.mock_icsp_jobs.add_job(network_config), self.mock_icsp_jobs)
        calls = [monitor_build_plan, monitor_update_server]

        self.mock_icsp.common.monitor_execution.assert_has_calls(calls)

    def test_should_update_server_when_task_include_custom_attributes(self):
        self.mock_get_build_plan.return_value = DEFAULT_BUILD_PLAN
        self.mock_get_server_by_serial.return_value = DEFAULT_SERVER

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]
        self.mock_server_service.update_server.return_value = DEFAULT_SERVER_UPDATED

        task_with_custom_attr = deepcopy(TASK_OS_DEPLOYMENT)
        custom_attr = [{"SSH_CERT": "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}]
        task_with_custom_attr['custom_attributes'] = custom_attr
        mock_ansible_instance = create_ansible_mock(task_with_custom_attr)
        self.mock_ansible_module.return_value = mock_ansible_instance

        hpe_icsp_os_deployment.main()

        personality_data = deepcopy(DEFAULT_SERVER)
        personality_data['customAttributes'] = [
            {'values': [{'scope': 'server', 'value': "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}],
             'key': 'SSH_CERT'}]

        self.mock_server_service.update_server.assert_called_once_with(personality_data)

    if __name__ == '__main__':
        unittest.main()
