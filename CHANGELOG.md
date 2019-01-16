# Ansible Modules for HPE OneView Change Log

## v5.2.0 (Unreleased)

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
