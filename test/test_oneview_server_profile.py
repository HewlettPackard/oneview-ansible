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
import logging
import unittest
import mock

from copy import deepcopy

from oneview_module_loader import (ServerProfileModule,
                                   HPOneViewException,
                                   HPOneViewTaskError,
                                   OneViewModuleBase,
                                   SPKeys,
                                   ServerProfileMerger,
                                   ServerProfileReplaceNamesByUris,
                                   ResourceComparator)

from hpe_test_utils import OneViewBaseTestCase

SERVER_PROFILE_NAME = "Profile101"
SERVER_PROFILE_URI = "/rest/server-profiles/94B55683-173F-4B36-8FA6-EC250BA2328B"
SHT_URI = "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
TEMPLATE_URI = '/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'
FAKE_SERVER_HARDWARE = {'uri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'}

MESSAGE_COMPLIANT_ERROR = ServerProfileModule.MSG_MAKE_COMPLIANT_NOT_SUPPORTED.format(SERVER_PROFILE_NAME)
FAKE_MSG_ERROR = 'Fake message error'

TASK_ERROR = HPOneViewTaskError(msg=FAKE_MSG_ERROR, error_code='AssignProfileToDeviceBayError')

BASIC_PROFILE = dict(
    name=SERVER_PROFILE_NAME,
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI,
    uri=SERVER_PROFILE_URI
)

BASIC_TEMPLATE = dict(
    name="Server-Template-7000",
    serverHardwareTypeUri=SHT_URI,
    enclosureGroupUri=ENCLOSURE_GROUP_URI,
    uri='/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=BASIC_PROFILE
)

PARAMS_FOR_COMPLIANT = dict(
    config='config.json',
    state='compliant',
    data=dict(name="Server-Template-7000")
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name="Server-Template-7000")
)

CREATED_BASIC_PROFILE = dict(
    affinity="Bay",
    bios=dict(manageBios=False, overriddenSettings=[]),
    boot=dict(manageBoot=False, order=[]),
    bootMode=dict(manageMode=False, mode=None, pxeBootPolicy=None),
    category="server-profile-templates",
    enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
    name=SERVER_PROFILE_NAME,
    serialNumber='VCGGU8800W',
    serialNumberType="Virtual",
    serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B",
    serverHardwareUri='/rest/server-hardware/37333036-3831-76jh-4831-303658389766',
    status="OK",
    type="ServerProfileV5",
    uri="/rest/server-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea490",
    serverProfileTemplateUri='/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda',
    templateCompliance='Compliant',
    wwnType="Virtual"
)

AVAILABLE_TARGETS = dict(
    category='available-targets',
    targets=[
        dict(enclosureBay=2, serverHardwareUri=''),
        dict(enclosureBay=3, serverHardwareUri='/rest/server-hardware/31393736-3831-4753-567h-30335837524E'),
        dict(enclosureBay=4, serverHardwareUri='/rest/server-hardware/37333036-3831-6776-gdfd-3037583rewr0'),
        dict(enclosureBay=8, serverHardwareUri='/rest/server-hardware/37333036-3831-4753-4831-303158sdf458'),
    ]
)

BOOT_CONN = dict(priority="NotBootable", chapLevel="none")

CONNECTION_1 = dict(id=1, name="connection-1", mac="E2:4B:0D:30:00:29", boot=BOOT_CONN)
CONNECTION_2 = dict(id=2, name="connection-2", mac="E2:4B:0D:30:00:2A", boot=BOOT_CONN)

CONNECTION_1_WITH_WWPN = dict(name="connection-1", wwpnType="Virtual",
                              wwnn="10:00:3a:43:88:50:00:01", wwpn="10:00:3a:43:88:50:00:00")
CONNECTION_2_WITH_WWPN = dict(name="connection-2", wwpnType="Physical",
                              wwnn="10:00:3a:43:88:50:00:03", wwpn="10:00:3a:43:88:50:00:02")

CONN_1_NO_MAC_BASIC_BOOT = dict(id=1, name="connection-1", boot=dict(priority="NotBootable"))
CONN_2_NO_MAC_BASIC_BOOT = dict(id=2, name="connection-2", boot=dict(priority="NotBootable"))

PATH_1 = dict(isEnabled=True, connectionId=1, storageTargets=["20:00:00:02:AC:00:08:D6"])
PATH_2 = dict(isEnabled=True, connectionId=2, storageTargetType="Auto")

VOLUME_1 = dict(id=1, volumeUri="/rest/volume/id1", lun=123, lunType="Auto", storagePaths=[PATH_1, PATH_2])
VOLUME_2 = dict(id=2, volumeUri="/rest/volume/id2", lun=345, lunType="Auto", storagePaths=[])

SAN_STORAGE = dict(hostOSType="Windows 2012 / WS2012 R2",
                   volumeAttachments=[VOLUME_1, VOLUME_2])

OS_CUSTOM_ATTRIBUTES = [dict(name="hostname", value="newhostname"),
                        dict(name="username", value="administrator")]

OS_DEPLOYMENT_SETTINGS = dict(osDeploymentPlanUri="/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493",
                              osVolumeUri="/rest/deployed-targets/a166c84a-4964-4f20-b4ba-ef2f154b8596",
                              osCustomAttributes=OS_CUSTOM_ATTRIBUTES)

