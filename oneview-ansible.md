# Ansible HPE OneView Modules

### Modules

  * [hpe_icsp - Deploy the operating system on a server using HPE ICsp.](#hpe_icsp)
  * [oneview_enclosure - Manage OneView Enclosure resources.](#oneview_enclosure)
  * [oneview_enclosure_facts - Retrieve facts about one or more Enclosures.](#oneview_enclosure_facts)
  * [oneview_fc_network - Manage OneView Fibre Channel Network resources.](#oneview_fc_network)
  * [oneview_fc_network_facts - Retrieve facts about one or more of the OneView Fibre Channel Networks.](#oneview_fc_network_facts)
  * [oneview_fcoe_network - Manage OneView FCoE Network resources.](#oneview_fcoe_network)
  * [oneview_fcoe_network_facts - Retrieve facts about one or more of the OneView FCoE Networks.](#oneview_fcoe_network_facts)
  * [oneview_logical_interconnect_group - Manage OneView Logical Interconnect Group resources.](#oneview_logical_interconnect_group)
  * [oneview_logical_interconnect_group_facts - Retrieve facts about one or more of the OneView Logical Interconnect Groups.](#oneview_logical_interconnect_group_facts)
  * [oneview_server_profile - Selects a server hardware automatically based on the server hardware template.](#oneview_server_profile)

---(https://github.com/HewlettPackard/oneview-ansible/blob/master/oneview-ansible.md)

## hpe_icsp
Deploy the operating system on a server using HPE ICsp.

#### Synopsis
 Deploy the operating system on a server, based on an available ICsp OS build plan.

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
- name : Deploy OS
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
 Provides an interface to manage Enclosure resources. Can add, update, or remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpOneView

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   yes  |  | |  List with the Enclosure properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Enclosure resource. 'present' will ensure data properties are compliant to OneView. 'absent' will remove the resource from OneView, if it exists.  |
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
      newName : "Test-Enclosure-Renamed

- name: Ensure that enclosure is absent
  oneview_enclosure:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'Test-Enclosure'

```


#### Notes

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


---


## oneview_fc_network_facts
Retrieve facts about one or more of the OneView Fibre Channel Networks.

#### Synopsis
 Retrieve facts about one or more of the Fibre Channel Networks from OneView.

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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


---


## oneview_fcoe_network_facts
Retrieve facts about one or more of the OneView FCoE Networks.

#### Synopsis
 Retrieve facts about one or more of the FCoE Networks from OneView.

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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


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

- A sample configuration file for the config parameter can be found at&colon; https://github.hpe.com/Rainforest/oneview-ansible/blob/master/examples/oneview_config.json


---


## oneview_server_profile
Selects a server hardware automatically based on the server hardware template.

#### Synopsis
 Manage servers lifecycle with OneView Server Profiles using an existing server profile template.

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
