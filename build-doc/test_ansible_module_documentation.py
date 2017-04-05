###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import sys
import os

# Workaround to run this test
sys.path.insert(0, os.path.dirname(__file__))

from ansible_module_documentation import format_dict


class AnsibleModuleDocumentationTest(unittest.TestCase):
    DICT_WITH_FORMATTING = {
        "key1": {
            "key1.key1": "List with params X(parentheses): C(count), C(fields) and C(view)."},
        "key2": [
            "",
            {'k2.l2': '1'},
            {'k2.l3':
                 {'l3.k1':
                      {'l3.k1.l1':
                           ['C(test)',
                            None]
                       }
                  }
             },
            "More format: C(count) C(without end"],
        "key3": '',
        "key4": None,
        "key5": False,
        "key6": 1,
        "key7": "Test I(Italic), C(highlight), U(http://teste.com)"
    }

    def test_resource_compare_equals(self):
        ret = format_dict(self.DICT_WITH_FORMATTING)

        self.assertEqual(ret,
                         {'key1': {'key1.key1': 'List with params X(parentheses): `count`, `fields` and `view`.'},
                          'key2': ['',
                                   {'k2.l2': '1'},
                                   {'k2.l3': {'l3.k1': {'l3.k1.l1': ['`test`', None]}}},
                                   'More format: `count` C(without end'],
                          'key3': '',
                          'key4': None,
                          'key5': False,
                          'key6': 1,
                          'key7': "Test _Italic_, `highlight`, http://teste.com"}
                         )
