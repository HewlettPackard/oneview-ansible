# Ansible Modules for HPE OneView

Ansible modules that provide resources for managing OneView.

**NOTE:** This is an early version that provides some specific Ansible resources. This version does not fully support the OneView yet.

## Requirements

 - Ansible 2.0.2
 - Python 2.7.11
 - python-OneView SDK ([Install python-OneView SDK](https://github.com/HewlettPackard/python-hpOneView#installation))

## Modules
Each OneView resource is exposed over a module that allow ensure that a resource is `present` or `absent`. It is provided a module to gather the facts about that resource too.

### Example of playbook using Ansible OneView modules

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

## Ansible OneView configuration

Clone the project:
```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
```

Configure `ANSIBLE_LIBRARY` environment variable specifying the full path to the cloned project:
```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible
```


**Configuration File**

To use the Ansible OneView modules you need create a configuration file. A configuration file is used to define client configuration (json format). Here's an example json file:

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

:lock: Tip: Check the file permissions because the password is stored in clear-text.

The configuration file path must be provided for playbook `config` argument:

```
- name: Gather facts about the FCoE Network with name 'Test FCoE Network Facts'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "Test FCoE Network Facts"
```