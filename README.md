[![Build Status](https://travis-ci.org/HewlettPackard/oneview-ansible.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-ansible)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/oneview-ansible/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/oneview-ansible?branch=master)

# Ansible Modules for HPE OneView

Modules to manage HPE OneView using Ansible playbooks.

## Requirements

 - Ansible >= 2.0.2
 - Python >= 2.7.9
 - HPE OneView Python SDK ([Install HPE OneView Python SDK](https://github.com/HewlettPackard/python-hpOneView#installation))

## Modules

Each OneView resource operation is exposed through an Ansible module. We also provide a specific module to gather facts about the resource.

The detailed documentation for each module is available at: [HPE OneView Ansible Modules Documentation](oneview-ansible.md)

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

### Examples

Sample playbooks and instructions on how to run the modules can be found in the [`examples`](/examples) directory.

#### End-to-end examples

- An end-to-end DevOps example using HPE OneView for the bare metal server provisioning, HPE ICsp for OS deployment, and Ansible modules for software setup is provided at: [Accelerating DevOps with HPE OneView and Ansible sample](/examples/oneview-web-farm).

- An example of how to use HPE OneView with HPE Synergy Image Streamer for OS Deployment is available at: [HPE Synergy OS Deployment Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_create_server_profile_with_deployment_plan.yml) and [HPE Image Streamer Samples](https://github.com/devdil/oneview-ansible/blob/master/examples/ImageStreamer)

- An example of how to upload an artifact bundle for HPE Synergy Image Streamer and deploy a blade server in HPE OneView using the OS build plan provided in the artifact bundle is available at: [HPE Synergy + OneView Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_image_streamer.yml).

- Examples of bare metal infrastructure setup using HPE OneView and Ansible are available at:
  - [C7000 Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/c7000_environment_setup.yml)
  - [HPE Synergy Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_environment_setup.yml)

## Setup

To run the Ansible modules provided in this project, you should execute the following steps:

###1. Clone the repository

Run:

```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
```

###2. Configure the ANSIBLE_LIBRARY environmental variable

Set the `ANSIBLE_LIBRARY` path, specifying the `library` full path from the cloned project:

```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
```

###3. OneViewClient Configuration

####Using a JSON Configuration File

To use the Ansible OneView modules, you can store the configuration on a JSON file. This file is used to define the
settings, which will be used on the OneView appliance connection, like hostname, username, and password. Here's an
example:

```json
{
  "ip": "172.25.105.12",
  "credentials": {
    "userName": "Administrator",
    "authLoginDomain": "",
    "password": "secret123"
  },
  "api_version": 200
}
```

The `api_version` specifies the version of the Rest API to invoke. When not defined, it will use `300` as the
default value.

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

####Environment Variables

If you prefer, the configuration can also be stored in environment variables.

```bash
# Required
export ONEVIEWSDK_IP='172.25.105.12'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='200'  # default value is 300
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

###4. OneView 3.0

The Ansible Modules for HPE OneView already supports the new API endpoints for OneView 3.0 and for HPE Synergy.
To access this feature, you must set the API version on the OneViewClient configuration, either using the JSON configuration:

```json
  "api_version": 300
```
OR using the Environment variable:

```bash
export ONEVIEWSDK_API_VERSION='300'
```


###5. HPE Synergy Image Streamer

Modules to manage HPE Synergy Image Streamer appliances are also included in this project.
To use these modules, you must set the Image Streamer IP on the OneViewClient configuration,
either using the JSON configuration:

```json
"image_streamer_ip": "100.100.100.100"
```

OR using the Environment variable:

```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

You can find sample playbooks in the [examples](https://github.com/HewlettPackard/oneview-ansible/tree/master/examples) folder. Just look for the playbooks with the ```image_streamer_``` prefix.


## License

This project is licensed under the Apache 2.0 license. Please see the [LICENSE](LICENSE) for more information.

## Contributing and feature requests

**Contributing:** You know the drill. Fork it, branch it, change it, commit it, and pull-request it.
We are passionate about improving this project, and glad to accept help to make it better. However, keep the following in mind:

 - You must sign a Contributor License Agreement first. Contact one of the authors (from Hewlett Packard Enterprise) for details and the CLA.
 - We reserve the right to reject changes that we feel do not fit the scope of this project, so for feature additions, please open an issue to discuss your ideas before doing the work.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

## Naming convention

By adding support for a new resource, 3 files are required: self-contained module, test and example.
The following is a summary of the code structure and naming conventions for the oneview-ansible modules.

**Modules**

Modules are located in **library** folder. All modules need to be self-contained,
without external dependencies except hpOneView.
The module is named according to the **HPE OneView API Reference** resource title, but in singular.
The name should have the "oneview_" prefix, with all characters in lowercase,
replacing spaces by underscores. For example: **oneview_fc_network**

**Tests**

Tests are located in **tests** folder. The name of the test modules should start with
"test_" prefix in addition to the tested module name, for example: **test_oneview_fc_network**

**Playbook Examples**

Examples are located in **examples** folder with the same name of corresponding module,
for example: **oneview_fc_network.yml**

**Facts**

Modules that implement facts follow the same rules of any other modules, but the filenames have a suffix: "_facts", for example: **oneview_fc_network_facts**
