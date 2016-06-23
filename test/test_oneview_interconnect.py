###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
import unittest
import mock

from hpOneView.oneview_client import OneViewClient
from oneview_interconnect import InterconnectModule


def create_params_for(power_state):
    return dict(
        config='config.json',
        state=power_state,
        id='e542bdab-c75f-4cf2-b89e-9a566849e292'
    )


def create_ansible_mock(params):
    mock_params = mock.Mock()
    mock_params.__getitem__ = mock.Mock(side_effect=lambda name: params[name])

    mock_ansible = mock.Mock()
    mock_ansible.params = mock_params
    return mock_ansible


class InterconnectPowerStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_powered_on_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.patch.return_value = dict()

        params_for_powered_on = create_params_for('powered_on')

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_for_powered_on)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=params_for_powered_on['id'],
            operation='replace',
            path='/powerState',
            value='On'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(resource=dict())
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_powered_off_state(self, mock_ansible_module, mock_ov_client_from_json_file):
        mock_ov_instance = mock.Mock()
        mock_ov_instance.interconnects.patch.return_value = dict()

        params_for_power_off = create_params_for('powered_off')

        mock_ov_client_from_json_file.return_value = mock_ov_instance
        mock_ansible_instance = create_ansible_mock(params_for_power_off)
        mock_ansible_module.return_value = mock_ansible_instance

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=params_for_power_off['id'],
            operation='replace',
            path='/powerState',
            value='Off'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(resource=dict())
        )


if __name__ == '__main__':
    unittest.main()
