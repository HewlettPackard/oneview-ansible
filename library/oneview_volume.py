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


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_volume
short_description: Manage OneView Volume resources.
description:
    - Provides an interface to manage Volume resources. It allows create, update, delete or repair the volume, and
      create or delete a snapshot.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
        description:
            - Indicates the desired state for the Volume resource.
              C(present) creates/adds the resource when it does not exist, otherwise it updates the resource. When the
              resource already exists, the update operation is non-convergent, since it is always called even though
              the given options are compliant with the existent data. To change the name of the volume, a C(newName) in
              the I(data) must be provided.
              C(absent) by default deletes a volume from OneView and the storage system. When export_only is True, the
              volume is removed only from OneView.
              C(repaired) removes extra presentations from a specified volume on the storage system. This operation is
              non-idempotent.
              C(snapshot_created) creates a snapshot for the volume specified. This operation is non-idempotent.
              C(snapshot_deleted) deletes a snapshot from OneView and the storage system.
        choices: ['present', 'absent', 'repaired', 'snapshot_created', 'snapshot_deleted']
    data:
      description:
        - Volume or snapshot data.
      required: true
    export_only:
      description:
        - If set to True, when the status is C(absent) and the resource exists, it will be removed only from OneView.
      default: False
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Volume with a specified Storage Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      properties:
        name: 'Volume with Storage Pool'
        description: 'Test volume with common creation: Storage Pool'
        size: 2147483648  # 2GB
        storagePool: '{{ storage_pool_uri }}'
      templateUri: '/rest/storage-volume-templates/e2f95f1d-de9d-406e-803f-a8aa00da92b0'
      isPermanent: false
      initialScopeUris: ['/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7']
  delegate_to: localhost

- name: Create a volume with a specified Snapshot Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      properties:
        name: 'Volume with Snapshot Pool'
        description: 'Test volume with common creation: Storage System + Storage Pool + Snapshot Pool'
        size: 1073741824  # 1GB
        storagePool: '{{ storage_pool_uri }}'
        snapshotPool: '{{ storage_pool_uri }}'
      templateUri: '/rest/storage-volume-templates/e2f95f1d-de9d-406e-803f-a8aa00da92b0'
      isPermanent: false
      initialScopeUris: ['/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7']
  delegate_to: localhost

- name: Add a volume for management by the appliance using the WWN of the volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 300
    state: present
    data:
      type: AddStorageVolumeV2
      name: 'Volume added with a specific WWN'
      description: 'Test volume added for management: Storage System + Storage Pool + WWN'
      storageSystemUri: '/rest/storage-systems/TXQ1000307'
      wwn: 'DC:32:13:72:47:00:10:00:30:71:47:16:33:58:47:95'
      provisioningParameters:
          shareable: True
  when: wwn is defined

- name: Update the name of the volume to 'Volume with Storage Pool - Renamed' and shareable to false
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'Volume with Storage Pool'
      newName: 'Volume with Storage Pool - Renamed'
      isShareable: False
    delegate_to: localhost

- name: Remove extra presentations from the specified volume on the storage system
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: repaired
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Create a new snapshot for the specified volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: snapshot_created
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'
        description: 'New snapshot'

- name: Delete the snapshot
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: snapshot_deleted
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'

- name: Delete the volume previously created with a Storage Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Delete the volume previously created with a Snapshot Pool
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'Volume with Snapshot Pool - Renamed'

- name: Delete the volume previously added using the WWN of the volume
  oneview_volume:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    data:
      name: 'Volume added with a specific WWN'
    export_only: True
'''

RETURN = '''
storage_volume:
    description: Has the facts about the Storage Volume.
    returned: On state 'present', but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleValueError, OneViewModuleResourceNotFound, OneViewModuleException, compare


