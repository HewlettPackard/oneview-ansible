##############################################################################
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# File Name: Update-UserScript.py
# VERSION 1.0
# Usage: python Update-UserScript.py <SDK_REPO_PATH>
#
# This script can be used independently from the hpeOneView 5.4.0 library to
# parse a user script and update all legacy hpeOneView brand names from
# hpOneView to hpeOneView, and any reference to HPOneView to HPEOneView.
#
##############################################################################
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
# 
##############################################################################

import re
import os
import sys

self_name = sys.argv[0]
path = sys.argv[1] # Fetch the SDK repository path from cmd line
search_pattern1 = re.compile('hpOneView')
search_string1 = 'hpOneView'
replace_string1 = 'hpeOneView'
search_pattern2 = re.compile('HPOneView')
search_string2 = 'HPOneView'
replace_string2 = 'HPEOneView'

source = os.path.join(path, search_string1)
destination = os.path.join(path, replace_string1)

# Changing the module directory name if not renamed
if os.path.isdir(source):
    os.rename(source, destination)

print("\n\t>>> STARTING THE DE-BRANDING TASK...<<< \n") 


# Replacing the old module name with new name
def replacement(path, search_pattern, replace_string, search_string):
    for dirpath, dirname, filename in os.walk(path):                 # Getting a list of the full paths of files
        for fname in filename:
            path = os.path.join(dirpath, fname)                      # Join dirpath and filenames

            # ignore unecessary files
            if fname.endswith('.pyc') or fname.endswith('.png') or fname.endswith('.gz') or fname.endswith('doctree') \
                or fname.endswith('.zip') or '.git' in dirpath or '.tox' in dirpath or search_string1 in dirpath or self_name == fname:
                continue
            try:
                strg = open(path).read()                                 # Open the files for read only
                if re.search(search_pattern, strg):
                    strg_count = strg.count(search_string)
                    print("Found '{}' {} times in '{}'".format(search_string, strg_count, path))
                    strg = strg.replace(search_string, replace_string)   # Create the replacement condition
                    f = open(path, 'w')                                  # open the file with the WRITE option
                    f.write(strg)                                        # write the the changes to the file
                    f.close()                                            # Closing the file


replacement(path, search_pattern1, replace_string1, search_string1)
replacement(path, search_pattern2, replace_string2, search_string2)

print("\n\t>>> FINISHED THE DE-BRANDING TASK...<<< \n")
