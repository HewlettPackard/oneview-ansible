###
# Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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


def mock_oneview_instance(mock_ov_client):
    mock_ov_instance = mock.Mock()
    mock_ov_instance.interconnects.patch.return_value = dict()
    mock_ov_client.return_value = mock_ov_instance

    return mock_ov_instance


def mock_ansible_module_instance(ansible_arguments, mock_ansible_module):
    mock_ansible_instance = create_ansible_mock(ansible_arguments)
    mock_ansible_module.return_value = mock_ansible_instance

    return mock_ansible_instance


class InterconnectPowerStateSpec(unittest.TestCase):

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_powered_on_state(self, mock_ansible_module, mock_ov_from_file):
        ansible_arguments = create_params_for('powered_on')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        mock_ov_instance.interconnects.get.return_value = dict(powerState='Off')

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=ansible_arguments['id'],
            operation='replace',
            path='/powerState',
            value='On'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=dict())
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_return_changed_false_when_interconnect_is_already_powered_on(self,
                                                                                 mock_ansible_module,
                                                                                 mock_ov_from_file):
        ansible_arguments = create_params_for('powered_on')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        fake_interconnect = dict(powerState='On')
        mock_ov_instance.interconnects.get.return_value = fake_interconnect

        InterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_powered_off_state(self, mock_ansible_module, mock_ov_from_file):
        ansible_arguments = create_params_for('powered_off')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        mock_ov_instance.interconnects.get.return_value = dict(powerState='On')

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=ansible_arguments['id'],
            operation='replace',
            path='/powerState',
            value='Off'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=dict())
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_uid_on_state(self, mock_ansible_module, mock_ov_from_file):
        ansible_arguments = create_params_for('uid_on')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        mock_ov_instance.interconnects.get.return_value = dict(uidState='Off')

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=ansible_arguments['id'],
            operation='replace',
            path='/uidState',
            value='On'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=dict())
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_return_changed_false_when_uid_is_already_on(self,
                                                                mock_ansible_module,
                                                                mock_ov_from_file):
        ansible_arguments = create_params_for('uid_on')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        fake_interconnect = dict(uidState='On')
        mock_ov_instance.interconnects.get.return_value = fake_interconnect

        InterconnectModule().run()

        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    @mock.patch.object(OneViewClient, 'from_json_file')
    @mock.patch('oneview_interconnect.AnsibleModule')
    def test_should_ensure_uid_off_state(self, mock_ansible_module, mock_ov_from_file):
        ansible_arguments = create_params_for('uid_off')
        mock_ov_instance = mock_oneview_instance(mock_ov_from_file)
        mock_ansible_instance = mock_ansible_module_instance(ansible_arguments, mock_ansible_module)

        mock_ov_instance.interconnects.get.return_value = dict(uidState='On')

        InterconnectModule().run()

        mock_ov_instance.interconnects.patch.assert_called_with(
            id_or_uri=ansible_arguments['id'],
            operation='replace',
            path='/uidState',
            value='Off'
        )
        mock_ansible_instance.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=dict())
        )


if __name__ == '__main__':
    unittest.main()
