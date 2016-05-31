#!/bin/bash

COLOR_START="[01;34m"
COLOR_SUCCESS="\e[32m"
COLOR_FAILURE="\e[31m"
COLOR_END="[00m"
exit_code_build_oneview_ansible=0

print_summary () {
  if [ $2 -eq 0 ]
  then
    echo -e "  ${COLOR_SUCCESS}$1: ok${COLOR_END}"
  else
    echo -e "  ${COLOR_FAILURE}$1: failed${COLOR_END}"
    exit_code_build_oneview_ansible=$((${exit_code_build_oneview_ansible}+1))
  fi
}

if [ -z ${ANSIBLE_LIBRARY+x} ]
then
  echo "ANSIBLE_LIBRARY is unset. Your build exited with 1."
  exit 1
fi

echo -e "${COLOR_START}Validating modules${COLOR_END}"
ansible-validate-modules library
exit_code_module_validation=$?

echo -e "${COLOR_START}Validating playbooks${COLOR_END}"
ansible-playbook -i "localhost," --syntax-check examples/*.yml
exit_code_playbook_validation=$?

echo -e "${COLOR_START}Running tests${COLOR_END}"
python -m unittest discover
exit_code_tests=$?

echo -e "${COLOR_START}Running flake8${COLOR_END}"
flake8 library test
exit_code_flake8=$?

echo -e "\n=== Summary =========================="
print_summary "Modules validation" ${exit_code_module_validation}
print_summary "Playboks validation" ${exit_code_playbook_validation}
print_summary "Unit tests" ${exit_code_tests}
print_summary "Flake8" ${exit_code_flake8}

echo "Done. Your build exited with ${exit_code_build_oneview_ansible}."
exit ${exit_code_build_oneview_ansible}