SAS_LOGICAL_JBOD_1 = dict(id=1, deviceSlot="Mezz 1", name="jbod-1", driveTechnology="SasHdd", status="OK",
                          sasLogicalJBODUri="/rest/sas-logical-jbods/3128c9e6-e3de-43e7-b196-612707b54967")

SAS_LOGICAL_JBOD_2 = dict(id=2, deviceSlot="Mezz 1", name="jbod-2", driveTechnology="SataHdd", status="Pending")

DRIVES_CONTROLLER_EMBEDDED = [dict(driveNumber=1, name="drive-1", raidLevel="RAID1", bootable=False,
                                   sasLogicalJBODId=None),
                              dict(driveNumber=2, name="drive-2", raidLevel="RAID1", bootable=False,
                                   sasLogicalJBODId=None)]

CONTROLLER_EMBEDDED = dict(deviceSlot="Embedded", mode="RAID", initialize=False, importConfiguration=True,
                           logicalDrives=DRIVES_CONTROLLER_EMBEDDED)

DRIVES_CONTROLLER_MEZZ_1 = [dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=1),
                            dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=2)]
CONTROLLER_MEZZ_1 = dict(deviceSlot="Mezz 1", mode="RAID", initialize=False, importConfiguration=True,
                         logicalDrives=DRIVES_CONTROLLER_MEZZ_1)

INDEX_EMBED = 0
INDEX_MEZZ = 1


def gather_facts(mock_ov_client, created=False, online_update=True):
    compliance_preview = {
        'automaticUpdates': ['fake change.'],
        'isOnlineUpdate': online_update,
        'manualUpdates': [],
        'type': 'ServerProfileCompliancePreviewV1'
    }

    mock_ov_client.server_profiles.get_compliance_preview.return_value = compliance_preview
    mock_ov_client.server_hardware.get.return_value = {}
    facts = {
        'serial_number': CREATED_BASIC_PROFILE.get('serialNumber'),
        'server_profile': CREATED_BASIC_PROFILE,
        'server_hardware': {},
        'compliance_preview': compliance_preview,
        'created': created
    }

    return facts


