# Ansible HPE OneView Modules

### Modules

  * [hpe_icsp - Deploy the operating system on a server using HPE ICsp.](#hpe_icsp)
  * [oneview_enclosure - Manage OneView Enclosure resources.](#oneview_enclosure)
  * [oneview_enclosure_env_config_facts - Retrieve the facts about the environmental configuration of one enclosure.](#oneview_enclosure_env_config_facts)
  * [oneview_enclosure_facts - Retrieve facts about one or more Enclosures.](#oneview_enclosure_facts)
  * [oneview_enclosure_group - Manage OneView Enclosure Group resources.](#oneview_enclosure_group)
  * [oneview_enclosure_group_facts - Retrieve facts about one or more of the OneView Enclosure Groups.](#oneview_enclosure_group_facts)
  * [oneview_enclosure_group_script_facts - Retrieve the configuration script associated with a OneView Enclosure Group.](#oneview_enclosure_group_script_facts)
  * [oneview_enclosure_script_facts - Retrieve facts about the script of one enclosure.](#oneview_enclosure_script_facts)
  * [oneview_enclosure_utilization_facts - Retrieve the facts about the utilization of one enclosure.](#oneview_enclosure_utilization_facts)
  * [oneview_ethernet_network - Manage OneView Ethernet Network resources.](#oneview_ethernet_network)
  * [oneview_ethernet_network_associated_profile_facts - Retrieve the facts about the profiles which are using an Ethernet network.](#oneview_ethernet_network_associated_profile_facts)
  * [oneview_ethernet_network_associated_uplink_group_facts - Gather facts about the uplink sets which are using an Ethernet network.](#oneview_ethernet_network_associated_uplink_group_facts)
  * [oneview_ethernet_network_facts - Retrieve the facts about one or more of the OneView Ethernet Networks.](#oneview_ethernet_network_facts)
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
  * [oneview_interconnect_statistics_facts - Retrieve the statistics facts about one interconnect from OneView.](#oneview_interconnect_statistics_facts)
  * [oneview_interconnect_type_facts - Retrieve facts about one or more of the OneView Interconnect Types.](#oneview_interconnect_type_facts)
  * [oneview_logical_enclosure - Manage OneView Logical Enclosure resources.](#oneview_logical_enclosure)
  * [oneview_logical_enclosure_facts - Retrieve facts about one or more of the OneView Logical Enclosures.](#oneview_logical_enclosure_facts)
  * [oneview_logical_enclosure_script_facts - Retrieve the configuration script associated with the OneView Logical Enclosure.](#oneview_logical_enclosure_script_facts)
  * [oneview_logical_interconnect - Manage OneView Logical Interconnect resources.](#oneview_logical_interconnect)
  * [oneview_logical_interconnect_facts - Retrieve facts about one or more of the OneView Logical Interconnects.](#oneview_logical_interconnect_facts)
  * [oneview_logical_interconnect_group - Manage OneView Logical Interconnect Group resources.](#oneview_logical_interconnect_group)
  * [oneview_logical_interconnect_group_facts - Retrieve facts about one or more of the OneView Logical Interconnect Groups.](#oneview_logical_interconnect_group_facts)
  * [oneview_server_hardware - Manage OneView Server Hardware resources.](#oneview_server_hardware)
  * [oneview_server_hardware_facts - Retrieve facts about the OneView Server Hardwares.](#oneview_server_hardware_facts)
  * [oneview_server_profile - Selects a server hardware automatically based on the server hardware template.](#oneview_server_profile)
  * [oneview_server_profile_template - Manage OneView Server Profile Template resources.](#oneview_server_profile_template)
  * [oneview_server_profile_template_facts - Retrieve facts about the Server Profile Templates from OneView.](#oneview_server_profile_template_facts)
  * [oneview_storage_pool - Manage OneView Storage Pool resources.](#oneview_storage_pool)
  * [oneview_storage_pool_facts - Retrieve facts about one or more Storage Pools.](#oneview_storage_pool_facts)
  * [oneview_storage_system - Manage OneView Storage System resources.](#oneview_storage_system)
  * [oneview_storage_system_facts - Retrieve facts about the OneView Storage Systems.](#oneview_storage_system_facts)
  * [oneview_storage_system_host_types_facts - Retrieve facts about Host Types of the OneView Storage Systems.](#oneview_storage_system_host_types_facts)
  * [oneview_storage_system_managed_ports_facts - Retrieve facts about Managed Ports of the OneView Storage System.](#oneview_storage_system_managed_ports_facts)
  * [oneview_storage_system_pools_facts - Retrieve facts about Storage Pools of the OneView Storage System.](#oneview_storage_system_pools_facts)
  * [oneview_storage_volume_template - Manage OneView Storage Volume Template resources.](#oneview_storage_volume_template)
  * [oneview_storage_volume_templates_facts - Retrieve facts about Storage Volume Templates of the OneView.](#oneview_storage_volume_templates_facts)
  * [oneview_uplink_set - Manage OneView Uplink Set resources.](#oneview_uplink_set)
  * [oneview_uplink_set_facts - Retrieve facts about one or more of the OneView Uplink Sets.](#oneview_uplink_set_facts)

---

## hpe_icsp
Deploy the operating system on a server using HPE ICsp.

#### Synopsis
 Deploy the operating system on a server based on the available ICsp OS build plan.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpICsp

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | |  ICsp username.  |
| server_id  |   yes  |  | |  Server ID.  |
| personality_data  |   no  |  | |  Personality Data.  |
| os_build_plan  |   yes  |  | |  OS Build plan.  |
| custom_attributes  |   no  |  | |  Custom Attributes.  |
| icsp_host  |   yes  |  | |  ICsp hostname.  |
| password  |   yes  |  | |  ICsp password.  |


 
#### Examples

```
- name: Deploy OS
  hpe_icsp:
    icsp_host: "{{ icsp }}"
    username: "{{ icsp_username }}"
    password: "{{ icsp_password }}"
    server_id: "{{ server_profile.serialNumber }}"
    os_build_plan: "{{ os_build_plan }}"
    custom_attributes: "{{ osbp_custom_attributes }}"
    personality_data: "{{ network_config }}"
    when: created
  delegate_to: localhost

```




---


## oneview_enclosure
Manage OneView Enclosure resources.

#### Synopsis
 Provides an interface to manage Enclosure resources. Can add, update, remove, or reconfigure.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with the Enclosure properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>reconfigured</li>  <li>refreshed</li> </ul> |  Indicates the desired state for the Enclosure resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists. 'reconfigured' will reapply the appliance's configuration on the enclosure. This includes running the same configuration steps that were performed as part of the enclosure add. 'refreshed' will refresh the enclosure along with all of its components, including interconnects and servers. Any new hardware is added, and any hardware that is no longer present within the enclosure is removed.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Ensure that an Enclosure is present using the default configuration
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: present
    data:
      enclosureGroupUri : {{ enclosure_group_uri }},
      hostname : {{ enclosure_hostname }},
      username : {{ enclosure_username }},
      password : {{ enclosure_password }},
      name: 'Test-Enclosure'
      licensingIntent : "OneView"

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
  config: "{{ config }}"
  state: present
  data:
    name: 'Test-Enclosure'
    calibratedMaxPower: 1700
  delegate_to: localhost

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure   | Has all the facts about the enclosure. |  On states 'present', 'reconfigured', 'refreshed'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_env_config_facts
Retrieve the facts about the environmental configuration of one enclosure.

#### Synopsis
 Retrieve the facts about the settings that describe the environmental configuration (supported feature set, calibrated minimum and maximum power, location and dimensions, ...) of the enclosure resource.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Enclosure name.  |


 
#### Examples

```
- name: Gather facts about the environmental configuration of the enclosure named 'Test-Enclosure'
  oneview_enclosure_env_config_facts:
    config: "{{ config_file_path }}"
    name: "Test-Enclosure"

- debug: var=enclosure_env_config

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_env_config   | Has all the OneView facts about the environmental configuration of one enclosure. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_facts
Retrieve facts about one or more Enclosures.

#### Synopsis
 Retrieve facts about one or more of the Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Enclosure name.  |


 
#### Examples

```
- name: Gather facts about all Enclosures
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"

- debug: var=enclosures

- name: Gather facts about an Enclosure by name
  oneview_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Enclosure-Name"

- debug: var=enclosures

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosures   | Has all the OneView facts about the Enclosures. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_group
Manage OneView Enclosure Group resources.

#### Synopsis
 Provides an interface to manage Enclosure Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Enclosure Group properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Enclosure Group resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group   | Has the facts about the Enclosure Group. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_group_facts
Retrieve facts about one or more of the OneView Enclosure Groups.

#### Synopsis
 Retrieve facts about one or more of the Enclosure Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Enclosure Group name.  |


 
#### Examples

```
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather facts about a Enclosure Group by name
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
  delegate_to: localhost

- debug: var=enclosure_groups

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_groups   | Has all the OneView facts about the Enclosure Groups. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_group_script_facts
Retrieve the configuration script associated with a OneView Enclosure Group.

#### Synopsis
 Retrieve the configuration script associated with a OneView Enclosure Group.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Enclosure Group name.  |


 
#### Examples

```
- name: Get Enclosure Group Script by Enclosure Group name
  oneview_enclosure_group_script_facts:
    config: "{{ config }}"
    name: "Enclosure Group (For Demo)"
  delegate_to: localhost

- debug: var=enclosure_group_script

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group_script   | Gets the Enclosure Group script by Enclosure Group name. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_script_facts
Retrieve facts about the script of one enclosure.

#### Synopsis
 Retrieve facts about the script of one Enclosure from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Enclosure name.  |


 
#### Examples

```
- name: Gather facts about the script of the enclosure named 'Test-Enclosure'
  oneview_enclosure_script_facts:
    config: "{{ config_file_path }}"
    name: "Enclosure-Name"

- debug: var=enclosure_script

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_script   | Has all the OneView facts about the script of one enclosure. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_enclosure_utilization_facts
Retrieve the facts about the utilization of one enclosure.

#### Synopsis
 Retrieve the facts about the historical utilization data, metrics, and time span of the enclosure resource.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| startDate  |   no  |  | |  Start date of requested starting time range in ISO 8601 format.  |
| endDate  |   no  |  | |  End date of requested starting time range in ISO 8601 format. When omitted the endDate includes the latest data sample available.  |
| name  |   yes  |  | |  Enclosure name.  |
| fields  |   no  |  | |  Name of the metric(s) to be retrieved in the format METRIC[,METRIC]... Enclosures support the following utilization metrics: AmbientTemperature, AveragePower, PeakPower, PowerCap, DeratedCapacity and RatedCapacity. If unspecified, all metrics supported are returned.  |
| refresh  |   no  |  | |  Specifies that if necessary an additional request will be queued to obtain the most recent utilization data from the enclosure.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| view  |   no  |  | <ul> <li>native</li>  <li>hour</li>  <li>day</li> </ul> |  Specifies the resolution interval length of the samples to be retrieved.  |


 
#### Examples

```
- name: "Gather facts about the 24 hours of data for all available metrics at a resolution of one sample
         every 5 minutes for the enclosure named 'Test-Enclosure'"
  oneview_enclosure_utilization_facts:
    config: "{{ config }}"
    name: 'Test-Enclosure'
    delegate_to: localhost

- debug: var=enclosure_utilization

- name: "Gather facts about all temperature data at a resolution of one sample per day for the enclosure
         named 'Test-Enclosure', between two specified dates"
  oneview_enclosure_utilization_facts:
    config: "{{ config }}"
    name: 'Test-Enclosure'
    fields: 'AmbientTemperature
    start_date: '2016-06-30T03:29:42.000Z'
    end_date: '2018-07-01T03:29:42.000Z'
    view: 'day'
    refresh: False
delegate_to: localhost

- debug: var=enclosure_utilization

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_utilization   | Has all the OneView facts about the utilization of one enclosure. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_ethernet_network
Manage OneView Ethernet Network resources.

#### Synopsis
 Provides an interface to manage Ethernet Network resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Ethernet Network properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Ethernet Network resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Ensure that the Ethernet Network is present using the default configuration
  oneview_ethernet_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Ethernet Network'
      vlanId: '201'

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

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_network_bulk   | Has the facts about the Ethernet Networks affected by the bulk insert. |  when 'vlanIdRange' attribute is in data argument. Can be null. |  complex |
| ethernet_network   | Has the facts about the Ethernet Networks. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_ethernet_network_associated_profile_facts
Retrieve the facts about the profiles which are using an Ethernet network.

#### Synopsis
 Retrieve the facts about the profiles which are using an Ethernet network.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Ethernet Network name.  |


 
#### Examples

```
- name: Gather facts about profiles which are using an Ethernet network named 'Test-Ethernet-Network'
  oneview_ethernet_network_associated_profile_facts:
    config: "{{ config_file_path }}"
    name: "Test-Ethernet-Network"

- debug: var=enet_associated_profiles

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enet_associated_profiles   | List of profile URIs for the Ethernet network. |  Always, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_ethernet_network_associated_uplink_group_facts
Gather facts about the uplink sets which are using an Ethernet network.

#### Synopsis
 Retrieve a list of uplink port group URIs for the Ethernet network with specified name.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Ethernet Network name.  |


 
#### Examples

```
- name: Gather facts about the uplink sets which are using an Ethernet network named 'Test Ethernet Network'
  oneview_ethernet_network_associated_uplink_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Ethernet Network"

- debug: var=enet_associated_uplink_groups

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enet_associated_uplink_groups   | Has all the uplink port group URIs which are using an ethernet network. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_ethernet_network_facts
Retrieve the facts about one or more of the OneView Ethernet Networks.

#### Synopsis
 Retrieve the facts about one or more of the Ethernet Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Ethernet Network name.  |


 
#### Examples

```
- name: Gather facts about all Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    name: Ethernet network name

- debug: var=ethernet_networks

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_networks   | Has all the OneView facts about the Ethernet Networks. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_fabric_facts
Retrieve the facts about one or more of the OneView Fabrics.

#### Synopsis
 Retrieve the facts about one or more of the Fabrics from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Fabric name.  |


 
#### Examples

```
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fabrics   | Has all the OneView facts about the Fabrics. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_fc_network
Manage OneView Fibre Channel Network resources.

#### Synopsis
 Provides an interface to manage Fibre Channel Network resources. Can create, update, delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with the Fibre Channel Network properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Fibre Channel Network resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Ensure that a Fibre Channel Network is present using the default configuration
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

- name: Ensure that Fibre Channel Network is absent
  oneview_fc_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FC Network'

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fc_network   | Has the facts about the OneView FC Networks. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_fc_network_facts
Retrieve the facts about one or more of the OneView Fibre Channel Networks.

#### Synopsis
 Retrieve the facts about one or more of the Fibre Channel Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Fibre Channel Network name.  |


 
#### Examples

```
- name: Gather facts about all Fibre Channel Networks
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fc_networks

- name: Gather facts about a Fibre Channel Network by name
  oneview_fc_network_facts:
    config: "{{ config_file_path }}"
    name: network name

- debug: var=fc_networks

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fc_networks   | Has all the OneView facts about the Fibre Channel Networks. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_fcoe_network
Manage OneView FCoE Network resources.

#### Synopsis
 Provides an interface to manage FCoE Network resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with FCoE Network properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the FCoE Network resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fcoe_network   | Has the facts about the OneView FCoE Networks. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_fcoe_network_facts
Retrieve the facts about one or more of the OneView FCoE Networks.

#### Synopsis
 Retrieve the facts about one or more of the FCoE Networks from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  FCoE Network name.  |


 
#### Examples

```
- name: Gather facts about all FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fcoe_networks

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"
    name: "Test FCoE Network Facts"

- debug: var=fcoe_networks

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fcoe_networks   | Has all the OneView facts about the FCoE Networks. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_firmware_bundle
Upload OneView Firmware Bundle resources.

#### Synopsis
 Upload an SPP ISO image file or a hotfix file to the appliance.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| state  |   |  | <ul> <li>present</li> </ul> |  Indicates the desired state for the Firmware Driver resource. 'present' will ensure that the firmware bundle is at OneView.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| file_path  |   yes  |  | |  The full path of a local file to be loaded.  |


 
#### Examples

```
- name: Ensure that the Firmware Driver is present
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm"


```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_bundle   | Has the facts about the OneView Firmware Bundle. |  Always. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_firmware_driver
Provides an interface to remove Firmware Driver resources.

#### Synopsis
 Provides an interface to remove Firmware Driver resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| state  |   |  | <ul> <li>absent</li> </ul> |  Indicates the desired state for the Firmware Driver. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Firmware driver name.  |


 
#### Examples

```
- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"

```



#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_firmware_driver_facts
Retrieve the facts about one or more of the OneView Firmware Drivers.

#### Synopsis
 Retrieve the facts about one or more of the Firmware Drivers from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Firmware driver name.  |


 
#### Examples

```
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"

- debug: var=firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=firmware_drivers

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_drivers   | Has all the OneView facts about the Firmware Drivers. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_interconnect
Manage the OneView Interconnect resources.

#### Synopsis
 Provides an interface to manage the Interconnect power state and the UID light state. Can change the power state, UID light state, perform device reset, reset port protection, and update the interconnect ports.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| ip  |   no  |  | |  Interconnect IP add  |
| state  |   |  | <ul> <li>powered_on</li>  <li>powered_off</li>  <li>uid_on</li>  <li>uid_off</li>  <li>device_reset</li>  <li>update_ports</li>  <li>reset_port_protection</li> </ul> |  Indicates the desired state for the Interconnect resource. 'powered_on' turns the power on. 'powered_off' turns the power off. 'uid_on' turns the UID light on. 'uid_off' turns the UID light off. 'device_reset' perform a device reset. 'update_ports' updates the interconnect ports. 'reset_port_protection' triggers a reset of port protection.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Interconnect name  |
| ports  |   no  |  | |  List with ports to update. This option should be used together with 'update_ports' state.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect   | Has the facts about the OneView Interconnect. |  Always. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_interconnect_facts
Retrieve facts about one or more of the OneView Interconnects.

#### Synopsis
 Retrieve facts about one or more of the Interconnects from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Interconnect name  |
| gather_name_servers  |   no  |  False  | |  If true facts about the name servers will also be gathered.  |


 
#### Examples

```
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: "{{ interconnect_name }}"

- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: "{{ interconnect_name }}"
    gather_name_servers: true

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| name_servers   | The named servers for an interconnect. |  When the gather_name_servers is true |  list |
| interconnects   | The list of interconnects. |  Always, but can be null |  list |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_interconnect_statistics_facts
Retrieve the statistics facts about one interconnect from OneView.

#### Synopsis
 Retrieve the statistics facts about one interconnect from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| port_name  |   no  |  | |  Interconnect name  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Interconnect name  |


 
#### Examples

```
- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_statistics_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    delegate_to: localhost

- debug: interconnect_statistics

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_statistics   | Has all the OneView facts about the Interconnect Statistics. |  If port_name is undefined |  dict |
| port_statistics   | Statistics for the specified port name on an interconnect. |  If port name is defined |  dict |
| subport_statistics   | The subport statistics on an interconnect |  If subport_number is defined |  dict |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_interconnect_type_facts
Retrieve facts about one or more of the OneView Interconnect Types.

#### Synopsis
 Retrieve facts about one or more of the Interconnect Types from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Interconnect Type name.  |


 
#### Examples

```
- name: Gather facts about all Interconnect Types
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"

- debug: var=interconnect_types

- name: Gather facts about a Interconnect Type by name
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"
    name: HP VC Flex-10 Enet Module

- debug: var=interconnect_types

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_types   | Has all the OneView facts about the Interconnect Types. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_enclosure
Manage OneView Logical Enclosure resources.

#### Synopsis
 Provides an interface to manage Logical Enclosure resources. Can update, update firmware, perform dump, update configuration script, reapply configuration, or update from group.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Logical Enclosure properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>firmware_updated</li>  <li>script_updated</li>  <li>dumped</li>  <li>reconfigured</li>  <li>updated_from_group</li> </ul> |  Indicates the desired state for the Logical Enclosure resource. 'present' enable to change the Logical Enclosure name. 'firmware_updated' update the firmware for the Logical Enclosure. 'script_updated' update the Logical Enclosure configuration script. 'dumped' generates a support dump for the Logical Enclosure. 'reconfigured' reconfigure all enclosures associated with logical enclosure. 'updated_from_group' makes the logical enclosure consistent with the enclosure group.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_enclosure   | Has the facts about the OneView Logical Enclosure. |  On states 'present', 'firmware_updated', 'reconfigured', 'updated_from_group'. Can be null. |  complex |
| configuration_script   | Has the facts about the Logical Enclosure configuration script. |  On state 'script_updated'. Can be null. |  complex |
| generated_dump_uri   | Has the facts about the Logical Enclosure generated support dump uri. |  On state 'dumped'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_enclosure_facts
Retrieve facts about one or more of the OneView Logical Enclosures.

#### Synopsis
 Retrieve facts about one or more of the Logical Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Logical Enclosure name.  |


 
#### Examples

```
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_enclosures   | Has all the OneView facts about the Logical Enclosures. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_enclosure_script_facts
Retrieve the configuration script associated with the OneView Logical Enclosure.

#### Synopsis
 Retrieve the configuration script associated with the OneView Logical Enclosure.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   yes  |  | |  Logical Enclosure name.  |


 
#### Examples

```
- name: Get Logical Enclosure Script by Logical Enclosure name
  oneview_logical_enclosure_script_facts:
    config: "{{ config }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosure_script

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_enclosure_script   | Gets the Logical Enclosure script by Logical Enclosure name. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_interconnect
Manage OneView Logical Interconnect resources.

#### Synopsis
 Provides an interface to manage Logical Interconnect resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with the options.  |
| state  |   |  | <ul> <li>compliant</li>  <li>ethernet_settings_updated</li>  <li>internal_networks_updated</li>  <li>settings_updated</li>  <li>forwarding_information_base_generated</li>  <li>qos_aggregated_configuration_updated</li>  <li>snmp_configuration_updated</li>  <li>port_monitor_updated</li>  <li>configuration_updated</li>  <li>firmware_installed</li> </ul> |  Indicates the desired state for the Logical Interconnect resource. 'compliant' brings the logical interconnect back to a consistent state. 'ethernet_settings_updated' updates the Ethernet interconnect settings for the logical interconnect. 'internal_networks_updated' updates the internal networks on the logical interconnect. This operation is non-idempotent. 'settings_updated' updates the Logical Interconnect settings. 'forwarding_information_base_generated' generates the forwarding information base dump file for the logical interconnect. This operation is non-idempotent and asynchronous. 'qos_aggregated_configuration_updated' updates the QoS aggregated configuration for the logical interconnect. 'snmp_configuration_updated' updates the SNMP configuration for the logical interconnect. 'port_monitor_updated' updates the port monitor configuration of a logical interconnect. 'configuration_updated' asynchronously applies or re-applies the logical interconnect configuration to all managed interconnects. This operation is non-idempotent. 'firmware_installed' installs firmware to a logical interconnect. The three operations that are supported for the firmware update are Stage (uploads firmware to the interconnect), Activate (installs firmware on the interconnect) and Update (which does a Stage and Activate in a sequential manner). All of them are non-idempotent.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume_template   | Has the OneView facts about the Logical Interconnect. |  on 'compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',               and 'configuration_updated' states, but can be null. |  complex |
| interconnect_fib   | Has the OneView facts about the Forwarding information Base. |  on 'forwarding_information_base_generated' state, but can be null. |  complex |
| li_firmware   | Has the OneView facts about the installed Firmware. |  on 'firmware_installed' state, but can be null. |  complex |
| snmp_configuration   | Has the OneView facts about the SNMP Configuration. |  on 'snmp_configuration_updated' state, but can be null. |  complex |
| port_monitor   | Has the OneView facts about the Port Monitor Configuration. |  on 'port_monitor_updated' state, but can be null. |  complex |
| qos_configuration   | Has the OneView facts about the QoS Configuration. |  on 'qos_aggregated_configuration_updated' state, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_interconnect_facts
Retrieve facts about one or more of the OneView Logical Interconnects.

#### Synopsis
 Retrieve facts about one or more of the OneView Logical Interconnects.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Logical Interconnect name.  |
| options  |   no  |  | |  List with options to gather additional facts about Logical Interconnect. Options allowed: 'qos_aggregated_configuration' get the QoS aggregated configuration for the logical interconnect. 'snmp_configuration' get the SNMP configuration for a logical interconnect. 'port_monitor' get the port monitor configuration of a logical interconnect. 'internal_vlans' get the internal VLAN IDs for the provisioned networks on a logical interconnect. 'forwarding_information_base' get the forwarding information base data for a logical interconnect. 'firmware' get the installed firmware for a logical interconnect.  These options are valid just when a 'name' is provided. Otherwise it will be ignored.  |


 
#### Examples

```
- name: Gather facts about all Logical Interconnects
  oneview_logical_interconnect_facts:
  config: "{{ config }}"

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

- debug: var=logical_interconnects
- debug: var=qos_aggregated_configuration
- debug: var=snmp_configuration
- debug: var=port_monitor
- debug: var=internal_vlans
- debug: var=forwarding_information_base
- debug: var=firmware

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnects   | The list of logical interconnects. |  Always, but can be null. |  list |
| forwarding_information_base   | The forwarding information base data for a logical interconnect. |  When requested, but can be null. |  complex |
| firmware   | The installed firmware for a logical interconnect. |  When requested, but can be null. |  complex |
| internal_vlans   | The internal VLAN IDs for the provisioned networks on a logical interconnect. |  When requested, but can be null. |  complex |
| snmp_configuration   | The SNMP configuration for a logical interconnect. |  When requested, but can be null. |  complex |
| qos_aggregated_configuration   | The QoS aggregated configuration for the logical interconnect. |  When requested, but can be null. |  complex |
| port_monitor   | The port monitor configuration of a logical interconnect. |  When requested, but can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_interconnect_group
Manage OneView Logical Interconnect Group resources.

#### Synopsis
 Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with the Logical Interconnect Group properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Logical Interconnect Group resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      type: 'logical-interconnect-groupV3'
      name: 'New Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates: []

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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnect_group   | Has the facts about the OneView Logical Interconnect Group. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_logical_interconnect_group_facts
Retrieve facts about one or more of the OneView Logical Interconnect Groups.

#### Synopsis
 Retrieve facts about one or more of the Logical Interconnect Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Logical Interconnect Group name.  |


 
#### Examples

```
- name: Gather facts about all Logical Interconnect Groups
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_interconnect_groups

- name: Gather facts about a Logical Interconnect Group by name
  oneview_logical_interconnect_group_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=logical_interconnect_groups

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_interconnect_groups   | Has all the OneView facts about the Logical Interconnect Groups. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_server_hardware
Manage OneView Server Hardware resources.

#### Synopsis
 Provides an interface to manage Server Hardware resources. Can add, update, remove, change power state and refresh state.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Server Hardware properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>power_state_set</li>  <li>refresh_state_set</li>  <li>ilo_firmware_version_updated</li> </ul> |  Indicates the desired state for the Server Hardware resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists. 'power_state_set' will set the power state of the Server Hardware. 'refresh_state_set will set the refresh state of the Server Hardware. 'ilo_firmware_version_updated' will update the iLO firmware version of the Server Hardware.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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
        hostname : "172.18.6.15"
        powerStateData:
            powerState: "Off"
            powerControl: "MomentaryPress"
  delegate_to: localhost

- name: Refresh the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: refresh_state_set
    data:
        hostname : "172.18.6.15"
        refreshStateData:
            refreshState : "RefreshPending"
  delegate_to: localhost

- name: Update the Server Hardware iLO firmware version
  oneview_server_hardware:
    config: "{{ config }}"
    state: ilo_firmware_version_updated
    data:
        hostname : "172.18.6.15"
  delegate_to: localhost

- name: Set the calibrated max power of a server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: present
    data:
        hostname : "172.18.6.15"
        calibratedMaxPower: 2500
  delegate_to: localhost

- name: Remove the server hardware by its IP
  oneview_server_hardware:
    config: "{{ config }}"
    state: absent
    data:
        hostname : "172.18.6.15"
  delegate_to: localhost

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware   | Has the OneView facts about the Server Hardware. |  On states 'present', 'power_state_set', 'refresh_state_set', 'ilo_firmware_version_updated'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_server_hardware_facts
Retrieve facts about the OneView Server Hardwares.

#### Synopsis
 Retrieve facts about the Server Hardware from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Server Hardware name.  |
| options  |   no  |  | |  List with options to gather additional facts about Server Hardware related resources. Options allowed: bios, javaRemoteConsoleUrl, environmentalConfig, iloSsoUrl, remoteConsoleUrl, utilization  |


 
#### Examples

```
- name: Gather facts about all Server Hardwares
  oneview_server_hardware_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=server_hardwares


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
                filter : 'startDate=2016-05-30T03:29:42.000Z'
                view : 'day'
  delegate_to: localhost

- debug: var=server_hardwares
- debug: var=server_hardware_bios
- debug: var=server_hardware_env_config
- debug: var=server_hardware_java_remote_console_url
- debug: var=server_hardware_ilo_sso_url
- debug: var=server_hardware_remote_console_url
- debug: var=server_hardware_utilization

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_hardware_remote_console_url   | Has the facts about the Server Hardware remote console url. |  when requested, but can be null |  complex |
| server_hardware_bios   | Has all the facts about the Server Hardware BIOS. |  when requested, but can be null |  complex |
| server_hardware_ilo_sso_url   | Has the facts about the Server Hardware iLO SSO url. |  when requested, but can be null |  complex |
| server_hardwares   | Has all the OneView facts about the Server Hardware. |  always, but can be null |  complex |
| server_hardware_utilization   | Has all the facts about the Server Hardware utilization. |  when requested, but can be null |  complex |
| server_hardware_java_remote_console_url   | Has the facts about the Server Hardware java console url. |  when requested, but can be null |  complex |
| server_hardware_env_config   | Has all the facts about the Server Hardware environmental configuration. |  when requested, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_server_profile
Selects a server hardware automatically based on the server hardware template.

#### Synopsis
 Manage the servers lifecycle with OneView Server Profiles using an existing server profile template.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | |  Username that will be used to authenticate on the provided OneView appliance.  |
| name  |   yes  |  | |  Name of the server profile that will be created or updated.  |
| oneview_host  |   yes  |  | |  OneView appliance IP or hostname.  |
| server_template  |   yes  |  | |  Name of the server profile template that will be used to provision the server profiles.  |
| state  |   |  present  | <ul> <li>present</li>  <li>powered_off</li>  <li>absent</li>  <li>powered_on</li>  <li>restarted</li> </ul> |  Desired state for the server profile by the end of the playbook execution.  |
| password  |   yes  |  | |  Password that will be used to authenticate on the provided OneView appliance.  |


 
#### Examples

```
- oneview_server_profile:
    oneview_host: <ip>
    username: oneview_username
    password: oneview_password
    server_template: Compute-node-template
    name: <server-profile-name>

```




---


## oneview_server_profile_template
Manage OneView Server Profile Template resources.

#### Synopsis
 Provides an interface to create, modify, and delete server profile templates.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  Dict with Server Profile Template properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Server Profile Template. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Create a basic connection-less server profile template
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile_template   | Has the OneView facts about the Server Profile Template. |  On state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_server_profile_template_facts
Retrieve facts about the Server Profile Templates from OneView.

#### Synopsis
 Retrieve facts about the Server Profile Templates from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Server Profile Template name.  |
| options  |   no  |  | |  List with options to gather additional facts about Server Profile Template resources. Options allowed: new_profile  |


 
#### Examples

```
- name: Gather facts about all Server Profile Templates
  oneview_server_profile_template_facts:
    config: "{{ config }}"

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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| new_profile   | A profile object with the configuration based on this template. |  when requested, but can be null |  complex |
| server_profile_templates   | Has all the OneView facts about the Server Profile Templates. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_pool
Manage OneView Storage Pool resources.

#### Synopsis
 Provides an interface to manage Storage Pool resources. Can add and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Storage Pool properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Pool resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pool   | Has the OneView facts about the Storage Pool. |  on 'present' state, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_pool_facts
Retrieve facts about one or more Storage Pools.

#### Synopsis
 Retrieve facts about one or more of the Storage Pools from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Storage Pool name.  |


 
#### Examples

```
- name: Gather facts about all Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_pools

- name: Gather facts about a Storage Pool by name
  oneview_storage_pool_facts:
    config: "{{ config }}"
    name: "CPG_FC-AO"
  delegate_to: localhost

- debug: var=storage_pools

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pools   | Has all the OneView facts about the Storage Pools. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_system
Manage OneView Storage System resources.

#### Synopsis
 Provides an interface to manage Storage System resources. Can add, update and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Storage System properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage System resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system   | Has the OneView facts about the Storage System. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_system_facts
Retrieve facts about the OneView Storage Systems.

#### Synopsis
 Retrieve facts about the Storage Systems from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Storage System name.  |
| ip_hostname  |   no  |  | |  Storage System IP or hostname.  |


 
#### Examples

```
- name: Gather facts about all Storage Systems
  oneview_storage_system_facts:
    config: "{{ config }}"
  delegate_to: localhost

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

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_systems   | Has all the OneView facts about the Storage Systems. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_system_host_types_facts
Retrieve facts about Host Types of the OneView Storage Systems.

#### Synopsis
 Retrieve facts about Host Types of the OneView Storage Systems.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Gather facts about Storage System - Host Types
  oneview_storage_system_host_types_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=oneview_storage_host_types

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_host_types   | Has all the OneView facts about the Storage Systems - Host Types. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_system_managed_ports_facts
Retrieve facts about Managed Ports of the OneView Storage System.

#### Synopsis
 Retrieve facts about Managed Ports of the Storage Systems from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Storage System name.  |
| ip_hostname  |   no  |  | |  Storage System IP or hostname.  |


 
#### Examples

```
- name: Gather facts about managed ports by Storage System IP
  oneview_storage_system_managed_ports_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_system_managed_ports


- name: Gather facts about managed ports by Storage System Name
  oneview_storage_system_managed_ports_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_system_managed_ports

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system_managed_ports   | Has all Managed Ports facts about the OneView Storage Systems. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_system_pools_facts
Retrieve facts about Storage Pools of the OneView Storage System.

#### Synopsis
 Retrieve facts about Storage Pools of the Storage Systems from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Storage System name.  |
| ip_hostname  |   no  |  | |  Storage System IP or hostname.  |


 
#### Examples

```
- name: Gather facts about Storage Pools of a Storage System by IP
  oneview_storage_system_pools_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=storage_system_pools

- name: Gather facts about Storage Pools of a Storage System by name
  oneview_storage_system_pools_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=storage_system_pools

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system_pools   | Has all the OneView facts about the Storage Systems - Storage Pools. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_volume_template
Manage OneView Storage Volume Template resources.

#### Synopsis
 Provides an interface to manage Storage Volume Template resources. Can create, update and delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Storage Volume Template properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Volume Template resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume_template   | Has the OneView facts about the Storage Volume Template. |  on 'present' state, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_storage_volume_templates_facts
Retrieve facts about Storage Volume Templates of the OneView.

#### Synopsis
 Retrieve facts about Storage Volume Templates of the OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Storage Volume Template name.  |


 
#### Examples

```
- name: Gather facts about all Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
  delegate_to: localhost

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

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connectable_volume_templates   | Has facts about the Connectable Storage Volume Templates. |  when requested, but can be null |  complex |
| storage_volume_templates   | Has all the OneView facts about the Storage Volume Templates. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_uplink_set
Manage OneView Uplink Set resources.

#### Synopsis
 Provides an interface to manage Uplink Set resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Uplink Set properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Uplink Set resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |


 
#### Examples

```
- name: Ensure that the Uplink Set is present
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test Uplink Set'
      status: "OK"
      logicalInterconnectUri: "/rest/logical-interconnects/0de81de6-6652-4861-94f9-9c24b2fd0d66"
      networkUris: [
         '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4'
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

- name: Ensure that the Uplink Set is absent
  oneview_uplink_set:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test Uplink Set'

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| uplink_set   | Has the OneView facts about the Uplink Set. |  on state 'present'. Can be null. |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json

- To rename an uplink set you must inform a 'newName' in the data argument. The rename is non-idempotent


---


## oneview_uplink_set_facts
Retrieve facts about one or more of the OneView Uplink Sets.

#### Synopsis
 Retrieve facts about one or more of the Uplink Sets from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |
| name  |   no  |  | |  Uplink Set name.  |


 
#### Examples

```
- name: Gather facts about all Uplink Sets
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"

- debug: var=uplink_sets

- name: Gather facts about a Uplink Set by name
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=uplink_sets

```



#### Return Values

| Name          | Decription  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| uplink_sets   | Has all the OneView facts about the Uplink Sets. |  always, but can be null |  complex |


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


---

