#!/usr/bin/python
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
from ansible.module_utils.basic import *
from ansible.utils import module_docs
from fnmatch import fnmatch
import os
import yaml

DOCUMENTATION = '''
---
module: ansible_module_documentation
short_description: Create markdown file for Ansible Modules documentation.
description:
    - It allows to generate a markdown file extracting the documentation from the ansible modules of a
      given folder. It performs a recursive search in all subfolders and files.
requirements:
    - "python >= 2.7.9"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    path:
        description:
            - Absolute path where the Ansible Modules are located.
        required: true
    exclusion_filters:
        description:
            - "A list of filters to skip files from the documentation reading, it accepts Unix wildcards.
               Examples: ['*icsp*', '__init__.py']"
        required: false
'''

EXAMPLES = '''
# Step 1, exctract the docs variables
- name: Extract documentation, examples and returns from the Ansible modules
  ansible_module_documentation:
    path: '/home/user/oneview-ansible/library'
    exclusion_filters: ['*icsp*', '__init__.py']
  register: result
- debug: var=result.errors

# Step 2, Apply the retrieved data to the template
- name: Build the markdown file
  template:
    src: 'oneview_ansible_documentation.j2'
    dest: '~/oneview-ansible.md'
'''

RETURN = '''
modules_docs:
    description: Has a list with all modules documentation.
    returned: Always, but can be empty.
    type: complex

errors:
    description: Has a list of errors that occurred while extracting the documentation.
    returned: Always, but can be empty.
    type: complex
'''


def main():
    argument_spec = {
        "path": {
            "required": True,
            "type": 'str'
        },
        "exclusion_filters": {
            "required": False,
            "type": 'list'
        }
    }

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    root_path = module.params['path']
    root_path = os.path.abspath(root_path)

    if not os.path.isdir(root_path):
        module.fail_json(msg=root_path + " is not a directory or not exists.")

    exclusion_filters = module.params['exclusion_filters']

    doc_list = list()
    errors = list()

    for root, dirs, files in os.walk(root_path):
        for file_name in sorted(files):
            # Skips all non python files
            if not fnmatch(file_name, "*.py"):
                continue

            # Skips according exclusion_filters
            if check_exclusion(file_name, exclusion_filters):
                continue

            try:
                module_file_name = os.path.normpath(os.path.join(root, file_name))

                doc, plainexamples, returndocs = module_docs.get_docstring(module_file_name)

                if doc:
                    if plainexamples:
                        doc['examples'] = plainexamples.split('\n')

                    if returndocs:
                        try:
                            doc['returns'] = yaml.load(returndocs)
                        except Exception as e:
                            errors.append("{0} - Failed yaml.load(doc['returns']) - {1}".format(file_name, e.args[0]))

                    doc_list.append(doc)
                else:
                    errors.append(file_name + " - No docs found")

            except Exception as ex:
                errors.append("{0} - {1}".format(file_name, ex.args[0]))

    module.exit_json(modules_docs=doc_list, errors=errors)


def check_exclusion(file_name, exclusion_filters):
    if exclusion_filters:
        for pattern in exclusion_filters:
            if fnmatch(file_name, pattern):
                return True
    return False


if __name__ == '__main__':
    main()
