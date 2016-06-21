# Ansible playbook to provide an application

Execute an Ansible playbook to provision hardware, deploy an operating system, and deploy an application stack with HPE OneView and Ansible.

Basically this playbook will:

1. Create server profiles for all the servers in the stack – two Web servers and one load balancer. Servers will be configured as defined in the template and powered on.
2. Deploy the operating system.
3. Deploy the application stack on the Web servers.
4. Install and configure the load balancer.
5. Deploy the application on the two Web servers behind the load balancer.

## Requirements

- Oneview 2.0 installed
- Server profile Templates must be created for use by the playbook.
- Server Hardware must be imported into OneView, so that Oneview can deploy profiles on them.
- Insight Control Provisioning 7.4 or later installed (if you need OS Install)
- Python 2.7.11
- Ansible 2.0.2
- HPE OneView Python SDK installed (https://github.com/HewlettPackard/python-hpOneView)
- HPE ICsp installed - available at `dependencies/python-hpICsp`

## Running the example

The `demo` folder contains the Ansible inventory definitions.
The `demo/hosts` file is the inventory definition and the `demo/group_vars` contains some global definitions like HPE OneView hostname, credentials, the profile template, ICSP preferences etc.

Update `demo/hosts` and provide the names of the servers you want to deploy – for this example, webservers and load balancers.

Update `demo/group_vars/all` and update the variables that match your test environment. Specify the HPE OneView hostname and credentials, ICSP hostname and credentials (if you are using ICSP).
Feel free to customize any custom arguments – or remove them if using defaults.

This example passes the SSH keys from the current system to ICSP build plan, so Ansible can do a ssh login into the newly deployed nodes.

To execute the playbook, run:
```$ ansible-playbook -i demo/hosts ov_site.yml```
