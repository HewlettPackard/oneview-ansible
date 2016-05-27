import unittest
import mock
from fc_network import main


def create_fc_network_will_raise(message):
    mock_client = mock.Mock()
    mock_client.fc_networks.create.side_effect = Exception(message)
    return mock_client


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


ERROR_MESSAGE = 'mocked error'

PARAMS = dict(
    oneview_host="oneview_host",
    username="username",
    password="password",
    state='present',
    template=dict(name='New FC Network 2')
)

class FcNetworkErrorHandlingSpec(unittest.TestCase):

    @mock.patch('fc_network.OneViewClient')
    @mock.patch('fc_network.AnsibleModule')
    @mock.patch('fc_network.get_by_name')
    def test_should_not_update_when_create_raises_exception(self, mock_get_by_name, mock_ansible_module, mock_ov_client):
        mock_get_by_name.return_value = []
        mock_ov_client.return_value = create_fc_network_will_raise(ERROR_MESSAGE)
        mock_ansible_instance = create_ansible_mock(PARAMS)
        mock_ansible_module.return_value = mock_ansible_instance

        self.assertRaises(Exception, main())
        mock_ansible_instance.fail_json.assert_called_once_with(msg=ERROR_MESSAGE)


if __name__ == '__main__':
    unittest.main()
