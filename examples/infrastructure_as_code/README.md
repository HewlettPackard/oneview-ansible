# Infrastructure as code with HPE OneView and Ansible

Ansible playbooks to provision bare metal infrastructure with [HPE OneView](https://hpe.com/info/oneview) and the [oneview-ansible](https://github.com/HewlettPackard/oneview-ansible) module.

## Use case

Configure a hardware server with boot settings and a network connection, then boot the server.

## Running the sample

* Edit `oneview-config.json` and provide the IP address and credentials for OneView.
* Edit `infrastructure-config.yml` Provide names for the server profile template and server profile that will be created. Provide the names of the enclosure group, hardware server type, hardware server, and network that will be provisioned.
* Run the playbook that will create the server profile template:

```console
ansible-playbook server_profile_template.yml
```

* Run the playbook that will create a server profile, provision the hardware, and boot the server:

```console
ansible-playbook server_profile.yml
```

In the spirit of "Leave no Trace", the playbook `clean.yml` will remove all artifacts.
