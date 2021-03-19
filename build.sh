#!/bin/bash
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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

COLOR_START="[01;34m"
COLOR_SUCCESS="\e[32m"
COLOR_FAILURE="\e[31m"
COLOR_END="[00m"

exit_code_doc_generation=0
exit_code_build_oneview_ansible=0
exit_code_module_validation=0
exit_code_playbook_validation=0
exit_code_tests=0
exit_code_flake8=0
exit_code_coveralls=0

setup () {
  # Change the current path and set the environment variables
  echo "Changing current directory to: ${BASH_SOURCE%/*}"
  echo ${PYTHON_SDK}
  cd ${BASH_SOURCE%/*}
  export ANSIBLE_LIBRARY=library
  export ANSIBLE_MODULE_UTILS=$ANSIBLE_LIBRARY/module_utils

  if [ -z ${PYTHON_SDK+x} ]; then
    export PYTHON_SDK=../oneview-python
  fi

  export PYTHONPATH="test:$PYTHON_SDK:$ANSIBLE_LIBRARY:$PYTHONPATH"
}

update_doc_fragments () {
  # NOTE: Set the destination path to copy the oneview doc fragments in an env var named DOC_FRAGMENTS_PATH.
  # Otherwise, the destination will be defined automatically.
  local docfragments="build-doc/module_docs_fragments/oneview.py"

  if [ "$DOC_FRAGMENTS_PATH" ]; then
    cp -f $docfragments $DOC_FRAGMENTS_PATH
  else
    # Find site packages. If it exists, OneView doc fragment will be copied to the discovered path
    local site_packages=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
    if [ -d "${site_packages}/ansible/utils/module_docs_fragments/" ]; then
      cp -f $docfragments ${site_packages}/ansible/utils/module_docs_fragments/
    else
      # Copy OneView doc fragments to the Ansible codebase path
      local ansible_path=$(echo $(which ansible) | sed -e 's/\/bin\/ansible//g')
      if [ "$ansible_path" ]; then
        cp -f $docfragments ${ansible_path}/lib/ansible/utils/module_docs_fragments/
      fi
    fi
  fi
}

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
    local command="ansible-validate-modules library --exclude module_utils"
  elif [[ $ANSIBLE_HOME ]]; then
    local command="${ANSIBLE_HOME}/test/sanity/validate-modules/validate-modules library/*.py"
  else
    echo "WARNING: Skipping module validation. Unable to find 'ansible-validate-modules' or 'validate-modules'."
  fi

  if [[ $command ]]; then
    while read -r line
    do
      if [[ "$line" =~ "GPLv3" ]]; then
        continue
      else
        if [[ "$line" =~ "ERROR:" || "$line" =~ "IGNORE:" ]]; then
          exit_code_module_validation=1
        fi
        echo "$line"
      fi
    done < <($command)
  fi
}

setup
update_doc_fragments


echo -e "\n${COLOR_START}Validating modules${COLOR_END}"
validate_modules

echo -e "\n${COLOR_START}Validating playbooks${COLOR_END}"
ansible-playbook -i "localhost," --syntax-check examples/*.yml
exit_code_playbook_validation=$?


echo -e "\n${COLOR_START}Running flake8${COLOR_END}"
if hash flake8 2>/dev/null; then
  flake8 library test --max-line-length=160 --ignore=F401,E402,F403,F405
  exit_code_flake8=$?
else
  echo "ERROR:flake8 is not installed."
  exit_code_flake8=1
fi

#Documentation is generated only in local builds
if [ -z "$TRAVIS" ]; then
  echo -e "\n${COLOR_START}Generating markdown documentation${COLOR_END}"
  build-doc/run-doc-generation.sh
  exit_code_doc_generation=$?

#Coveralls runs only when Travis is running the build
#else
#  echo -e "\n${COLOR_START}Running Coveralls${COLOR_END}"
#  coverage run --source=library/ -m pytest test/
#  coveralls
#  exit_code_coveralls=$?
fi


echo -e "\n${COLOR_START}Running tests${COLOR_END}"
#python -m pytest test/
pytest --cov-report= xml:coverage.xml --cov=library test/
exit_code_tests=$?

echo -e "\n=== Summary =========================="
print_summary "Modules validation" ${exit_code_module_validation}
print_summary "Playbooks validation" ${exit_code_playbook_validation}
print_summary "Unit tests" ${exit_code_tests}
print_summary "Flake8" ${exit_code_flake8}
print_summary "Doc Generation" ${exit_code_doc_generation}
print_summary "Coveralls" ${exit_code_coveralls}

echo "Done. Your build exited with ${exit_code_build_oneview_ansible}."
exit ${exit_code_build_oneview_ansible}
