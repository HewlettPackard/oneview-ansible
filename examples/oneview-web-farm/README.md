# Ansible playbook to provide an application

Execute an Ansible playbook to provision hardware, deploy an operating system, and the application stack with HPE OneView and Ansible.

Basically this playbook will:

1. Create server profiles for all the servers in the stack – two Web servers and one load balancer. Servers will be configured and powered on, as defined in the server profile template.
2. Deploy the operating system using ICsp.
3. Deploy the application stack on the Web servers.
4. Install and configure the load balancer.
5. Deploy the application on the web servers behind the load balancer.

## Requirements

- Oneview 2.0 or 3.0 installed
- Server profile templates must be created for use by the playbook.
- Server hardware must be imported into OneView, so that OneView can deploy profiles on them.
- Insight Control Provisioning 7.4 or later must be installed (if you need to install the OS).
- Python >= 2.7.9
- Ansible >= 2.0.2
- HPE OneView Python SDK must be installed - available at: https://github.com/HewlettPackard/python-hpOneView.
- HPE ICsp installed - available at: `dependencies/python-hpICsp`.

## Running the example

### Inventory

The `demo` folder contains the Ansible inventory definitions.

If you wish, you can create a copy of the demo folder for a test environment that you want to operate.
Then, update the `hosts` file and provide the names of the servers you want to deploy – for this example, Web servers and load balancers.

### Variables and settings

`demo/group_vars` contains some global definitions like the profile template, ICsp preferences, etc.

You should update the `demo/group_vars/all` and set the variables to match your test environment. Specify the ICsp hostname and credentials (if you are using ICsp).

Feel free to customize any argument – or remove them if using defaults.

:lock: Tip: Check file permissions of the files inside the directory `demo/group_vars` since the passwords are stored in clear-text.

### Custom Attributes

In the `demo/group_vars/all` file, you'll find the `osbp_custom_attributes` map. In the custom attributes map, you can specify any data that you would like to pass into your ICsp build plan scripts or configuration files. For example, to specify a list of trusted public keys to be placed into the node's .ssh/authorized_keys file, add a custom attribute to the map:

```yaml
osbp_custom_attributes:
  - SSH_CERT: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
```

Then create/modify a custom build script in ICsp that will do something with this data. To access it, use the format: `@variable_name@` or `@variable_name:default_value@`. For our example, we could do something like:

```bash
#!/bin/bash
authorized_keys="@SSH_CERT@"
if [ -n "$authorized_keys" ]; then
  mkdir -p /root/.ssh/
  touch /root/.ssh/authorized_keys
  echo -e "$authorized_keys" > /root/.ssh/authorized_keys
fi
```

This example passes the SSH keys from the current system to the ICsp build plan, so Ansible can pass the SSH keys into the newly deployed nodes.

### OneView Appliance Connection

**NOTE:** You should specify the HPE OneView hostname and credentials on a file. A sample configuration file is provided within the examples directory. To use it, execute the following steps:

1. `cd` into the `examples` directory.
2. Copy the `oneview_config-rename.json` file into a new file named `oneview_config.json`.
3. Modify the file inserting your credentials, OneView appliance IP or hostname.

:lock: Tip: Check the oneview_config.json file permissions, since the password is stored in clear-text.

To execute the playbook, run:

```$ ansible-playbook -i demo/hosts ov_site.yml```
