#!/bin/bash

###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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

COLOR_START="[01;34m"
COLOR_SUCCESS="\e[32m"
COLOR_FAILURE="\e[31m"
COLOR_END="[00m"

exit_code_build_oneview_ansible=0
exit_code_module_validation=0
exit_code_playbook_validation=0
exit_code_tests=0
exit_code_flake8=0


print_summary () {
  if [ $2 -eq 0 ]; then
    echo -e "  ${COLOR_SUCCESS}$1: ok${COLOR_END}"
  else
    echo -e "  ${COLOR_FAILURE}$1: failed${COLOR_END}"
    exit_code_build_oneview_ansible=$((${exit_code_build_oneview_ansible}+1))
  fi
}

validate_modules () {
  if hash ansible-validate-modules 2>/dev/null; then
    while read -r line
    do
      if [[ "$line" =~ "GPLv3" ]]; then
        echo "IGNORED ERROR: GPLv3 license header not found"
      else
        if [[ "$line" =~ "ERROR:" || "$line" =~ "IGNORE:" ]]; then
          exit_code_module_validation=1
        fi
        echo "$line"
      fi
    done < <(ansible-validate-modules library)
  else
    echo "ERROR: ansible-validate-modules is not installed."
    exit_code_module_validation=1
  fi
}

if [ -z ${ANSIBLE_LIBRARY+x} ]; then
  echo "ANSIBLE_LIBRARY is unset. Your build exited with 1."
  exit 1
fi

echo -e "\n${COLOR_START}Validating modules${COLOR_END}"
validate_modules

echo -e "\n${COLOR_START}Validating playbooks${COLOR_END}"
ansible-playbook -i "localhost," --syntax-check examples/*.yml
exit_code_playbook_validation=$?

echo -e "\n${COLOR_START}Running tests${COLOR_END}"
python -m unittest discover
exit_code_tests=$?

echo -e "\n${COLOR_START}Running flake8${COLOR_END}"
if hash ansible-validate-modules 2>/dev/null; then
  flake8 library test --max-line-length=120 --ignore=F403
  exit_code_flake8=$?
else
  echo "ERROR:flake8 is not installed."
  exit_code_flake8=1
fi

echo -e "\n=== Summary =========================="
print_summary "Modules validation" ${exit_code_module_validation}
print_summary "Playboks validation" ${exit_code_playbook_validation}
print_summary "Unit tests" ${exit_code_tests}
print_summary "Flake8" ${exit_code_flake8}

echo "Done. Your build exited with ${exit_code_build_oneview_ansible}."
exit ${exit_code_build_oneview_ansible}
