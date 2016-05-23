import unittest
import mock
from fc_network import main


class FakeModule(object):

    def __init__(self):
        self.called = False
        self.msg = ''

    def fail_json(self, msg):
        self.msg = msg
        self.called = True

    def fail_msg(self):
        return self.msg

    def was_called(self):
        return self.called


class FcNetworkErrorHandlingSpec(unittest.TestCase):

    @mock.patch('fc_network.OneViewClient')
    @mock.patch('fc_network.AnsibleModule')
    @mock.patch('fc_network.get_by_name')
    def test_should_not_update_when_create_raises_exception(self, mock_get_by_name, mock_ansible_module, mock_ov_client):
        mock_get_by_name.return_value = []
        error_message = 'mocked error'

        mock_client = mock.Mock()
        mock_client.fc_networks.create.side_effect = Exception(error_message)
        mock_ov_client.return_value = mock_client

        fakeModule = FakeModule()
        fakeModule.params = dict(
            oneview_host="oneview_host",
            username="username",
            password="password",
            state='present',
            template=dict(name= 'New FC Network 2')
        )

        mock_ansible_module.return_value = fakeModule

        self.assertRaises(Exception, main())
        self.assertTrue(fakeModule.was_called())
        self.assertEquals(error_message, fakeModule.fail_msg())


if __name__ == '__main__':
  unittest.main()
