[![Build Status](https://travis-ci.org/HewlettPackard/oneview-ansible.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-ansible)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/oneview-ansible/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/oneview-ansible?branch=master)

# Ansible Modules for HPE OneView

Modules to manage HPE OneView using Ansible playbooks.

## Requirements

 - Ansible >= 2.1
 - Python >= 3.4.2
 - HPE OneView Python SDK
 
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

- A collection of examples of how to use HPE OneView with HPE Synergy Image Streamer for OS Deployment is available at: [HPE Synergy OS Deployment Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_create_server_profile_with_deployment_plan.yml) and [HPE Image Streamer Samples](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/ImageStreamer)

- An example of how to upload an artifact bundle for HPE Synergy Image Streamer and deploy a blade server in HPE OneView using the OS build plan provided in the artifact bundle is available at: [HPE Synergy + OneView Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_image_streamer.yml).

- Examples of bare metal infrastructure setup using HPE OneView and Ansible are available at:
  - [C7000 Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/c7000_environment_setup.yml)
  - [HPE Synergy Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_environment_setup.yml)

## Setup

To run the Ansible modules provided in this project, you may run a containerized version or perform a full installation. The containerized version of the `oneview-ansible` modules is available in the [Docker Store](https://store.docker.com/community/images/hewlettpackardenterprise/oneview-ansible-debian). There is also a [how-to guide](https://github.com/HewlettPackard/oneview-ansible-samples/blob/master/oneview-ansible-in-container/oneview-ansible-in-container.md) with instructions on how to use the container.

To perform a full installation, you should execute the following steps:

### 1. Clone the repository

Run:

```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
```

### 2. Install dependency packages

Run pip command from the cloned directory:
    
  ```bash
  pip install -r requirements.txt
  ```
  
### 3. Configure the ANSIBLE_LIBRARY environmental variable

Set the environment variables `ANSIBLE_LIBRARY` and `ANSIBLE_MODULE_UTILS`, specifying the `library` full path from the cloned project:

```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
$ export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/
```

### 4. OneViewClient Configuration

#### Using a JSON Configuration File

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

The `api_version` specifies the version of the Rest API to invoke. When not defined, it will use `600` as the
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

#### Environment Variables

If you prefer, the configuration can also be stored in environment variables.

```bash
# Required
export ONEVIEWSDK_IP='172.25.105.12'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='1600'  # default value is 600
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

#### Parameters in the playbook

The third way to pass in your HPE OneView credentials to your tasks is through explicit specification on the task.

This option allows the parameters `hostname`, `username`, `password`, `api_version` and `image_streamer_hostname` to be passed directly inside your task.

```yaml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
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

#### Storing credentials using Ansible Vault.

If you prefer, the credential of the user can be stored in encrypted format.

1. Create a oneview_config.yml file.
2. Run below commands to encrypt your username and password for oneview. 

   `ansible-vault encrypt_string 'secret123' --name ONEVIEWSDK_PASSWORD`

Note: This password will be used to run the playbook.

3. Paste the encrypted password along with the configuration in oneview_config.yml file.

```yaml
# Required
ip: 172.168.1.1
api_version:1600
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
  - oneview_config.yml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: "{{ ip }}"
    username: "{{ username }}"
    password: "{{ password }}"
    api_version: "{{ api_version }}"
    state: present
    data:
      name: "Test Network"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost

# Optional
We can encrypt the oneview_config.yml file also, but if you encrypt the file then you shall not encrypt the password inside the encrypted file. 
```
🔒 Tip: Make sure no unauthorised person has access to the encrypted variables/files, since the password can be decrypted with the password.

5. Run the playbook with --ask-vault-pass option to get the password prompt to run the playbook.
```bash   
ansible-playbook example.yml --ask-vault-pass
```

Note: Most of the examples provided in this repository uses OneView Credentials in plain text.

### 5. Setting your OneView version

The Ansible modules for HPE OneView support the API endpoints for HPE OneView 4.00, 4.10, 4.20, 5.00 and 5.20.

The current `default` HPE OneView version used by the modules is `4.00`, API `600`.

To use a different API, you must set the API version together with your credentials, either using the JSON configuration:

```json
"api_version": 1600
```
OR using the Environment variable:

```bash
export ONEVIEWSDK_API_VERSION='1600'
```

If this property is not specified, it will fall back to the ```600``` default value.

The API list is as follows:

- HPE OneView 4.00 API version: `600`
- HPE OneView 4.10 API version: `800`
- HPE OneView 4.20 API version: `1000`
- HPE OneView 5.00 API version: `1200`
- HPE OneView 5.20 API version: `1600`


### 6. HPE Synergy Image Streamer

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

**Contributing:** We welcome your contributions to the Ansible Modules for HPE OneView. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

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

Modules that implement facts follow the same rules of any other modules, but the filenames have a suffix: "\_facts", for example: **oneview_fc_network_facts**

## Testing

The basic test execution can be achieved by executing the `build.sh` file.

Please refer to [TESTING.md](TESTING.md) for further testing information.
