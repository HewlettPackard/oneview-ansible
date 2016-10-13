[![Build Status](https://travis-ci.org/HewlettPackard/oneview-ansible.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-ansible)

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

Sample playbooks and instructions on how to run the modules can be found in the [`examples`](/examples) directory.

An end-to-end DevOps example using OneView for the bare metal server provisioning, HPE ICsp for OS deployment, and Ansible modules for software setup is provided at: [Accelerating DevOps with HPE OneView and Ansible sample](/examples/oneview-web-farm).

## Setup

To run the Ansible modules provided in this project, you should execute the following steps:

**1. Clone the repository**

Run:

```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
```

**2. Configure the ANSIBLE_LIBRARY environmental variable**

Set the `ANSIBLE_LIBRARY` path, specifying the `library` full path from the cloned project:

```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
```

**3. Create the JSON Configuration File**

To use the Ansible OneView modules, you need to create OneView Python SDK JSON configuration file. This file is used to define the settings, which will be used on the OneView appliance connection, like hostname, username, and password. Here's an example:

```json
# config.json
{
  "ip": "172.25.105.12",
  "credentials": {
    "userName": "Administrator",
    "password": "secret123"
  }
}
```

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:

```json
  "proxy": "<proxy_host>:<proxy_port>"
```

:lock: Tip: Check the file permissions since the password is stored in clear-text.

The configuration file path must be provided for all of the playbooks `config` arguments. For example:

```yml
- name: Gather facts about the FCoE Network with name 'Test FCoE Network Facts'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "Test FCoE Network Facts"
```

## License

This project is licensed under the Apache 2.0 license. Please see the [LICENSE](LICENSE) for more information.

## Contributing and feature requests

**Contributing:** You know the drill. Fork it, branch it, change it, commit it, and pull-request it.
We are passionate about improving this project, and glad to accept help to make it better. However, keep the following in mind:

 - You must sign a Contributor License Agreement first. Contact one of the authors (from Hewlett Packard Enterprise) for details and the CLA.
 - We reserve the right to reject changes that we feel do not fit the scope of this project, so for feature additions, please open an issue to discuss your ideas before doing the work.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.
