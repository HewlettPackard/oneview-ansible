#!/usr/bin/python
from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient


FC_NETWORK_CREATED = 'FC Network created sucessfully.'
FC_NETWORK_ALREADY_EXIST = 'FC Network already exists.'


def create(oneview_client, template):
    new_fc_network = oneview_client.fc_networks.create(template)
    return FC_NETWORK_CREATED, new_fc_network


def present(oneview_client, template):
    result = get_by_name(oneview_client, template)

    if not result:
        msg, fc_network = create(oneview_client, template)
        changed = True
    else:
        msg = FC_NETWORK_ALREADY_EXIST
        fc_network = result[0]
        changed = False

    facts = dict(fc_network=fc_network)

    return changed, msg, facts


def get_by_name(oneview_client, template):
    return oneview_client.fc_networks.get_by('name', template['name'])


def create_arguments():
    return dict(
        oneview_host=dict(required=True, type='str'),
        username=dict(required=True, type='str'),
        password=dict(required=True, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        template=dict(required=True, type='dict')
    )


def create_config(module):
    return dict(
        ip=module.params['oneview_host'],
        credentials=dict(
            userName=module.params['username'],
            password=module.params['password']
        )
    )


def main():
    module = AnsibleModule(argument_spec=create_arguments(),
                           supports_check_mode=False)

    config = create_config(module)
    state = module.params['state']
    template = module.params['template']

    oneview_client = OneViewClient(config)

    if state != 'present':
        module.exit_json(changed=False)
    else:
        try:
            changed, message, facts = present(oneview_client, template)
            module.exit_json(changed=changed, msg=message, ansible_facts=facts)
        except Exception as exception:
            module.fail_json(msg=exception.message)


if __name__ == '__main__':
    main()