class VolumeModule(OneViewModule):
    MSG_CREATED = 'Volume added/created successfully.'
    MSG_UPDATED = 'Volume updated successfully.'
    MSG_DELETED = 'Volume removed/deleted successfully.'
    MSG_REPAIRED = 'Volume repaired successfully.'
    MSG_ALREADY_MANAGED = 'Volume is already managed by the appliance.'
    MSG_ADDED = 'Volume is now managed by the appliance.'
    MSG_SNAPSHOT_CREATED = 'Volume snapshot created successfully.'
    MSG_SNAPSHOT_DELETED = 'Volume snapshot deleted successfully.'
    MSG_NOT_FOUND = 'Volume not found.'
    MSG_SNAPSHOT_NOT_FOUND = 'Snapshot not found.'
    MSG_ALREADY_ABSENT = 'Volume is already absent.'
    MSG_NO_OPTIONS_PROVIDED = 'No options provided.'
    MSG_NEW_NAME_INVALID = 'Rename failed: the new name provided is being used by another Volume.'
    MSG_NO_CHANGES_PROVIDED = 'No changed have been provided fro the update.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent', 'managed', 'repaired',
                         'snapshot_created', 'snapshot_deleted']
            ),
            data=dict(required=True, type='dict'),
            export_only=dict(required=False, type='bool'),
            suppress_device_updates=dict(required=False, type='bool')
        )
        super(VolumeModule, self).__init__(additional_arg_spec=argument_spec,
                                           validate_etag_support=True)

        name = self.__find_resource_name()
        self.set_resource_object(self.oneview_client.volumes, name)

    def __find_resource_name(self):
        name = None
        if self.data:
            if self.data.get('deviceVolumeName'):
                name = self.data.get('deviceVolumeName')
            elif self.data.get('properties'):
                name = self.data.get('properties').get('name')
        return name

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        if self.state == 'managed':
            return self.__managed()
        elif self.state == 'absent':
            return self.__absent()
        else:
            if not self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

            if self.state == 'repaired':
                return self.__repair()
            elif self.state == 'snapshot_created':
                return self.__create_snapshot()
            elif self.state == 'snapshot_deleted':
                return self.__delete_snapshot()

    def __present(self):
        if 'snapshotUri' in self.data:
            return self.__create_from_snapshot()
        elif not self.current_resource:
            return self.__create()
        else:
            return self.__update()

    def __managed(self):
        if not self.current_resource:
            added_volume = self.resource_client.add_from_existing(self.data)
            changed = True
            msg = self.MSG_ADDED
        else:
            added_volume = self.current_resource.data
            changed = False
            msg = self.MSG_ALREADY_MANAGED

        return dict(changed=changed, msg=msg, ansible_facts=dict(storage_volume=added_volume))

    def __absent(self):
        if self.current_resource:
            self.current_resource.delete()
            return dict(changed=True, msg=self.MSG_DELETED)
        else:
            return dict(changed=False, msg=self.MSG_ALREADY_ABSENT)

    def __create(self):
        created_volume = self.resource_client.create(self.data)
        return dict(changed=True,
                    msg=self.MSG_CREATED,
                    ansible_facts=dict(storage_volume=created_volume.data))

    def __create_from_snapshot(self):
        created_volume = self.resource_client.create_from_snapshot(self.data)
        return dict(changed=True,
                    msg=self.MSG_CREATED,
                    ansible_facts=dict(storage_volume=created_volume.data))

    def __update(self):
        if "newName" in self.data:
            new_resource = self.resource_client.get_by_name(self.data["newName"])
            if new_resource:
                raise OneViewModuleValueError(self.MSG_NEW_NAME_INVALID)
            self.data["name"] = self.data.pop("newName")

        merged_data = self.current_resource.data.copy()
        merged_data.update(self.data)

        if compare(self.current_resource.data, merged_data):
            changed = False
            msg = self.MSG_NO_CHANGES_PROVIDED
        else:
            changed = True
            self.current_resource.update(merged_data)
            msg = self.MSG_UPDATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(storage_volume=self.current_resource.data))

    def __repair(self):

        self.current_resource.repair()
        return dict(changed=True, msg=self.MSG_REPAIRED)

    def __create_snapshot(self):
        if 'snapshotParameters' not in self.data:
            raise OneViewModuleResourceNotFound(self.MSG_NO_OPTIONS_PROVIDED)

        self.current_resource.create_snapshot(self.data["snapshotParameters"])
        return dict(changed=True, msg=self.MSG_SNAPSHOT_CREATED)

    def __delete_snapshot(self):
        if 'snapshotParameters' not in self.data:
            raise OneViewModuleResourceNotFound(self.MSG_NO_OPTIONS_PROVIDED)
        snapshot_parameters = self.data['snapshotParameters']

        snapshot = self.current_resource.get_snapshot_by_name(snapshot_parameters['name'])
        if not snapshot:
            raise OneViewModuleResourceNotFound(self.MSG_SNAPSHOT_NOT_FOUND)
        else:
            snapshot.delete()
            return dict(changed=True, msg=self.MSG_SNAPSHOT_DELETED)


def main():
    VolumeModule().run()


if __name__ == '__main__':
    main()
