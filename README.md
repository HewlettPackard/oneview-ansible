# HPE OneView SDK for Ansible

## Build Status 

| 5.50 Branch   | 5.40 Branch   | 5.30 Branch   | 5.20 Branch   | 5.00 Branch   |
| ------------- |:-------------:| -------------:| -------------:| -------------:|
| ![Build status](https://ci.appveyor.com/api/projects/status/u84505l6syp70013?svg=true)| ![Build status](https://ci.appveyor.com/api/projects/status/u84505l6syp70013?svg=true)| ![Build status](https://ci.appveyor.com/api/projects/status/u84505l6syp70013?svg=true)| ![Build status](https://ci.appveyor.com/api/projects/status/u84505l6syp70013?svg=true)| ![Build status](https://ci.appveyor.com/api/projects/status/u84505l6syp70013?svg=true)


## Introduction

HPE OneView makes it simple to deploy and manage today’s complex hybrid cloud infrastructure. HPE OneView can help you transform your data center to software-defined, and it supports HPE’s broad portfolio of servers, storage, and networking solutions, ensuring the simple and automated management of your hybrid infrastructure. Software-defined intelligence enables a template-driven approach for deploying, provisioning, updating, and integrating compute, storage, and networking infrastructure.

The HPE OneView Ansible library provides modules to manage HPE OneView using Ansible playbooks using HPE OneView REST APIs. You can find the latest supported HPE OneView Ansible SDK [here](https://github.com/HewlettPackard/oneview-ansible/releases/latest)

Each OneView resource operation is exposed through an Ansible module. Specific modules are provided to gather facts about the resource. The detailed documentation for each module is available at: [HPE OneView Ansible Modules Documentation](https://github.com/HewlettPackard/oneview-ansible/blob/master/oneview-ansible.md)


## What's New

HPE OneView Ansible library extends support of the SDK to OneView REST API version 2200 (OneView v5.50)

Please refer to [notes](https://github.com/HewlettPackard/oneview-ansible/blob/master/CHANGELOG.md) for more information on the changes , features supported and issues fixed in this version


## Getting Started 

## Installation and Configuration
HPE OneView SDK for Ansible can be installed from Source and Docker container installation methods.
	
## Requirements
To run the Ansible modules provided in this project, we need the below : 
 
	Ansible < 2.9
	Python >= 3.4.2
	HPE OneView Python SDK
 
## Installation

### Perform a full installation from Source
   
#### Clone the repository
```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
$ cd oneview-ansible
```

#### Install dependency packages using PIP
```bash
$ pip install -r requirements.txt
```

#### Configure the ANSIBLE_LIBRARY environmental variable
Set the environment variables `ANSIBLE_LIBRARY` and `ANSIBLE_MODULE_UTILS`, specifying the `library` full path from the cloned project:
```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
$ export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/
```

### From Docker Image / Container
The containerized version of the oneview-ansible modules is available in the [Docker Store](https://store.docker.com/community/images/hewlettpackardenterprise/hpe-oneview-sdk-for-ansible). The Docker Store image tag consist of two sections: <sdk_version-OV_version>

#### Download and store a local copy of  hpe-oneview-sdk-for-ansible and use it as a Docker image.
```bash
$ docker pull hewlettpackardenterprise/hpe-oneview-sdk-for-ansible:v5.9.0-OV5.5
```

#### Run docker command which in turn will create a sh session where SDK user can create files, issue commands and execute playbooks
```bash
$ docker run -it hewlettpackardenterprise/hpe-oneview-sdk-for-ansible:v5.9.0-OV5.5 /bin/sh
```

There is also a [how-to guide](https://github.com/HewlettPackard/oneview-ansible-samples/blob/master/oneview-ansible-in-container/oneview-ansible-in-container.md) with instructions on how to use the container without creating a sh session.
   
   
## OneView Client Configuration

### Using a JSON Configuration File
To use the Ansible OneView modules, connection properties for accessing the OneView appliance can be set in a JSON file. This file is used to define the settings, which will be used on the OneView appliance connection, like hostname, username, and password. Here's an example:
```json
{
  "ip": "172.25.105.12",
  "credentials": {
    "userName": "Administrator",
    "authLoginDomain": "",
    "password": "secret123"
  },
  "api_version": 2200
}
```

The api_version specifies the version of the REST API to be invoked. When api_version is not specified, it will use `600` as the default value.

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:
```json
  "proxy": "<proxy_host>:<proxy_port>"
```

:lock: Tip: Check the file permissions since the password is stored in clear-text.

The configuration file path must be provided for all of the playbooks `config` arguments. For example:

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "FCoE Network Test"
```

### Environment Variables

Configuration can also be defined through environment variables:

```bash
# Required
export ONEVIEWSDK_IP='172.25.105.12'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='2200'
export ONEVIEWSDK_AUTH_LOGIN_DOMAIN='authdomain'
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
```

:lock: Tip: Make sure no unauthorised person has access to the environment variables, since the password is stored in clear-text.

In this case, you shouldn't provide the `config` argument. For example:

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    name: "FCoE Network Test"
```

Once you have defined the environment variables, you can run the plays.

### Parameters in the playbook

The third way to pass in your HPE OneView credentials to your tasks is through explicit specification on the task. 
This option allows the parameters `hostname`, `username`, `password`, `api_version` and `image_streamer_hostname` to be passed directly inside your task.

```yaml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2200
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost
```
Setting `no_log: true` is highly recommended in this case, as the credentials are otherwise returned in the log after task completion.

### Storing credentials using Ansible Vault

Ansible Vault feature may be leveraged for storing the credential of the user in encrypted format.

  1. Create a oneview_config.yml file.
  2. Run below commands to encrypt your username and password for oneview. 
     ```ansible-vault
     ansible-vault encrypt_string 'secret123' --name ONEVIEWSDK_PASSWORD
     ```
     Note: This password will be used to run the playbook.
  3. Paste the encrypted password along with the configuration in oneview_config.yml file.

	    ```yaml
	    # Required
	    ip: 172.168.1.1
	    api_version:2200
	    username: Administrator
	    password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          37646435306637633461376438653439323666383934353234333934616363313164636637376536
          3239356538653537643734626265366662623863323661350a613834313562303635343931356139
          35343863313563363830356638343339373138316539613636336532333065366133386662333833
          6663363236663031340a636562646634323136353737373539326434626137353837333530376665
          3835
	    ```

  4. Update the oneview_config.yml as vars_file in playbook for example:

```yaml
- vars_file:
   oneview_config.yml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: "{{ ip }}"
    username: "{{ username }}"
    password: "{{ password }}"
    api_version: "{{ api_version }}"
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost
```

We can encrypt the oneview_config.yml file also, but if you encrypt the file then you shall not encrypt the password inside the encrypted file. 
	
🔒 Tip: Make sure no unauthorised person has access to the encrypted variables/files, since the password can be decrypted with the password.

5. Run the playbook with --ask-vault-pass option to get the password prompt to run the playbook.
```bash   
ansible-playbook example.yml --ask-vault-pass
```
Note: Most of the examples provided in this repository uses OneView Credentials in plain text.

### Setting OneView API Version

The Ansible modules for HPE OneView support the API endpoints for HPE OneView 4.00, 4.10, 4.20, 5.00, 5.20, 5.30, 5.40, 5.50 <br/>
The current `default` HPE OneView version will pick the OneView appliance version.

To use a different API, you must set the API version together with your credentials, either using the JSON configuration:
```bash
"api_version": 2200
```

OR using the Environment variable: 
```bash
export ONEVIEWSDK_API_VERSION='2200'
```

If this property is not specified, it will fall back to the default value.

### HPE Synergy Image Streamer

Modules to manage HPE Synergy Image Streamer appliances are also included in this project. To use these modules, you must set the Image Streamer IP on the OneViewClient configuration, either using the JSON configuration:

```json
"image_streamer_ip": "100.100.100.100"
```

OR using the Environment variable:
```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

## Examples

Sample playbooks and instructions on how to run the modules can be found in the [`examples`](/examples) directory.
You can find sample playbooks in the [examples](https://github.com/HewlettPackard/oneview-ansible/tree/master/examples) folder. Just look for the playbooks with the ```image_streamer_``` prefix.

### Example of a playbook using Ansible OneView modules

```yml
- hosts: all
  tasks:

    - name: Ensure that the Fibre Channel Network is present with fabricType 'DirectAttach'
      oneview_fc_network:
        config: "/path/to/config.json"
        state: present
        data:
          name: 'New FC Network'
          fabricType: 'DirectAttach'

    - name: Ensure that Fibre Channel Network is absent
      oneview_fc_network:
        config: "/path/to/config.json"
        state: absent
        data:
          name: 'New FC Network'

    - name: Gather facts about the FCoE Network with name 'Test FCoE Network Facts'
      oneview_fcoe_network_facts:
        config: "/path/to/config.json"
        name: "Test FCoE Network Facts"
```


#### End-to-end examples

- An end-to-end DevOps example using HPE OneView for the bare metal server provisioning, HPE ICsp for OS deployment, and Ansible modules for software setup is provided at: [Accelerating DevOps with HPE OneView and Ansible sample](/examples/oneview-web-farm).

- A collection of examples of how to use HPE OneView with HPE Synergy Image Streamer for OS Deployment is available at: [HPE Synergy OS Deployment Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_create_server_profile_with_deployment_plan.yml) and [HPE Image Streamer Samples](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/ImageStreamer)

- An example of how to upload an artifact bundle for HPE Synergy Image Streamer and deploy a blade server in HPE OneView using the OS build plan provided in the artifact bundle is available at: [HPE Synergy + OneView Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_image_streamer.yml).

- Examples of bare metal infrastructure setup using HPE OneView and Ansible are available at:
  - [C7000 Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/c7000_environment_setup.yml)
  - [HPE Synergy Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_environment_setup.yml)


## Getting Help 

Are you running into a road block? Have an issue with unexpected bahriov? Feel free to open a new issue on the [issue tracker](https://github.com/HewlettPackard/oneview-ansible/issues)

For more information on how to open a new issue refer to [How can I get help & support](https://github.com/HewlettPackard/oneview-ansible/wiki#getting-help---how-can-i-get-help—support)

## License 

This project is licensed under the Apache license. Please see [LICENSE](https://github.com/HewlettPackard/oneview-ansible/blob/master/LICENSE) for more information.

## Contributing and feature requests

We welcome your contributions to the Ansible Modules for HPE OneView. See [CONTRIBUTING.md](https://github.com/HewlettPackard/oneview-ansible/blob/master/CONTRIBUTING.md) for more details.

## Additional Resources 

**HPE OneView Documentation**

[HPE OneView Release Notes](http://hpe.com/info/OneView/docs)

[HPE OneView Support Matrix](http://hpe.com/info/OneView/docs)

[HPE OneView Installation Guide](http://hpe.com/info/OneView/docs)

[HPE OneView User Guide](http://hpe.com/info/OneView/docs)

[HPE OneView Online Help](http://hpe.com/info/OneView/docs)

[HPE OneView REST API Reference](http://hpe.com/info/OneView/docs)

[HPE OneView Firmware Management White Paper](http://hpe.com/info/OneView/docs)

[HPE OneView Deployment and Management White Paper](http://hpe.com/info/OneView/docs)


**HPE OneView Community**

[HPE OneView Community Forums](http://hpe.com/info/oneviewcommunity)

Learn more about HPE OneView at [hpe.com/info/oneview](https://hpe.com/info/oneview)
