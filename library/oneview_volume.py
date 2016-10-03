#!/usr/bin/python

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

from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_volume
short_description: Manage OneView Volume resources.
description:
    - Provides an interface to manage Volume resources. It allows create, update, delete or repair the volume, and
      create or delete a snapshot.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    state:
        description:
            - Indicates the desired state for the Volume resource.
              'present' creates/adds the resource when it does not exist, otherwise it updates the resource. When the
              resource already exists, the update operation is non-idempotent, since it is always called even though
              the given options are compliant with the existent data. To change the name of the volume, a 'newName' in
              the data must be provided.
              'absent' by default deletes a volume from OneView and storage system. When export_only is True, the
              volume is removed only from OneView.
              'repaired' removes extra presentations from a specified volume on the storage system. This operation is
              non-idempotent.
              'snapshot_created' creates a snapshot for the volume specified. This operation is non-idempotent.
              'snapshot_deleted' deletes a snapshot from OneView and storage system.
        choices: ['present', 'absent', 'repaired', 'snapshot_created', 'snapshot_deleted']
    data:
      description:
        - Volume or snapshot data.
      required: true
    export_only:
      description:
        - If set to True, when the status is 'absent' and the resource exists, it will be removed only from OneView.
      default: False
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Create a Volume with a specified Storage Pool
  oneview_volume:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'Volume with Storage Pool'
      description: 'Test volume with common creation: Storage Pool'
      provisioningParameters:
          provisionType: 'Full'
          shareable: True
          requestedCapacity: 1073741824  # 1GB
          storagePoolUri: '/rest/storage-pools/3B1CF17F-7657-4C89-B580-D236507A9182'
  delegate_to: localhost

- name: Create a volume with a specified Snapshot Pool
  oneview_volume:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'Volume with Snapshot Pool'
      description: 'Test volume with common creation: Storage System + Storage Pool + Snapshot Pool'
      provisioningParameters:
          provisionType: 'Full'
          shareable: True
          requestedCapacity: 1073741824
          storagePoolUri: '/rest/storage-pools/3B1CF17F-7657-4C89-B580-D236507A9182'
      storageSystemUri: '/rest/storage-systems/TXQ1000307'
      snapshotPoolUri: '/rest/storage-pools/3B1CF17F-7657-4C89-B580-D236507A9182'
  delegate_to: localhost

- name: Add a volume for management by the appliance using the WWN of the volume
  oneview_volume:
    config: '{{ config_path }}'
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
    config: '{{ config_path }}'
    state: present
    data:
      name: 'Volume with Storage Pool'
      newName: 'Volume with Storage Pool - Renamed'
      shareable: False
    delegate_to: localhost

- name: Remove extra presentations from the specified volume on the storage system
  oneview_volume:
    config: '{{ config_path }}'
    state: repaired
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Create a new snapshot for the specified volume
    oneview_volume:
    config: '{{ config_path }}'
    state: snapshot_created
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'
        type: 'Snapshot'
        description: 'New snapshot'

- name: Delete the snapshot
    oneview_volume:
    config: '{{ config_path }}'
    state: snapshot_deleted
    data:
      name: 'Volume with Snapshot Pool'
      snapshotParameters:
        name: 'test_snapshot'

- name: Delete the volume previously created with a Storage Pool
  oneview_volume:
    config: '{{ config_path }}'
    state: absent
    data:
      name: 'Volume with Storage Pool - Renamed'

- name: Delete the volume previously created with a Snapshot Pool
  oneview_volume:
    config: '{{ config_path }}'
    state: absent
    data:
      name: 'Volume with Snapshot Pool - Renamed'

- name: Delete the volume previously added using the WWN of the volume
  oneview_volume:
    config: '{{ config_path }}'
    state: absent
    data:
      name: 'Volume added with a specific WWN'
    export_only: True
'''

RETURN = '''
storage_volume:
    description: Has the facts about the Storage Volume.
    returned: on state 'present', but can be null.
    type: complex
