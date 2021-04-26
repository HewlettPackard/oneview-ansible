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
    - name: Gather facts about the last 5 running tasks
      oneview_task_facts:
        config: "{{ config }}"
        params:
          count: 5
          view: "tree"
          filter: ["taskState='Running'", "isCancellable=true"]
      delegate_to: localhost

    - debug: var=tasks

    - name: Sets the state of task to 'Cancelling'
      oneview_task:
        config: "{{ config }}"
        data:
          name: "{{ tasks[0]['name'] }}"
          uri: "{{ tasks[0]['uri'] }}"
      delegate_to: localhost
      when: contents.api_version >= 1200 and ( tasks | length > 0 )
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
    MSG_RESOURCE_NOT_FOUND = 'Task Resource not found.'

    def __init__(self):
        argument_spec = dict(
            data=dict(required=True, type='dict')
        )

        super(TaskModule, self).__init__(additional_arg_spec=argument_spec)

        self.set_resource_object(self.oneview_client.tasks)

    def execute_module(self):
        self.current_resource.patch(self.data['uri'])

        return dict(
            changed=True,
            msg=self.MSG_TASK_UPDATED,
            ansible_facts=dict(tasks=self.current_resource.data))


def main():
    TaskModule().run()


if __name__ == '__main__':
    main()
