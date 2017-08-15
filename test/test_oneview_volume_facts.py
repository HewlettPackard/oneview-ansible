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

from oneview_module_loader import VolumeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_ALL_WITH_OPTIONS = dict(
    config='config.json',
    name=None,
    options=[
        'attachableVolumes', 'extraManagedVolumePaths'
    ],
    params={
        'networks': ['rest/fake/network']
    }
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Volume"
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Volume",
    options=[
        'attachableVolumes', 'extraManagedVolumePaths', 'snapshots']
)

PARAMS_GET_SNAPSHOT_BY_NAME = dict(
    config='config.json',
    name="Test Volume",
    options=[{"snapshots": {"name": 'snapshot_name'}}])


class VolumeFactsSpec(unittest.TestCase,
                      FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, VolumeFactsModule)
        self.resource = self.mock_ov_client.volumes
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_volumes(self):
        self.resource.get_all.return_value = [{"name": "Test Volume"}]
        self.mock_ansible_module.params = PARAMS_GET_ALL

        VolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume"}]))

    def test_should_get_all_volumes_and_appliance_information(self):
        self.resource.get_all.return_value = [{"name": "Test Volume"}]
        self.resource.get_extra_managed_storage_volume_paths.return_value = ['/path1', '/path2']
        self.resource.get_attachable_volumes.return_value = [{"name": "attachable Volume 1"}]

        self.mock_ansible_module.params = PARAMS_GET_ALL_WITH_OPTIONS

        VolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume"}],
                               attachable_volumes=[{"name": "attachable Volume 1"}],
                               extra_managed_volume_paths=['/path1', '/path2']))

    def test_should_get_volume_by_name(self):
        self.resource.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        VolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}]))

    def test_should_get_volume_by_name_with_snapshots_and_appliance_information(self):
        self.resource.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]
        self.resource.get_extra_managed_storage_volume_paths.return_value = ['/path1', '/path2']
        self.resource.get_attachable_volumes.return_value = [{"name": "attachable Volume 1"}]
        self.resource.get_snapshots.return_value = [{"filename": "snapshot_name"}]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        VolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}],
                               attachable_volumes=[{"name": "attachable Volume 1"}],
                               extra_managed_volume_paths=['/path1', '/path2'],
                               snapshots=[{"filename": "snapshot_name"}]))

    def test_should_get_volume_by_name_with_snapshots_by_name(self):
        self.resource.get_by.return_value = [{"name": "Test Volume", 'uri': '/uri'}]
        self.resource.get_snapshot_by.return_value = [{"filename": "snapshot_name"}]

        self.mock_ansible_module.params = PARAMS_GET_SNAPSHOT_BY_NAME

        VolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volumes=[{"name": "Test Volume", 'uri': '/uri'}],
                               snapshots=[{"filename": "snapshot_name"}]))


if __name__ == '__main__':
    unittest.main()