class ServerProfileModuleSpec(unittest.TestCase,
                              OneViewBaseTestCase):
    """
    Test the module constructor
    OneViewBaseTestCase has common tests for class constructor and main function.
    """

    def setUp(self):
        self.configure_mocks(self, ServerProfileModule)
        self.sleep_patch = mock.patch('time.sleep')
        self.sleep_patch.start()
        self.sleep_patch.return_value = None

    def tearDown(self):
        self.sleep_patch.stop()

    @mock.patch.dict('os.environ', dict(LOGFILE='/path/log.txt'))
    @mock.patch.object(logging, 'getLogger')
    @mock.patch.object(logging, 'basicConfig')
    def test_should_config_logging_when_logfile_env_var_defined(self, mock_logging_config, mock_get_logger):
        fake_logger = mock.Mock()
        mock_get_logger.return_value = fake_logger

        OneViewModuleBase.get_logger('/home/dev/oneview-ansible/library/oneview_server_profile.py')

        mock_get_logger.assert_called_once_with('oneview_server_profile.py')
        fake_logger.addHandler.not_been_called()
        mock_logging_config.assert_called_once_with(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                                                    format='%(asctime)s %(levelname)s %(name)s %(message)s',
                                                    filename='/path/log.txt', filemode='a')

    @mock.patch('os.environ')
    @mock.patch.object(logging, 'getLogger')
    @mock.patch.object(logging, 'basicConfig')
    @mock.patch.object(logging, 'NullHandler')
    def test_should_add_null_handler_when_logfile_env_var_undefined(self, mock_null_handler, mock_logging_config,
                                                                    mock_get_logger, mock_env):
        mock_env.get.return_value = None
        fake_logger = mock.Mock()
        mock_get_logger.return_value = fake_logger

        OneViewModuleBase.get_logger('/home/dev/oneview-ansible/library/oneview_server_profile.py')

        mock_get_logger.assert_called_once_with('oneview_server_profile.py')
        fake_logger.addHandler.assert_called_once_with(logging.NullHandler())
        mock_logging_config.not_been_called()

    def test_should_fail_when_server_not_associated_with_template(self):
        fake_server = deepcopy(CREATED_BASIC_PROFILE)
        fake_server['templateCompliance'] = 'Unknown'
        fake_server['serverProfileTemplateUri'] = ''

        self.mock_ov_client.server_profiles.get_by_name.return_value = fake_server
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_COMPLIANT)

        ServerProfileModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=MESSAGE_COMPLIANT_ERROR)

    def test_should_not_update_when_already_compliant(self):
        fake_server = deepcopy(CREATED_BASIC_PROFILE)
        mock_facts = gather_facts(self.mock_ov_client)

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_COMPLIANT)
        self.mock_ov_client.server_profiles.get_by_name.return_value = fake_server

        ServerProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False, msg=ServerProfileModule.MSG_ALREADY_COMPLIANT, ansible_facts=mock_facts)

    def test_should_update_when_not_compliant(self):
        fake_server = deepcopy(CREATED_BASIC_PROFILE)
        fake_server['templateCompliance'] = 'NonCompliant'
        mock_facts = gather_facts(self.mock_ov_client)

        self.mock_ov_client.server_profiles.get_by_name.return_value = fake_server
        self.mock_ov_client.server_profiles.patch.return_value = CREATED_BASIC_PROFILE
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_COMPLIANT)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.patch.assert_called_once_with(
            CREATED_BASIC_PROFILE['uri'], 'replace', '/templateCompliance', 'Compliant')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True, msg=ServerProfileModule.MSG_REMEDIATED_COMPLIANCE, ansible_facts=mock_facts)

    def test_should_power_off_when_is_offline_update(self):
        fake_server = deepcopy(CREATED_BASIC_PROFILE)
        fake_server['templateCompliance'] = 'NonCompliant'

        self.mock_ov_client.server_profiles.get_by_name.return_value = fake_server
        self.mock_ov_client.server_profiles.patch.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_COMPLIANT)

        # shoud power off server to update
        mock_facts = gather_facts(self.mock_ov_client, online_update=False)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.patch.assert_called_once_with(
            CREATED_BASIC_PROFILE['uri'], 'replace', '/templateCompliance', 'Compliant')

        power_set_calls = [
            mock.call(dict(powerState='Off', powerControl='PressAndHold'), fake_server['serverHardwareUri']),
            mock.call(dict(powerState='On', powerControl='MomentaryPress'), fake_server['serverHardwareUri'])]

        self.mock_ov_client.server_hardware.update_power_state.assert_has_calls(power_set_calls)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True, msg=ServerProfileModule.MSG_REMEDIATED_COMPLIANCE, ansible_facts=mock_facts)

    def test_should_create_with_automatically_selected_hardware_when_not_exists(self):
        profile_data = deepcopy(BASIC_PROFILE)
        profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_profiles.get_available_targets.return_value = AVAILABLE_TARGETS
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.create.assert_called_once_with(profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_create_from_template_with_automatically_selected_hardware_when_not_exists(self):
        template = deepcopy(BASIC_TEMPLATE)
        profile_from_template = deepcopy(BASIC_PROFILE)

        param_for_present = deepcopy(PARAMS_FOR_PRESENT)
        param_for_present['data']['server_template'] = 'Server-Template-7000'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_profiles.get_available_targets.return_value = AVAILABLE_TARGETS
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = template
        self.mock_ov_client.server_profile_templates.get_new_profile.return_value = profile_from_template
        self.mock_ov_client.server_profiles.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = param_for_present
        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        expected_profile_data = deepcopy(BASIC_PROFILE)
        expected_profile_data.update(PARAMS_FOR_PRESENT['data'])
        expected_profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'
        expected_profile_data['serverProfileTemplateUri'] \
            = '/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'

        self.mock_ov_client.server_profiles.create.assert_called_once_with(expected_profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_create_from_template_uri_with_automatically_selected_hardware_when_not_exists(self):
        template = deepcopy(BASIC_TEMPLATE)
        profile_from_template = deepcopy(BASIC_PROFILE)

        param_for_present = deepcopy(PARAMS_FOR_PRESENT)
        param_for_present['data']['serverProfileTemplateUri'] \
            = '/rest/server-profile-templates/31393736-3831-4753-567h-30335837524E'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_profiles.get_available_targets.return_value = AVAILABLE_TARGETS
        self.mock_ov_client.server_profile_templates.get.return_value = template
        self.mock_ov_client.server_profile_templates.get_new_profile.return_value = profile_from_template
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = param_for_present
        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        expected_profile_data = deepcopy(BASIC_PROFILE)
        expected_profile_data.update(param_for_present['data'])
        expected_profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'

        self.mock_ov_client.server_profiles.create.assert_called_once_with(expected_profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_create_with_informed_hardware_when_not_exists(self):
        profile_data = deepcopy(BASIC_PROFILE)
        profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'

        param_for_present = deepcopy(PARAMS_FOR_PRESENT)
        param_for_present['data']['server_hardware'] = "ServerHardwareName"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ansible_module.params = param_for_present
        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.create.assert_called_once_with(profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_create_with_informed_hardware_and_template_when_not_exists(self):
        template = deepcopy(BASIC_TEMPLATE)

        profile_from_template = deepcopy(BASIC_PROFILE)

        param_for_present = deepcopy(PARAMS_FOR_PRESENT)
        param_for_present['data']['server_hardware'] = "ServerHardwareName"
        param_for_present['data']['server_template'] = "TemplateA200"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = template
        self.mock_ov_client.server_profile_templates.get_new_profile.return_value = profile_from_template
        self.mock_ansible_module.params = param_for_present
        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        expected_profile_data = deepcopy(BASIC_PROFILE)
        expected_profile_data.update(PARAMS_FOR_PRESENT['data'])
        expected_profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'
        expected_profile_data['serverProfileTemplateUri'] \
            = '/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'

        self.mock_ov_client.server_profiles.create.assert_called_once_with(expected_profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_try_create_with_informed_hardware_25_times_when_not_exists(self):
        param_for_present = deepcopy(PARAMS_FOR_PRESENT)
        param_for_present['data']['server_hardware'] = "ServerHardwareName"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.side_effect = TASK_ERROR
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ansible_module.params = param_for_present

        ServerProfileModule().run()

        times_get_targets_called = self.mock_ov_client.server_profiles.get_available_targets.call_count
        self.assertEqual(0, times_get_targets_called)

        times_create_called = self.mock_ov_client.server_profiles.create.call_count
        self.assertEqual(25, times_create_called)

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ServerProfileModule.MSG_ERROR_ALLOCATE_SERVER_HARDWARE
        )

    def test_should_try_create_with_informed_hardware_2_times_when_not_exists(self):
        profile_data = deepcopy(BASIC_PROFILE)
        profile_data['serverHardwareUri'] = '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'

        params_for_present = deepcopy(PARAMS_FOR_PRESENT)
        params_for_present['data']['server_hardware'] = "ServerHardwareName"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.side_effect = [TASK_ERROR, CREATED_BASIC_PROFILE]
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ansible_module.params = params_for_present

        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        times_get_targets_called = self.mock_ov_client.server_profiles.get_available_targets.call_count
        self.assertEqual(0, times_get_targets_called)

        create_calls = [mock.call(profile_data), mock.call(profile_data)]
        self.mock_ov_client.server_profiles.create.assert_has_calls(create_calls)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_try_create_with_automatically_selected_hardware_25_times_when_not_exists(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.side_effect = TASK_ERROR
        self.mock_ov_client.server_profiles.get_available_targets.return_value = AVAILABLE_TARGETS
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        ServerProfileModule().run()

        times_get_targets_called = self.mock_ov_client.server_profiles.get_available_targets.call_count
        self.assertEqual(25, times_get_targets_called)

        times_create_called = self.mock_ov_client.server_profiles.create.call_count
        self.assertEqual(25, times_create_called)

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ServerProfileModule.MSG_ERROR_ALLOCATE_SERVER_HARDWARE
        )

    def test_should_fail_when_exception_is_not_related_with_server_hardware(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.side_effect = HPOneViewException(FAKE_MSG_ERROR)
        self.mock_ov_client.server_profiles.get_available_targets.return_value = AVAILABLE_TARGETS
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        ServerProfileModule().run()

        times_get_targets_called = self.mock_ov_client.server_profiles.get_available_targets.call_count
        self.assertEqual(1, times_get_targets_called)

        times_create_called = self.mock_ov_client.server_profiles.create.call_count
        self.assertEqual(1, times_create_called)

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )

    def test_fail_when_informed_template_not_exist_for_creation(self):
        params_for_present = deepcopy(PARAMS_FOR_PRESENT)
        params_for_present['data']['server_hardware'] = "ServerHardwareName"
        params_for_present['data']['server_template'] = "TemplateA200"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = None
        self.mock_ansible_module.params = params_for_present

        ServerProfileModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg="Informed Server Profile Template 'TemplateA200' not found")

    def test_fail_when_informed_hardware_not_exist_for_creation(self):
        params_for_present = deepcopy(PARAMS_FOR_PRESENT)
        params_for_present['data']['server_hardware'] = "ServerHardwareName"
        params_for_present['data']['server_template'] = "TemplateA200"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_hardware.get_by.return_value = None
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE
        self.mock_ansible_module.params = params_for_present

        ServerProfileModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg="Informed Server Hardware 'ServerHardwareName' not found")

    def test_should_create_without_hardware_when_there_are_any_available(self):
        available_targets = deepcopy(AVAILABLE_TARGETS)
        available_targets['targets'] = []

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_profiles.create.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_profiles.get_available_targets.return_value = available_targets
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)
        mock_facts = gather_facts(self.mock_ov_client, created=True)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.create.assert_called_once_with(deepcopy(BASIC_PROFILE))
        power_set_calls = self.mock_ov_client.server_hardware.update_power_state.call_count
        self.assertEqual(0, power_set_calls)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_CREATED,
            ansible_facts=mock_facts
        )

    def test_should_replace_os_deployment_name_by_uri_on_creation(self):
        uri = '/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493'

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.os_deployment_plans.get_by.return_value = [dict(uri=uri)]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0][SPKeys.OS_DEPLOYMENT], dict(osDeploymentPlanUri=uri))

    def test_should_fail_when_deployment_plan_not_found_on_creation(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.os_deployment_plans.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND + "Deployment Plan Name"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_enclosure_group_name_by_uri_on_creation(self):
        uri = '/rest/enclosure-groups/81decf85-0dff-4a5e-8a95-52994eeb6493'

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.enclosure_groups.get_by.return_value = [dict(uri=uri)]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0].get('enclosureGroupUri'), uri)
        self.assertFalse(args[0].get('enclosureGroupName'))

    def test_should_fail_when_enclosure_group_not_found_on_creation(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.enclosure_groups.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        message = ServerProfileReplaceNamesByUris.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND + "Enclosure Group Name"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=message)

    def test_should_replace_connections_name_by_uri_on_creation(self):
        conn_1 = dict(name="connection-1", networkUri='/rest/fc-networks/98')
        conn_2 = dict(name="connection-2", networkName='FC Network')
        conn_3 = dict(name="connection-3", networkName='Ethernet Network')

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [conn_1, conn_2, conn_3]

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.fc_networks.get_by.side_effect = [[dict(uri='/rest/fc-networks/14')], []]
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [dict(name="connection-1", networkUri='/rest/fc-networks/98'),
                                dict(name="connection-2", networkUri='/rest/fc-networks/14'),
                                dict(name="connection-3", networkUri='/rest/ethernet-networks/18')]

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0].get(SPKeys.CONNECTIONS), expected_connections)

    def test_should_fail_when_network_not_found_on_creation(self):
        conn = dict(name="connection-1", networkName='FC Network')

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [conn]

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_NETWORK_NOT_FOUND + "FC Network"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_server_hardware_type_name_by_uri(self):
        sht_uri = "/rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C"
        sht = {"name": "SY 480 Gen9 1", "uri": sht_uri}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_hardware_types.get_by.return_value = [sht]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0].get('serverHardwareTypeUri'), sht_uri)
        self.assertEqual(args[0].get('serverHardwareTypeName'), None)

    def test_should_fail_when_server_hardware_type_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_hardware_types.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SERVER_HARDWARE_TYPE_NOT_FOUND + "SY 480 Gen9 1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_volume_names_by_uri(self):
        volume1 = {"name": "volume1", "uri": "/rest/storage-volumes/1"}
        volume2 = {"name": "volume2", "uri": "/rest/storage-volumes/2"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1"},
                {"id": 2, "volumeName": "volume2"}
            ]
        }
        expected_dict = deepcopy(params['data'])
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeUri": "/rest/storage-volumes/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeUri": "/rest/storage-volumes/2"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.volumes.get_by.side_effect = [[volume1], [volume2]]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)

    def test_should_not_replace_when_inform_volume_uri(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_volume_attachments_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_san_storage_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_fail_when_volume_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1"}
            ]}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.volumes.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.VOLUME_NOT_FOUND + "volume1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_storage_pool_names_by_uri(self):
        pool1 = {"name": "pool1", "uri": "/rest/storage-pools/1"}
        pool2 = {"name": "pool2", "uri": "/rest/storage-pools/2"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"},
                {"id": 2, "volumeStoragePoolName": "pool2"}
            ]
        }
        expected_dict = deepcopy(params['data'])
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStoragePoolUri": "/rest/storage-pools/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStoragePoolUri": "/rest/storage-pools/2"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_pools.get_by.side_effect = [[pool1], [pool2]]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)

    def test_should_not_replace_when_inform_storage_pool_uri(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeStoragePoolUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_volume_attachments_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_san_storage_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_fail_when_storage_pool_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"}
            ]
        }

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_POOL_NOT_FOUND + "pool1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_storage_system_names_by_uri(self):
        storage_system1 = {"name": "system1", "uri": "/rest/storage-systems/1"}
        storage_system2 = {"name": "system2", "uri": "/rest/storage-systems/2"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"},
                {"id": 2, "volumeStorageSystemName": "system2"}
            ]
        }
        expected = deepcopy(params['data'])
        expected['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"}
        expected['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_systems.get_by.side_effect = [[storage_system1], [storage_system2]]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected)

    def test_should_not_replace_when_inform_storage_system_uri(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"},
                {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}
            ]
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_volume_attachments_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_san_storage_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_fail_when_storage_system_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"}
            ]
        }

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_systems.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_SYSTEM_NOT_FOUND + "system1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_enclosure_name_by_uri(self):
        uri = "/rest/enclosures/09SGH100X6J1"
        enclosure = {"name": "Enclosure-474", "uri": uri}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.enclosures.get_by.return_value = [enclosure]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0].get('enclosureUri'), uri)
        self.assertEqual(args[0].get('enclosureName'), None)

    def test_should_fail_when_enclosure_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.enclosures.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.ENCLOSURE_NOT_FOUND + "Enclosure-474"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_interconnect_name_by_uri(self):
        interconnect1 = {"name": "interconnect1", "uri": "/rest/interconnects/1"}
        interconnect2 = {"name": "interconnect2", "uri": "/rest/interconnects/2"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['connections'] = [
            {"id": 1, "interconnectName": "interconnect1"},
            {"id": 2, "interconnectName": "interconnect2"}
        ]

        expected = deepcopy(params['data'])
        expected['connections'][0] = {"id": 1, "interconnectUri": "/rest/interconnects/1"}
        expected['connections'][1] = {"id": 2, "interconnectUri": "/rest/interconnects/2"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.interconnects.get_by.side_effect = [[interconnect1], [interconnect2]]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected)

    def test_should_not_replace_when_inform_interconnect_uri(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['connections'] = [
            {"id": 1, "interconnectUri": "/rest/interconnects/1"},
            {"id": 2, "interconnectUri": "/rest/interconnects/2"}
        ]

        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_not_replace_interconnect_name_when_connections_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['connections'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_fail_when_interconnect_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['connections'] = [{"id": 1, "interconnectName": "interconnect1"}]

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.interconnects.get_by.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.INTERCONNECT_NOT_FOUND + "interconnect1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_firmware_baseline_name_by_uri(self):
        firmware_driver = {"name": "firmwareName001", "uri": "/rest/firmware-drivers/1"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        expected = deepcopy(params['data'])
        expected['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.firmware_drivers.get_by.return_value = [firmware_driver]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected)

    def test_should_not_replace_when_inform_firmware_baseline_uri(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_not_replace_firmware_baseline_name_when_firmware_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['firmware'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_fail_when_firmware_baseline_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.firmware_drivers.get_by.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.FIRMWARE_DRIVER_NOT_FOUND + "firmwareName001"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_sas_logical_jbod_names_by_uris(self):
        sas_logical_jbod1 = {"name": "jbod1", "uri": "/rest/sas-logical-jbods/1"}
        sas_logical_jbod2 = {"name": "jbod2", "uri": "/rest/sas-logical-jbods/2"}
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"},
                {"id": 2, "sasLogicalJBODName": "jbod2"}
            ]
        }
        expected = deepcopy(params['data'])
        expected['localStorage']['sasLogicalJBODs'][0] = {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"}
        expected['localStorage']['sasLogicalJBODs'][1] = {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.sas_logical_jbods.get_by.side_effect = [[sas_logical_jbod1], [sas_logical_jbod2]]

        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected)

    def test_should_not_replace_when_inform_sas_logical_jbod_uris(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"},
                {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}
            ]
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_jbod_list_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['localStorage'] = {
            "sasLogicalJBODs": None
        }
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_local_storage_is_none(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['localStorage'] = None
        expected_dict = deepcopy(params['data'])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0], expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_fail_when_sas_logical_jbod_name_not_found(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"}
            ]
        }

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.sas_logical_jbods.get_by.return_value = []
        self.mock_ansible_module.params = params

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SAS_LOGICAL_JBOD_NOT_FOUND + "jbod1"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_remove_mac_from_connections_before_create_when_mac_is_virtual(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
        params['data'][SPKeys.MAC_TYPE] = 'Virtual'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [deepcopy(CONNECTION_1), deepcopy(CONNECTION_2)]
        expected_connections[0].pop(SPKeys.MAC)
        expected_connections[1].pop(SPKeys.MAC)

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    def test_should_remove_mac_from_connections_before_create_when_mac_is_physical(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
        params['data'][SPKeys.MAC_TYPE] = 'Physical'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [deepcopy(CONNECTION_1), deepcopy(CONNECTION_2)]
        expected_connections[0].pop(SPKeys.MAC)
        expected_connections[1].pop(SPKeys.MAC)

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    def test_should_remove_serial_number_before_create_when_serial_number_type_is_virtual(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Virtual'
        params['data'][SPKeys.UUID] = 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806'
        params['data'][SPKeys.SERIAL_NUMBER] = 'VCGNC3V000'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertTrue(SPKeys.UUID not in args[0])
        self.assertTrue(SPKeys.SERIAL_NUMBER not in args[0])

    def test_should_remove_serial_number_before_create_when_serial_number_type_is_physical(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Physical'
        params['data'][SPKeys.UUID] = 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806'
        params['data'][SPKeys.SERIAL_NUMBER] = 'VCGNC3V000'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertTrue(SPKeys.UUID not in args[0])
        self.assertTrue(SPKeys.SERIAL_NUMBER not in args[0])

    def test_should_remove_wwpn_from_conns_before_create_when_wwpn_is_virtual_or_physical(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1_WITH_WWPN, CONNECTION_2_WITH_WWPN]
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [deepcopy(CONNECTION_1_WITH_WWPN), deepcopy(CONNECTION_2_WITH_WWPN)]
        expected_connections[0].pop(SPKeys.WWNN)
        expected_connections[0].pop(SPKeys.WWPN)
        expected_connections[1].pop(SPKeys.WWNN)
        expected_connections[1].pop(SPKeys.WWPN)

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    def test_should_remove_drive_number_from_controller_drives_before_create(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.LOCAL_STORAGE] = dict(controllers=[CONTROLLER_EMBEDDED.copy()])

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_drives = deepcopy(DRIVES_CONTROLLER_EMBEDDED)
        expected_drives[0].pop(SPKeys.DRIVE_NUMBER)
        expected_drives[1].pop(SPKeys.DRIVE_NUMBER)

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertEqual(args[0][SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][0][SPKeys.LOGICAL_DRIVES], expected_drives)

    def test_should_remove_lun_from_san_volumes_before_create_when_luntype_is_auto(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SAN] = SAN_STORAGE

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_volumes = [deepcopy(VOLUME_1), deepcopy(VOLUME_2)]
        expected_volumes[0].pop(SPKeys.LUN)
        expected_volumes[1].pop(SPKeys.LUN)

        args, _ = self.mock_ov_client.server_profiles.create.call_args
        self.assertFalse(args[0][SPKeys.SAN][SPKeys.VOLUMES][0].get(SPKeys.LUN))
        self.assertFalse(args[0][SPKeys.SAN][SPKeys.VOLUMES][1].get(SPKeys.LUN))

    def test_should_not_fail_creating_basic_server_profile_when_assignment_types_are_virtual(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.MAC_TYPE] = 'Virtual'
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Virtual'
        params['data'][SPKeys.WWPN_TYPE] = 'Virtual'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.create.assert_called_once()

    def test_should_not_fail_creating_basic_server_profile_when_assignment_types_are_physical(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.MAC_TYPE] = 'Physical'
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Physical'
        params['data'][SPKeys.WWPN_TYPE] = 'Physical'

        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.create.assert_called_once()

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_update_when_data_changed(self, mock_resource_compare):
        profile_data = deepcopy(BASIC_PROFILE)
        mock_resource_compare.return_value = False

        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ov_client.server_profiles.update.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        mock_facts = gather_facts(self.mock_ov_client)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.update.assert_called_once_with(profile_data, SERVER_PROFILE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_UPDATED,
            ansible_facts=mock_facts
        )

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_power_off_before_update_when_data_changed(self, mock_resource_compare):
        fake_profile_data = deepcopy(BASIC_PROFILE)
        fake_profile_data['serverHardwareUri'] = SHT_URI

        mock_resource_compare.return_value = False

        self.mock_ov_client.server_profiles.get_by_name.return_value = fake_profile_data
        self.mock_ov_client.server_profiles.update.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        mock_facts = gather_facts(self.mock_ov_client)

        ServerProfileModule().run()

        power_set_calls = [
            mock.call(dict(powerState='Off', powerControl='PressAndHold'), SHT_URI),
            mock.call(dict(powerState='On', powerControl='MomentaryPress'), SHT_URI)]
        self.mock_ov_client.server_hardware.update_power_state.assert_has_calls(power_set_calls)

        self.mock_ov_client.server_profiles.update.assert_called_once_with(fake_profile_data, SERVER_PROFILE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_UPDATED,
            ansible_facts=mock_facts
        )

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_update_when_data_is_equals(self, mock_resource_compare):
        profile_data = deepcopy(CREATED_BASIC_PROFILE)

        mock_resource_compare.return_value = True
        mock_facts = gather_facts(self.mock_ov_client)
        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        ServerProfileModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerProfileModule.MSG_ALREADY_PRESENT,
            ansible_facts=mock_facts
        )

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_change_power_state_when_data_is_equals(self, mock_resource_compare):
        profile_data = deepcopy(CREATED_BASIC_PROFILE)

        mock_resource_compare.return_value = True
        gather_facts(self.mock_ov_client)
        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        ServerProfileModule().run()

        self.mock_ov_client.server_hardware.update_power_state.not_been_called()

    @mock.patch.object(ResourceComparator, 'compare')
    def test_fail_when_informed_template_not_exist_for_update(self, mock_resource_compare):
        profile_data = deepcopy(CREATED_BASIC_PROFILE)

        params_for_present = deepcopy(PARAMS_FOR_PRESENT)
        params_for_present['data']['server_hardware'] = "ServerHardwareName"
        params_for_present['data']['server_template'] = "TemplateA200"

        mock_resource_compare.return_value = False

        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ov_client.server_hardware.get_by.return_value = [FAKE_SERVER_HARDWARE]
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = None

        self.mock_ansible_module.params = params_for_present

        ServerProfileModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg="Informed Server Profile Template 'TemplateA200' not found")

    @mock.patch.object(ResourceComparator, 'compare')
    def test_fail_when_informed_hardware_not_exist_for_update(self, mock_resource_compare):
        profile_data = deepcopy(CREATED_BASIC_PROFILE)

        params_for_present = deepcopy(PARAMS_FOR_PRESENT)
        params_for_present['data']['server_hardware'] = "ServerHardwareName"
        params_for_present['data']['server_template'] = "TemplateA200"

        mock_resource_compare.return_value = False

        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ov_client.server_hardware.get_by.return_value = None
        self.mock_ov_client.server_profile_templates.get_by_name.return_value = BASIC_TEMPLATE

        self.mock_ansible_module.params = params_for_present

        ServerProfileModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg="Informed Server Hardware 'ServerHardwareName' not found")

    @mock.patch.object(ResourceComparator, 'compare')
    @mock.patch.object(ServerProfileMerger, 'merge_data')
    def test_should_call_deep_merge_when_resource_found(self, mock_deep_merge, mock_resource_compare):
        server_profile = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.server_profiles.get_by_name.return_value = server_profile
        self.mock_ov_client.server_profiles.update.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        ServerProfileModule().run()

        mock_deep_merge.assert_called_once_with(server_profile, PARAMS_FOR_PRESENT['data'])

    @mock.patch.object(ResourceComparator, 'compare')
    @mock.patch.object(ServerProfileMerger, 'merge_data')
    def test_should_compare_original_and_merged_resource(self, mock_deep_merge, mock_resource_compare):
        server_profile = deepcopy(BASIC_PROFILE)
        merged_data = dict(name="merged data")
        self.mock_ov_client.server_profiles.get_by_name.return_value = server_profile
        self.mock_ov_client.server_profiles.update.return_value = CREATED_BASIC_PROFILE
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_PRESENT)

        mock_deep_merge.return_value = merged_data

        ServerProfileModule().run()

        mock_resource_compare.assert_called_once_with(server_profile, merged_data)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_replace_os_deployment_name_by_uri_on_update(self, mock_resource_compare):
        uri = '/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493'
        mock_resource_compare.return_value = False

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.os_deployment_plans.get_by.return_value = [dict(uri=uri)]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.OS_DEPLOYMENT], dict(osDeploymentPlanUri=uri))

    def test_should_fail_when_deployment_plan_not_found_on_update(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.os_deployment_plans.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND + "Deployment Plan Name"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    def test_should_replace_enclosure_group_name_by_uri_on_update(self):
        uri = '/rest/enclosure-groups/81decf85-0dff-4a5e-8a95-52994eeb6493'

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.enclosure_groups.get_by.return_value = [dict(uri=uri)]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0].get('enclosureGroupUri'), uri)
        self.assertFalse(args[0].get('enclosureGroupName'))

    def test_should_fail_when_enclosure_group_not_found_on_update(self):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.enclosure_groups.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        message = ServerProfileReplaceNamesByUris.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND + "Enclosure Group Name"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=message)

    def test_should_replace_connections_name_by_uri_on_update(self):
        conn_1 = dict(name="connection-1", networkUri='/rest/fc-networks/98')
        conn_2 = dict(name="connection-2", networkName='FC Network')
        conn_3 = dict(name="connection-3", networkName='Ethernet Network')

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [conn_1, conn_2, conn_3]

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.fc_networks.get_by.side_effect = [[dict(uri='/rest/fc-networks/14')], []]
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [dict(name="connection-1", networkUri='/rest/fc-networks/98'),
                                dict(name="connection-2", networkUri='/rest/fc-networks/14'),
                                dict(name="connection-3", networkUri='/rest/ethernet-networks/18')]

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0].get(SPKeys.CONNECTIONS), expected_connections)

    def test_should_fail_when_network_not_found_on_update(self):
        conn = dict(name="connection-1", networkName='FC Network')

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [conn]

        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.ethernet_networks.get_by.return_value = []
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_NETWORK_NOT_FOUND + "FC Network"
        self.mock_ansible_module.fail_json.assert_called_once_with(msg=expected_error)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_mac_from_connections_before_update_when_mac_is_virtual(self, mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
        params['data'][SPKeys.MAC_TYPE] = 'Virtual'

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [CONNECTION_1, CONNECTION_2]
        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_mac_from_connections_before_update_when_mac_is_physical(self, mock_resource_compare):
        mock_resource_compare.return_value = False

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
        params['data'][SPKeys.MAC_TYPE] = 'Physical'

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [CONNECTION_1, CONNECTION_2]
        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_serial_number_before_update_when_serial_number_type_is_virtual(self,
                                                                                              mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Virtual'
        params['data'][SPKeys.UUID] = 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806'
        params['data'][SPKeys.SERIAL_NUMBER] = 'VCGNC3V000'

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.UUID], 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806')
        self.assertEqual(args[0][SPKeys.SERIAL_NUMBER], 'VCGNC3V000')

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_serial_number_before_update_when_serial_number_type_is_physical(self,
                                                                                               mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SERIAL_NUMBER_TYPE] = 'Physical'
        params['data'][SPKeys.UUID] = 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806'
        params['data'][SPKeys.SERIAL_NUMBER] = 'VCGNC3V000'

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.UUID], 'eb0e2fac-bbe5-4ad1-84d3-3e38481c9806')
        self.assertEqual(args[0][SPKeys.SERIAL_NUMBER], 'VCGNC3V000')

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_wwpn_from_conns_before_update_when_wwpn_is_virtual(self, mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_1_WITH_WWPN]

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [CONNECTION_1_WITH_WWPN]
        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_wwpn_from_conns_before_update_when_wwpn_is_physical(self, mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.CONNECTIONS] = [CONNECTION_2_WITH_WWPN]

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_connections = [CONNECTION_2_WITH_WWPN]
        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.CONNECTIONS], expected_connections)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_drive_number_from_controller_drives_before_update(self, mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.LOCAL_STORAGE] = dict(controllers=[CONTROLLER_EMBEDDED.copy()])

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        expected_drives = DRIVES_CONTROLLER_EMBEDDED
        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][0][SPKeys.LOGICAL_DRIVES], expected_drives)

    @mock.patch.object(ResourceComparator, 'compare')
    def test_should_not_remove_lun_from_san_volumes_before_update_when_luntype_is_auto(self,
                                                                                       mock_resource_compare):
        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data'][SPKeys.SAN] = SAN_STORAGE

        mock_resource_compare.return_value = False
        self.mock_ov_client.server_profiles.get_by_name.return_value = deepcopy(BASIC_PROFILE)
        self.mock_ansible_module.params = deepcopy(params)

        ServerProfileModule().run()

        args, _ = self.mock_ov_client.server_profiles.update.call_args
        self.assertEqual(args[0][SPKeys.SAN][SPKeys.VOLUMES][0], VOLUME_1)
        self.assertEqual(args[0][SPKeys.SAN][SPKeys.VOLUMES][1], VOLUME_2)

    def test_should_do_nothing_when_server_hardware_already_absent(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT)

        ServerProfileModule().run()

        self.mock_ov_client.server_profiles.delete.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerProfileModule.MSG_ALREADY_ABSENT
        )

    def test_should_turn_off_hardware_before_delete(self):
        sh_uri = '/rest/server-hardware/37333036-3831-76jh-4831-303658389766'
        profile_data = deepcopy(BASIC_PROFILE)
        profile_data['serverHardwareUri'] = sh_uri

        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT)

        ServerProfileModule().run()

        self.mock_ov_client.server_hardware.update_power_state.assert_called_once_with(
            {'powerControl': 'PressAndHold', 'powerState': 'Off'}, sh_uri)

        self.mock_ov_client.server_profiles.delete.assert_called_once_with(profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_DELETED
        )

    def test_should_not_turn_off_hardware_if_not_associated_before_delete(self):
        profile_data = deepcopy(BASIC_PROFILE)

        self.mock_ov_client.server_profiles.get_by_name.return_value = profile_data

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_ABSENT)

        ServerProfileModule().run()

        times_power_off_was_called = self.mock_ov_client.server_hardware.update_power_state.call_count
        self.assertEqual(0, times_power_off_was_called)

        self.mock_ov_client.server_profiles.delete.assert_called_once_with(profile_data)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerProfileModule.MSG_DELETED
        )


if __name__ == '__main__':
    unittest.main()
