#!/usr/bin/python
from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient


FC_NETWORK_CREATED = 'FC Network created sucessfully.'
FC_NETWORK_ALREADY_EXIST = 'FC Network already exists.'


def create(oneview_client, template):
    new_fc_network = None
    try:
        new_fc_network = oneview_client.fc_networks.create(template)
        msg = FC_NETWORK_CREATED
        failed = False
    except Exception as e:
        msg = e.message
        failed = True

    return msg, new_fc_network, failed


def present(oneview_client, template):
    changed = False
    failed = False
    result = get_by_name(oneview_client, template)

    if not result:
        msg, fc_network, failed = create(oneview_client, template)
        changed = not failed
    else:
        msg = FC_NETWORK_ALREADY_EXIST
        fc_network = result[0]

    facts = dict(fc_network=fc_network)
    return changed, msg, facts, failed


def get_by_name(oneview_client, template):
    result = oneview_client.fc_networks.get_by('name', template['name'])
    return result


def create_arguments():
    return dict(
        oneview_host = dict(required=True, type='str'),
        username = dict(required=True, type='str'),
        password = dict(required=True, type='str'),
        state = dict(
            required= True,
            choices= [ 'present', 'absent' ]
        ),
        template = dict(required=True, type='dict')
    )


def create_config(module):
    return dict(
        ip = module.params['oneview_host'],
        credentials=dict(
            userName = module.params['username'],
            password = module.params['password']
        )
    )


def main():
    module = AnsibleModule(argument_spec=create_arguments(),
        supports_check_mode=False)

    config = create_config(module)
    state = module.params['state']
    template = module.params['template']

    oneview_client = OneViewClient(config)

    if (state != 'present'):
        module.exit_json(changed=False)
    else:
        changed, message, facts, failed = present(oneview_client, template)
        module.exit_json(changed=changed, msg=message, ansible_facts=facts,
            failed=failed)


if __name__ == '__main__':
  main()
