# Ansible Modules for HPE OneView Change Log
## v6.0.0(unreleased)
This release extends the planned support of the modules to OneView REST API version 2600 (OneView v6.0)

### Modules supported in this release
- oneview_id_pools_ipv4_subnets
- oneview_id_pools_ipv4_subnets_facts

## v6.0.0 (unreleased)
This release extends the planned support of the modules to OneView REST API version 2600 (OneView v6.0).

### Modules supported in this release
- oneview_appliance_configuration_timeconfig_facts
- oneview_appliance_device_snmpv1_trap_destions
- oneview_appliance_device_snmpv1_trap_destions_facts
- oneview_appliance_device_snmpv3_trap_destions
- oneview_appliance_device_snmpv3_trap_destions_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts
- oneview_appliance_ssh_access
- oneview_appliance_ssh_access_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_id_pools_ipv4_range
- oneview_id_pools_ipv4_range_facts

#### Bug fixes & Enhancements
- [#633] (https://github.com/HewlettPackard/oneview-ansible/issues/633) Internal network in LogicalInterconnectGroup

## v5.10.0
This release extends the planned support of the modules to OneView REST API version 2400 (OneView v5.6).

#### Major changes
1. Achieved idempotency for below resources.
   - Logical Interconnect Group
   - Scope
   - Server Profile
   - Server Profile Template
 
2. Added support for 4 new endpoints in oneview_logical_interconnect and oneview_logical_interconnect_facts resource.
   - POST /rest/logical-interconnects/bulk-inconsistency-validation
   - GET /rest/logical-interconnects/{id}/igmpSettings
   - PUT /rest/logical-interconnects/{id}/igmpSettings
   - PUT /rest/logical-interconnects/{id}/portFlapSettings

#### Bug fixes & Enhancements
- [#597] (https://github.com/HewlettPackard/oneview-ansible/issues/597) Rack rename do not work.
- [#594] (https://github.com/HewlettPackard/oneview-ansible/issues/594) Updated library file for LIG Uplink Set Issue
- [#599] (https://github.com/HewlettPackard/oneview-ansible/issues/599) Server maintenance mode.
- [#609] (https://github.com/HewlettPackard/oneview-ansible/issues/609) Enclosure Group creation using an address pool for interconnect configuration
- [#611] (https://github.com/HewlettPackard/oneview-ansible/issues/611) IPv4 range creation fails with "Invalid Pool Range IPv4"
- [#612] (https://github.com/HewlettPackard/oneview-ansible/issues/612) FC network bandwidth
- [#614] (https://github.com/HewlettPackard/oneview-ansible/issues/614) Typo in oneview_server_profile_template_with_resource_name.yml
- [#620] (https://github.com/HewlettPackard/oneview-ansible/issues/620) git installed ansible oneview container image.
- [#622] (https://github.com/HewlettPackard/oneview-ansible/issues/622) Updating LIG with network set uri with mentioning networkset names.
- [#624] (https://github.com/HewlettPackard/oneview-ansible/issues/624) Assign static MAC address from pool ID in SP template creation.

### Modules supported in this release
- oneview_alert_facts
- oneview_appliance_device_read_community
- oneview_appliance_device_read_community_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_interconnect_link_topology_facts
- oneview_internal_link_set_facts
- oneview_logical_downlink_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_login_detail_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_switch_type_facts
- oneview_task_facts
- oneview_unmanaged_device
- oneview_unmanaged_device_facts
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_version_facts

## v5.9.0
This release extends the planned support of the modules to OneView REST API version 2200 (OneView v5.5) and ImageStreamer REST API version 2000 (I3S v5.4)

#### Bug fixes & Enhancements
- [#581] (https://github.com/HewlettPackard/oneview-ansible/issues/581) Updating single uplinkSet in LIG removes other uplinkSet.
- [#582] (https://github.com/HewlettPackard/oneview-ansible/issues/582) description field is empty after server profile creation.

### Modules supported in this release
- image_streamer_artifact_bundle
- image_streamer_artifact_bundle_facts
- image_streamer_build_plan
- image_streamer_build_plan_facts
- image_streamer_deployment_group_facts
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts
- image_streamer_golden_image
- image_streamer_golden_image_facts
- image_streamer_os_volume_facts
- image_streamer_plan_script
- image_streamer_plan_script_facts
- oneview_alert_facts.yml
- oneview_appliance_device_read_community.yml
- oneview_appliance_device_read_community_facts.yml
- oneview_appliance_time_and_locale_configuration.yml
- oneview_appliance_time_and_locale_configuration_facts.yml
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_interconnect_link_topology_facts.yml
- oneview_internal_link_set_facts.yml
- oneview_logical_downlink_facts.yml
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_login_detail_facts.yml
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts.yml
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_switch_type_facts.yml
- oneview_task_facts
- oneview_unmanaged_device.yml
- oneview_unmanaged_device_facts.yml
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_version_facts

## v5.8.0
This release extends the planned support of the modules to OneView REST API version 2000 (OneView v5.4)

#### Breaking Changes
- Enhancement made in this version breaks the previous version of the SDK.
- From this version onwards, oneview-ansible library refers to hpeOneView module.

#### Major changes
- Added support for automatic publish of Docker Image when there is a new release in GitHub

#### Bug fixes & Enhancements
- [#565] (https://github.com/HewlettPackard/oneview-ansible/issues/565) Problem creating / changing a network_set
- [#559] (https://github.com/HewlettPackard/oneview-ansible/issues/559) Unable to delete rack resources

### Modules supported in this release
- oneview_alert_facts.yml
- oneview_appliance_device_read_community.yml
- oneview_appliance_device_read_community_facts.yml
- oneview_appliance_time_and_locale_configuration.yml
- oneview_appliance_time_and_locale_configuration_facts.yml
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_interconnect_link_topology_facts.yml
- oneview_internal_link_set_facts.yml
- oneview_logical_downlink_facts.yml
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_login_detail_facts.yml
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts.yml
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_switch_type_facts.yml
- oneview_task_facts
- oneview_unmanaged_device.yml
- oneview_unmanaged_device_facts.yml
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_version_facts

## v5.7.0

This release extends the planned support of the modules to OneView REST API version 1800 (OneView v5.3)

### Modules supported in this release
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts

## v5.6.1
Added 'dict_merge' method in oneview library to merge nested dictionaries and lists and avoid idempotency issues.

#### Bug fixes & Enhancements
- [#171](https://github.com/HewlettPackard/oneview-ansible/issues/171) oneview_server_profile doesn't appear to be idempotent
- [#311](https://github.com/HewlettPackard/oneview-ansible/issues/311) Module oneview_storage_system_facts examples and documentation contains old/incorrect parameter "ip_hostname"
- [#341](https://github.com/HewlettPackard/oneview-ansible/issues/341) Logical_Interconnect_Group Module , idempotency , Uplinksets for Synergy.
- [#342](https://github.com/HewlettPackard/oneview-ansible/issues/532) Re-Running Server Profile Creation(including OS Deployment via Image Streamer) updates Server Profile over and over.
- [#358](https://github.com/HewlettPackard/oneview-ansible/issues/358) oneview_rack task overwriting other rack mounts
- [#370](https://github.com/HewlettPackard/oneview-ansible/issues/370) oneview_logical_interconnect_group doesn't support network names.
- [#380](https://github.com/HewlettPackard/oneview-ansible/issues/380) oneview_network_set does not support bandwidth and untagged network
- [#397](https://github.com/HewlettPackard/oneview-ansible/issues/397) oneview_network_set does not support clearing the nativeNetworkUri.
- [#451](https://github.com/HewlettPackard/oneview-ansible/issues/451) auto_assign_server_hardware does not work with DLs
- [#456](https://github.com/HewlettPackard/oneview-ansible/issues/456) oneview_storage_system - How to assign Ports to Networks?
- [#469](https://github.com/HewlettPackard/oneview-ansible/issues/469) module: ov_server_profile auto_assign_hw with scoped user
- [#481](https://github.com/HewlettPackard/oneview-ansible/issues/481) oneview_volume is not idempotent
- [#487](https://github.com/HewlettPackard/oneview-ansible/issues/487) Fails Server profile update in case of existing network_set
- [#496](https://github.com/HewlettPackard/oneview-ansible/issues/496) Feature: Check Mode.
- [#510](https://github.com/HewlettPackard/oneview-ansible/issues/510) Ensure users are aware of how to secure oneview credentials.
- [#525](https://github.com/HewlettPackard/oneview-ansible/issues/525) Server Hardware Facts - Extract the Server Hardware Details by URI.
- [#532](https://github.com/HewlettPackard/oneview-ansible/issues/532) Add multiple servers method in server hardware module returns invalid response.
- [#550](https://github.com/HewlettPackard/oneview-ansible/issues/550) Failed to delete last sasJBOD connection in server profile


## v5.6.0

Extends support of the SDK to OneView REST API version 1600 (OneView v5.20).

Added usecases for the following scenarios
  1. Infrastructure provisioning with OS on Synergy with Image Streamer and having NIC connections.
  2. Server Profile creation with network connections using profile template and power it on.
  3. Cleanup activity which includes power off the server hardware, delete the profile and template.

### Modules supported in this release
- image_streamer_artifact_bundle
- image_streamer_artifact_bundle_facts
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts

#### Bug fixes & Enhancements
- [#489](https://github.com/HewlettPackard/oneview-ansible/issues/489) Server Profile - create operation fails with an error -Value specified for enclosure is not valid or not supported

## v5.5.0
This release extends the planned support of the modules to OneView REST API version 800 (OneView v4.1), 1000 (OneView v4.2) and 1200 (OneView v5.0).

#### Major changes
1. Extended support of planned modules to API800/1000/1200.
2. Modules implemented in this release requires hpOneView version 5.1.1.

#### Modules supported in this release
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_server_hardware
- oneview_server_hardware_facts

## v5.4.0
This release extends the planned support of the modules to OneView REST API version 800 (OneView v4.1), 1000 (OneView v4.2) and 1200 (OneView v5.0).

#### Major changes
1. Extended support of planned modules to API800/1000/1200.
2. Modules upgraded in this release requires hpOneView version 5.0.0. Also, OneView Python library is now migrated to new repository which is available at https://github.com/HewlettPackard/oneview-python.

#### Modules supported in this release
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosure
- oneview_logical_enclosure_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts

## v5.3.1

This release is to support resource name instead of resource URIs in server profile and profile template.

#### Major changes
 1. Updated ReplaceServerProfileNamebyUris class to support the schema changes in latest API version.
 2. Added an end-to-end example playbook for server profile template with the below resources
    - enclosure group
    - server hardware type
    - server profile name
    - ethernet network
    - fc network
    - volume storage system
    - os deployment plan
    - storage pool
    - volme template
    - firmware baseline

#### Example playbook added
- oneview_server_profile_template_with_resource_name

## v5.3.0

This release extends the planned support of the modules to OneView REST API version 800 (OneView v4.1).

#### Major changes
1. Extended support of planned modules to API800.
2. Updated library files to support Python SDK changes.
3. Modules upgraded in this release requires hpOneView version 5.0.0b0 or above.

#### Modules supported in this release
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_internal_link_set_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosure
- oneview_logical_enclosure_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_logical_switch_group
- oneview_logical_switch_group_facts
- oneview_managed_san
- oneview_managed_san_facts
- oneview_sas_interconnect
- oneview_sas_interconnect_facts
- oneview_sas_interconnect_type_facts
- oneview_sas_logical_interconnect
- oneview_sas_logical_interconnect_facts
- oneview_sas_logical_interconnect_group
- oneview_sas_logical_interconnect_group_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_switch_type_facts

## v5.2.0

#### Notes
Added the capability to handle OneView Appliance SNMP Settings
This release adds the [endpoints-support.md](endpoints-support.md) file.
This release extends the planned support for the OneView REST API v800

#### Modules added
- oneview_appliance_device_read_community
- oneview_appliance_device_read_community_facts
- oneview_appliance_device_snmp_v1_trap_destinations
- oneview_appliance_device_snmp_v1_trap_destinations_facts
- oneview_appliance_device_snmp_v3_trap_destinations
- oneview_appliance_device_snmp_v3_trap_destinations_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts

#### Big fixes
- [#392](https://github.com/HewlettPackard/oneview-ansible/issues/392) Use networkName field for SP with API600

#### Big fixes
- [#392](https://github.com/HewlettPackard/oneview-ansible/issues/392) Use networkName field for SP with API600

## v5.1.1

This release extends the planned support for the OneView REST API v600

#### Modules supported
- oneview_alert_facts

## v5.1.0

This release achieves the planned support for the OneView REST API v600 and HPE Image Streamer.

#### Major changes
 1. Extended support of HPE Image Streamer to API500 and API600.
 2. Extended support of planned modules to API600

## v5.0.0

This release adds the [TESTING.md](TESTING.md) document.

#### Major changes
 1. Extended support of most modules to API600.

#### Modules added
- oneview_login_detail_facts
- oneview_version_facts

#### Breaking changes
1. On the modules setup instructions, the requirement of setting up a PYTHONPATH environment variable is being dropped and replaced by the setup of the ANSIBLE_MODULE_UTILS environment variable.
2. Updating unittest with pytest in all the test cases as per Ansible core library.

#### Bug fixes & Enhancements
- [#172](https://github.com/HewlettPackard/oneview-ansible/issues/172) Allow credentials to be defined inside the playbooks
- [#273](https://github.com/HewlettPackard/oneview-ansible/issues/273) Investigate probably unused AnsibleModule imports
- [#282](https://github.com/HewlettPackard/oneview-ansible/issues/282) Updating a Server Profile causes Server Hardware reboots for operations which do not require it
- [#285](https://github.com/HewlettPackard/oneview-ansible/issues/285) Modules cannot unassign a Server Hardware or create SP with unassigned SH
- [#288](https://github.com/HewlettPackard/oneview-ansible/issues/288) Adding osCustomAttributes to a SP which had none before results in failure
- [#290](https://github.com/HewlettPackard/oneview-ansible/issues/290) Issue with filter on oneview_server_profile_facts
- [#297](https://github.com/HewlettPackard/oneview-ansible/issues/297) Allow specifying a custom path for the module_utils

## v4.0.0

This release extends the planned support of the module to OneView REST API version 500 (OneView v3.10).

#### Major changes
 1. Extended support of most modules to API500.
 2. Added CHANGELOG and officially adopted Semantic Versioning for the repository.
 3. Updated example files for most resources for improved readability and usability.

## v3.1.1

Minor changes and bug fixes.

## v3.1.0

This release adds new resource modules and achieves the planned support for the OneView REST API v300 and HPE Image Streamer.

#### Modules added
- image_streamer_artifact_bundle
- image_streamer_artifact_bundle_facts
- image_streamer_deployment_group_facts
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts

## v3.0.0
#### Major changes
1. Added support for OneView 3.0 and HPE Synergy resources
2. Added support for the OneView REST API v300
3. Enhancements to ICsP modules
4. Added partial support for HPE Synergy Image Streamer

#### Modules added
- hpe_icsp_os_deployment
- hpe_icsp_server
- image_streamer_artifact_bundle_facts
- image_streamer_build_plan
- image_streamer_build_plan_facts
- image_streamer_golden_image
- image_streamer_golden_image_facts
- image_streamer_os_volume_facts
- image_streamer_plan_script
- image_streamer_plan_script_facts
- oneview_alert_facts
- oneview_drive_enclosure
- oneview_drive_enclosure_facts
- oneview_os_deployment_plan_facts
- oneview_sas_interconnect
- oneview_sas_interconnect_facts
- oneview_sas_interconnect_type_facts
- oneview_sas_logical_interconnect
- oneview_sas_logical_interconnect_facts
- oneview_sas_logical_interconnect_group
- oneview_sas_logical_interconnect_group_facts
- oneview_sas_logical_jbod_attachment_facts
- oneview_sas_logical_jbod_facts
- oneview_scope
- oneview_scope_facts

## v2.0.0

This release adds new resource modules and achieves the planned support for the OneView REST API on version 120 and 200, on OneView appliances with versions 2.00.00.

#### Modules added
- oneview_datacenter.yml
- oneview_datacenter_facts.yml
- oneview_managed_san.yml
- oneview_managed_san_facts.yml
- oneview_server_hardware_type.yml
- oneview_server_hardware_type_facts.yml
- oneview_storage_volume_attachment.yml
- oneview_storage_volume_attachment_facts.yml
- oneview_unmanaged_device.yml
- oneview_unmanaged_device_facts.yml

## v1.0.0 (Beta)
Initial release of the OneView modules for Ansible. It adds support to managing core features of OneView through the addition of the modules listed bellow.
This version of the module supports OneView appliances with versions 2.00.00 or higher, using the OneView REST API version 120 or 200.

#### Modules added
- hpe_icsp
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fabric_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_firmware_bundle
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_downlinks_facts
- oneview_logical_enclosure
- oneview_logical_enclosure_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_logical_switch
- oneview_logical_switch_facts
- oneview_logical_switch_group
- oneview_logical_switch_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_power_device
- oneview_power_device_facts
- oneview_rack
- oneview_rack_facts
- oneview_san_manager
- oneview_san_manager_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_switch
- oneview_switch_type_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_volume
- oneview_volume_facts
