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
  * [oneview_logical_interconnect_group - Manage OneView Logical Interconnect Group resources.](#oneview_logical_interconnect_group)
  * [oneview_logical_interconnect_group_facts - Retrieve facts about one or more of the OneView Logical Interconnect Groups.](#oneview_logical_interconnect_group_facts)
  * [oneview_server_hardware - Manage OneView Server Hardware resources.](#oneview_server_hardware)
  * [oneview_server_hardware_facts - Retrieve facts about the OneView Server Hardwares.](#oneview_server_hardware_facts)
  * [oneview_server_profile - Selects a server hardware automatically based on the server hardware template.](#oneview_server_profile)
  * [oneview_storage_system - Manage OneView Storage System resources.](#oneview_storage_system)
  * [oneview_storage_system_facts - Retrieve facts about the OneView Storage Systems.](#oneview_storage_system_facts)
  * [oneview_storage_system_host_types_facts - Retrieve facts about Host Types of the OneView Storage Systems.](#oneview_storage_system_host_types_facts)
  * [oneview_storage_system_managed_ports_facts - Retrieve facts about Managed Ports of the OneView Storage System.](#oneview_storage_system_managed_ports_facts)
  * [oneview_storage_system_pools_facts - Retrieve facts about Storage Pools of the OneView Storage System.](#oneview_storage_system_pools_facts)

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

- debug: var=oneview_enclosure_env_config_facts

```


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

- debug: var=enclosure_group

- name: Gather facts about a Enclosure Group by name
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
  delegate_to: localhost

- debug: var=enclosure_group

```


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

- debug: var=enclosure_group

```


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

- debug: var=oneview_enclosure_utilization

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

- debug: var=oneview_enclosure_utilization

```


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

- name: Ensure that the Logical Interconnect Group is present with name 'Renamed Ethernet Network'
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

- debug: var=oneview_enet_associated_profiles

```


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

- debug: var=oneview_fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=oneview_fabrics

```


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

- debug: var=fcoe_network

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"
    name: "Test FCoE Network Facts"

- debug: var=fcoe_network

```


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

- debug: var=oneview_firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=oneview_firmware_drivers

```


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

- debug: var=oneview_logical_enclosure

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=oneview_logical_enclosure

```


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

- debug: var=oneview_logical_enclosure

```


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


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---


## oneview_server_hardware
Manage OneView Server Hardware resources.

#### Synopsis
 Provides an interface to manage Server Hardware resources. Can add, update, remove and change power state.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with Server Hardware properties and its associated states  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>set_power_state</li> </ul> |  Indicates the desired state for the Server Hardware resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists. 'set_power_state' will set the power state of the Server Hardware.  |
| config  |   yes  |  | |  Path to a .json configuration file containing the OneView client configuration.  |



#### Examples

```
- name: Add a Server Hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: present
    data:
         hostname : "172.18.6.15"
         username : "dcs"
         password : "dcs"
         force : false
         licensingIntent: "OneView"
         configurationState: "Managed"
  delegate_to: localhost

- name: Power Off the server hardware
  oneview_server_hardware:
    config: "{{ config }}"
    state: set_power_state
    data:
        hostname : "172.18.6.15"
        powerStateData:
            powerState: "Off"
            powerControl: "MomentaryPress"
  delegate_to: localhost

- name: Remove the server hardware by its IP
  oneview_server_hardware:
    config: "{{ config }}"
    state: absent
    data:
        hostname : "172.18.6.15"
  delegate_to: localhost

```


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



#### Examples

```
- name: Gather facts about all Server Hardwares
  oneview_server_hardware_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=oneview_server_hardware


- name: Gather facts about a Server Hardware by name
  oneview_server_hardware_facts:
    config: "{{ config }}"
    name: "172.18.6.15"
  delegate_to: localhost

- debug: var=oneview_server_hardware

```


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

- debug: var=oneview_storage_system


- name: Gather facts about a Storage System by IP
  oneview_storage_system_facts:
    config: "{{ config }}"
    ip_hostname: "172.18.11.12"
  delegate_to: localhost

- debug: var=oneview_storage_system


- name: Gather facts about a Storage System by name
  oneview_storage_system_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=oneview_storage_system

```


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

- debug: var=oneview_storage_system_managed_ports


- name: Gather facts about managed ports by Storage System Name
  oneview_storage_system_managed_ports_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=oneview_storage_system_managed_ports

```


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

- debug: var=oneview_storage_pools

- name: Gather facts about Storage Pools of a Storage System by name
  oneview_storage_system_pools_facts:
    config: "{{ config }}"
    name: "ThreePAR7200-4555"
  delegate_to: localhost

- debug: var=oneview_storage_pools

```


#### Notes

- A sample configuration file for the config parameter can be found at: https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json


---
