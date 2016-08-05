# Examples

This directory contains everything you need to start provisioning with OneView and Ansible.

## Running the sample playbooks

**Requirements:** To run these examples you need to execute the [Ansible OneView Setup.](https://github.com/HewlettPackard/oneview-ansible/#ansible-oneview-sdk-setup)

**NOTE:** A sample configuration file is provided within the examples directory. To use it, execute the following steps:

1. `cd` into the `examples` directory.
2. Copy the `oneview_config-rename.json` file into a new file named `oneview_config.json`.
3. Modify the file inserting your credentials, OneView appliance IP or hostname, and anything else that your environment requires.
4. Some playbooks like `oneview_enclosure`, for example, need specific configurations. These are set in the `var/config.yml` file. To create the file, you should:
  1. `cd` into the `examples/vars` directory.
  2. Copy the `config.yml.rename` file into a new file named `config.yml`.
  3. Set the variables according to your environment.

:lock: Tip: Check the `oneview_config.json` file permissions, since the password is stored in clear-text.

To run an Ansible playbook, execute the following command:

`ansible-playbook -i <path_to_inventory_file> <example_file>.yml`
