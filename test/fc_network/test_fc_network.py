import unittest
import mock

from hpOneView import oneview_client
from fc_network import FcNetworkModule
from fc_network import FC_NETWORK_CREATED, FC_NETWORK_ALREADY_EXIST


FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
    connectionTemplateUri=None,
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    oneview_host="oneview_host",
    username="username",
    password="password",
    state='present',
    template=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)

def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class FcNetworkPresentStateSpec(unittest.TestCase):

    @mock.patch('fc_network.OneViewClient')
    @mock.patch('fc_network.AnsibleModule')
    def test_should_create_new_fc_network(self, mock_ansible_module, mock_ov_client):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = []
        mock_ov_instance.fc_networks.create.return_value = DEFAULT_FC_NETWORK_TEMPLATE

        mock_ov_client.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            msg=FC_NETWORK_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    @mock.patch('fc_network.OneViewClient')
    @mock.patch('fc_network.AnsibleModule')
    def test_should_not_update_when_fc_network_already_exist(self, mock_ansible_module, mock_ov_client):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]

        mock_ov_client.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        FcNetworkModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            msg=FC_NETWORK_ALREADY_EXIST,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )


class FcNetworkErrorHandlingSpec(unittest.TestCase):

    @mock.patch('fc_network.OneViewClient')
    @mock.patch('fc_network.AnsibleModule')
    def test_should_not_update_when_create_raises_exception(self, mock_ansible_module, mock_ov_client):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.fc_networks.get_by.return_value = []
        mock_ov_instance.fc_networks.create.side_effect = Exception(FAKE_MSG_ERROR)

        mock_ov_client.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(PARAMS_FOR_PRESENT)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, FcNetworkModule().run())

        mock_ansible_instance.fail_json.assert_called_once_with(
            msg=FAKE_MSG_ERROR
        )


if __name__ == '__main__':
    unittest.main()