'''

VOLUME_CREATED = 'Volume added/created successfully.'
VOLUME_UPDATED = 'Volume updated successfully.'
VOLUME_DELETED = 'Volume removed/deleted successfully.'
VOLUME_REPAIRED = 'Volume repaired successfully.'
VOLUME_SNAPSHOT_CREATED = 'Volume snapshot created successfully.'
VOLUME_SNAPSHOT_DELETED = 'Volume snapshot deleted successfully.'
VOLUME_NOT_FOUND = 'Volume not found.'
VOLUME_SNAPSHOT_NOT_FOUND = 'Snapshot not found.'
VOLUME_ALREADY_ABSENT = 'Nothing to do.'
VOLUME_NO_OPTIONS_PROVIDED = 'No options provided.'
VOLUME_NEW_NAME_INVALID = 'Rename failed: the new name provided is being used by another Volume.'


class VolumeModule(object):
    argument_spec = dict(
        config=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent', 'repaired', 'snapshot_created', 'snapshot_deleted']
        ),
        data=dict(required=True, type='dict'),
        export_only=dict(required=False, type='bool'),
    )

    def __init__(self):
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def run(self):
        state = self.module.params['state']
        data = self.module.params['data'].copy()

        try:
            if state == 'present':
                self.__present(data)
            elif state == 'absent':
                export_only = self.module.params.get('export_only', False)
                self.__absent(data, export_only)
            elif state == 'repaired':
                self.__repair(data)
            elif state == 'snapshot_created':
                self.__create_snapshot(data)
            elif state == 'snapshot_deleted':
                self.__delete_snapshot(data)

        except Exception as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))

    def __present(self, data):
        resource = self.__get_by_name(data['name'])

        if not resource:
            self.__create(data)
        else:
            self.__update(data, resource)

    def __absent(self, data, export_only):
        resource = self.__get_by_name(data['name'])

        if resource:
            self.oneview_client.volumes.delete(resource, export_only=export_only)
            self.module.exit_json(changed=True,
                                  msg=VOLUME_DELETED)
        else:
            self.module.exit_json(changed=False, msg=VOLUME_ALREADY_ABSENT)

    def __create(self, data):
        created_volume = self.oneview_client.volumes.create(data)

        self.module.exit_json(changed=True,
                              msg=VOLUME_CREATED,
                              ansible_facts=dict(storage_volume=created_volume))

    def __update(self, data, resource):
        if 'newName' in data:
            if self.__get_by_name(data['newName']):
                raise Exception(VOLUME_NEW_NAME_INVALID)
            data['name'] = data.pop('newName')

        merged_data = resource.copy()
        merged_data.update(data)

        updated_volume = self.oneview_client.volumes.update(merged_data)

        self.module.exit_json(changed=True,
                              msg=VOLUME_UPDATED,
                              ansible_facts=dict(storage_volume=updated_volume))

    def __repair(self, data):
        resource = self.__get_by_name(data['name'])

        if resource:
            self.oneview_client.volumes.repair(resource['uri'])
            self.module.exit_json(changed=True,
                                  msg=VOLUME_REPAIRED)
        else:
            self.module.fail_json(msg=VOLUME_NOT_FOUND)

    def __create_snapshot(self, data):
        if 'snapshotParameters' not in data:
            raise Exception(VOLUME_NO_OPTIONS_PROVIDED)

        resource = self.__get_by_name(data['name'])

        if resource:
            self.oneview_client.volumes.create_snapshot(resource['uri'], data['snapshotParameters'])
            self.module.exit_json(changed=True,
                                  msg=VOLUME_SNAPSHOT_CREATED)
        else:
            self.module.fail_json(msg=VOLUME_NOT_FOUND)

    def __delete_snapshot(self, data):
        if 'snapshotParameters' not in data:
            raise Exception(VOLUME_NO_OPTIONS_PROVIDED)

        resource = self.__get_by_name(data['name'])

        if not resource:
            self.module.fail_json(msg=VOLUME_NOT_FOUND)
        else:
            snapshot = self.__get_snapshot_by_name(resource, data)
            if not snapshot:
                self.module.fail_json(msg=VOLUME_SNAPSHOT_NOT_FOUND)
            else:
                self.oneview_client.volumes.delete_snapshot(snapshot)
                self.module.exit_json(changed=True,
                                      msg=VOLUME_SNAPSHOT_DELETED)

    def __get_by_name(self, name):
        result = self.oneview_client.volumes.get_by('name', name)
        return result[0] if result else None

    def __get_snapshot_by_name(self, resource, data):
        if 'name' not in data['snapshotParameters']:
            raise Exception(VOLUME_NO_OPTIONS_PROVIDED)

        result = self.oneview_client.volumes.get_snapshot_by(resource['uri'], 'name',
                                                             data['snapshotParameters']['name'])
        return result[0] if result else None


def main():
    VolumeModule().run()


if __name__ == '__main__':
    main()
