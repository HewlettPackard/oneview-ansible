# Ansible playbook to provide an application

Execute an Ansible playbook to provision hardware, deploy an operating system and an application stack with HPE OneView and Ansible.

Basically this playbook will:

1. Create server profiles for all the servers in the stack – two Web servers and one load balancer. Servers will be configured as defined in the server profile template and powered on.
2. Deploy the operating system using ICsp.
3. Deploy the application stack on the Web servers.
4. Install and configure the load balancer.
5. Deploy the application on the web servers behind the load balancer.

## Requirements

- Oneview 2.0 installed
- Server profile Templates must be created for use by the playbook.
- Server Hardware must be imported into OneView, so that Oneview can deploy profiles on them.
- Insight Control Provisioning 7.4 or later installed (if you need OS Install)
- Python >= 2.7.9
- Ansible >= 2.0.2
- HPE OneView Python SDK installed (https://github.com/HewlettPackard/python-hpOneView)
- HPE ICsp installed - available at `dependencies/python-hpICsp`

## Running the example

### Inventory

The `demo` folder contains the Ansible inventory definitions.

If you wish, you can create a copy of the demo folder for a test environment, which you want to operate.
Then, update the `hosts` file and provide the names of the servers you want to deploy – for this example, webservers and load balancers.

### Variables and Settings

`demo/group_vars` contains some global definitions like HPE OneView hostname, credentials, the profile template, ICsp preferences, etc.

You should update the `demo/group_vars/all` and set the variables to match your test environment. Specify the HPE OneView hostname and credentials, ICsp hostname and credentials (if you are using ICsp).

Feel free to customize any argument – or remove them if using defaults.

:lock: Tip: Check file permissions of the files inside the directory `demo/group_vars` since the passwords are stored in clear-text.

This example passes the SSH keys from the current system to ICsp build plan, so Ansible can ssh into the newly deployed nodes.

To execute the playbook, run:

```$ ansible-playbook -i demo/hosts ov_site.yml```
