# Testing 'oneview-ansible' modules
The 'oneview-ansible' modules require tests to accompany the code being delivered, ensuring higher quality, and also helping to avoid minor mistakes and future regressions.

## Executing tests
The tests can be executed by executing the `build.sh` file that consolidates everything that needs to be tested at once.

If needed it is possible to execute each individual testing or checking task by using its specific tools.

### PEP-8
This code is PEP-8 compliant, so to validate it you may use the `flake8` tool.

### Playbooks and Module validations
The validation in the modules and playbooks can be achieved by using the Ansible `validate-modules` and the `ansible-playbook` with `--syntax-check` tag.

### Unit tests
All unit tests are inside the test folder. You can execute them manually by using your desired tool, like `pytest` or `nosetests`.

## Implementing tests
All code must have associated tests, be it the already implemented or newly submitted, and this section covers what tests need to be implemented.

### Unit tests
The unit tests are required for each new resource, bug fix, or enhancement. They must cover what is being submitted and if necessary use the `mock` to mock OneView appliance communication.

### Acceptance criteria
The necessary amount of testing is dictated by who is implementing and by who is reviewing and accepting the code, however, the unit test coverage is inspected by the coveralls and it won't allow it to drop.
