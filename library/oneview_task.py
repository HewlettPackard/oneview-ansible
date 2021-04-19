#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
module: oneview_task_facts
short_description: Retrieve facts about the OneView Tasks.
description:
    - Retrieve facts about the OneView Tasks.
version_added: "2.4"
requirements:
    - "python >= 3.4.0"
    - "hpeOneView >= 6.1.0"
author: "Yuvarani Chidambaram (@yuvirani)"
options:
    state:
       required: True
       choices: update - Set the task state to cancelling 
       type: dict
    data:
       required: True
       type: dict
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
tasks: 
    - name: Gather facts about the tasks
      oneview_task_facts:
        config: "{{ config }}"
        params:
          count: 2
      delegate_to: localhost

    - debug: var=tasks

    - name: Sets the state of task to cancelling
      oneview_task:
        config: "{{ config }}"
        state: update
        data:
          name: "{{ tasks[0]['name'] }}"
          task: "{{ tasks[0] }}"
          isCancellable: False
      delegate_to: localhost

'''

RETURN = '''
tasks:
    description: The updated task.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule, OneViewModuleTaskError


class TaskModule(OneViewModule):
    MSG_TASK_UPDATED = 'Task has been updated.'
    MSG_ALREADY_PRESENT = 'Task already updated.'

    def __init__(self):
        argument_spec = dict(
            data=dict(required=True, type='dict'),
            state=dict(
                required=True,
                choices=['update'])
        )

        super(TaskModule, self).__init__(additional_arg_spec=argument_spec)

        self.set_resource_object(self.oneview_client.tasks)

    def execute_module(self):
        changed = False

        if self.state == 'update':
           task_uri = self.data['task']['uri']
           task = self.oneview_client.tasks.get_by_id(task_uri.split('/')[-1])

           if task.data['isCancellable'] is False:
              try:
                 changed = True
                 self.current_resource.patch(operation='replace', path='/isCancellable', value=True)
              except OneViewModuleTaskError as task_error:
                 raise task_error

        if changed:
            msg = self.MSG_ALREADY_PRESENT
        else:
            msg = self.MSG_TASK_UPDATED

        return dict(
            changed=changed, 
            msg=msg,
            ansible_facts=dict(tasks=self.current_resource.data))


def main():
    TaskModule().run()


if __name__ == '__main__':
    main()
