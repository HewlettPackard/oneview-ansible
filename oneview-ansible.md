# Ansible HPE OneView Modules

### Modules

  * [hpe_icsp_os_deployment - Deploy the operating system on a server using HPE ICsp.](#hpe_icsp_os_deployment)
  * [hpe_icsp_server - Adds, removes and configures servers in ICsp.](#hpe_icsp_server)
  * [image_streamer_artifact_bundle - Manage the Artifact Bundle resource.](#image_streamer_artifact_bundle)
  * [image_streamer_artifact_bundle_facts - Retrieve facts about the Artifact Bundle.](#image_streamer_artifact_bundle_facts)
  * [image_streamer_build_plan - Manages Image Stream OS Build Plan resources.](#image_streamer_build_plan)
  * [image_streamer_build_plan_facts - Retrieve facts about one or more of the Image Streamer Build Plans.](#image_streamer_build_plan_facts)
  * [image_streamer_deployment_group_facts - Retrieve facts about the Image Streamer Deployment Groups.](#image_streamer_deployment_group_facts)
  * [image_streamer_deployment_plan - Manage Image Streamer Deployment Plan resources.](#image_streamer_deployment_plan)
  * [image_streamer_deployment_plan_facts - Retrieve facts about the Image Streamer Deployment Plans.](#image_streamer_deployment_plan_facts)
  * [image_streamer_golden_image - Manage Image Streamer Golden Image resources.](#image_streamer_golden_image)
  * [image_streamer_golden_image_facts - Retrieve facts about one or more of the Image Streamer Golden Image.](#image_streamer_golden_image_facts)
  * [image_streamer_os_volume_facts - Retrieve facts about the Image Streamer OS Volumes.](#image_streamer_os_volume_facts)
  * [image_streamer_plan_script - Manage the Image Streamer Plan Script resources.](#image_streamer_plan_script)
  * [image_streamer_plan_script_facts - Retrieve facts about the Image Streamer Plan Scripts.](#image_streamer_plan_script_facts)
  * [oneview_alert_facts - Retrieve facts about the OneView Alerts.](#oneview_alert_facts)
  * [oneview_connection_template - Manage the OneView Connection Template resources.](#oneview_connection_template)
  * [oneview_connection_template_facts - Retrieve facts about the OneView Connection Templates.](#oneview_connection_template_facts)
  * [oneview_datacenter - Manage OneView Data Center resources.](#oneview_datacenter)
  * [oneview_datacenter_facts - Retrieve facts about the OneView Data Centers.](#oneview_datacenter_facts)
  * [oneview_drive_enclosure - Manage OneView Drive Enclosure resources.](#oneview_drive_enclosure)
  * [oneview_drive_enclosure_facts - Retrieve the facts about one or more of the OneView Drive Enclosures.](#oneview_drive_enclosure_facts)
  * [oneview_enclosure - Manage OneView Enclosure resources.](#oneview_enclosure)
  * [oneview_enclosure_facts - Retrieve facts about one or more Enclosures.](#oneview_enclosure_facts)
  * [oneview_enclosure_group - Manage OneView Enclosure Group resources.](#oneview_enclosure_group)
  * [oneview_enclosure_group_facts - Retrieve facts about one or more of the OneView Enclosure Groups.](#oneview_enclosure_group_facts)
  * [oneview_ethernet_network - Manage OneView Ethernet Network resources.](#oneview_ethernet_network)
  * [oneview_ethernet_network_facts - Retrieve the facts about one or more of the OneView Ethernet Networks.](#oneview_ethernet_network_facts)
  * [oneview_fabric - Manage OneView Fabric resources.](#oneview_fabric)
  * [oneview_fabric_facts - Retrieve the facts about one or more of the OneView Fabrics.](#oneview_fabric_facts)
  * [oneview_fc_network - Manage OneView Fibre Channel Network resources.](#oneview_fc_network)
  * [oneview_fc_network_facts - Retrieve the facts about one or more of the OneView Fibre Channel Networks.](#oneview_fc_network_facts)
  * [oneview_fcoe_network - Manage OneView FCoE Network resources.](#oneview_fcoe_network)
  * [oneview_fcoe_network_facts - Retrieve the facts about one or more of the OneView FCoE Networks.](#oneview_fcoe_network_facts)
  * [oneview_firmware_bundle - Upload OneView Firmware Bundle resources.](#oneview_firmware_bundle)
  * [oneview_firmware_driver - Provides an interface to remove Firmware Driver resources.](#oneview_firmware_driver)
  * [oneview_firmware_driver_facts - Retrieve the facts about one or more of the OneView Firmware Drivers.](#oneview_firmware_driver_facts)
  * [oneview_interconnect - Manage the OneView Interconnect resources.](#oneview_interconnect)
  * [oneview_interconnect_facts - Retrieve facts about one or more of the OneView Interconnects.](#oneview_interconnect_facts)
  * [oneview_interconnect_link_topology_facts - Retrieve facts about the OneView Interconnect Link Topologies.](#oneview_interconnect_link_topology_facts)
  * [oneview_interconnect_type_facts - Retrieve facts about one or more of the OneView Interconnect Types.](#oneview_interconnect_type_facts)
  * [oneview_internal_link_set_facts - Retrieve facts about the OneView Internal Link Sets.](#oneview_internal_link_set_facts)
  * [oneview_logical_downlinks_facts - Retrieve facts about one or more of the OneView Logical Downlinks.](#oneview_logical_downlinks_facts)
  * [oneview_logical_enclosure - Manage OneView Logical Enclosure resources.](#oneview_logical_enclosure)
  * [oneview_logical_enclosure_facts - Retrieve facts about one or more of the OneView Logical Enclosures.](#oneview_logical_enclosure_facts)
  * [oneview_logical_interconnect - Manage OneView Logical Interconnect resources.](#oneview_logical_interconnect)
  * [oneview_logical_interconnect_facts - Retrieve facts about one or more of the OneView Logical Interconnects.](#oneview_logical_interconnect_facts)
  * [oneview_logical_interconnect_group - Manage OneView Logical Interconnect Group resources.](#oneview_logical_interconnect_group)
  * [oneview_logical_interconnect_group_facts - Retrieve facts about one or more of the OneView Logical Interconnect Groups.](#oneview_logical_interconnect_group_facts)
  * [oneview_logical_switch - Manage OneView Logical Switch resources.](#oneview_logical_switch)
  * [oneview_logical_switch_facts - Retrieve the facts about one or more of the OneView Logical Switches.](#oneview_logical_switch_facts)
  * [oneview_logical_switch_group - Manage OneView Logical Switch Group resources.](#oneview_logical_switch_group)
  * [oneview_logical_switch_group_facts - Retrieve facts about OneView Logical Switch Groups.](#oneview_logical_switch_group_facts)
  * [oneview_managed_san - Manage OneView Managed SAN resources.](#oneview_managed_san)
  * [oneview_managed_san_facts - Retrieve facts about the OneView Managed SANs.](#oneview_managed_san_facts)
  * [oneview_network_set - Manage OneView Network Set resources.](#oneview_network_set)
  * [oneview_network_set_facts - Retrieve facts about the OneView Network Sets.](#oneview_network_set_facts)
  * [oneview_os_deployment_plan_facts - Retrieve facts about one or more Os Deployment Plans.](#oneview_os_deployment_plan_facts)
  * [oneview_os_deployment_server - Manage OneView Deployment Server resources.](#oneview_os_deployment_server)
  * [oneview_os_deployment_server_facts - Retrieve facts about one or more OS Deployment Servers.](#oneview_os_deployment_server_facts)
  * [oneview_power_device - Manage OneView Power Device resources.](#oneview_power_device)
  * [oneview_power_device_facts - Retrieve facts about the OneView Power Devices.](#oneview_power_device_facts)
  * [oneview_rack - Manage OneView Racks resources.](#oneview_rack)
  * [oneview_rack_facts - Retrieve facts about Rack resources.](#oneview_rack_facts)
  * [oneview_san_manager - Manage OneView SAN Manager resources.](#oneview_san_manager)
  * [oneview_san_manager_facts - Retrieve facts about one or more of the OneView SAN Managers.](#oneview_san_manager_facts)
  * [oneview_sas_interconnect - Manage the OneView SAS Interconnect resources.](#oneview_sas_interconnect)
  * [oneview_sas_interconnect_facts - Retrieve facts about the OneView SAS Interconnects.](#oneview_sas_interconnect_facts)
  * [oneview_sas_interconnect_type_facts - Retrieve facts about the OneView SAS Interconnect Types.](#oneview_sas_interconnect_type_facts)
  * [oneview_sas_logical_interconnect - Manage OneView SAS Logical Interconnect resources.](#oneview_sas_logical_interconnect)
  * [oneview_sas_logical_interconnect_facts - Retrieve facts about one or more of the OneView SAS Logical Interconnects.](#oneview_sas_logical_interconnect_facts)
  * [oneview_sas_logical_interconnect_group - Manage OneView SAS Logical Interconnect Group resources.](#oneview_sas_logical_interconnect_group)
  * [oneview_sas_logical_interconnect_group_facts - Retrieve facts about one or more of the OneView SAS Logical Interconnect Groups.](#oneview_sas_logical_interconnect_group_facts)
  * [oneview_sas_logical_jbod_attachment_facts - Retrieve facts about one or more of the OneView SAS Logical JBOD Attachments.](#oneview_sas_logical_jbod_attachment_facts)
  * [oneview_sas_logical_jbod_facts - Retrieve facts about one or more of the OneView SAS Logical JBODs.](#oneview_sas_logical_jbod_facts)
  * [oneview_scope - Manage OneView Scope resources.](#oneview_scope)
  * [oneview_scope_facts - Retrieve facts about one or more of the OneView Scopes.](#oneview_scope_facts)
  * [oneview_server_hardware - Manage OneView Server Hardware resources.](#oneview_server_hardware)
  * [oneview_server_hardware_facts - Retrieve facts about the OneView Server Hardwares.](#oneview_server_hardware_facts)
  * [oneview_server_hardware_type - Manage OneView Server Hardware Type resources.](#oneview_server_hardware_type)
  * [oneview_server_hardware_type_facts - Retrieve facts about Server Hardware Types of the OneView.](#oneview_server_hardware_type_facts)
  * [oneview_server_profile - Manage OneView Server Profile resources.](#oneview_server_profile)
  * [oneview_server_profile_facts - Retrieve facts about the OneView Server Profiles.](#oneview_server_profile_facts)
  * [oneview_server_profile_template - Manage OneView Server Profile Template resources.](#oneview_server_profile_template)
  * [oneview_server_profile_template_facts - Retrieve facts about the Server Profile Templates from OneView.](#oneview_server_profile_template_facts)
  * [oneview_storage_pool - Manage OneView Storage Pool resources.](#oneview_storage_pool)
  * [oneview_storage_pool_facts - Retrieve facts about one or more Storage Pools.](#oneview_storage_pool_facts)
  * [oneview_storage_system - Manage OneView Storage System resources.](#oneview_storage_system)
  * [oneview_storage_system_facts - Retrieve facts about the OneView Storage Systems.](#oneview_storage_system_facts)
  * [oneview_storage_volume_attachment - Provides an interface to remove extra presentations from a specified server profile.](#oneview_storage_volume_attachment)
  * [oneview_storage_volume_attachment_facts - Retrieve facts about the OneView Storage Volume Attachments.](#oneview_storage_volume_attachment_facts)
  * [oneview_storage_volume_template - Manage OneView Storage Volume Template resources.](#oneview_storage_volume_template)
  * [oneview_storage_volume_template_facts - Retrieve facts about Storage Volume Templates of the OneView.](#oneview_storage_volume_template_facts)
  * [oneview_switch - Provides an interface to remove ToR Switch resources.](#oneview_switch)
  * [oneview_switch_facts - Retrieve facts about the OneView Switches.](#oneview_switch_facts)
  * [oneview_switch_type_facts - Retrieve facts about the OneView Switch Types.](#oneview_switch_type_facts)
  * [oneview_task_facts - Retrieve facts about the OneView Tasks.](#oneview_task_facts)
  * [oneview_unmanaged_device - Manage OneView Unmanaged Device resources.](#oneview_unmanaged_device)
  * [oneview_unmanaged_device_facts - Retrieve facts about one or more of the OneView Unmanaged Device.](#oneview_unmanaged_device_facts)
  * [oneview_uplink_set - Manage OneView Uplink Set resources.](#oneview_uplink_set)
  * [oneview_uplink_set_facts - Retrieve facts about one or more of the OneView Uplink Sets.](#oneview_uplink_set_facts)
  * [oneview_volume - Manage OneView Volume resources.](#oneview_volume)
  * [oneview_volume_facts - Retrieve facts about the OneView Volumes.](#oneview_volume_facts)

---

## hpe_icsp_os_deployment
Deploy the operating system on a server using HPE ICsp.

#### Synopsis
 Deploy the operating system on a server based on the available ICsp OS build plan.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpICsp

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| custom_attributes  |   No  |  | |  Custom Attributes.  |
| icsp_host  |   Yes  |  | |  ICsp hostname.  |
| os_build_plan  |   Yes  |  | |  OS Build plan.  |
| password  |   Yes  |  | |  ICsp password.  |
| personality_data  |   No  |  | |  Personality Data.  |
| server_id  |   Yes  |  | |  Server ID.  |
| username  |   Yes  |  | |  ICsp username.  |


 
#### Examples

```yaml
- name: Deploy OS
  hpe_icsp_os_deployment:
    icsp_host: "{{ icsp }}"
    username: "{{ icsp_username }}"
    password: "{{ icsp_password }}"
    server_id: "{{ server_profile.serialNumber }}"
    os_build_plan: "{{ os_build_plan }}"
    custom_attributes: "{{ osbp_custom_attributes }}"
    personality_data: "{{ network_config }}"
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| icsp_server   | Has the facts about the server that was provisioned with ICsp. |  When the module runs successfully, but can be null. |  complex |



---


## hpe_icsp_server
Adds, removes and configures servers in ICsp.

#### Synopsis
 This module allows you to add, remove and configure servers in the Insight Control Server Provisioning (ICsp). In ICsp, a server, often referred to as a Target Server, is a physical ProLiant server or a virtual machine that can have actions taken upon it.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpICsp

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| icsp_host  |   Yes  |  | |  ICsp hostname.  |
| password  |   Yes  |  | |  ICsp password.  |
| server_ipAddress  |   Yes  |  | |  The IP address of the iLO of the server.  |
| server_password  |   Yes  |  | |  The password required to log into the server's iLO  |
| server_personality_data  |   No  |  | |  Additional data to send to ICsp.  |
| server_port  |   No  |  [443]  | |  The iLO port to use when logging in.  |
| server_username  |   Yes  |  | |  The username required to log into the server's iLO.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>network_configured</li> </ul> |  Indicates the desired state for the ICsp server. 'present' will register the resource on ICsp. 'absent' will remove the resource from ICsp, if it exists. 'network_configured' will set the network configuration.  |
| username  |   Yes  |  | |  ICsp username.  |


 
#### Examples

```yaml
  - name: Ensure the server is registered in ICsp
    hpe_icsp_server:
      icsp_host: "{{icsp_host}}"
      username: "{{icsp_username}}"
      password: "{{icsp_password}}"
      server_ipAddress: "{{server_iLO_ip}}"
      server_username: "Admin"
      server_password: "admin"
      state: present
    delegate_to: localhost

  - name: Set the network configuration
    hpe_icsp_server:
      icsp_host: "{{ icsp }}"
      username: "{{ icsp_username }}"
      password: "{{ icsp_password }}"
      server_ipAddress: "{{ server_ipAddress }}"
      server_username: "{{ server_username }}"
      server_password: "{{ server_password }}"
      server_personality_data: "{{ network_config }}"
      state: network_configured
    delegate_to: localhost

  - name: Ensure the server is removed from ICsp
    hpe_icsp_server:
      icsp_host: "{{icsp_host}}"
      username: "{{icsp_username}}"
      password: "{{icsp_password}}"
      server_ipAddress: "{{server_iLO_ip}}"
      server_username: "Admin"
      server_password: "admin"
      state: absent
    delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| target_server   | Has the facts about the server that was added to ICsp. |  On states 'present' and 'network_configured' . Can be null. |  complex |



---


## image_streamer_artifact_bundle
Manage the Artifact Bundle resource.

#### Synopsis
 Provides an interface to manage the Artifact Bundle. Can create, update, remove, and download, upload, extract

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Artifact Bundle properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>downloaded</li>  <li>archive_downloaded</li>  <li>backup_uploaded</li>  <li>backup_created</li>  <li>extracted</li>  <li>backup_extracted</li> </ul> |  Indicates the desired state for the Artifact Bundle resource. 'present' will ensure data properties are compliant with OneView. 'absent' will remove the resource from OneView, if it exists. 'downloaded' will download the Artifact Bundle to the file path provided. 'archive_downloaded' will download the Artifact Bundle archive to the file path provided. 'backup_uploaded' will upload the Backup for the Artifact Bundle from the file path provided. 'backup_created' will create a Backup for the Artifact Bundle. 'extracted' will extract an Artifact Bundle. 'backup_extracted' will extract an Artifact Bundle from the Backup.  |


 
#### Examples

```yaml
- name: Create an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      name: 'Artifact Bundle'
      description: 'Description of Artifact Bundles Test'
      buildPlans:
        resourceUri: '/rest/build-plans/ab65bb06-4387-48a0-9a5d-0b0da2888508'
        readOnly: 'false'
  delegate_to: localhost

- name: Download the Artifact Bundle to the file path provided
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: downloaded
    data:
      name: 'Artifact Bundle'
      destinationFilePath: '~/downloaded_artifact.zip'
  delegate_to: localhost

- name: Download the Archive for Artifact Bundle to the file path provided
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: archive_downloaded
    data:
      name: 'Artifact Bundle'
      destinationFilePath: '~/downloaded_archive.zip'
  delegate_to: localhost

- name: Upload an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      localArtifactBundleFilePath: '~/uploaded_artifact.zip'
  delegate_to: localhost

- name: Upload Backup an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_uploaded
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
      localBackupArtifactBundleFilePath: '~/uploaded_backup.zip'
  delegate_to: localhost

- name: Create Backup for Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_created
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
  delegate_to: localhost

- name: Extract an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: extracted
    data:
      name: 'Artifact Bundle'
  delegate_to: localhost

- name: Extract Backup an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: backup_extracted
    data:
      deploymentGroupURI: '/rest/deployment-groups/c5a727ef-71e9-4154-a512-6655b168c2e3'
  delegate_to: localhost

- name: Update an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: present
    data:
      name: 'Artifact Bundle'
      newName: 'Artifact Bundle Updated'
  delegate_to: localhost

- name: Remove an Artifact Bundle
  image_streamer_artifact_bundle:
    config: "{{ config }}"
    state: absent
    data:
      name: 'Artifact Bundle'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| artifact_bundle   | Has the OneView facts about the Artifact Bundles. |  On state 'present' and 'extracted'. |  complex |
| artifact_bundle_deployment_group   | Has the OneView facts about the Deployment Group. |  On state 'backup_extracted', 'backup_uploaded', and 'backup_created'. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## image_streamer_artifact_bundle_facts
Retrieve facts about the Artifact Bundle.

#### Synopsis
 Retrieve facts about the Artifact Bundle.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Artifact Bundle.  |
| options  |   No  |  | |  List with options to gather additional facts about the Artifact Bundle. Options allowed: 'allBackups' gets the list of backups for the Artifact Bundles. 'backupForAnArtifactBundle' gets the list of backups for the Artifact Bundle.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Artifact Bundles
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather paginated, filtered and sorted facts about Artifact Bundles
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=OK
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather facts about an Artifact Bundle by name
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    name: "Artifact Bundles Test"
  delegate_to: localhost
- debug: var=artifact_bundles

- name: Gather facts about all Backups for Artifact Bundle
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    name: "Artifact Bundles Test"
    options:
      - allBackups
  delegate_to: localhost
- debug: var=artifact_bundles
- debug: var=artifact_bundle_backups

- name: Gather facts about Backup for an Artifact Bundle
  image_streamer_artifact_bundle_facts:
    config: "{{ config }}"
    name: "Artifact Bundles Test"
    options:
      - backupForAnArtifactBundle
  delegate_to: localhost
- debug: var=artifact_bundles
- debug: var=backup_for_artifact_bundle

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| artifact_bundle_backups   | The list of backups for the Artifact Bundles. |  When requested, but can also be null. |  list |
| artifact_bundles   | The list of Artifact Bundles. |  Always, but can be also null. |  list |
| backup_for_artifact_bundle   | The backup for an Artifact Bundle. |  When requested, but can also be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## image_streamer_build_plan
Manages Image Stream OS Build Plan resources.

#### Synopsis
 Provides an interface to manage Image Stream OS Build Plans. Can create, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with OS Build Plan properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the OS Build Plan resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists.  |


 
#### Examples

```yaml
- name: Create an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "oebuildplan"
      oeBuildPlanType: "deploy"
  delegate_to: localhost

- name: Update the OS Build Plan description and name
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "New description"
      newName: 'OS Build Plan Renamed'
  delegate_to: localhost

- name: Remove an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo OS Build Plan'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| build_plan   | Has the OneView facts about the OS Build Plan. |  On state 'present'. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_build_plan_facts
Retrieve facts about one or more of the Image Streamer Build Plans.

#### Synopsis
 Retrieve facts about one or more of the Image Streamer Build Plans.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Build Plan name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Build Plans
  image_streamer_build_plan_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=build_plans

- name: Gather paginated, filtered and sorted facts about Build Plans
  image_streamer_build_plan_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: oeBuildPlanType=capture
  delegate_to: localhost
- debug: var=build_plans

- name: Gather facts about a Build Plan by name
  image_streamer_build_plan_facts:
    config: "{{ config }}"
    name: "{{ name }}"
  delegate_to: localhost
- debug: var=build_plans

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| build_plans   | The list of Build Plans. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_deployment_group_facts
Retrieve facts about the Image Streamer Deployment Groups.

#### Synopsis
 Retrieve facts about the Image Streamer Deployment Groups.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Deployment Group.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather paginated, filtered and sorted facts about Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=OK
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather facts about a Deployment Group by name
  image_streamer_deployment_group_facts:
    config: "{{ config_path }}"
    name: "OSS"
  delegate_to: localhost

- debug: var=deployment_groups

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| deployment_groups   | The list of Deployment Groups |  Always, but can be empty. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_deployment_plan
Manage Image Streamer Deployment Plan resources.

#### Synopsis
 Provides an interface to manage Image Streamer Deployment Plans. Can create, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Deployment Plan properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Deployment Plan resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists.  |


 
#### Examples

```yaml
- name: Create a Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      description: "Description of this Deployment Plan"
      name: 'Demo Deployment Plan'
      hpProvided: 'false'
      oeBuildPlanName: "Demo Build Plan"
  delegate_to: localhost

- name: Update the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Deployment Plan'
      newName:  'Demo Deployment Plan (changed)'
      description: "New description"
  delegate_to: localhost

- name: Remove the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo Deployment Plan'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| deployment_plan   | Has the facts about the Image Streamer Deployment Plan. |  On state 'present', but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_deployment_plan_facts
Retrieve facts about the Image Streamer Deployment Plans.

#### Synopsis
 Retrieve facts about one or more of the Image Streamer Deployment Plans.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Deployment Plan name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Deployment Plans
  image_streamer_deployment_plan_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather paginated, filtered and sorted facts about Deployment Plans
  image_streamer_deployment_plan_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=active
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather facts about a Deployment Plan by name
  image_streamer_deployment_plan_facts:
    config: "{{ config }}"
    name: "Demo Deployment Plan"
  delegate_to: localhost
- debug: var=deployment_plans

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| deployment_plans   | The list of Deployment Plans. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_golden_image
Manage Image Streamer Golden Image resources.

#### Synopsis
 Provides an interface to manage Image Streamer Golden Image. Can create, add, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Golden Image properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>downloaded</li>  <li>archive_downloaded</li> </ul> |  Indicates the desired state for the Golden Image resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists. `downloaded` will download the Golden Image to the file path provided. `archive_downloaded` will download the Golden Image archive to the file path provided.  |


 
#### Examples

```yaml
- name: Add a Golden Image from OS Volume
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image creation'
      description: "Test Description"
      imageCapture: "true"
      osVolumeName: 'OSVolume-20'
      buildPlanName: 'Buld Plan name'
  delegate_to: localhost

- name: Create a Golden Image uploading from a local file
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image upload'
      description: "Test"
      localImageFilePath: '~/image_file.zip'
  delegate_to: localhost

- name: Update the Golden Image description and name
  image_streamer_golden_image:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Golden Image upload'
      description: "New description"
      newName: 'Golden Image Renamed'
  delegate_to: localhost

- name: Download the Golden Image to the file path provided
  image_streamer_golden_image:
    config: "{{ config }}"
    state: downloaded
    data:
      name: 'Demo Golden Image'
      destination_file_path: '~/downloaded_image.zip'
  delegate_to: localhost

- name: Download the Golden Image archive log to the file path provided
  image_streamer_golden_image:
    config: "{{ config }}"
    state: archive_downloaded
    data:
      name: 'Demo Golden Image'
      destination_file_path: '~/archive.log'
  delegate_to: localhost

- name: Remove a Golden Image
  image_streamer_golden_image:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Golden Image name'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| golden_image   | Has the OneView facts about the Golden Image. |  On state 'present'. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_golden_image_facts
Retrieve facts about one or more of the Image Streamer Golden Image.

#### Synopsis
 Retrieve facts about one or more of the Image Streamer Golden Image.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Golden Image name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Golden Images
  image_streamer_golden_image_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=golden_images

- name: Gather paginated, filtered and sorted facts about Golden Images
  image_streamer_golden_image_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: importedFromBundle=true
  delegate_to: localhost
- debug: var=golden_images

- name: Gather facts about a Golden Image by name
  image_streamer_golden_image_facts:
    config: "{{ config }}"
    name: "{{ name }}"
  delegate_to: localhost
- debug: var=golden_images

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| golden_images   | The list of Golden Images. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_os_volume_facts
Retrieve facts about the Image Streamer OS Volumes.

#### Synopsis
 Retrieve facts about the Image Streamer OS Volumes.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the OS Volume.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all OS Volumes
  image_streamer_os_volume_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=os_volumes

- name: Gather paginated, filtered and sorted facts about OS Volumes
  image_streamer_os_volume_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: status=OK
  delegate_to: localhost

- debug: var=os_volumes

- name: Gather facts about an OS Volume by name
  image_streamer_os_volume_facts:
    config: "{{ config_path }}"
    name: "Test Volume"
  delegate_to: localhost

- debug: var=os_volumes

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| os_volumes   | The list of OS Volumes |  Always, but can be empty. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_plan_script
Manage the Image Streamer Plan Script resources.

#### Synopsis
 Provides an interface to manage the Image Streamer Plan Script. Can create, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Plan Script properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>differences_retrieved</li> </ul> |  Indicates the desired state for the Plan Script resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists. `differences_retrieved` will retrieve the modified contents of the Plan Script as per the selected attributes.  |


 
#### Examples

```yaml
- name: Create a Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: present
    data:
      description: "Description of this plan script"
      name: 'Demo Plan Script'
      hpProvided: False
      planType: "deploy"
      content: 'echo "test script"'
  delegate_to: localhost

- name: Update the Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Plan Script'
      newName:  'Demo Plan Script new name'
      description: "New description"
      content: 'echo "test script changed"'
  delegate_to: localhost

- name: Retrieve the Plan Script content differences
  image_streamer_plan_script:
    config: "{{ config }}"
    state: differences_retrieved
    data:
      name: 'Demo Plan Script'
      content: 'echo "test script changed 2"'
  delegate_to: localhost
- debug: var=plan_script_differences

- name: Remove the Plan Script
  image_streamer_plan_script:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo Plan Script'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| plan_script   | Has the facts about the Image Streamer Plan Script. |  On state 'present', but can be null. |  complex |
| plan_script_differences   | Has the facts about the modified contents of the Plan Script as per the selected attributes. |  On state 'differences_retrieved'. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## image_streamer_plan_script_facts
Retrieve facts about the Image Streamer Plan Scripts.

#### Synopsis
 Retrieve facts about one or more of the Image Streamer Plan Script.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Plan Script name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather paginated, filtered and sorted facts about Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: planType=capture
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather facts about a Plan Script by name
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    name: "Demo Plan Script"
  delegate_to: localhost
- debug: var=plan_scripts

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| plan_scripts   | The list of Plan Scripts. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_alert_facts
Retrieve facts about the OneView Alerts.

#### Synopsis
 Retrieve facts about the OneView Alerts.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |   No  |  | |  List with parameters to help filter the alerts. Params allowed: `count`, `fields`, `filter`, `query`, `sort`, `start`, and `view`.  |


 
#### Examples

```yaml
- name: Gather facts about the last 2 alerts
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 2

- debug: var=alerts

- name: Gather facts about the alerts with state 'Cleared'
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 2
      filter: "alertState='Cleared'"

- debug: var=alerts

- name: Gather facts about the alerts with urgency 'High'
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 5
      filter: "urgency='High'"

- debug: var=alerts

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| alerts   | The list of alerts. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_connection_template
Manage the OneView Connection Template resources.

#### Synopsis
 Provides an interface to manage the Connection Template resources. Can update.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Connection Template properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li> </ul> |  Indicates the desired state for the Connection Template resource. `'present'` will ensure data properties are compliant with OneView.  |


 
#### Examples

```yaml
- name: Update the Connection Template
  oneview_connection_template:
    config: "{{ config }}"
    state: present
    data:
        name: 'name1304244267-1467656930023'
        type : "connection-template"
        bandwidth :
            maximumBandwidth : 10000
            typicalBandwidth : 2000
        newName : "CT-23"
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connection_template   | Has the OneView facts about the Connection Template. |  On 'present' state, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_connection_template_facts
Retrieve facts about the OneView Connection Templates.

#### Synopsis
 Retrieve facts about the OneView Connection Templates.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Connection Template name.  |
| options  |   No  |  | |  List with options to gather additional facts about Connection Template related resources. Options allowed: `defaultConnectionTemplate`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Connection Templates
  oneview_connection_template_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather paginated, filtered and sorted facts about Connection Templates
  oneview_connection_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=defaultConnectionTemplate'

- debug: var=connection_templates

- name: Gather facts about a Connection Template by name
  oneview_connection_template_facts:
    config: "{{ config }}"
    name: 'connection template name'
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather facts about the Default Connection Template
  oneview_connection_template_facts:
    config: "{{ config }}"
    options:
      - defaultConnectionTemplate
  delegate_to: localhost
- debug: var=default_connection_template

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connection_templates   | Has all the OneView facts about the Connection Templates. |  Always, except when defaultConnectionTemplate is requested. Can be null. |  complex |
| default_connection_template   | Has the facts about the Default Connection Template. |  When requested, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_datacenter
Manage OneView Data Center resources.

#### Synopsis
 Provides an interface to manage Data Center resources. Can add, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Data Center properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Data Center resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Add a Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        width: 5000
        depth: 6000
        contents:
            # You can choose either resourceName or resourceUri to inform the Rack
            - resourceName: '{{ datacenter_content_rack_name }}' # option 1
              resourceUri: ''                                    # option 2
              x: 1000
              y: 1000
  delegate_to: localhost

- name: Update the Data Center with specified properties (no racks)
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        coolingCapacity: '5'
        costPerKilowattHour: '0.10'
        currency: USD
        deratingType: NaJp
        deratingPercentage: '20.0'
        defaultPowerLineVoltage: '220'
        coolingMultiplier: '1.5'
        width: 4000
        depth: 5000
        contents: ~

  delegate_to: localhost

- name: Rename the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        newName: "My Datacenter"
  delegate_to: localhost

- name: Remove the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: absent
    data:
        name: 'My Datacenter'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| datacenter   | Has the OneView facts about the Data Center. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_datacenter_facts
Retrieve facts about the OneView Data Centers.

#### Synopsis
 Retrieve facts about the OneView Data Centers.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Data Center name.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: 'visualContent'.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=datacenters

- name: Gather paginated, filtered and sorted facts about Data Centers
  oneview_datacenter_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'state=Unmanaged'
- debug: var=datacenters

- name: Gather facts about a Data Center by name
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
  delegate_to: localhost
- debug: var=datacenters

- name: Gather facts about the Data Center Visual Content
  oneview_datacenter_facts:
    config: "{{ config }}"
    name: "My Data Center"
    options:
      - visualContent
  delegate_to: localhost
- debug: var=datacenters
- debug: var=datacenter_visual_content

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| datacenter_visual_content   | Has facts about the Data Center Visual Content. |  When requested, but can be null. |  complex |
| datacenters   | Has all the OneView facts about the Data Centers. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_drive_enclosure
Manage OneView Drive Enclosure resources.

#### Synopsis
 Provides an interface to manage Drive Enclosure resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Drive Enclosure properties.  |
| state  |   |  | <ul> <li>power_state_set</li>  <li>uid_state_set</li>  <li>hard_reset_state_set</li>  <li>refresh_state_set</li> </ul> |  Indicates the desired state for the Drive Enclosure resource. 'power_state_set' will set the power state for the Drive Enclosure. 'uid_state_set' will set the uid state for the Drive Enclosure. 'hard_reset_state_set' will request a hard reset of the Drive Enclosure. 'refresh_state_set' will refresh a Drive Enclosure.  |


 
#### Examples

```yaml
- name: Power off the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: power_state_set
    data:
        name: '0000A66108, bay 1'
        powerState: 'Off'

- name: Power on the UID for the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: uid_state_set
    data:
        name: '0000A66108, bay 1'
        uidState: 'On'

- name: Request a hard reset of the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: hard_reset_state_set
    data:
        name: '0000A66108, bay 1'

- name: Refresh the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: refresh_state_set
    data:
        name: '0000A66108, bay 1'
        refreshState: 'RefreshPending'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| drive_enclosure   | Has the facts about the Drive Enclosure. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- This resource is only available on HPE Synergy.


---


## oneview_drive_enclosure_facts
Retrieve the facts about one or more of the OneView Drive Enclosures.

#### Synopsis
 Retrieve the facts about one or more of the Drive Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Drive Enclosure name.  |
| options  |   No  |  | |  List with options to gather additional facts about Drive Enclosure related resources. Options allowed: portMap. To gather additional facts it is required to inform the Drive Enclosure name. Otherwise, these options will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Drive Enclosures
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"

- debug: var=drive_enclosures

- name: Gather paginated, filtered and sorted facts about Drive Enclosures
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=Warning'

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure by name
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure and the Port Map
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure
    options:
        - portMap

- debug: var=drive_enclosures
- debug: var=drive_enclosure_port_map

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| drive_enclosure_port_map   | Has all the OneView facts about the Drive Enclosure Port Map. |  When requested, but can be null. |  complex |
| drive_enclosures   | Has all the OneView facts about the Drive Enclosures. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- This resource is only available on HPE Synergy.


---


## oneview_enclosure
Manage OneView Enclosure resources.

#### Synopsis
 Provides an interface to manage Enclosure resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Enclosure properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>reconfigured</li>  <li>refreshed</li>  <li>appliance_bays_powered_on</li>  <li>uid_on</li>  <li>uid_off</li>  <li>manager_bays_uid_on</li>  <li>manager_bays_uid_off</li>  <li>manager_bays_power_state_e_fuse</li>  <li>manager_bays_power_state_reset</li>  <li>appliance_bays_power_state_e_fuse</li>  <li>device_bays_power_state_e_fuse</li>  <li>device_bays_power_state_reset</li>  <li>interconnect_bays_power_state_e_fuse</li>  <li>manager_bays_role_active</li>  <li>device_bays_ipv4_removed</li>  <li>interconnect_bays_ipv4_removed</li>  <li>support_data_collection_set</li> </ul> |  Indicates the desired state for the Enclosure resource. `present` will ensure data properties are compliant with OneView. You can rename the enclosure providing an attribute `newName`. You can also rename the rack providing an attribute `rackName`. `absent` will remove the resource from OneView, if it exists. `reconfigured` will reapply the appliance's configuration on the enclosure. This includes running the same configuration steps that were performed as part of the enclosure add. `refreshed` will refresh the enclosure along with all of its components, including interconnects and servers. Any new hardware is added, and any hardware that is no longer present within the enclosure is removed. `appliance_bays_powered_on` will set the appliance bay power state on. `uid_on` will set the UID state on. `uid_off` will set the UID state off. `manager_bays_uid_on` will set the UID state on for the Synergy Frame Link Module. `manager_bays_uid_off` will set the UID state off for the Synergy Frame Link Module. `manager_bays_power_state_e_fuse` will E-Fuse the Synergy Frame Link Module bay in the path. `manager_bays_power_state_reset` will Reset the Synergy Frame Link Module bay in the path. `appliance_bays_power_state_e_fuse` will E-Fuse the appliance bay in the path. `device_bays_power_state_e_fuse` will E-Fuse the device bay in the path. `device_bays_power_state_reset` will Reset the device bay in the path. `interconnect_bays_power_state_e_fuse` will E-Fuse the IC bay in the path. `manager_bays_role_active` will set the active Synergy Frame Link Module. `device_bays_ipv4_removed` will release the IPv4 address in the device bay. `interconnect_bays_ipv4_removed` will release the IPv4 address in the interconnect bay. `support_data_collection_set` will set the support data collection state for the enclosure. The supported values for this state are `PendingCollection`, `Completed`, `Error` and `NotSupported`  |


 
#### Examples

```yaml
- name: Ensure that an Enclosure is present using the default configuration
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: present
    data:
      enclosureGroupUri : '{{ enclosure_group_uri }}'
      hostname : '{{ enclosure_hostname }}'
      username : '{{ enclosure_username }}'
      password : '{{ enclosure_password }}'
      name: 'Test-Enclosure'
      licensingIntent : 'OneView'

- name: Updates the enclosure to have a name of "Test-Enclosure-Renamed".
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test-Enclosure'
      newName : 'Test-Enclosure-Renamed'

- name: Reconfigure the enclosure "Test-Enclosure"
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: reconfigured
    data:
      name: 'Test-Enclosure'

- name: Ensure that enclosure is absent
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test-Enclosure'

- name: Ensure that an enclosure is refreshed
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: refreshed
    data:
      name: 'Test-Enclosure'
      refreshState: Refreshing

- name: Set the calibrated max power of an unmanaged or unsupported enclosure
  oneview_enclosure:
    config: "{{ config }}"
    state: present
    data:
      name: 'Test-Enclosure'
      calibratedMaxPower: 1700

- name: Set the appliance bay power state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: appliance_bays_powered_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Set the appliance UID state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: uid_on
    data:
      name: 'Test-Enclosure'

- name: Set the appliance UID state off
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: uid_off
    data:
      name: 'Test-Enclosure'

- name: Set the UID for the Synergy Frame Link Module state on
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_uid_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Set the UID for the Synergy Frame Link Module state off
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_uid_off
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the Synergy Frame Link Module bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Reset the Synergy Frame Link Module bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the appliance bay 1
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: appliance_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the device bay 10
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 10

- name: Reset the device bay 8
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 8

- name: E-Fuse the IC bay 3
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: interconnect_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 3

- name: Set the active Synergy Frame Link Module on bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: manager_bays_role_active
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: device_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: interconnect_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Set the supportDataCollectionState for the enclosure
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: support_data_collection_set
    data:
      name: 'Test-Enclosure'
      supportDataCollectionState: 'PendingCollection'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure   | Has all the facts about the enclosure. |  On states 'present', 'reconfigured', and 'refreshed'. Can be null. |  complex |


#### Notes

- These states are only available on HPE Synergy: `appliance_bays_powered_on`, `uid_on`, `uid_off`, `manager_bays_uid_on`, `manager_bays_uid_off`, `manager_bays_power_state_e_fuse`, `manager_bays_power_state_reset`, `appliance_bays_power_state_e_fuse`, `device_bays_power_state_e_fuse`, `device_bays_power_state_reset`, `interconnect_bays_power_state_e_fuse`, `manager_bays_role_active`, `device_bays_ipv4_removed` and `interconnect_bays_ipv4_removed`

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_enclosure_facts
Retrieve facts about one or more Enclosures.

#### Synopsis
 Retrieve facts about one or more of the Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Enclosure name.  |
| options  |   No  |  | |  List with options to gather additional facts about an Enclosure and related resources. Options allowed: `script`, `environmentalConfiguration`, and `utilization`. For the option `utilization`, you can provide specific parameters.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Enclosures
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
- debug: var=enclosures

- name: Gather paginated, filtered and sorted facts about Enclosures
  oneview_enclosure_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'
- debug: var=enclosures

- name: Gather facts about an Enclosure by name
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Enclosure-Name"
  delegate_to: localhost
- debug: var=enclosures

- name: Gather facts about an Enclosure by name with options
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: 'Test-Enclosure'
    options:
      - script                       # optional
      - environmentalConfiguration   # optional
      - utilization                  # optional
  delegate_to: localhost
- debug: var=enclosures
- debug: var=enclosure_script
- debug: var=enclosure_environmental_configuration
- debug: var=enclosure_utilization

- name: "Gather facts about an Enclosure with temperature data at a resolution of one sample per day, between two
         specified dates"
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: 'Test-Enclosure'
    options:
      - utilization:                   # optional
          fields: 'AmbientTemperature'
          filter:
            - "startDate=2016-07-01T14:29:42.000Z"
            - "endDate=2017-07-01T03:29:42.000Z"
          view: 'day'
          refresh: False
  delegate_to: localhost
- debug: var=enclosures
- debug: var=enclosure_utilization

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_environmental_configuration   | Has all the OneView facts about the environmental configuration of an Enclosure. |  When requested, but can be null. |  complex |
| enclosure_script   | Has all the OneView facts about the script of an Enclosure. |  When requested, but can be null. |  complex |
| enclosure_utilization   | Has all the OneView facts about the utilization of an Enclosure. |  When requested, but can be null. |  complex |
| enclosures   | Has all the OneView facts about the Enclosures. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_enclosure_group
Manage OneView Enclosure Group resources.

#### Synopsis
 Provides an interface to manage Enclosure Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Enclosure Group properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Enclosure Group resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |


 
#### Examples

```yaml
- name: Ensure that Enclosure Group is present using the default configuration
  oneview_enclosure_group:
    config: "{{ config_file_name }}"
    state: present
    data:
        name: "Enclosure Group 1"
        stackingMode: "Enclosure"
        interconnectBayMappings:
            - interconnectBay: 1
            - interconnectBay: 2
            - interconnectBay: 3
            - interconnectBay: 4
            - interconnectBay: 5
            - interconnectBay: 6
            - interconnectBay: 7
            - interconnectBay: 8
  delegate_to: localhost

- name: Update the Enclosure Group changing the name attribute
  oneview_enclosure_group:
        config: "{{ config_file_name }}"
        state: present
        data:
            name: "Enclosure Group 1"
            newName: "Enclosure Group 1 (renamed)"
  delegate_to: localhost

- name: Ensure that Enclosure Group is absent
  oneview_enclosure_group:
    config: "{{ config_file_name }}"
    state: absent
    data:
      name: "Enclosure Group 1 (renamed)"
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group   | Has the facts about the Enclosure Group. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_enclosure_group_facts
Retrieve facts about one or more of the OneView Enclosure Groups.

#### Synopsis
 Retrieve facts about one or more of the Enclosure Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Enclosure Group name.  |
| options  |   No  |  | |  List with options to gather additional facts about Enclosure Group. Options allowed: `configuration_script` Gets the configuration script for an Enclosure Group.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather paginated, filtered and sorted facts about Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=enclosure_groups

- name: Gather facts about an Enclosure Group by name with configuration script
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
    options:
      - configuration_script
    delegate_to: localhost

- debug: var=enclosure_groups
- debug: var=enclosure_group_script

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group_script   | The configuration script for an Enclosure Group. |  When requested, but can be null. |  string |
| enclosure_groups   | Has all the OneView facts about the Enclosure Groups. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_ethernet_network
Manage OneView Ethernet Network resources.

#### Synopsis
 Provides an interface to manage Ethernet Network resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Ethernet Network properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>default_bandwidth_reset</li> </ul> |  Indicates the desired state for the Ethernet Network resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists. `default_bandwidth_reset` will reset the network connection template to the default.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the Ethernet Network is present using the default configuration
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      vlanId: '201'

- name: Update the Ethernet Network changing bandwidth and purpose
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      purpose: Management
      bandwidth:
          maximumBandwidth: 3000
          typicalBandwidth: 2000
  delegate_to: localhost

- name: Ensure that the Ethernet Network is present with name 'Renamed Ethernet Network'
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      newName: 'Renamed Ethernet Network'

- name: Ensure that the Ethernet Network is absent
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New Ethernet Network'

- name: Create Ethernet networks in bulk
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      vlanIdRange: '1-10,15,17'
      purpose: General
      namePrefix: TestNetwork
      smartLink: false
      privateNetwork: false
      bandwidth:
        maximumBandwidth: 10000
        typicalBandwidth: 2000

- name: Reset to the default network connection template
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: default_bandwidth_reset
    data:
      name: 'Test Ethernet Network'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_network   | Has the facts about the Ethernet Networks. |  On state 'present'. Can be null. |  complex |
| ethernet_network_bulk   | Has the facts about the Ethernet Networks affected by the bulk insert. |  When 'vlanIdRange' attribute is in data argument. Can be null. |  complex |
| ethernet_network_connection_template   | Has the facts about the Ethernet Network Connection Template. |  On state 'default_bandwidth_reset'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_ethernet_network_facts
Retrieve the facts about one or more of the OneView Ethernet Networks.

#### Synopsis
 Retrieve the facts about one or more of the Ethernet Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Ethernet Network name.  |
| options  |   No  |  | |  List with options to gather additional facts about an Ethernet Network and related resources. Options allowed: `associatedProfiles` and `associatedUplinkGroups`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"

- debug: var=ethernet_networks

- name: Gather paginated and filtered facts about Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'purpose=General'

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    name: Ethernet network name

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name with options
  oneview_ethernet_network_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - associatedProfiles
      - associatedUplinkGroups
  delegate_to: localhost

- debug: var=enet_associated_profiles
- debug: var=enet_associated_uplink_groups

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enet_associated_profiles   | Has all the OneView facts about the profiles which are using the Ethernet network. |  When requested, but can be null. |  complex |
| enet_associated_uplink_groups   | Has all the OneView facts about the uplink sets which are using the Ethernet network. |  When requested, but can be null. |  complex |
| ethernet_networks   | Has all the OneView facts about the Ethernet Networks. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fabric
Manage OneView Fabric resources.

#### Synopsis
 Provides an interface for managing fabrics in OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Fabrics properties.  |
| name  |   No  |  | |  Fabric name.  |


 
#### Examples

```yaml
- name: Update the range of the fabric
  oneview_fabric:
    config: '{{ config }}'
    state: reserved_vlan_range_updated
    data:
      name: '{{ name }}'
      reservedVlanRangeParameters:
        start: '300'
        length: '62'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fabric   | Has all the OneView facts about the Fabrics. |  Always, but can be null. |  complex |


#### Notes

- This module is only available on HPE Synergy.

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fabric_facts
Retrieve the facts about one or more of the OneView Fabrics.

#### Synopsis
 Retrieve the facts about one or more of the Fabrics from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Fabric name.  |
| options  |   No  |  | |  List with options to gather additional facts about an Fabrics and related resources. Options allowed: `reservedVlanRange`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather paginated, filtered and sorted facts about Fabrics
  oneview_fabric_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=DefaultFabric'

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics

- name: Gather facts about a Fabric by name with options
  oneview_fabric_facts:
    config: "{{ config }}"
    name: DefaultFabric
    options:
      - reservedVlanRange          # optional

- debug: var=fabrics

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fabric_reserved_vlan_range   | Has all the OneView facts about the reserved VLAN range |  When requested, but can be null. |  complex |
| fabrics   | Has all the OneView facts about the Fabrics. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fc_network
Manage OneView Fibre Channel Network resources.

#### Synopsis
 Provides an interface to manage Fibre Channel Network resources. Can create, update, and delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Fibre Channel Network properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Fibre Channel Network resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the Fibre Channel Network is present using the default configuration
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New FC Network'

- name: Ensure that the Fibre Channel Network is present with fabricType 'DirectAttach'
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New FC Network'
      fabricType: 'DirectAttach'

- name: Ensure that the Fibre Channel Network is absent
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FC Network'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fc_network   | Has the facts about the OneView FC Networks. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fc_network_facts
Retrieve the facts about one or more of the OneView Fibre Channel Networks.

#### Synopsis
 Retrieve the facts about one or more of the Fibre Channel Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Fibre Channel Network name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Fibre Channel Networks
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fc_networks

- name: Gather paginated, filtered and sorted facts about Fibre Channel Networks
  oneview_fc_network_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'fabricType=FabricAttach'
- debug: var=fc_networks

- name: Gather facts about a Fibre Channel Network by name
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"
    name: network name

- debug: var=fc_networks

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fc_networks   | Has all the OneView facts about the Fibre Channel Networks. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fcoe_network
Manage OneView FCoE Network resources.

#### Synopsis
 Provides an interface to manage FCoE Network resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with FCoE Network properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the FCoE Network resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that FCoE Network is present using the default configuration
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test FCoE Network'
      vlanId: '201'

- name: Ensure that FCoE Network is absent
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FCoE Network'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fcoe_network   | Has the facts about the OneView FCoE Networks. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_fcoe_network_facts
Retrieve the facts about one or more of the OneView FCoE Networks.

#### Synopsis
 Retrieve the facts about one or more of the FCoE Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  FCoE Network name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fcoe_networks

- name: Gather paginated, filtered and sorted facts about FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'vlanId=2'

- debug: var=fcoe_networks

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"
    name: "Test FCoE Network Facts"

- debug: var=fcoe_networks

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fcoe_networks   | Has all the OneView facts about the FCoE Networks. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_firmware_bundle
Upload OneView Firmware Bundle resources.

#### Synopsis
 Upload an SPP ISO image file or a hotfix file to the appliance.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| file_path  |   Yes  |  | |  The full path of a local file to be loaded.  |
| state  |   |  | <ul> <li>present</li> </ul> |  Indicates the desired state for the Firmware Driver resource. `present` will ensure that the firmware bundle is at OneView.  |


 
#### Examples

```yaml
- name: Ensure that the Firmware Driver is present
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm"


```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_bundle   | Has the facts about the OneView Firmware Bundle. |  Always. Can be null. |  complex |


#### Notes

- This module is non-idempotent

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_firmware_driver
Provides an interface to remove Firmware Driver resources.

#### Synopsis
 Provides an interface to remove Firmware Driver resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   Yes  |  | |  Firmware driver name.  |
| state  |   |  | <ul> <li>absent</li> </ul> |  Indicates the desired state for the Firmware Driver. `absent` will remove the resource from OneView, if it exists.  |


 
#### Examples

```yaml
- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"

```



#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_firmware_driver_facts
Retrieve the facts about one or more of the OneView Firmware Drivers.

#### Synopsis
 Retrieve the facts about one or more of the Firmware Drivers from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Firmware driver name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"

- debug: var=firmware_drivers

- name: Gather paginated, filtered and sorted facts about Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=firmware_drivers

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_drivers   | Has all the OneView facts about the Firmware Drivers. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_interconnect
Manage the OneView Interconnect resources.

#### Synopsis
 Provides an interface to manage Interconnect resources. Can change the power state, UID light state, perform device reset, reset port protection, and update the interconnect ports.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| ip  |   No  |  | |  Interconnect IP address.  |
| name  |   No  |  | |  Interconnect name.  |
| ports  |   No  |  | |  List with ports to update. This option should be used together with `update_ports` state.  |
| state  |   |  | <ul> <li>powered_on</li>  <li>powered_off</li>  <li>uid_on</li>  <li>uid_off</li>  <li>device_reset</li>  <li>update_ports</li>  <li>reset_port_protection</li> </ul> |  Indicates the desired state for the Interconnect resource. `powered_on` turns the power on. `powered_off` turns the power off. `uid_on` turns the UID light on. `uid_off` turns the UID light off. `device_reset` perform a device reset. `update_ports` updates the interconnect ports. `reset_port_protection` triggers a reset of port protection.  |


 
#### Examples

```yaml
- name: Turn the power off for Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'powered_off'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'On' for interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'Off' for interconnect that matches the ip 172.18.1.114
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    ip: '172.18.1.114'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect   | Has the facts about the OneView Interconnect. |  Always. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_interconnect_facts
Retrieve facts about one or more of the OneView Interconnects.

#### Synopsis
 Retrieve facts about one or more of the Interconnects from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Interconnect name.  |
| options  |   No  |  | |  List with options to gather additional facts about Interconnect. Options allowed: `nameServers` gets the named servers for an interconnect. `statistics` gets the statistics from an interconnect. `portStatistics` gets the statistics for the specified port name on an interconnect. `subPortStatistics` gets the subport statistics on an interconnect. `ports` gets all interconnect ports. `port` gets a specific interconnect port.  To gather additional facts it is required inform the Interconnect name. Otherwise, these options will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"

- debug: var=interconnects

- name: Gather paginated, filtered and sorted facts about Interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "enclosureName='0000A66101'"

- debug: var=interconnects

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'

- debug: var=interconnects


- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - nameServers

- debug: var=interconnects
- debug: var=interconnect_name_servers

- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - statistics

- debug: var=interconnects
- debug: var=interconnect_statistics

- name: Gather facts about statistics for the Port named 'd3' of the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - portStatistics: 'd3'

- debug: var=interconnects
- debug: var=interconnect_port_statistics

- name: Gather facts about statistics for the sub Port number '1' of the Interconnect named 'Enc2, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: 'Enc2, interconnect 2'
    options:
        - subPortStatistics:
            portName: 'd4'
            subportNumber: 1

- debug: var=interconnects
- debug: var=interconnect_subport_statistics

- name: Gather facts about all the Interconnect ports
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - ports

- debug: var=interconnects
- debug: var=interconnect_ports

- name: Gather facts about an Interconnect port
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - port: d1

- debug: var=interconnects
- debug: var=interconnect_port

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_name_servers   | The named servers for an interconnect. |  When requested, but can be null. |  list |
| interconnect_port   | The interconnect port. |  When requested, but can be null. |  dict |
| interconnect_port_statistics   | Statistics for the specified port name on an interconnect. |  When requested, but can be null. |  dict |
| interconnect_ports   | All interconnect ports. |  When requested, but can be null. |  list |
| interconnect_statistics   | Has all the OneView facts about the Interconnect Statistics. |  When requested, but can be null. |  dict |
| interconnect_subport_statistics   | The subport statistics on an interconnect. |  When requested, but can be null. |  dict |
| interconnects   | The list of interconnects. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_interconnect_link_topology_facts
Retrieve facts about the OneView Interconnect Link Topologies.

#### Synopsis
 Retrieve facts about the Interconnect Link Topologies from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Interconnect Link Topology.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Interconnect Link Topologies
  oneview_interconnect_link_topology_facts:
    config: "{{ config_path }}"

- debug: var=interconnect_link_topologies

- name: Gather paginated, filtered and sorted facts about Interconnect Link Topologies
  oneview_interconnect_link_topology_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='name1900571853-1483553596802'"

- debug: var=interconnect_link_topologies

- name: Gather facts about an Interconnect Link Topology by name
  oneview_interconnect_link_topology_facts:
    config: "{{ config_path }}"
    name: "Name of the Interconnect Link Topologies"

- debug: var=interconnect_link_topologies

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_link_topologies   | Has all the OneView facts about the Interconnect Link Topologies. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy.

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_interconnect_type_facts
Retrieve facts about one or more of the OneView Interconnect Types.

#### Synopsis
 Retrieve facts about one or more of the Interconnect Types from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Interconnect Type name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Interconnect Types
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"

- debug: var=interconnect_types

- name: Gather paginated, filtered and sorted facts about Interconnect Types
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "maximumFirmwareVersion='4000.99'"

- debug: var=interconnect_types

- name: Gather facts about an Interconnect Type by name
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"
    name: HP VC Flex-10 Enet Module

- debug: var=interconnect_types

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_types   | Has all the OneView facts about the Interconnect Types. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_internal_link_set_facts
Retrieve facts about the OneView Internal Link Sets.

#### Synopsis
 Retrieve facts about the Internal Link Sets from OneView. It is possible get all Internal Link Sets or filter by name.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Internal Link Set.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set. 'query': A general query string to narrow the list of resources returned. 'fields': Specifies which fields should be returned in the result set. 'view': Return a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.  |


 
#### Examples

```yaml
- name: Gather facts about all Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"

- debug: var=internal_link_sets

- name: Gather paginated and sorted facts about Internal Link Sets
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:ascending'

- debug: var=internal_link_sets

- name: Gather facts about an Internal Link Set by name
  oneview_internal_link_set_facts:
    config: "{{ config_path }}"
    name: "Internal Link Set Name"

- debug: var=internal_link_sets

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| internal_link_sets   | Has all the OneView facts about the Internal Link Sets. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is available for API version 300 or later


---


## oneview_logical_downlinks_facts
Retrieve facts about one or more of the OneView Logical Downlinks.

#### Synopsis
 Retrieve facts about one or more of the Logical Downlinks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Downlink name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Downlinks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather paginated, filtered and sorted facts about Logical Downlinks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='LDa4c64fd9-0b76-46c3-8335-0bbb76459aff (Cisco Fabric Extender for HP BladeSystem)'"

- debug: var=logical_downlinks

- name: Gather facts about all Logical Downlinks excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather facts about a Logical Downlink by name and excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    name: "LD415a472f-ed77-42cc-9a5e-b9bd5d096923 (HP VC FlexFabric-20/40 F8 Module)"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnects   | The list of logical downlinks. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## oneview_logical_enclosure
Manage OneView Logical Enclosure resources.

#### Synopsis
 Provides an interface to manage Logical Enclosure resources. Can create, update, update firmware, perform dump, update configuration script, reapply configuration, update from group, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Logical Enclosure properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>firmware_updated</li>  <li>script_updated</li>  <li>dumped</li>  <li>reconfigured</li>  <li>updated_from_group</li>  <li>absent</li> </ul> |  Indicates the desired state for the Logical Enclosure resource. `present` ensures data properties are compliant with OneView. You can rename the enclosure providing an attribute `newName`. `firmware_updated` updates the firmware for the Logical Enclosure. `script_updated` updates the Logical Enclosure configuration script. `dumped` generates a support dump for the Logical Enclosure. `reconfigured` reconfigures all enclosures associated with a logical enclosure. `updated_from_group` makes the logical enclosure consistent with the enclosure group. `absent` will remove the resource from OneView, if it exists.  |


 
#### Examples

```yaml
- name: Create a Logical Enclosure (available only on HPE Synergy)
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: present
    data:
        enclosureUris:
          - "/rest/enclosures/0000000000A66101"
        enclosureGroupUri: "/rest/enclosure-groups/9fafc382-bbef-4a94-a9d1-05f77042f3ac"
        name: "Encl1"
  ignore_errors: true
  delegate_to: localhost

- name: Update the firmware for the Logical Enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: firmware_updated
    data:
        name: "Encl1"
        firmware:
            firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
            firmwareUpdateOn: "EnclosureOnly"
            forceInstallFirmware: "false"
  delegate_to: localhost

# This play is compatible with Synergy Enclosures
- name: Update the firmware for the Logical Enclosure with the logical-interconnect validation set as true
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: firmware_updated
    data:
        name: "Encl1"
        firmware:
            firmwareBaselineUri: "/rest/firmware-drivers/SPPGen9Snap3_2015_0221_71"
            firmwareUpdateOn: "EnclosureOnly"
            forceInstallFirmware: "false"
            validateIfLIFirmwareUpdateIsNonDisruptive: "true"
            logicalInterconnectUpdateMode: "Orchestrated"
            updateFirmwareOnUnmanagedInterconnect: "true"
  delegate_to: localhost

- name: Update the Logical Enclosure configuration script
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: script_updated
    data:
        name: "Encl1"
        configurationScript: "# script (updated)"
  delegate_to: localhost

- name: Generates a support dump for the Logical Enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: dumped
    data:
        name: "Encl1"
        dump:
          errorCode: "MyDump16"
          encrypt: "true"
          excludeApplianceDump: "false"
  delegate_to: localhost
- debug: var=generated_dump_uri

- name: Reconfigure all enclosures associated with logical enclosure
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: reconfigured
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Makes the logical enclosure consistent with the enclosure group
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: updated_from_group
    data:
        name: "Encl1"
  delegate_to: localhost

- name: Update the Logical Enclosure changing the name attribute
  oneview_logical_enclosure:
    config: "{{ config_file_name }}"
    state: present
    data:
        name: "Encl1"
        newName: "Encl1 (renamed)"
  delegate_to: localhost

- name: Delete a Logical Enclosure (available only on HPE Synergy)
  oneview_logical_enclosure:
      config: "{{ config_file_name }}"
      state: absent
      data:
          name: 'Encl1'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| configuration_script   | Has the facts about the Logical Enclosure configuration script. |  On state 'script_updated'. Can be null. |  complex |
| generated_dump_uri   | Has the facts about the Logical Enclosure generated support dump URI. |  On state 'dumped'. Can be null. |  complex |
| logical_enclosure   | Has the facts about the OneView Logical Enclosure. |  On states 'present', 'firmware_updated', 'reconfigured', 'updated_from_group', and 'absent'. Can be null. |  complex |


#### Notes

- The `absent` state and the creation of a Logical Enclosure done through the `present` state are available only on HPE Synergy.

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_enclosure_facts
Retrieve facts about one or more of the OneView Logical Enclosures.

#### Synopsis
 Retrieve facts about one or more of the Logical Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Enclosure name.  |
| options  |   No  |  | |  List with options to gather additional facts about a Logical Enclosure and related resources. Options allowed: script.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather paginated, filtered and sorted facts about Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name with options
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
    options:
      - script
  delegate_to: localhost

- debug: var=logical_enclosures
- debug: var=logical_enclosure_script

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_enclosure_script   | Has the facts about the script of a Logical Enclosure. |  When required, but can be null. |  complex |
| logical_enclosures   | Has all the OneView facts about the Logical Enclosures. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_interconnect
Manage OneView Logical Interconnect resources.

#### Synopsis
 Provides an interface to manage Logical Interconnect resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the options.  |
| state  |   |  | <ul> <li>compliant</li>  <li>ethernet_settings_updated</li>  <li>internal_networks_updated</li>  <li>settings_updated</li>  <li>forwarding_information_base_generated</li>  <li>qos_aggregated_configuration_updated</li>  <li>snmp_configuration_updated</li>  <li>port_monitor_updated</li>  <li>configuration_updated</li>  <li>firmware_installed</li>  <li>telemetry_configuration_updated</li> </ul> |  Indicates the desired state for the Logical Interconnect resource. `compliant` brings the logical interconnect back to a consistent state. `ethernet_settings_updated` updates the Ethernet interconnect settings for the logical interconnect. `internal_networks_updated` updates the internal networks on the logical interconnect. This operation is non-idempotent. `settings_updated` updates the Logical Interconnect settings. `forwarding_information_base_generated` generates the forwarding information base dump file for the logical interconnect. This operation is non-idempotent and asynchronous. `qos_aggregated_configuration_updated` updates the QoS aggregated configuration for the logical interconnect. `snmp_configuration_updated` updates the SNMP configuration for the logical interconnect. `port_monitor_updated` updates the port monitor configuration of a logical interconnect. `configuration_updated` asynchronously applies or re-applies the logical interconnect configuration to all managed interconnects. This operation is non-idempotent. `firmware_installed` installs firmware to a logical interconnect. The three operations that are supported for the firmware update are Stage (uploads firmware to the interconnect), Activate (installs firmware on the interconnect) and Update (which does a Stage and Activate in a sequential manner). All of them are non-idempotent. `telemetry_configuration_updated` updates the telemetry configuration of a logical interconnect.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Return the Logical Interconnect to a consistent state
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: compliant
  data:
    name: "Name of the Logical Interconnect"

- name: Update the Ethernet interconnect settings for the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: ethernet_settings_updated
  data:
    name: "Name of the Logical Interconnect"
    ethernetSettings:
      macRefreshInterval: 10

- name: Update the internal networks on the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: internal_networks_updated
    data:
      name: "Name of the Logical Interconnect"
      internalNetworks:
        - name: "Name of the Ethernet Network 1"
        - name: "Name of the Ethernet Network 2"
        - uri: "/rest/ethernet-networks/8a58cf7c-d49d-43b1-94ce-da5621be490c"

- name: Update the interconnect settings
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: settings_updated
    data:
      name: "Name of the Logical Interconnect"
      ethernetSettings:
        macRefreshInterval: 10

- name: Generate the forwarding information base dump file for the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: forwarding_information_base_generated
    data:
      name: "{{ logical_interconnect_name }}"  # could also be 'uri'

- name: Update the QoS aggregated configuration for the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: qos_aggregated_configuration_updated
    data:
      name: "Name of the Logical Interconnect"
      qosConfiguration:
      activeQosConfig:
        category: 'qos-aggregated-configuration'
        configType: 'Passthrough'
        downlinkClassificationType: ~
        uplinkClassificationType: ~
        qosTrafficClassifiers: []
        type: 'QosConfiguration'

- name: Update the SNMP configuration for the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: snmp_configuration_updated
  data:
    name: "Name of the Logical Interconnect"
    snmpConfiguration:
      enabled: True

- name: Update the port monitor configuration of the logical interconnect
  oneview_logical_interconnect:
    config: "{{ config_file_path }}"
    state: port_monitor_updated
    data:
      name: "Name of the Logical Interconnect"
      portMonitor:
        enablePortMonitor: False

- name: Update the configuration on the logical interconnect
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: configuration_updated
  data:
    name: "Name of the Logical Interconnect"

- name: Install a firmware to the logical interconnect, running the stage operation to upload the firmware
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: firmware_installed
  data:
    name: "Name of the Logical Interconnect"
    firmware:
      command: Stage
      spp: "filename"  # could also be sppUri: '/rest/firmware-drivers/<filename>'

- name: Updates the telemetry configuration of a logical interconnect.
  oneview_logical_interconnect:
  config: "{{ config_file_path }}"
  state: telemetry_configuration_updated
  data:
    name: "Name of the Logical Interconnect"
    telemetryConfiguration:
      sampleCount: 12
      enableTelemetry: True
      sampleInterval: 300

- debug: var=telemetry_configuration

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_fib   | Has the OneView facts about the Forwarding information Base. |  On 'forwarding_information_base_generated' state, but can be null. |  complex |
| li_firmware   | Has the OneView facts about the installed Firmware. |  On 'firmware_installed' state, but can be null. |  complex |
| port_monitor   | Has the OneView facts about the Port Monitor Configuration. |  On 'port_monitor_updated' state, but can be null. |  complex |
| qos_configuration   | Has the OneView facts about the QoS Configuration. |  On 'qos_aggregated_configuration_updated' state, but can be null. |  complex |
| snmp_configuration   | Has the OneView facts about the SNMP Configuration. |  On 'snmp_configuration_updated' state, but can be null. |  complex |
| storage_volume_template   | Has the OneView facts about the Logical Interconnect. |  On 'compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',               and 'configuration_updated' states, but can be null. |  complex |
| telemetry_configuration   | Has the OneView facts about the Telemetry Configuration. |  On 'telemetry_configuration_updated' state, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_interconnect_facts
Retrieve facts about one or more of the OneView Logical Interconnects.

#### Synopsis
 Retrieve facts about one or more of the OneView Logical Interconnects.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Interconnect name.  |
| options  |   No  |  | |  List with options to gather additional facts about Logical Interconnect. Options allowed: `qos_aggregated_configuration` gets the QoS aggregated configuration for the logical interconnect. `snmp_configuration` gets the SNMP configuration for a logical interconnect. `port_monitor` gets the port monitor configuration of a logical interconnect. `internal_vlans` gets the internal VLAN IDs for the provisioned networks on a logical interconnect. `forwarding_information_base` gets the forwarding information base data for a logical interconnect. `firmware` get the installed firmware for a logical interconnect. `unassigned_uplink_ports` gets a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port. `telemetry_configuration` gets the telemetry configuration of the logical interconnect. `ethernet_settings` gets the Ethernet interconnect settings for the Logical Interconnect. - These options are valid just when a `name` is provided. Otherwise it will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Interconnects
  oneview_logical_interconnect_facts:
  config: "{{ config }}"

- debug: var=logical_interconnects

- name: Gather paginated and sorted facts about Logical Interconnects
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=logical_interconnects

- name: Gather facts about a Logical Interconnect by name with QOS Configuration
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - qos_aggregated_configuration

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration

- name: Gather facts about a Logical Interconnect by name with all options
  oneview_logical_interconnect_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - qos_aggregated_configuration
      - snmp_configuration
      - port_monitor
      - internal_vlans
      - forwarding_information_base
      - firmware
      - unassigned_uplink_ports
      - telemetry_configuration
      - ethernet_settings

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration
- debug: var=snmp_configuration
- debug: var=port_monitor
- debug: var=internal_vlans
- debug: var=forwarding_information_base
- debug: var=firmware
- debug: var=unassigned_uplink_ports
- debug: var=telemetry_configuration
- debug: var=ethernet_settings

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_settings   | The Ethernet Interconnect Settings. |  When requested, but can be null. |  complex |
| firmware   | The installed firmware for a logical interconnect. |  When requested, but can be null. |  complex |
| forwarding_information_base   | The forwarding information base data for a logical interconnect. |  When requested, but can be null. |  complex |
| internal_vlans   | The internal VLAN IDs for the provisioned networks on a logical interconnect. |  When requested, but can be null. |  complex |
| logical_interconnects   | The list of logical interconnects. |  Always, but can be null. |  list |
| port_monitor   | The port monitor configuration of a logical interconnect. |  When requested, but can be null. |  complex |
| qos_aggregated_configuration   | The QoS aggregated configuration for the logical interconnect. |  When requested, but can be null. |  complex |
| snmp_configuration   | The SNMP configuration for a logical interconnect. |  When requested, but can be null. |  complex |
| telemetry_configuration   | The telemetry configuration of the logical interconnect. |  When requested, but can be null. |  complex |
| unassigned_uplink_ports   | A collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port on a logical interconnect. |  When requested, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_interconnect_group
Manage OneView Logical Interconnect Group resources.

#### Synopsis
 Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Logical Interconnect Group properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Logical Interconnect Group resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalDownlinkUri: ~
            logicalLocation:
                locationEntries:
                    - relativeValue: "1"
                      type: "Bay"
                    - relativeValue: 1
                      type: "Enclosure"
            permittedInterconnectTypeName: 'HP VC Flex-10/10D Module'
            # Alternatively you can inform permittedInterconnectTypeUri

- name: Ensure that the Logical Interconnect Group is present with name 'Test'
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the Logical Interconnect Group is absent
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New Logical Interconnect Group'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnect_group   | Has the facts about the OneView Logical Interconnect Group. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_interconnect_group_facts
Retrieve facts about one or more of the OneView Logical Interconnect Groups.

#### Synopsis
 Retrieve facts about one or more of the Logical Interconnect Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Interconnect Group name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_interconnect_groups

- name: Gather paginated, filtered and sorted facts about Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=LIGName'

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=logical_interconnect_groups

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnect_groups   | Has all the OneView facts about the Logical Interconnect Groups. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_logical_switch
Manage OneView Logical Switch resources.

#### Synopsis
 Provides an interface to manage Logical Switch resources. Can create, update, delete, or refresh.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Logical Switches properties. You can choose set the Logical Switch Group by logicalSwitchGroupName or logicalSwitchGroupUri.  |
| state  |   |  | <ul> <li>present</li>  <li>updated</li>  <li>absent</li>  <li>refreshed</li> </ul> |  Indicates the desired state for the Logical Switch resource. 'present' creates a Logical Switch, if it doesn't exist. To update the Logical Switch, use the 'updated' state instead. 'updated' ensures the Logical Switch is updated. Currently OneView only supports updating the credentials and name of the Logical Switch. To change the name of the Logical Switch, a 'newName' in the data must be provided. The update operation is non-idempotent. 'absent' removes the resource from OneView, if it exists. 'refreshed' reclaims the top-of-rack switches in the logical switch. This operation is non-idempotent.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Logical Switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: present
    data:
      logicalSwitch:
        name: 'Test Logical Switch'
        # You can choose set the Logical Switch Group by logicalSwitchGroupName or logicalSwitchGroupUri
        logicalSwitchGroupName: 'Group Nexus 55xx'                                                   # option 1
        # logicalSwitchGroupUri: '/rest/logical-switch-groups/dce11b79-6fce-48af-84fb-a315b9644571'  # option 2
        switchCredentialConfiguration:
          - snmpV1Configuration:  # Switch 1
              communityString: 'public'
            logicalSwitchManagementHost: '172.18.16.1'
            snmpVersion: 'SNMPv1'
            snmpPort: 161
          - snmpV1Configuration:  # Switch 2
              communityString: 'public'
            logicalSwitchManagementHost: '172.18.16.2'
            snmpVersion: 'SNMPv1'
            snmpPort: 161
      logicalSwitchCredentials:
        - connectionProperties:  # Switch 1
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_1'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_1'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'
        - connectionProperties:  # Switch 2
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_2'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_2'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'

- name: Update the Logical Switch name and credentials
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: updated
    data:
      logicalSwitch:
        name: 'Test Logical Switch'
        newName: 'Test Logical Switch - Renamed'
      logicalSwitchCredentials:
        - connectionProperties:  # Switch 1
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_1'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_1'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'
        - connectionProperties:  # Switch 2
            - propertyName: 'SshBasicAuthCredentialUser'
              value: 'ssh_username_switch_2'
              valueFormat: 'Unknown'
              valueType: 'String'
            - propertyName: 'SshBasicAuthCredentialPassword'
              value: 'ssh_password_switch_2'
              valueFormat: 'SecuritySensitive'
              valueType: 'String'

- name: Reclaim the top-of-rack switches in the logical switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: refreshed
    data:
      logicalSwitch:
        name: 'Test Logical Switch'

- name: Delete a Logical Switch
  oneview_logical_switch:
    config: "{{ config_path }}"
    state: absent
    data:
      logicalSwitch:
        name: 'Test Logical Switch'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_switch   | Has the facts about the OneView Logical Switch. |  On the states 'present', 'updated', and 'refreshed'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is only available on C7000 enclosures


---


## oneview_logical_switch_facts
Retrieve the facts about one or more of the OneView Logical Switches.

#### Synopsis
 Retrieve the facts about one or more of the Logical Switches from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Switch name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Switches
  oneview_logical_switch_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_switches

- name: Gather paginated, filtered and sorted facts about Logical Switches
  oneview_logical_switch_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_switches

- name: Gather facts about a Logical Switch by name
  oneview_logical_switch_facts:
    config: "{{ config_file_path }}"
    name: 'Name of the Logical Switch'

- debug: var=logical_switches

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_switches   | Has all the OneView facts about the Logical Switches. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is only available on C7000 enclosures


---


## oneview_logical_switch_group
Manage OneView Logical Switch Group resources.

#### Synopsis
 Provides an interface to manage Logical Switch Group resources. Can add, update, remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Logical Switch Group properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Logical Switch Group resource. 'present' will ensure data properties are compliant with OneView. 'absent' will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  # You can choose either permittedSwitchTypeName or permittedSwitchTypeUri to inform the Switch Type
                  permittedSwitchTypeName: 'Cisco Nexus 50xx'
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Update the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        newName: "Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Delete the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Test Logical Switch Group'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_switch_group   | Has the OneView facts about the Logical Switch Group. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is only available on C7000 enclosures


---


## oneview_logical_switch_group_facts
Retrieve facts about OneView Logical Switch Groups.

#### Synopsis
 Retrieve facts about the Logical Switch Groups of the OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Switch Group name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Logical Switch Groups
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=logical_switch_groups

- name: Gather paginated, filtered and sorted facts about Logical Switch Groups
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='Logical_Switch_Group+56'"

- debug: var=logical_switch_groups

- name: Gather facts about a Logical Switch Group by name
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
    name: "LogicalSwitchGroupDemo"
  delegate_to: localhost

- debug: var=logical_switch_groups

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_switch_groups   | Has all the OneView facts about the Logical Switch Groups. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is only available on C7000 enclosures


---


## oneview_managed_san
Manage OneView Managed SAN resources.

#### Synopsis
 Provides an interface to manage Managed SAN resources. Can update the Managed SAN, set the refresh state, create a SAN endpoints CSV file, and create an unexpected zoning issue report.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Managed SAN properties and its associated states. Warning: For the 'present' state, the contents of the publicAttributes will replace the existing list, so leaving out a public attribute from the given list will effectively delete it.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>refresh_state_set</li>  <li>endpoints_csv_file_created</li>  <li>issues_report_created</li> </ul> |  Indicates the desired state for the Managed SAN resource. `present` ensures data properties are compliant with OneView. `refresh_state_set` updates the refresh state of the Managed SAN. `endpoints_csv_file_created` creates a SAN endpoints CSV file. `issues_report_created` creates an unexpected zoning report for a SAN.  |


 
#### Examples

```yaml
  - name: Refresh the Managed SAN
    oneview_managed_san:
      config: '{{ config_path }}'
      state: refresh_state_set
      data:
          name: 'SAN1_0'
          refreshStateData:
              refreshState: 'RefreshPending'
    delegate_to: localhost

  - name: Update the Managed SAN
    oneview_managed_san:
      config: '{{ config_path }}'
      state: present
      data:
          name: 'SAN1_0'
          publicAttributes:
            - name: 'MetaSan'
              value: 'Neon SAN'
              valueType: 'String'
              valueFormat: 'None'
          sanPolicy:
            zoningPolicy: 'SingleInitiatorAllTargets'
            zoneNameFormat: '{hostName}_{initiatorWwn}'
            enableAliasing: True
            initiatorNameFormat: '{hostName}_{initiatorWwn}'
            targetNameFormat: '{storageSystemName}_{targetName}'
            targetGroupNameFormat: '{storageSystemName}_{targetGroupName}'
    delegate_to: localhost

  - name: Create an endpoints CSV file for the SAN
    oneview_managed_san:
      config: '{{ config }}'
      state: endpoints_csv_file_created
      data:
          name: '{{ name }}'
    delegate_to: localhost

  - name: Create an unexpected zoning report for the SAN
    oneview_managed_san:
      config: '{{ config }}'
      state: issues_report_created
      data:
          name: '{{ name }}'
    delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| managed_san   | Has the OneView facts about the Managed SAN. |  On states 'present' and 'refresh_state_set'. Can be null. |  complex |
| managed_san_endpoints   | Has the OneView facts about the Endpoints CSV File created. |  On state 'endpoints_csv_file_created'. Can be null. |  complex |
| managed_san_issues   | Has the OneView facts about the unexpected zoning report created. |  On state 'issues_report_created'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_managed_san_facts
Retrieve facts about the OneView Managed SANs.

#### Synopsis
 Retrieve facts about the OneView Managed SANs.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Managed SAN.  |
| options  |   No  |  | |  List with options to gather additional facts about Managed SAN. Options allowed: `endpoints` gets the list of endpoints in the SAN identified by name. `wwn` gets the list of Managed SANs associated with an informed WWN `locate`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `query`: A general query string to narrow the list of resources returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Managed SANs
  oneview_managed_san_facts:
    config: "{{ config_path }}"
  delegate_to: localhost

- debug: var=managed_sans

- name: Gather paginated, filtered and sorted facts about Managed SANs
  oneview_managed_san_facts:
    config: "{{ config_path }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      query: imported eq true
  delegate_to: localhost

- debug: var=managed_sans

- name: Gather facts about a Managed SAN by name
  oneview_managed_san_facts:
    config: "{{ config_path }}"
    name: "SAN1_0"
  delegate_to: localhost

- debug: var=managed_sans

- name: Gather facts about the endpoints in the SAN identified by name
  oneview_managed_san_facts:
    config: "{{ config_path }}"
    name: "SAN1_0"
    options:
      - endpoints
  delegate_to: localhost

- debug: var=managed_sans
- debug: var=managed_san_endpoints

- name: Gather facts about Managed SANs for an associated WWN
  oneview_managed_san_facts:
    config: "{{ config_path }}"
    options:
      - wwn:
         locate: "20:00:4A:2B:21:E0:00:01"
  delegate_to: localhost

- debug: var=wwn_associated_sans

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| managed_san_endpoints   | The list of endpoints in the SAN identified by name. |  When requested, but can be null. |  complex |
| managed_sans   | The list of Managed SANs. |  Always, but can be null. |  list |
| wwn_associated_sans   | The list of associations between provided WWNs and the SANs. |  When requested, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_network_set
Manage OneView Network Set resources.

#### Synopsis
 Provides an interface to manage Network Set resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Network Set properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Network Set resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      networkUris:
        - 'Test Ethernet Network_1'                                       # can be a name
        - '/rest/ethernet-networks/e4360c9d-051d-4931-b2aa-7de846450dd8'  # or a URI

- name: Update the Network Set name to 'OneViewSDK Test Network Set - Renamed' and change the associated networks
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      newName: 'OneViewSDK Test Network Set - Renamed'
      networkUris:
        - 'Test Ethernet Network_1'

- name: Delete the Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: absent
    data:
        name: 'OneViewSDK Test Network Set - Renamed'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| network_set   | Has the facts about the Network Set. |  On state 'present', but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_network_set_facts
Retrieve facts about the OneView Network Sets.

#### Synopsis
 Retrieve facts about the Network Sets from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Network Set name.  |
| options  |   No  |  | |  List with options to gather facts about Network Set. Option allowed: `withoutEthernet`. The option `withoutEthernet` retrieves the list of network_sets excluding Ethernet networks.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Network Sets
  oneview_network_set_facts:
    config: '{{ config_path }}'

- debug: var=network_sets

- name: Gather paginated, filtered, and sorted facts about Network Sets
  oneview_network_set_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: name='netset001'

- debug: var=network_sets

- name: Gather facts about all Network Sets, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    options:
        - withoutEthernet

- debug: var=network_sets


- name: Gather facts about a Network Set by name
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'

- debug: var=network_sets


- name: Gather facts about a Network Set by name, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'
    options:
        - withoutEthernet

- debug: var=network_sets

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| network_sets   | Has all the OneView facts about the Network Sets. |  Always, but can be empty. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_os_deployment_plan_facts
Retrieve facts about one or more Os Deployment Plans.

#### Synopsis
 Retrieve facts about one or more of the Os Deployment Plans from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Os Deployment Plan name.  |
| options  |   No  |  | |  List with options to gather facts about OS Deployment Plan. Option allowed: `osCustomAttributesForServerProfile` The option `osCustomAttributesForServerProfile` retrieves the list of editable OS Custom Atributes, prepared for Server Profile use.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all OS Deployment Plans
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather paginated, filtered and sorted facts about OS Deployment Plans
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: deploymentApplianceIpv4='15.212.171.216'
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather facts about an OS Deployment Plan by name
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    name: "Deployment Plan"
  delegate_to: localhost
- debug: var=os_deployment_plans

- name: Gather facts about an OS Deployment Plan by name with OS Custom Attributes option
  oneview_os_deployment_plan_facts:
    config: "{{ config }}"
    name: "Deployment Plan"
    options:
      # This option will generate an os_deployment_plan_custom_attributes facts in the Server Profile format.
      - osCustomAttributesForServerProfile
  delegate_to: localhost
- debug: var=os_deployment_plans
- debug: var=os_deployment_plan_custom_attributes

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| os_deployment_plan_custom_attributes   | Has the editable Custom Attribute facts of the Os Deployment Plans in the Server Profiles format. |  When requested, but can be empty. |  complex |
| os_deployment_plans   | Has all the OneView facts about the Os Deployment Plans. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_os_deployment_server
Manage OneView Deployment Server resources.

#### Synopsis
 Provides an interface to manage Deployment Server resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Deployment Server properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Deployment Server resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the Deployment Server is present
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Deployment Server'
      description: "OS Deployment Server"
      mgmtNetworkUri: "/rest/ethernet-networks/1b96d2b3-bc12-4757-ac72-e4cd0ef20535"
      applianceUri: "/rest/deployment-servers/image-streamer-appliances/aca554e2-09c2-4b14-891d-e51c0058efab"
- debug: var=os_deployment_server

- name: Ensure that the Deployment Server is present with name 'Renamed Deployment Server'
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Deployment Server'
      newName: 'Renamed Deployment Server'
- debug: var=os_deployment_server

- name: Ensure that the Deployment Server is absent
  oneview_os_deployment_server:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Renamed Deployment Server'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| os_deployment_server   | Has the facts about the Deployment Servers. |  On state 'present'. Can be null. |  complex |


#### Notes

- For the following data, you can provide either a name or a URI: `mgmtNetworkName` or `mgmtNetworkUri`, and `applianceName` or `applianceUri`

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_os_deployment_server_facts
Retrieve facts about one or more OS Deployment Servers.

#### Synopsis
 Retrieve facts about one or more of the OS Deployment Servers from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  OS Deployment Server name.  |
| options  |   No  |  | |  List with options to gather additional facts about an OS Deployment Server and related resources. Options allowed: `networks`, `appliances`, and `appliance`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set. `query`: A general query string to narrow the list of resources returned. `fields`: Specifies which fields should be returned in the result set. `view`: Return a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.  |


 
#### Examples

```yaml
- name: Gather facts about all OS Deployment Servers
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: "OS Deployment Server-Name"
  delegate_to: localhost

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name with options
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: 'Test-OS Deployment Server'
    options:
      - networks                    # optional
      - appliances                  # optional
      - appliance: 'Appliance name' # optional
  delegate_to: localhost

- debug: var=os_deployment_servers
- debug: var=os_deployment_server_networks
- debug: var=os_deployment_server_appliances
- debug: var=os_deployment_server_appliance

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| os_deployment_server_appliance   | Has the facts about the particular Image Streamer resource. |  When requested, but can be null. |  complex |
| os_deployment_server_appliances   | Has all the OneView facts about all the Image Streamer resources. |  When requested, but can be null. |  complex |
| os_deployment_server_networks   | Has all the OneView facts about the OneView networks. |  When requested, but can be null. |  complex |
| os_deployment_servers   | Has all the OneView facts about the OS Deployment Servers. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_power_device
Manage OneView Power Device resources.

#### Synopsis
 Provides an interface to manage Power delivery devices resources. Can add, update, remove, change power state, change UID state and refresh state.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Power Device properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>discovered</li>  <li>absent</li>  <li>power_state_set</li>  <li>refresh_state_set</li>  <li>uid_state_set</li> </ul> |  Indicates the desired state for the Power Device resource. `present` will ensure data properties are compliant with OneView. `discovered` will add an iPDU to the OneView. `absent` will remove the resource from OneView, if it exists. `power_state_set` will set the power state of the Power Device. `refresh_state_set` will set the refresh state of the Power Device. `uid_state_set` will set the UID state of the Power Device.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Add a Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: present
    data:
        name: 'Power Device Name'
        ratedCapacity: 40
  delegate_to: localhost

- name: Add an iPDU
  oneview_power_device:
    config: "{{ config }}"
    state: discovered
    data:
         hostname : '{{ power_device_hostname }}'
         username : '{{ power_device_username }}'
         password : '{{ power_device_password }}'
         force : false
  delegate_to: localhost

- name: Power off the Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: power_state_set
    data:
        name: 'Power Device Name'
        powerStateData:
            powerState: "Off"
  delegate_to: localhost

- name: Refresh the Power Device
  oneview_power_device:
    config: "{{ config }}"
    state: refresh_state_set
    data:
        name: 'Power Device Name'
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Set UID light state of the Power Device on
  oneview_power_device:
    config: "{{ config }}"
    state: uid_state_set
    data:
        name: 'Power Device Name'
        uidStateData:
            uidState: "On"
  delegate_to: localhost

- name: Remove the Power Device by its name
  oneview_power_device:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Power Device Name'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| power_device   | Has the OneView facts about the Power Device. |  On states 'present', 'discovered', 'power_state_set', 'refresh_state_set', 'uid_state_set'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_power_device_facts
Retrieve facts about the OneView Power Devices.

#### Synopsis
 Retrieve facts about the Power Delivery Devices from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Power Device name.  |
| options  |   No  |  | |  List with options to gather additional facts about Power Device. Options allowed: `powerState`, `uidState`, `utilization`  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `query`: A general query string to narrow the list of resources returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Power Devices
  oneview_power_device_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: msg="{{power_devices | map(attribute='name') | list }}"

- name:  Gather paginated, filtered and sorted facts about Power Devices
  oneview_power_device_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state='Unmanaged'
      query: feedIdentifier eq 'A'
  delegate_to: localhost
- debug: var=power_devices

- name: Gather facts about a Power Device by name
  oneview_power_device_facts:
    config: "{{ config }}"
    name: "Power Device Name"
  delegate_to: localhost
- debug: var=power_devices

- name: Gather facts about the power state of a Power Device
  oneview_power_device_facts:
    config: "{{ config }}"
    name: "Power Device Name"
    options:
      - powerState            # optional
  delegate_to: localhost
- debug: msg="{{power_devices | map(attribute='name') | list }}"
- debug: var=power_device_power_state

- name: Gather all facts about a Power Device with all options
  oneview_power_device_facts:
   config: "{{ config }}"
   name : "Power Device Name"
   options:
       - powerState             # optional
       - uidState               # optional
       - utilization:           # optional
                fields : 'AveragePower'
                filter : ['startDate=2016-05-30T03:29:42.000Z']
                view : 'day'
  delegate_to: localhost

- debug: msg="{{power_devices | map(attribute='name') | list }}"
- debug: var=power_device_power_state
- debug: var=power_device_uid_state
- debug: var=power_device_utilization

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| power_device_power_state   | Has all the facts about the Power state of the Power Device. |  When requested, but can be null. |  complex |
| power_device_uid_state   | Has all the facts about the Power Device UID state. |  When requested, but can be null. |  complex |
| power_device_utilization   | Has all the facts about the Power Device utilization. |  When requested, but can be null. |  complex |
| power_devices   | Has all the OneView facts about the Power Device. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_rack
Manage OneView Racks resources.

#### Synopsis
 Provides an interface to manage Rack resources. Can create, update, and delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Rack properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Rack resource. `present` will ensure data properties are compliant with OneView. To change the name of the Rack, a _newName_ in the data must be provided. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that a Rack is present using the default configuration
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'

- name: Add rack with custom size and a single mounted enclosure at slot 20
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack101'
      depth: 1500
      height: 2500
      width: 1200
      rackMounts:
        - mountUri: "/rest/enclosures/39SGH102X6J2"
          topUSlot: 20
          uHeight: 10

- name: Rename the Rack to 'Rack101'
  oneview_rack:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Rack Name'
      newName: 'Rack101'

- name: Ensure that Rack is absent
  oneview_rack:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Rack Name'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| rack   | Has the facts about the OneView Racks. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_rack_facts
Retrieve facts about Rack resources.

#### Synopsis
 Gets a list of rack resources. Filter by name can be used to get a specific Rack. If a name is specified, it is  allowed to retrieve information about the device topology.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Rack name.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: 'deviceTopology'.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Racks
  oneview_rack_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=racks

- name: Gather paginated, filtered and sorted facts about Racks
  oneview_rack_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "depth=1000"

- name: Gather facts about a Rack by name
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
  delegate_to: localhost
- debug: var=racks

- name: Gather facts about the topology information for the rack
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
    options:
      - deviceTopology
  delegate_to: localhost
- debug: var=racks
- debug: var=rack_device_topology

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| rack_device_topology   | Retrieves the topology information for the rack resource. |  When requested, but can be null. |  complex |
| racks   | Has all the OneView facts about the Racks. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_san_manager
Manage OneView SAN Manager resources.

#### Synopsis
 Provides an interface to manage SAN Manager resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with SAN Manager properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Uplink Set resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Creates a Device Manager for the Brocade SAN provider with the given hostname and credentials
  oneview_san_manager:
    config: "{{ config }}"
    state: present
    data:
      providerDisplayName: 'Brocade Network Advisor'
      connectionInfo:
        - name: Host
          value: '172.18.15.1'
        - name: Port
          value: '5989'
        - name: Username
          value: 'username'
        - name: Password
          value: 'password'
        - name: UseSsl
          value: true

- name: Update the SAN Manager
  oneview_san_manager:
    config: "{{ config_path }}"
    state: present
    data:
      providerDisplayName: 'Brocade Network Advisor'
      refreshState: 'RefreshPending'

- name: Delete the SAN Manager recently created
  oneview_san_manager:
    config: "{{ config_path }}"
    state: absent
    data:
      providerDisplayName: 'Brocade Network Advisor'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| san_manager   | Has the OneView facts about the SAN Manager. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_san_manager_facts
Retrieve facts about one or more of the OneView SAN Managers.

#### Synopsis
 Retrieve facts about one or more of the SAN Managers from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `query`: A general query string to narrow the list of resources returned. `sort`: The sort order of the returned data set.  |
| provider_display_name  |   No  |  | |  Provider Display Name.  |


 
#### Examples

```yaml
- name: Gather facts about all SAN Managers
  oneview_san_manager_facts:
    config: "{{ config_path }}"

- debug: var=san_managers

- name: Gather paginated, filtered and sorted facts about SAN Managers
  oneview_san_manager_facts:
    config: "{{ config_path }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      query: isInternal eq false
  delegate_to: localhost

- debug: var=san_managers

- name: Gather facts about a SAN Manager by provider display name
  oneview_san_manager_facts:
    config: "{{ config_path }}"
    provider_display_name: "Brocade Network Advisor"

- debug: var=san_managers

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| san_managers   | Has all the OneView facts about the SAN Managers. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_interconnect
Manage the OneView SAS Interconnect resources.

#### Synopsis
 Provides an interface to manage the SAS Interconnect. Can change the power state, UID light state, perform soft and hard reset, and refresh the SAS Interconnect state.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   Yes  |  | |  The SAS Interconnect name.  |
| state  |   |  | <ul> <li>powered_on</li>  <li>powered_off</li>  <li>uid_on</li>  <li>uid_off</li>  <li>soft_reset</li>  <li>hard_reset</li>  <li>refreshed</li> </ul> |  Indicates the desired state for the Switch. `powered_on` turns the power on. `powered_off` turns the power off. `uid_on` turns the UID light on. `uid_off` turns the UID light off. `soft_reset` performs a soft reset. `hard_reset` performs a hard reset. `refreshed` performs a refresh.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that a SAS Interconnect is powered on
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: powered_on
    name: "0000A66101, interconnect 1"

- name: Refresh a SAS Interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: refreshed
    name: "0000A66101, interconnect 1"

- name: Perform a hard reset
  oneview_sas_interconnect:
    config: "{{ config }}"
    state: hard_reset
    name: "0000A66101, interconnect 1"

```



#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_interconnect_facts
Retrieve facts about the OneView SAS Interconnects.

#### Synopsis
 Retrieve facts about the OneView SAS Interconnects.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  SAS Interconnect name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"

- name: Gather paginated, filtered and sorted facts about SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "softResetState='Normal'"

- name: Gather facts about a SAS Interconnect by name
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    name: "0000A66103, interconnect 1"

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_interconnects   | The list of SAS Interconnects. |  Always, but can be null. |  list |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_interconnect_type_facts
Retrieve facts about the OneView SAS Interconnect Types.

#### Synopsis
 Retrieve facts about the SAS Interconnect Types from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the SAS Interconnect Type.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Interconnect Types
  oneview_sas_interconnect_type_facts:
    config: "{{ config_path }}"

- debug: var=sas_interconnect_types

- name: Gather paginated, filtered and sorted facts about SAS Interconnect Types
  oneview_sas_interconnect_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "enclosureType='SY12000'"

- debug: var=sas_interconnect_types

- name: Gather facts about a SAS Interconnect Type by name
  oneview_sas_interconnect_type_facts:
    config: "{{ config_path }}"
    name: "SAS Interconnect Type Name"

- debug: var=sas_interconnect_types

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_interconnect_types   | Has all the OneView facts about the SAS Interconnect Types. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_interconnect
Manage OneView SAS Logical Interconnect resources.

#### Synopsis
 Provides an interface to manage SAS Logical Interconnect resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with SAS Logical Interconnect properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>compliant</li>  <li>drive_enclosure_replaced</li>  <li>configuration_updated</li>  <li>firmware_updated</li> </ul> |  Indicates the desired state for the SAS Logical Interconnect resources. `compliant` brings the list of SAS Logical Interconnect back to a consistent state. `configuration_updated` asynchronously applies or re-applies the SAS Logical Interconnect configuration to all managed interconnects. `firmware_updated` installs firmware to a SAS Logical Interconnect. `drive_enclosure_replaced` replacement operation of a drive enclosure. * All of them are non-idempotent.  |


 
#### Examples

```yaml
- name: Update the configuration on the SAS Logical Interconnect
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: configuration_updated
    data:
      name: "SAS Logical Interconnect name"
  delegate_to: localhost

- name: Install a firmware to the SAS Logical Interconnect, running the stage operation to upload the firmware
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: firmware_updated
    data:
      name: "SAS Logical Interconnect name"
      firmware:
        command: Stage
        sppName: "firmware_driver_name"
        # Can be either the firmware name with "sppName" or the uri with "sppUri", e.g.:
        # sppUri: '/rest/firmware-drivers/<filename>'
  delegate_to: localhost

- name: Replace drive enclosure
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: drive_enclosure_replaced
    data:
      name: "SAS Logical Interconnect name"
      replace_drive_enclosure:
        oldSerialNumber: "S46016710000J4524YPT"
        newSerialNumber: "S46016710001J4524YPT"
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its names
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: compliant
    data:
      logicalInterconnectNames: ["SAS Logical Interconnect name 1", "SAS Logical Interconnect name 2"]
  delegate_to: localhost

- name: Return a SAS Logical Interconnect list to a consistent state by its URIs
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    state: compliant
    data:
      logicalInterconnectUris: [
        '/rest/sas-logical-interconnects/16b2990f-944a-449a-a78f-004d8b4e6824',
        '/rest/sas-logical-interconnects/c800b2e4-92bb-44fa-8a46-f71d40737fa5']
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| li_firmware   | Has the OneView facts about the updated Firmware. |  On 'firmware_updated' state, but can be null. |  complex |
| sas_logical_interconnect   | Has the OneView facts about the SAS Logical Interconnect. |  On states 'drive_enclosure_replaced', 'configuration_updated', but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_interconnect_facts
Retrieve facts about one or more of the OneView SAS Logical Interconnects.

#### Synopsis
 Retrieve facts about one or more of the OneView SAS Logical Interconnects.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  SAS Logical Interconnect name.  |
| options  |   No  |  | |  List with options to gather additional facts about SAS Logical Interconnect. `firmware` gets the installed firmware for a SAS Logical Interconnect.  These options are valid just when a `name` is provided. Otherwise it will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "status='OK'"
- debug: var=sas_logical_interconnects

- name: Gather facts about a SAS Logical Interconnect by name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather facts about an installed firmware for a SAS Logical Interconnect that matches the specified name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
    options:
      - firmware
  delegate_to: localhost
- debug: var=sas_logical_interconnect_firmware

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_interconnect_firmware   | The installed firmware for a SAS Logical Interconnect. |  When requested, but can be null. |  complex |
| sas_logical_interconnects   | The list of SAS Logical Interconnects. |  Always, but can be null. |  list |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_interconnect_group
Manage OneView SAS Logical Interconnect Group resources.

#### Synopsis
 Provides an interface to manage SAS Logical Interconnect Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the SAS Logical Interconnect Group properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the SAS Logical Interconnect Group resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the SAS Logical Interconnect Group is present
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    state: present
    data:
      name: "Test SAS Logical Interconnect Group"
      state: "Active"
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "1"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "4"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
      enclosureType: "SY12000"
      enclosureIndexes: [1]
      interconnectBaySet: "1"

- name: Ensure that the SAS Logical Interconnect Group is present with name 'Test'
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New SAS Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the SAS Logical Interconnect Group is absent
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New SAS Logical Interconnect Group'

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_interconnect_group   | Has the facts about the OneView SAS Logical Interconnect Group. |  On state 'present'. Can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_interconnect_group_facts
Retrieve facts about one or more of the OneView SAS Logical Interconnect Groups.

#### Synopsis
 Retrieve facts about one or more of the SAS Logical Interconnect Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the SAS Logical Interconnect Group.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Logical Interconnect Groups
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config_path }}"
- debug: var=sas_logical_interconnect_groups

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnect Groups
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "state='Active'"
- debug: var=sas_logical_interconnect_groups

- name: Gather facts about a SAS Logical Interconnect Group by name
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config_path }}"
    name: "LIG-SLJA-1"
- debug: var=sas_logical_interconnect_groups

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_interconnect_groups   | Has all the OneView facts about the SAS Logical Interconnect Groups. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_jbod_attachment_facts
Retrieve facts about one or more of the OneView SAS Logical JBOD Attachments.

#### Synopsis
 Retrieve facts about one or more of the SAS Logical JBOD Attachments from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of SAS Logical JBOD Attachment.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Logical JBOD Attachment
  oneview_sas_logical_jbod_attachment_facts:
  config: "{{ config_path }}"

- debug: var=sas_logical_jbod_attachments

- name: Gather paginated, filtered and sorted facts about SAS Logical JBOD Attachment
  oneview_sas_logical_jbod_attachment_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "state=Deployed"

- debug: var=sas_logical_jbod_attachments


- name: Gather facts about a SAS Logical JBOD Attachment by name
  oneview_sas_logical_jbod_attachment_facts:
    config: "{{ config_path }}"
    name: "logical-enclosure-SAS-Logical-Interconnect-Group-BDD-1-SLJA-1"

- debug: var=sas_logical_jbod_attachments

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_jbod_attachments   | Has all the OneView facts about the SAS Logical JBOD Attachment. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_sas_logical_jbod_facts
Retrieve facts about one or more of the OneView SAS Logical JBODs.

#### Synopsis
 Retrieve facts about one or more of the SAS Logical JBODs from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of SAS Logical JBODs.  |
| options  |   No  |  | |  List with options to gather additional facts about SAS Logical JBODs and related resources. Options allowed: `drives`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all SAS Logical JBODs
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"

- debug: var=sas_logical_jbods

- name: Gather paginated, filtered and sorted facts about SAS Logical JBODs
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "state='Configured'"

- debug: var=sas_logical_jbods

- name: Gather facts about a SAS Logical JBOD by name
  oneview_sas_logical_jbod_facts:
    config: "{{ config_path }}"
    name: "Name of the SAS Logical JBOD"

- debug: var=sas_logical_jbods

- name: Gather facts about a SAS Logical JBOD by name, with the list of drives allocated
  oneview_sas_logical_jbod_facts:
    config: "{{ config }}"
    name: "{{ sas_logical_jbod_name }}"
    options:
      - drives

- debug: var=sas_logical_jbods
- debug: var=sas_logical_jbod_drives

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_jbod_drives   | Has all the OneView facts about the list of drives allocated to a SAS logical JBOD. |  Always, but can be null. |  complex |
| sas_logical_jbods   | Has all the OneView facts about the SAS Logical JBODs. |  Always, but can be null. |  complex |


#### Notes

- This resource is only available on HPE Synergy

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_scope
Manage OneView Scope resources.

#### Synopsis
 Provides an interface to manage scopes. Can create, update, or delete scopes, and modify the scope membership by adding or removing resource assignments.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Scopes properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>resource_assignments_updated</li> </ul> |  Indicates the desired state for the Scope resource. 'present' ensures data properties are compliant with OneView. 'absent' removes the resource from OneView, if it exists. 'resource_assignments_updated' modifies scope membership by adding or removing resource assignments. This operation is non-idempotent.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a scope
  oneview_scope:
    config: '{{ config }}'
    state: present
    data:
      name: 'SampleScope'
  delegate_to: localhost

- name: Update the scope
  oneview_scope:
    config: '{{ config }}'
    state: present
    data:
      name: 'SampleScope'
      newName: 'SampleScopeRenamed'
  delegate_to: localhost

- name: Delete the Scope
  oneview_scope:
    config: '{{ config }}'
    state: absent
    data:
      name: 'SampleScopeRenamed'
  delegate_to: localhost

- name: Update the scope resource assignments, adding two resources
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        addedResourceUris:
          - '{{ fc_network_1.uri }}'
          - '{{ fc_network_2.uri }}'
  delegate_to: localhost

- name: Update the scope resource assignments, adding one resource and removing another previously added
  oneview_scope:
    config: '{{ config }}'
    state: resource_assignments_updated
    data:
      name: 'SampleScopeRenamed'
      resourceAssignments:
        addedResourceUris:
          - '{{ fc_network_3.uri }}'
        removedResourceUris:
          - '{{ fc_network_1.uri }}'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| scope   | Has the facts about the Scope. |  On state 'present' and 'resource_assignments_updated', but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is available for API version 300 or later.


---


## oneview_scope_facts
Retrieve facts about one or more of the OneView Scopes.

#### Synopsis
 Retrieve facts about one or more of the Scopes from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the scope.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'query': A general query string to narrow the list of resources returned. 'sort': The sort order of the returned data set. 'view': Returns a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.  |


 
#### Examples

```yaml
- name: Gather facts about all Scopes
    oneview_scope_facts:
    config: "{{ config_path }}"

- debug: var=scopes

- name: Gather paginated, filtered and sorted facts about Scopes
  oneview_scope_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      query: name eq 'SampleScope'
  delegate_to: localhost

- debug: var=scopes

- name: Gather facts about a Scope by name
    oneview_scope_facts:
    config: "{{ config_path }}"
    name: "Name of the Scope"

- debug: var=scopes

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| scopes   | Has all the OneView facts about the Scopes. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is available for API version 300 or later.


---


## oneview_server_hardware
Manage OneView Server Hardware resources.

#### Synopsis
 Provides an interface to manage Server Hardware resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Server Hardware properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>power_state_set</li>  <li>refresh_state_set</li>  <li>ilo_firmware_version_updated</li>  <li>ilo_state_reset</li>  <li>uid_state_on</li>  <li>uid_state_off</li>  <li>environmental_configuration_set</li> </ul> |  Indicates the desired state for the Server Hardware resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists. `power_state_set` will set the power state of the Server Hardware. `refresh_state_set` will set the refresh state of the Server Hardware. `ilo_firmware_version_updated` will update the iLO firmware version of the Server Hardware. `ilo_state_reset` will reset the iLO state. `uid_state_on` will set on the UID state, if necessary. `uid_state_off` will set on the UID state, if necessary. `environmental_configuration_set` will set the environmental configuration of the Server Hardware.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Add a Server Hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: present
    data:
         hostname : "172.18.6.15"
         username : "username"
         password : "password"
         force : false
         licensingIntent: "OneView"
         configurationState: "Managed"
  delegate_to: localhost

- name: Power Off the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: power_state_set
    data:
        name : "172.18.6.15"
        powerStateData:
            powerState: "Off"
            powerControl: "MomentaryPress"
  delegate_to: localhost

- name: Refresh the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: refresh_state_set
    data:
        name : "172.18.6.15"
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Update the Server Hardware iLO firmware version
  oneview_server_hardware:
    config: "{{ config }}"
    state: ilo_firmware_version_updated
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the calibrated max power of a server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: environmental_configuration_set
    data:
        name : "172.18.6.15"
        environmentalConfigurationData:
            calibratedMaxPower: 2500
  delegate_to: localhost

- name: Remove the server hardware by its IP
  oneview_server_hardware:
    config: "{{ config }}"
    state: absent
    data:
        name : "172.18.6.15"
  delegate_to: localhost

- name: Set the server UID state off
  oneview_server_hardware:
    config: "{{ config }}"
    state: uid_state_off
    data:
        name : '0000A66102, bay 12'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware   | Has the OneView facts about the Server Hardware. |  On states 'present', 'power_state_set', 'refresh_state_set', and 'ilo_firmware_version_updated'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_hardware_facts
Retrieve facts about the OneView Server Hardwares.

#### Synopsis
 Retrieve facts about the Server Hardware from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Server Hardware name.  |
| options  |   No  |  | |  List with options to gather additional facts about Server Hardware related resources. Options allowed: `bios`, `javaRemoteConsoleUrl`, `environmentalConfig`, `iloSsoUrl`, `remoteConsoleUrl`, `utilization`, `firmware`, and `firmwares`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Server Hardwares
  oneview_server_hardware_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=server_hardwares


- name: Gather paginated, filtered and sorted facts about Server Hardware
  oneview_server_hardware_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: uidState='Off'
  delegate_to: localhost

- debug: msg="{{server_hardwares | map(attribute='name') | list }}"


- name: Gather facts about a Server Hardware by name
  oneview_server_hardware_facts:
    config: "{{ config }}"
    name: "172.18.6.15"
  delegate_to: localhost

- debug: var=server_hardwares


- name: Gather BIOS facts about a Server Hardware
  oneview_server_hardware_facts:
    config: "{{ config }}"
    name: "Encl1, bay 1"
    options:
      - bios
  delegate_to: localhost

- debug: var=server_hardwares
- debug: var=server_hardware_bios


- name: Gather all facts about a Server Hardware
  oneview_server_hardware_facts:
   config: "{{ config }}"
   name : "Encl1, bay 1"
   options:
       - bios                   # optional
       - javaRemoteConsoleUrl   # optional
       - environmentalConfig    # optional
       - iloSsoUrl              # optional
       - remoteConsoleUrl       # optional
       - utilization:           # optional
                fields : 'AveragePower'
                filter : ['startDate=2016-05-30T03:29:42.000Z']
                view : 'day'
       - firmware               # optional
  delegate_to: localhost

- debug: var=server_hardwares
- debug: var=server_hardware_bios
- debug: var=server_hardware_env_config
- debug: var=server_hardware_java_remote_console_url
- debug: var=server_hardware_ilo_sso_url
- debug: var=server_hardware_remote_console_url
- debug: var=server_hardware_utilization
- debug: var=server_hardware_firmware

- name: Gather facts about the Server Hardware firmware
  oneview_server_hardware_facts:
   config: "{{ config }}"
   name : "0000A66102, bay 12"
   options:
       - firmware
  delegate_to: localhost

- debug: var=server_hardware_firmware

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware_bios   | Has all the facts about the Server Hardware BIOS. |  When requested, but can be null. |  complex |
| server_hardware_env_config   | Has all the facts about the Server Hardware environmental configuration. |  When requested, but can be null. |  complex |
| server_hardware_firmware   | Has all the facts about the Server Hardware firmware. |  When requested, but can be null. |  complex |
| server_hardware_firmwares   | Has all the facts about the firmwares inventory across all servers. |  When requested, but can be null. |  complex |
| server_hardware_ilo_sso_url   | Has the facts about the Server Hardware iLO SSO url. |  When requested, but can be null. |  complex |
| server_hardware_java_remote_console_url   | Has the facts about the Server Hardware java remote console url. |  When requested, but can be null. |  complex |
| server_hardware_remote_console_url   | Has the facts about the Server Hardware remote console url. |  When requested, but can be null. |  complex |
| server_hardware_utilization   | Has all the facts about the Server Hardware utilization. |  When requested, but can be null. |  complex |
| server_hardwares   | Has all the OneView facts about the Server Hardware. |  Always, but can be null. |  complex |


#### Notes

- The options `firmware` and `firmwares` are only available for API version 300 or later.

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_hardware_type
Manage OneView Server Hardware Type resources.

#### Synopsis
 Provides an interface to manage Server Hardware Type resources. Can update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Server Hardware Type properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Server Hardware Type resource. 'present' will ensure data properties are compliant with OneView. 'absent' will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Update the Server Hardware Type description
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
      name: 'DL380p Gen8 1'
      description: "New Description"
  delegate_to: localhost

- name: Rename the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
        name: 'DL380p Gen8 1'
        newName: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost

- name: Delete the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: absent
    data:
        name: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware_type   | Has the OneView facts about the Server Hardware Type. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## oneview_server_hardware_type_facts
Retrieve facts about Server Hardware Types of the OneView.

#### Synopsis
 Retrieve facts about Server Hardware Types of the OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Server Hardware Type name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=server_hardware_types

- name: Gather paginated, filtered and sorted facts about Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: name:ascending
      filter: formFactor='HalfHeight'
  delegate_to: localhost
- debug: msg="{{server_hardware_types | map(attribute='name') | list }}"

- name: Gather facts about a Server Hardware Type by name
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    name: "BL460c Gen8 1"
  delegate_to: localhost
- debug: var=server_hardware_types

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware_types   | Has all the OneView facts about the Server Hardware Types. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_profile
Manage OneView Server Profile resources.

#### Synopsis
 Manage the servers lifecycle with OneView Server Profiles. On `present` state, it selects a server hardware automatically based on the server profile configuration if no server hardware was provided.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Server Profile properties.  |
| state  |   |  present  | <ul> <li>present</li>  <li>absent</li>  <li>compliant</li> </ul> |  Indicates the desired state for the Server Profile resource by the end of the playbook execution. `present` will ensure data properties are compliant with OneView. This operation will power off the Server Hardware before configuring the Server Profile. After it completes, the Server Hardware is powered on. `absent` will remove the resource from OneView, if it exists. `compliant` will make the server profile compliant with its server profile template, when this option was specified. If there are Offline updates, the Server Hardware is turned off before remediate compliance issues and turned on after that.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Server Profile from a Server Profile Template with automatically selected hardware
  oneview_server_profile:
    config: "{{ config }}"
    state: "present"
    data:
        name: Web-Server-L2
        # You can choose either server_template or serverProfileTemplateUri to inform the Server Profile Template
        # serverProfileTemplateUri: "/rest/server-profile-templates/31ade62c-2112-40a0-935c-2f9450a75198"
        server_template: Compute-node-template
        # You can inform a server_hardware or a serverHardwareUri. If any hardware was informed, it will try
        # get one available automatically
        # server_hardware: "Encl1, bay 12"
        # serverHardwareUri: "/rest/server-hardware/30303437-3933-4753-4831-30335835524E"

        # You can choose either serverHardwareTypeUri or serverHardwareTypeName to inform the Server Hardware Type
        # serverHardwareTypeUri: '/rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C'
        # serverHardwareTypeName: 'SY 480 Gen9 1'
        # You can choose either enclosureName or enclosureUri to inform the Enclosure
        # enclosureUri: '/rest/enclosures/09SGH100Z6J1'
        enclosureName: '0000A66102'
        sanStorage:
          hostOSType: 'Windows 2012 / WS2012 R2'
          manageSanStorage: true
          volumeAttachments:
            - id: 1
              # You can choose either volumeName or volumeUri to inform the Volumes
              # volumeName: 'DemoVolume001'
              volumeUri: '/rest/storage-volumes/BCAB376E-DA2E-450D-B053-0A9AE7E5114C'
              # You can choose either volumeStoragePoolUri or volumeStoragePoolName to inform the Volume Storage Pool
              # volumeStoragePoolName: 'FST_CPG2'
              volumeStoragePoolUri: '/rest/storage-pools/30303437-3933-4753-4831-30335835524E'
              # You can choose either volumeStorageSystemUri or volumeStorageSystemName to inform the Volume Storage
              # System
              # volumeStorageSystemName: 'ThreePAR7200-2127'
              volumeStorageSystemUri: '/rest/storage-systems/TXQ1000307'
              lunType: 'Auto'
              storagePaths:
                - isEnabled: true
                  connectionId: 1
                  storageTargetType: 'Auto'
                - isEnabled: true
                  connectionId: 2
                  storageTargetType: 'Auto'
- debug: var=server_profile
- debug: var=serial_number
- debug: var=server_hardware
- debug: var=compliance_preview
- debug: var=created

- name : Remediate compliance issues
  oneview_server_profile:
     config: "{{ config }}"
     state: "compliant"
     data:
        name: Web-Server-L2

- name : Remove the server profile
  oneview_server_profile:
    config: "{{ config }}"
    state: "absent"
    data:
        name: Web-Server-L2

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| compliance_preview   | Has the OneView facts about the manual and automatic updates required to make the server profile consistent with its template. |  On states 'present' and 'compliant'. |  complex |
| created   | Indicates if the Server Profile was created. |  On states 'present' and 'compliant'. |  bool |
| serial_number   | Has the Server Profile serial number. |  On states 'present' and 'compliant'. |  complex |
| server_hardware   | Has the OneView facts about the Server Hardware. |  On states 'present' and 'compliant'. |  complex |
| server_profile   | Has the OneView facts about the Server Profile. |  On states 'present' and 'compliant'. |  complex |


#### Notes

- For the following data, you can provide either a name or a URI: enclosureGroupName or enclosureGroupUri, osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri, firmwareBaselineName or firmwareBaselineUri (on the firmware), and sasLogicalJBODName or sasLogicalJBODUri (on the sasLogicalJBODs list)

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_profile_facts
Retrieve facts about the OneView Server Profiles.

#### Synopsis
 Retrieve facts about the Server Profile from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Server Profile name.  |
| options  |   No  |  | |  List with options to gather additional facts about Server Profile related resources. Options allowed: `schema`, `compliancePreview`, `profilePorts`, `messages`, `transformation`, `available_networks`, `available_servers`, `available_storage_system`, `available_storage_systems`, `available_targets`  To gather facts about `compliancePreview`, `messages` and `transformation` it is required to inform the Server Profile name. Otherwise, these options will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Server Profiles
  oneview_server_profile_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=server_profiles

- name: Gather paginated, filtered and sorted facts about Server Profiles
  oneview_server_profile_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about a Server Profile by name
  oneview_server_profile_facts:
    config: "{{ config }}"
    name: "WebServer-1"
  delegate_to: localhost

- debug: var=server_profiles


- name: Gather facts about available servers and bays for a given enclosure group and server hardware type
  oneview_server_profile_facts:
    config: "{{ config }}"
    options:
      - availableTargets:
          enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
          serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
  delegate_to: localhost

- debug: var=server_profile_available_targets


- name: Gather all facts about a Server Profile
  oneview_server_profile_facts:
   config: "{{ config }}"
   name : "Encl1, bay 1"
   options:
        - schema
        - compliancePreview
        - profilePorts:
           enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
           serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - messages
        - transformation:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableNetworks:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableServers
        - availableStorageSystem:
            storageSystemId: "{{storage_system_id}}"
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableStorageSystems:
            enclosureGroupUri: '/rest/enclosure-groups/3af25c76-dec7-4753-83f6-e1ad06c29a43'
            serverHardwareTypeUri: '/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226'
        - availableTargets

  delegate_to: localhost

- debug: var=server_profiles
- debug: var=server_profile_schema
- debug: var=server_profile_compliance_preview
- debug: var=server_profile_profile_ports
- debug: var=server_profile_messages
- debug: var=server_profile_transformation
- debug: var=server_profile_available_networks
- debug: var=server_profile_available_servers
- debug: var=server_profile_available_storage_system
- debug: var=server_profile_available_storage_systems
- debug: var=server_profile_available_targets

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile_available_networks   | Has all the facts about the list of Ethernet networks, Fibre Channel networks and network sets that are available to the server profile along with their respective ports. |  When requested, but can be null. |  complex |
| server_profile_available_servers   | Has the facts about the list of available servers. |  When requested, but can be null. |  complex |
| server_profile_available_storage_system   | Has the facts about a specific storage system and its associated volumes that are available to the server profile. |  When requested, but can be null. |  complex |
| server_profile_available_storage_systems   | Has the facts about the list of the storage systems and their associated volumes that are available to the server profile. |  When requested, but can be null. |  complex |
| server_profile_available_targets   | Has the facts about the target servers and empty device bays that are available for assignment to the server profile. |  When requested, but can be null. |  complex |
| server_profile_compliance_preview   | Has all the facts about the manual and automatic updates required to make the server profile compliant with its template. |  When requested, but can be null. |  complex |
| server_profile_messages   | Has the facts about the profile status messages associated with the profile. |  When requested, but can be null. |  complex |
| server_profile_profile_ports   | Has the facts about the port model associated with the profile. |  When requested, but can be null. |  complex |
| server_profile_schema   | Has the facts about the Server Profile schema. |  When requested, but can be null. |  complex |
| server_profile_transformation   | Has the facts about the transformation of an existing profile by supplying a new server hardware type and/or enclosure group. |  When requested, but can be null. |  complex |
| server_profiles   | Has all the OneView facts about the Server Profiles. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_profile_template
Manage OneView Server Profile Template resources.

#### Synopsis
 Provides an interface to create, modify, and delete server profile templates.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  Dict with Server Profile Template properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Server Profile Template. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a basic connection-less server profile template (using URIs)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    delegate_to: localhost

- name: Create a basic connection-less server profile template (using names)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate102"
      serverHardwareTypeName: "BL460c Gen8 1"
      enclosureGroupName: "EGSAS_3"
  delegate_to: localhost

- name: Delete the Server Profile Template
  oneview_server_profile_template:
    config: "{{ config }}"
    state: absent
    data:
      name: "ProfileTemplate101"
    delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile_template   | Has the OneView facts about the Server Profile Template. |  On state 'present'. Can be null. |  complex |


#### Notes

- For the following data, you can provide either a name  or a URI: enclosureGroupName or enclosureGroupUri, osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri, firmwareBaselineName or firmwareBaselineUri (on the firmware), and sasLogicalJBODName or sasLogicalJBODUri (on the sasLogicalJBODs list)

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_server_profile_template_facts
Retrieve facts about the Server Profile Templates from OneView.

#### Synopsis
 Retrieve facts about the Server Profile Templates from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Server Profile Template name.  |
| options  |   No  |  | |  List with options to gather additional facts about Server Profile Template resources. Options allowed: `new_profile` and `transformation`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"

- debug: var=server_profile_templates

- name: Gather paginated, filtered and sorted facts about Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: macType='Virtual'
  delegate_to: localhost

- debug: var=server_profile_templates

- name: Gather facts about a Server Profile Template by name
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    name: "ProfileTemplate101"

- name: Gather facts about a template and a profile with the configuration based on this template
  oneview_server_profile_template_facts:
    config: "{{ config }}"
    name: "ProfileTemplate101"
    options:
      - new_profile

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| new_profile   | A profile object with the configuration based on this template. |  When requested, but can be null. |  complex |
| server_profile_templates   | Has all the OneView facts about the Server Profile Templates. |  Always, but can be null. |  complex |


#### Notes

- The option `transformation` is only available for API version 300 or later.

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_pool
Manage OneView Storage Pool resources.

#### Synopsis
 Provides an interface to manage Storage Pool resources. Can add and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Storage Pool properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Pool resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |


 
#### Examples

```yaml
- name: Create a Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: "FST_CPG2"
  delegate_to: localhost

- name: Delete the Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: absent
    data:
       poolName: "FST_CPG2"
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pool   | Has the OneView facts about the Storage Pool. |  On 'present' state, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_pool_facts
Retrieve facts about one or more Storage Pools.

#### Synopsis
 Retrieve facts about one or more of the Storage Pools from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Storage Pool name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_pools

- name: Gather paginated, filtered and sorted facts about Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_pools

- name: Gather facts about a Storage Pool by name
  oneview_storage_pool_facts:
    config: "{{ config }}"
    name: "CPG_FC-AO"
  delegate_to: localhost

- debug: var=storage_pools

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pools   | Has all the OneView facts about the Storage Pools. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_system
Manage OneView Storage System resources.

#### Synopsis
 Provides an interface to manage Storage System resources. Can add, update and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Storage System properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage System resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Storage System with one managed pool
  oneview_storage_system:
    config: "{{ config }}"
    state: present
    data:
        credentials:
            ip_hostname: '{{ storage_system_ip_hostname }}'
            username: '{{ storage_system_username }}'
            password: '{{ storage_system_password }}'
        managedDomain: TestDomain
        managedPools:
          - domain: TestDomain
            type: StoragePoolV2
            name: CPG_FC-AO
            deviceType: FC

  delegate_to: localhost

- name: Remove the storage system by its IP
  oneview_storage_system:
    config: "{{ config }}"
    state: absent
    data:
        credentials:
            ip_hostname: 172.18.11.12
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system   | Has the OneView facts about the Storage System. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_system_facts
Retrieve facts about the OneView Storage Systems.

#### Synopsis
 Retrieve facts about the Storage Systems from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| ip_hostname  |   No  |  | |  Storage System IP or hostname.  |
| name  |   No  |  | |  Storage System name.  |
| options  |   No  |  | |  List with options to gather additional facts about a Storage System and related resources. Options allowed: `hostTypes` gets the list of supported host types. `storagePools` gets a list of storage pools belonging to the specified storage system.  To gather facts about `storagePools` it is required to inform either the argument `name` or `ip_hostname`. Otherwise, this option will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather paginated, filtered and sorted facts about Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: managedDomain=TestDomain

- debug: var=storage_systems

- name: Gather facts about a Storage System by IP
  oneview_storage_system_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_systems


- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_systems

- name: Gather facts about a Storage System and all options
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
    options:
        - hostTypes
        - storagePools
  delegate_to: localhost

- debug: var=storage_systems
- debug: var=storage_system_host_types
- debug: var=storage_system_pools


```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system_host_types   | Has all the OneView facts about the supported host types. |  When requested, but can be null. |  complex |
| storage_system_pools   | Has all the OneView facts about the Storage Systems - Storage Pools. |  When requested, but can be null. |  complex |
| storage_systems   | Has all the OneView facts about the Storage Systems. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_volume_attachment
Provides an interface to remove extra presentations from a specified server profile.

#### Synopsis
 Provides an interface to remove extra presentations from a specified server profile.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| server_profile  |   Yes  |  | |  Server Profile name or Server Profile URI  |
| state  |   Yes  |  | <ul> <li>extra_presentations_removed</li> </ul> |  Indicates the desired state for the Storage Volume Attachment `extra_presentations_removed` will remove extra presentations from a specified server profile.  |


 
#### Examples

```yaml
- name: Removes extra presentations from a specified server profile URI
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
  delegate_to: localhost

- debug: var=server_profile


- name: Removes extra presentations from a specified server profile name
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "SV-1001"
  delegate_to: localhost

- debug: var=server_profile

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile   | Has all the OneView facts about the repaired Server Profile. |  Always. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_volume_attachment_facts
Retrieve facts about the OneView Storage Volume Attachments.

#### Synopsis
 Retrieve facts about the OneView Storage Volume Attachments. To gather facts about a specific Storage Volume Attachment it is required to inform the option _storageVolumeAttachmentUri_. It is also possible to retrieve a specific Storage Volume Attachment by the Server Profile and the Volume. For this option, it is required to inform the option _serverProfileName_ and the param _storageVolumeName_ or _storageVolumeUri_.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: `extraUnmanagedStorageVolumes` retrieve the list of extra unmanaged storage volumes. `paths` retrieve all paths or a specific attachment path for the specified volume attachment. To retrieve a specific path a `pathUri` or a `pathId` must be informed  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| serverProfileName  |   No  |  | |  Server Profile name.  |
| storageVolumeAttachmentUri  |   No  |  | |  Storage Volume Attachment uri.  |
| storageVolumeName  |   No  |  | |  Storage Volume name.  |
| storageVolumeUri  |   No  |  | |  Storage Volume uri.  |


 
#### Examples

```yaml
- name: Gather facts about all Storage Volume Attachments
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_volume_attachments

- name: Gather paginated, filtered and sorted facts about Storage Volume Attachments
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "storageVolumeUri='/rest/storage-volumes/E5B84BC8-75CF-4305-8DB5-7585A2979351'"

- debug: var=storage_volume_attachments

- name: Gather facts about a Storage Volume Attachment by Server Profile and Volume
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeName: "volume-test" # You could inform either the volume name or the volume uri
    # storageVolumeUri: "volume-test"
  delegate_to: localhost

- debug: var=storage_volume_attachments


- name: Gather facts about extra unmanaged storage volumes
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    options:
      - extraUnmanagedStorageVolumes:
            start: 0     # optional
            count: '-1'  # optional
            filter: ''   # optional
            sort: ''     # optional
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=extra_unmanaged_storage_volumes

- name: Gather facts about all paths for the specified volume attachment
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeUri: "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"
    options:
      - paths
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=storage_volume_attachment_paths

- name: Gather facts about a specific attachment path
  oneview_storage_volume_attachment_facts:
    config: "{{ config }}"
    serverProfileName: "sp-web"
    storageVolumeUri: "/rest/storage-volumes/12345-AAA-BBBB-CCCC-121212AA"
    options:
      - paths:
            # You could inform either the path id or the path uri
            pathId: '9DFC8953-15A4-4EA9-AB65-23AB12AB23' # optional
            # pathUri: '/rest/storage-volume-attachments/123-123-123/paths/123-123-123'
  delegate_to: localhost

- debug: var=storage_volume_attachments
- debug: var=storage_volume_attachment_paths

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| extra_unmanaged_storage_volumes   | Has facts about the extra unmanaged storage volumes. |  When requested, but can be null. |  complex |
| storage_volume_attachment_paths   | Has facts about all paths or a specific attachment path for the specified volume attachment. |  When requested, but can be null. |  complex |
| storage_volume_attachments   | Has all the OneView facts about the Storage Volume Attachments. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_volume_template
Manage OneView Storage Volume Template resources.

#### Synopsis
 Provides an interface to manage Storage Volume Template resources. Can create, update and delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Storage Volume Template properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Volume Template resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Create a Storage Volume Template
  oneview_storage_volume_template:
    config: "{{ config }}"
    state: present
    data:
        name: 'Volume Template Name'
        state: "Configured"
        description: "Example Template"
        provisioning:
             shareable: true
             provisionType: "Thin"
             capacity: "235834383322"
             storagePoolUri: "/rest/storage-pools/2D69A182-862E-4ECE-8BEE-73E0F5BEC855"
        stateReason: "None"
        storageSystemUri: "/rest/storage-systems/TXQ1010307"
        snapshotPoolUri: "/rest/storage-pools/2D69A182-862E-4ECE-8BEE-73E0F5BEC855"
        type: StorageVolumeTemplateV3
  delegate_to: localhost


- name: Delete the Storage Volume Template
  oneview_storage_volume_template:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Volume Template Name'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume_template   | Has the OneView facts about the Storage Volume Template. |  On 'present' state, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_storage_volume_template_facts
Retrieve facts about Storage Volume Templates of the OneView.

#### Synopsis
 Retrieve facts about Storage Volume Templates of the OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Storage Volume Template name.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: `connectableVolumeTemplates`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_volume_templates

- name: Gather paginated, filtered and sorted facts about Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_volume_templates

- name: Gather facts about a Storage Volume Template by name
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
  delegate_to: localhost

- debug: var=storage_volume_templates


- name: Gather facts about the connectable Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
    options:
      - connectableVolumeTemplates
  delegate_to: localhost

- debug: var=storage_volume_templates
- debug: var=connectable_volume_templates

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connectable_volume_templates   | Has facts about the Connectable Storage Volume Templates. |  When requested, but can be null. |  complex |
| storage_volume_templates   | Has all the OneView facts about the Storage Volume Templates. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_switch
Provides an interface to remove ToR Switch resources.

#### Synopsis
 Provides an interface to remove Top of Rack(ToR) Switch resources. The switch resource will be removed if it is in an unmanaged state. If the switch resource is associated with a Logical Switch, it's removal is treated as a hardware removal only. A reference to the switch is mantained, and the resource is marked as 'Absent'.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   Yes  |  | |  Switch name.  |
| state  |   |  | <ul> <li>absent</li>  <li>ports_updated</li> </ul> |  Indicates the desired state for the Switch resource. `absent` will remove the resource from OneView, if it exists. `ports_updated` will update the switch ports.  |


 
#### Examples

```yaml
- name: Delete the Switch
  oneview_switch:
    config: "{{ config }}"
    state: absent
    name: "172.18.16.2"

```



#### Notes

- This resource is only available on C7000 enclosures

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_switch_facts
Retrieve facts about the OneView Switches.

#### Synopsis
 Retrieve facts about the OneView Switches.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Switch name.  |
| options  |   No  |  | |  List with options to gather additional facts about the Switch. Options allowed: 'environmentalConfiguration' gets the environmental configuration for a switch.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all switches
  oneview_switch_facts:
    config: "{{ config }}"

- name: Gather paginated facts about switches
  oneview_switch_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3

- debug: var=switches

- name: Gather facts about the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"

- name: Gather facts about the environmental configuration for the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"
  options:
    - environmentalConfiguration

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| switch_environmental_configuration   | The environmental configuration for a switch. |  When requested, but can be null. |  complex |
| switches   | The list of switches. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- This resource is only available on C7000 enclosures


---


## oneview_switch_type_facts
Retrieve facts about the OneView Switch Types.

#### Synopsis
 Retrieve facts about the Switch Types from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Switch Type.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Switch Types
  oneview_switch_type_facts:
    config: "{{ config_path }}"

- debug: var=switch_types

- name: Gather paginated, filtered and sorted facts about Switch Types
  oneview_switch_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "partNumber='N5K-C56XX'"

- debug: var=switch_types

- name: Gather facts about a Switch Type by name
  oneview_switch_type_facts:
    config: "{{ config_path }}"
    name: "Name of the Switch Type"

- debug: var=switch_types

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| switch_types   | Has all the OneView facts about the Switch Types. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_task_facts
Retrieve facts about the OneView Tasks.

#### Synopsis
 Retrieve facts about the OneView Tasks.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |   No  |  | |  List with parameters to help filter the tasks. Params allowed: count, fields, filter, query, sort, start, and view.  |


 
#### Examples

```yaml
- name: Gather facts about the last 2 tasks
  oneview_task_facts:
    config: "{{ config }}"
    params:
      count: 2

- debug: var=tasks

- name: Gather facts about the last 2 tasks associated to Server Profile templates
  oneview_task_facts:
    config: "{{ config }}"
    params:
      count: 2
      filter: "associatedResource.resourceCategory='server-profile-templates'"

- debug: var=tasks

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| tasks   | The list of tasks. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## oneview_unmanaged_device
Manage OneView Unmanaged Device resources.

#### Synopsis
 Provides an interface to manage Unmanaged Device resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Unmanaged Device properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Unmanaged Device resource. 'present' will ensure data properties are compliant with OneView. 'absent' will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the unmanaged device is present
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      model: 'Procurve 4200VL'
      deviceType: 'Server'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Add another unmanaged device
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'AnotherUnmanagedDevice'
      model: 'Procurve 4200VL'
    delegate_to: localhost

- name: Update the unmanaged device changing the name attribute
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      newName: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Ensure that the unmanaged device is absent
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      name: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- name: Delete all the unmanaged devices
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      filter: "name matches '%'"
    delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| unmanaged_device   | Has the OneView facts about the Unmanaged Device. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- To rename an unamnaged device you must inform a 'newName' in the data argument. The rename is non-idempotent


---


## oneview_unmanaged_device_facts
Retrieve facts about one or more of the OneView Unmanaged Device.

#### Synopsis
 Retrieve facts about one or more of the Unmanaged Device from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Unmanaged Device name.  |
| options  |   |  | |  List with options to gather additional facts about the Unmanaged Device. Options allowed: 'environmental_configuration' gets a description of the environmental configuration for the Unmnaged Device.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: 'start': The first item to return, using 0-based indexing. 'count': The number of resources to return. 'filter': A general filter/query string to narrow the list of items returned. 'sort': The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Unmanaged Devices
  oneview_unmanaged_device_facts:
    config: "{{ config }}"

- debug: var=unmanaged_devices

- name: Gather paginated, filtered and sorted facts about Unmanaged Devices
  oneview_unmanaged_device_facts:
  config: "{{ config }}"
  params:
    start: 0
    count: 2
    sort: 'name:descending'
    filter: "status='Disabled'"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name with environmental configuration
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - environmental_configuration

- debug: var=unmanaged_device_environmental_configuration

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| unmanaged_device_environmental_configuration   | The description of the environmental configuration for the logical interconnect. |  When requested, but can be null. |  complex |
| unmanaged_devices   | The list of unmanaged devices. |  Always, but can be null. |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables


---


## oneview_uplink_set
Manage OneView Uplink Set resources.

#### Synopsis
 Provides an interface to manage Uplink Set resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 3.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Uplink Set properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Uplink Set resource. 'present' will ensure data properties are compliant with OneView. 'absent' will remove the resource from OneView, if it exists. The key used to find the resource to perform the operation is a compound key, that consists of the name of the uplink set and the URI (or name) of the Logical Interconnect combined. You can choose to set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
- name: Ensure that the Uplink Set is present
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Uplink Set'
      status: "OK"
      # You can choose set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName
      logicalInterconnectName: "Name of the Logical Interconnect"                                   # option 1
      # logicalInterconnectUri: "/rest/logical-interconnects/461a9cef-beef-4916-8be1-926078ffb948"  # option 2
      networkUris: [
         '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
         '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
      ]
      fcNetworkUris: []
      fcoeNetworkUris: []
      portConfigInfos: []
      connectionMode: "Auto"
      networkType: "Ethernet"
      manualLoginRedistributionState: "NotSupported"

- name: Rename the Uplink Set from 'Test Uplink Set' to 'Renamed Uplink Set'
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Uplink Set'
      newName: 'Renamed Uplink Set'
      logicalInterconnectName: "Name of the Logical Interconnect"

- name: Ensure that the Uplink Set is absent
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test Uplink Set'
      logicalInterconnectName: "Name of the Logical Interconnect"

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| uplink_set   | Has the OneView facts about the Uplink Set. |  On state 'present'. Can be null. |  complex |


#### Notes

- To rename an uplink set you must inform a 'newName' in the data argument. The rename is non-idempotent

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_uplink_set_facts
Retrieve facts about one or more of the OneView Uplink Sets.

#### Synopsis
 Retrieve facts about one or more of the Uplink Sets from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Uplink Set name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Uplink Sets
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"

- debug: var=uplink_sets

- name: Gather paginated, filtered and sorted facts about Uplink Sets
  oneview_uplink_set_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "logicalInterconnectUri='/rest/logical-interconnects/4a49ca0d-3782-4c11-b93e-79d8f90c5487'"

- debug: var=uplink_sets

- name: Gather facts about a Uplink Set by name
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=uplink_sets

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| uplink_sets   | Has all the OneView facts about the Uplink Sets. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_volume
Manage OneView Volume resources.

#### Synopsis
 Provides an interface to manage Volume resources. It allows create, update, delete or repair the volume, and create or delete a snapshot.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  Volume or snapshot data.  |
| export_only  |   |  False  | |  If set to True, when the status is `absent` and the resource exists, it will be removed only from OneView.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>repaired</li>  <li>snapshot_created</li>  <li>snapshot_deleted</li> </ul> |  Indicates the desired state for the Volume resource. `present` creates/adds the resource when it does not exist, otherwise it updates the resource. When the resource already exists, the update operation is non-idempotent, since it is always called even though the given options are compliant with the existent data. To change the name of the volume, a `newName` in the _data_ must be provided. `absent` by default deletes a volume from OneView and the storage system. When export_only is True, the volume is removed only from OneView. `repaired` removes extra presentations from a specified volume on the storage system. This operation is non-idempotent. `snapshot_created` creates a snapshot for the volume specified. This operation is non-idempotent. `snapshot_deleted` deletes a snapshot from OneView and the storage system.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


 
#### Examples

```yaml
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

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume   | Has the facts about the Storage Volume. |  On state 'present', but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---


## oneview_volume_facts
Retrieve facts about the OneView Volumes.

#### Synopsis
 Retrieve facts about the Volumes from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView >= 2.0.1

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Volume name.  |
| options  |   No  |  | |  List with options to gather additional facts about Volume and related resources. Options allowed: `attachableVolumes`, `extraManagedVolumePaths`, and `snapshots`. For the option `snapshots`, you may provide a name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


 
#### Examples

```yaml
- name: Gather facts about all Volumes
  oneview_volume_facts:
    config: "{{ config_path }}"

- debug: var=storage_volumes

- name: Gather paginated, filtered and sorted facts about Volumes
  oneview_volume_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "provisionType='Thin'"

- debug: var=storage_volumes

- name: "Gather facts about all Volumes, the attachable volumes managed by the appliance and the extra managed
         storage volume paths"
  oneview_volume_facts:
    config: "{{ config_path }}"
    options:
        - attachableVolumes        # optional
        - extraManagedVolumePaths  # optional

- debug: var=storage_volumes
- debug: var=attachable_volumes
- debug: var=extra_managed_volume_paths


- name: Gather facts about a Volume by name with a list of all snapshots taken
  oneview_volume_facts:
    config: "{{ config }}"
    name: "{{ volume_name }}"
    options:
        - snapshots  # optional

- debug: var=storage_volumes
- debug: var=snapshots


- name: "Gather facts about a Volume with one specific snapshot taken"
  oneview_volume_facts:
    config: "{{ config }}"
    name: "{{ volume_name }}"
    options:
       - snapshots:  # optional
           name: "{{ snapshot_name }}"

- debug: var=storage_volumes
- debug: var=snapshots

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| attachable_volumes   | Has all the facts about the attachable volumes managed by the appliance. |  When requested, but can be null. |  complex |
| extra_managed_volume_paths   | Has all the facts about the extra managed storage volume paths from the appliance. |  When requested, but can be null. |  complex |
| storage_volumes   | Has all the OneView facts about the Volumes. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json

- Check how to use environment variables for configuration at: https://github.com/HewlettPackard/oneview-ansible#environment-variables

- Additional Playbooks for the HPE OneView Ansible modules can be found at: https://github.com/HewlettPackard/oneview-ansible/tree/master/examples


---

