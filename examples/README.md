# Examples

Execute an Ansible playbook to test functionalities of individual resources.

**NOTE:** To run these examples you will need to [configure the Ansible OneView.](https://github.hpe.com/Rainforest/oneview-ansible/tree/readme#ansible-oneview-configuration)

To run an example:
  1. `cd` into this examples directory, then copy the `oneview_config-rename.json` file to a new file named `oneview_config.json`;
  2. Modify it by inserting your credentials and anything else your environment requires.
  3. Run `ansible-playbook -i <path_to_inventory_file> <example_file>.yml`


:lock: Tip: Check the `oneview_config.json` file permissions because the password is stored in clear-text.