# Testing 'oneview-ansible' modules
The 'oneview-ansible' modules require tests to accompany the code being delivered, ensuring higher quality, and also helping to avoid minor mistakes and future regressions.

## Executing tests
The tests can be executed by executing the `build.sh` file that consolidates everything that needs to be tested at once.

If needed it is possible to execute each individual testing or checking task by using its specific tools.

### PEP-8 compliance
This code is mostly PEP-8 compliant, it follows the Ansible standard, so to validate it you may use the `flake8` tool with some restrictions:
```shell
$ flake8 library test --max-line-length=160 --ignore=F401,E402,F403,F405
```

### Playbooks and Module validations
The validation in the modules and playbooks can be achieved by using the Ansible `validate-modules`:
```shell
$ git clone -b stable-2.4--single-branch https://github.com/ansible/ansible.git;
$ source ./ansible/hacking/env-setup;
$ <ANSIBLE_HOME>/test/sanity/validate-modules/validate-modules "<path-to-ansible-modules>/library/*.py"
```

To validate playbooks you may use the `ansible-playbook` tool with `--syntax-check` tag:
```shell
$ ansible-playbook -i "localhost," --syntax-check examples/*.yml
```

### Executing unit tests
All unit tests are inside the test folder. You can execute them manually by using your desired tool, like `python`, `pytest` or `nosetests`.

## Implementing tests
All code must have associated tests, be it the already implemented or newly submitted, and this section covers what tests need to be implemented.

### Implementing the unit tests
The unit tests are required for each new resource, bug fix or enhancement. They must cover what is being submitted and if necessary use the `mock` to mock OneView appliance communication.

### Acceptance criteria
The necessary amount of testing is defined by who is implementing and by who is reviewing and accepting the code, however, the unit test coverage is inspected by the coveralls and it won't allow it to drop.
