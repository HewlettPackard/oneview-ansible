#!/usr/bin/python
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

from __future__ import (absolute_import, division, print_function, unicode_literals)

import abc
import collections
import json
import logging
import os
import traceback

try:
    from hpeOneView.oneview_client import OneViewClient
    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False

try:
    from ansible.module_utils import six
    from ansible.module_utils._text import to_native
except ImportError:
    import six
    to_native = str

from ansible.module_utils.basic import AnsibleModule


# NOTE: VALIDATE IF REQUIRED
from copy import deepcopy
from collections import OrderedDict
# NOTE: VALIDATE IF REQUIRED


logger = logging.getLogger(__name__)  # Logger for development purposes only


def get_logger(mod_name):
    """
    To activate logs, setup the environment var LOGFILE
    e.g.: export LOGFILE=/tmp/ansible-oneview.log
    Args:
        mod_name: module name
    Returns: Logger instance
    """

    logger = logging.getLogger(os.path.basename(mod_name))
    global LOGFILE
    LOGFILE = os.environ.get('LOGFILE')
    if not LOGFILE:
        logger.addHandler(logging.NullHandler())
    else:
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            filename=LOGFILE, filemode='a')
    return logger


def transform_list_to_dict(list_):
    """
    Transforms a list into a dictionary, putting values as keys.

    :arg list list_: List of values
    :return: dict: dictionary built
    """

    ret = {}

    if not list_:
        return ret

    for value in list_:
        if isinstance(value, collections.Mapping):
            ret.update(value)
        else:
            ret[to_native(value)] = True

    return ret


# Makes a deep merge of 2 dictionaries and returns the merged dictionary
def dict_merge(original_resource_dict, data_dict):
    resource_dict = deepcopy(original_resource_dict)
    for key, val in data_dict.items():
        if not resource_dict.get(key):
            resource_dict[key] = val
        elif isinstance(resource_dict[key], dict) and isinstance(data_dict[key], collections.Mapping):
            resource_dict[key] = dict_merge(resource_dict[key], data_dict[key])
        elif isinstance(resource_dict[key], list) and isinstance(data_dict[key], list):
            resource_dict[key] = data_dict[key]
        else:
            resource_dict[key] = val

    return resource_dict


def merge_list_by_key(original_list, updated_list, key, ignore_when_null=None, replace_key=None, replace_value=None):
    """
    Merge two lists by the key. It basically:

    1. Adds the items that are present on updated_list and are absent on original_list.

    2. Removes items that are absent on updated_list and are present on original_list.

    3. For all items that are in both lists, overwrites the values from the original item by the updated item.

    :arg list original_list: original list.
    :arg list updated_list: list with changes.
    :arg str key: unique identifier.
    :arg list ignore_when_null: list with the keys from the updated items that should be ignored in the merge,
        if its values are null.
    :return: list: Lists merged.
    """
    ignore_when_null = [] if ignore_when_null is None else ignore_when_null

    if not original_list:
        return updated_list

    items_map = collections.OrderedDict([(i[key], i.copy()) for i in original_list])

    merged_items = collections.OrderedDict()

    for item in updated_list:
        item_key = item[key]
        if item_key in items_map:
            for ignored_key in ignore_when_null:
                if ignored_key in item and item[ignored_key] is None:
                    item.pop(ignored_key)
            if replace_key and item.get(replace_key) == replace_value:
                item[replace_key] = items_map[item_key][replace_key]
            merged_items[item_key] = items_map[item_key]
            merged_items[item_key].update(item)
            # merged_items[item_key] = dict_merge(merged_items[item_key], item)
        else:
            merged_items[item_key] = item

    return list(merged_items.values())


def _sort_by_keys(resource1, resource2):
    keys = ['name', 'enclosureIndex']

    if isinstance(resource1, list) and isinstance(resource1[0], dict):
        for key in keys:
            if key in resource1[0]:
                resource1 = sorted(resource1, key=lambda k: k[key])
                resource2 = sorted(resource2, key=lambda k: k[key])
    return resource1, resource2


def _str_sorted(obj):
    if isinstance(obj, collections.Mapping):
        return json.dumps(obj, sort_keys=True)
    else:
        return str(obj)


def _standardize_value(value):
    """
    Convert value to string to enhance the comparison.

    :arg value: Any object type.

    :return: str: Converted value.
    """
    if isinstance(value, float) and value.is_integer():
        # Workaround to avoid erroneous comparison between int and float
        # Removes zero from integer floats
        value = int(value)

    return str(value)


def compare(first_resource, second_resource):
    """
    Recursively compares dictionary contents equivalence, ignoring types and elements order.
    Particularities of the comparison:
        - Inexistent key = None
        - These values are considered equal: None, empty, False
        - Lists are compared value by value after a sort, if they have same size.
        - Each element is converted to str before the comparison.
    :arg dict first_resource: first dictionary
    :arg dict second_resource: second dictionary
    :return: bool: True when equal, False when different.
    """
    resource1 = first_resource
    resource2 = second_resource

    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)
    # The first resource is True / Not Null and the second resource is False / Null
    if resource1 and not resource2:
        logger.debug("resource1 and not resource2. " + debug_resources)
        return False

    # Checks all keys in first dict against the second dict
    for key in resource1:
        # compare uplinkset property logicalPortConfigInfos
        if key == 'logicalPortConfigInfos':
            if sort_by_uplink_set_location(resource1[key], resource2[key]):
                continue
            else:
                logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        if key not in resource2:
            if resource1[key] is not None:
                # Inexistent key is equivalent to exist with value None
                logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        # If both values are null, empty or False it will be considered equal.
        elif not resource1[key] and not resource2[key]:
            continue
        elif isinstance(resource1[key], collections.Mapping):
            # recursive call
            if not compare(resource1[key], resource2[key]):
                logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif isinstance(resource1[key], list):
            # change comparison function to compare_list
            if not compare_list(resource1[key], resource2[key]):
                logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif _standardize_value(resource1[key]) != _standardize_value(resource2[key]):
            logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
            return False

    # Checks all keys in the second dict, looking for missing elements
    for key in resource2.keys():
        if key not in resource1:
            if resource2[key] is not None:
                # Inexistent key is equivalent to exist with value None
                logger.debug(OneViewModuleBase.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False

    return True


def compare_list(first_resource, second_resource):
    """
    Recursively compares lists contents equivalence, ignoring types and element orders.
    Lists with same size are compared value by value after a sort,
    each element is converted to str before the comparison.
    :arg list first_resource: first list
    :arg list second_resource: second list
    :return: True when equal; False when different.
    """

    resource1 = first_resource
    resource2 = second_resource
    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)
    # The second list is null / empty  / False
    if not resource2:
        logger.debug("resource 2 is null. " + debug_resources)
        return False

    if len(resource1) != len(resource2):
        logger.debug("resources have different length. " + debug_resources)
        return False

    resource1 = sorted(resource1, key=_str_sorted)
    resource2 = sorted(resource2, key=_str_sorted)

    # sort resources by specific keys
    resource1, resource2 = _sort_by_keys(resource1, resource2)

    for i, val in enumerate(resource1):
        if isinstance(val, collections.Mapping):
            # change comparison function to compare dictionaries
            if not compare(val, resource2[i]):
                logger.debug("resources are different. " + debug_resources)
                return False
        elif isinstance(val, list):
            # recursive call
            if not compare_list(val, resource2[i]):
                logger.debug("lists are different. " + debug_resources)
                return False
        elif _standardize_value(val) != _standardize_value(resource2[i]):
            logger.debug("values are different. " + debug_resources)
            return False

    # no differences found
    return True


def sort_by_uplink_set_location(resource1, resource2):
    """
    Compares lists contents equivalence, sorting element orders.
    Inner dict elements(Bay, Enclosure, Port) are concatenated to compare unique values in the obj.
    :arg list resource1: first list of dicts
    :arg list resource2: second list of dicts
    :return: True when equal; False when different.
    """

    # Check first list elements
    for config_dict in resource1:
        location_entries = config_dict["logicalLocation"]["locationEntries"]

        # Append all types together ['Bay_3', 'Enclosure_1', 'Port_75']
        each_location = []
        for local_entry in location_entries:
            # Combine the values for comparison, 'Bay_3' if type='Bay' and relative value=3
            value = local_entry.get('type', '') + "_" + str(local_entry.get('relativeValue', ''))
            each_location.append(value)

        # Check second elements and add each entry in all_entries list
        all_entries = []
        for config_dict_res2 in resource2:
            location_entries_res2 = config_dict_res2["logicalLocation"]["locationEntries"]

            each_location_res2 = []
            for local_entry_res2 in location_entries_res2:
                value_res2 = local_entry_res2.get('type', '') + "_" + str(local_entry_res2.get('relativeValue', ''))
                each_location_res2.append(value_res2)

            if each_location_res2 not in all_entries:
                all_entries.append(sorted(each_location_res2))

        # Check first list element is present in second list
        if not sorted(each_location) in all_entries:
            return False

    return True


class OneViewModuleException(Exception):
    """
    OneView base Exception.

    Attributes:
       msg (str): Exception message.
       oneview_response (dict): OneView rest response.
   """

    def __init__(self, data):
        self.msg = None
        self.oneview_response = None

        if isinstance(data, six.string_types):
            self.msg = data
        else:
            self.oneview_response = data

            if data and isinstance(data, dict):
                self.msg = data.get('message')

        if self.oneview_response:
            Exception.__init__(self, self.msg, self.oneview_response)
        else:
            Exception.__init__(self, self.msg)


class OneViewModuleTaskError(OneViewModuleException):
    """
    OneView Task Error Exception.

    Attributes:
       msg (str): Exception message.
       error_code (str): A code which uniquely identifies the specific error.
    """

    def __init__(self, msg, error_code=None):
        super(OneViewModuleTaskError, self).__init__(msg)
        self.error_code = error_code


class OneViewModuleValueError(OneViewModuleException):
    """
    OneView Value Error.
    The exception is raised when the data contains an inappropriate value.

    Attributes:
       msg (str): Exception message.
    """
    pass


class OneViewModuleResourceNotFound(OneViewModuleException):
    """
    OneView Resource Not Found Exception.
    The exception is raised when an associated resource was not found.

    Attributes:
       msg (str): Exception message.
    """
    pass


# @six.add_metaclass(abc.ABCMeta)
class OneViewModule(object):
    MSG_CREATED = 'Resource created successfully.'
    MSG_UPDATED = 'Resource updated successfully.'
    MSG_DELETED = 'Resource deleted successfully.'
    MSG_ALREADY_PRESENT = 'Resource is already present.'
    MSG_ALREADY_ABSENT = 'Resource is already absent.'
    MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '
    MSG_MANDATORY_FIELD_MISSING = 'Missing mandatory field: name'
    HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'

    ONEVIEW_COMMON_ARGS = dict(
        api_version=dict(type='int'),
        config=dict(type='path'),
        hostname=dict(type='str'),
        image_streamer_hostname=dict(type='str'),
        password=dict(type='str', no_log=True),
        username=dict(type='str'),
        auth_login_domain=dict(type='str')
    )

    ONEVIEW_VALIDATE_ETAG_ARGS = dict(validate_etag=dict(type='bool', default=True))

    def __init__(self, additional_arg_spec=None, validate_etag_support=False):
        """
        OneViewModuleBase constructor.

        :arg dict additional_arg_spec: Additional argument spec definition.
        :arg bool validate_etag_support: Enables support to eTag validation.
        """
        argument_spec = self._build_argument_spec(additional_arg_spec, validate_etag_support)

        self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

        self.resource_client = None
        self.current_resource = None

        self.state = self.module.params.get('state')
        self.data = self.module.params.get('data')

        self._check_hpe_oneview_sdk()
        self._create_oneview_client()

        # Preload params for get_all - used by facts
        self.facts_params = self.module.params.get('params') or {}

        # Preload options as dict - used by facts
        self.options = transform_list_to_dict(self.module.params.get('options'))

        self.validate_etag_support = validate_etag_support

    def _build_argument_spec(self, additional_arg_spec, validate_etag_support):

        merged_arg_spec = dict()
        merged_arg_spec.update(self.ONEVIEW_COMMON_ARGS)

        if validate_etag_support:
            merged_arg_spec.update(self.ONEVIEW_VALIDATE_ETAG_ARGS)

        if additional_arg_spec:
            merged_arg_spec.update(additional_arg_spec)

        return merged_arg_spec

    def _check_hpe_oneview_sdk(self):
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=self.HPE_ONEVIEW_SDK_REQUIRED)

    def _create_oneview_client(self):
        if self.module.params.get('hostname'):
            config = dict(ip=self.module.params['hostname'],
                          credentials=dict(userName=self.module.params['username'], password=self.module.params['password'],
                                           authLoginDomain=self.module.params.get('auth_login_domain', '')),
                          api_version=self.module.params['api_version'],
                          image_streamer_ip=self.module.params['image_streamer_hostname'])
            self.oneview_client = OneViewClient(config)
        elif not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    def set_resource_object(self, resource_client, name=None):
        self.resource_client = resource_client
        uri = None

        if self.data:
            if self.data.get("name"):
                name = self.data["name"]
            elif self.data.get("uri"):
                uri = self.data["uri"]

        if not name and not uri:
            if self.module.params.get("name"):
                name = self.module.params["name"]
            elif self.module.params.get("uri"):
                uri = self.module.params["uri"]

        if name:
            self.current_resource = self.resource_client.get_by_name(name)
        elif uri:
            self.current_resource = self.resource_client.get_by_uri(uri)

    @abc.abstractmethod
    def execute_module(self):
        """
        Abstract method, must be implemented by the inheritor.

        This method is called from the run method. It should contain the module logic

        :return: dict: It must return a dictionary with the attributes for the module result,
            such as ansible_facts, msg and changed.
        """
        pass

    def run(self):
        """
        Common implementation of the OneView run modules.

        It calls the inheritor 'execute_module' function and sends the return to the Ansible.

        It handles any OneViewModuleException in order to signal a failure to Ansible, with a descriptive error message.

        """
        try:
            if self.validate_etag_support:
                if not self.module.params.get('validate_etag'):
                    self.oneview_client.connection.disable_etag_validation()

            result = self.execute_module()

            if not result:
                result = {}

            if "changed" not in result:
                result['changed'] = False

            self.module.exit_json(**result)

        except OneViewModuleException as exception:
            error_msg = '; '.join(to_native(e) for e in exception.args)
            self.module.fail_json(msg=error_msg, exception=traceback.format_exc())

    def resource_absent(self, method='delete'):
        """
        Generic implementation of the absent state for the OneView resources.

        It checks if the resource needs to be removed.

        :arg str method: Function of the OneView client that will be called for resource deletion.
            Usually delete or remove.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if self.current_resource:
            getattr(self.current_resource, method)()

            return {"changed": True, "msg": self.MSG_DELETED}
        else:
            return {"changed": False, "msg": self.MSG_ALREADY_ABSENT}

    def get_by_name(self, name):
        """
        Generic get by name implementation.

        :arg str name: Resource name to search for.

        :return: The resource found or None.
        """
        result = self.resource_client.get_by('name', name)
        return result[0] if result else None

    def resource_present(self, fact_name, create_method='create'):
        """
        Generic implementation of the present state for the OneView resources.

        It checks if the resource needs to be created or updated.

        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg str create_method: Function of the OneView client that will be called for resource creation.
            Usually create or add.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        changed = False

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        if not self.current_resource:
            self.current_resource = getattr(self.resource_client, create_method)(self.data)
            msg = self.MSG_CREATED
            changed = True
        else:
            changed, msg = self._update_resource()

        data = self.current_resource.data
        return dict(
            msg=msg,
            changed=changed,
            ansible_facts={fact_name: data}
        )

    def _update_resource(self):
        updated_data = self.current_resource.data.copy()
        updated_data = dict_merge(updated_data, self.data)
        changed = False

        if compare(self.current_resource.data, updated_data):
            msg = self.MSG_ALREADY_PRESENT
        else:
            self.current_resource.update(updated_data)
            changed = True
            msg = self.MSG_UPDATED

        return (changed, msg)

    def resource_scopes_set(self, state, fact_name, scope_uris):
        """
        Generic implementation of the scopes update PATCH for the OneView resources.
        It checks if the resource needs to be updated with the current scopes.
        This method is meant to be run after ensuring the present state.
        :arg dict state: Dict containing the data from the last state results in the resource.
            It needs to have the 'msg', 'changed', and 'ansible_facts' entries.
        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg list scope_uris: List with all the scope URIs to be added to the resource.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if scope_uris is None:
            scope_uris = []

        resource = state['ansible_facts'][fact_name]

        if resource.get('scopeUris') is None or set(resource['scopeUris']) != set(scope_uris):
            operation_data = dict(operation='replace', path='/scopeUris', value=scope_uris)
            updated_resource = self.current_resource.patch(**operation_data)
            state['ansible_facts'][fact_name] = updated_resource.data
            state['changed'] = True
            state['msg'] = self.MSG_UPDATED

        return state

    def check_resource_present(self, fact_name):

        """
        The following implementation will work for resource_present under check mode.
        Generic implementation of the present state to be run under check mode for the OneView resources.

        It checks if the resource needs to be created or updated.

        :arg str fact_name: Name of the fact returned to the Ansible.
        Usually checks if the resource will becreate or add.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        changed = False

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")
        if not self.current_resource:
            msg = self.MSG_CREATED
            changed = True
        else:
            changed, msg = self.check_update_resource()
        data = self.data
        return dict(
            msg=msg,
            changed=changed,
            ansible_facts={fact_name: data}
        )

    def check_update_resource(self):
        """
        The following implementation will work for update_resource under check mode.
        It checks if the resource needs to be updated or not.
        """

        updated_data = self.current_resource.data.copy()
        updated_data.update(self.data)
        changed = False

        if compare(self.current_resource.data, updated_data):
            msg = self.MSG_ALREADY_PRESENT
        else:
            changed = True
            msg = self.MSG_UPDATED
        return (changed, msg)

    def check_resource_absent(self, method='delete'):
        """
        The following implementation will work for resource_absent under check mode.
        Generic implementation of the absent state for the OneView resources that to be run under check_mode.
        It checks if the resource needs to be removed.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if self.current_resource:
            return {"changed": True, "msg": self.MSG_DELETED}
        else:
            return {"changed": False, "msg": self.MSG_ALREADY_ABSENT}

    def check_resource_scopes_set(self, state, fact_name, scope_uris):
        """
        The following implementation will work for resource_absent under check mode.
        Generic implementation of the scopes update PATCH for the OneView resources.
        It checks if the resource needs to be updated with the current scopes.
        This method is meant to be run after ensuring the present state.
        :arg dict state: Dict containing the data from the last state results in the resource.
            It needs to have the 'msg', 'changed', and 'ansible_facts' entries.
        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg list scope_uris: List with all the scope URIs to be added to the resource.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if scope_uris is None:
            scope_uris = []

        resource = state['ansible_facts'][fact_name]

        if resource.get('scopeUris') is None or set(resource['scopeUris']) != set(scope_uris):
            state['changed'] = True
            state['msg'] = self.MSG_UPDATED

        return state


# @six.add_metaclass(abc.ABCMeta)
class OneViewModuleBase(object):
    MSG_CREATED = 'Resource created successfully.'
    MSG_UPDATED = 'Resource updated successfully.'
    MSG_DELETED = 'Resource deleted successfully.'
    MSG_ALREADY_PRESENT = 'Resource is already present.'
    MSG_ALREADY_ABSENT = 'Resource is already absent.'
    MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '
    HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'

    ONEVIEW_COMMON_ARGS = dict(
        api_version=dict(type='int'),
        config=dict(type='path'),
        hostname=dict(type='str'),
        image_streamer_hostname=dict(type='str'),
        password=dict(type='str', no_log=True),
        username=dict(type='str'),
        auth_login_domain=dict(type='str')
    )

    resource_client = None

    ONEVIEW_VALIDATE_ETAG_ARGS = dict(validate_etag=dict(type='bool', default=True))

    def __init__(self, additional_arg_spec=None, validate_etag_support=False):
        """
        OneViewModuleBase constructor.

        :arg dict additional_arg_spec: Additional argument spec definition.
        :arg bool validate_etag_support: Enables support to eTag validation.
        """
        argument_spec = self._build_argument_spec(additional_arg_spec, validate_etag_support)

        self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

        self._check_hpe_oneview_sdk()
        self._create_oneview_client()

        self.state = self.module.params.get('state')
        self.data = self.module.params.get('data')

        # Preload params for get_all - used by facts
        self.facts_params = self.module.params.get('params') or {}

        # Preload options as dict - used by facts
        self.options = transform_list_to_dict(self.module.params.get('options'))

        self.validate_etag_support = validate_etag_support

    def _build_argument_spec(self, additional_arg_spec, validate_etag_support):

        merged_arg_spec = dict()
        merged_arg_spec.update(self.ONEVIEW_COMMON_ARGS)

        if validate_etag_support:
            merged_arg_spec.update(self.ONEVIEW_VALIDATE_ETAG_ARGS)

        if additional_arg_spec:
            merged_arg_spec.update(additional_arg_spec)

        return merged_arg_spec

    def _check_hpe_oneview_sdk(self):
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=self.HPE_ONEVIEW_SDK_REQUIRED)

    def _create_oneview_client(self):
        if self.module.params.get('hostname'):
            config = dict(ip=self.module.params['hostname'],
                          credentials=dict(userName=self.module.params['username'], password=self.module.params['password'],
                                           authLoginDomain=self.module.params.get('auth_login_domain', '')),
                          api_version=self.module.params['api_version'],
                          image_streamer_ip=self.module.params['image_streamer_hostname'])
            self.oneview_client = OneViewClient(config)
        elif not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

    @abc.abstractmethod
    def execute_module(self):
        """
        Abstract method, must be implemented by the inheritor.

        This method is called from the run method. It should contain the module logic

        :return: dict: It must return a dictionary with the attributes for the module result,
            such as ansible_facts, msg and changed.
        """
        pass

    def run(self):
        """
        Common implementation of the OneView run modules.

        It calls the inheritor 'execute_module' function and sends the return to the Ansible.

        It handles any OneViewModuleException in order to signal a failure to Ansible, with a descriptive error message.

        """
        try:
            if self.validate_etag_support:
                if not self.module.params.get('validate_etag'):
                    self.oneview_client.connection.disable_etag_validation()

            result = self.execute_module()

            if not result:
                result = {}

            if "changed" not in result:
                result['changed'] = False

            self.module.exit_json(**result)

        except OneViewModuleException as exception:
            error_msg = '; '.join(to_native(e) for e in exception.args)
            self.module.fail_json(msg=error_msg, exception=traceback.format_exc())

    def resource_absent(self, resource, method='delete'):
        """
        Generic implementation of the absent state for the OneView resources.

        It checks if the resource needs to be removed.

        :arg dict resource: Resource to delete.
        :arg str method: Function of the OneView client that will be called for resource deletion.
            Usually delete or remove.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if resource:
            getattr(self.resource_client, method)(resource)

            return {"changed": True, "msg": self.MSG_DELETED}
        else:
            return {"changed": False, "msg": self.MSG_ALREADY_ABSENT}

    def get_by_name(self, name):
        """
        Generic get by name implementation.

        :arg str name: Resource name to search for.

        :return: The resource found or None.
        """
        result = self.resource_client.get_by('name', name)
        return result[0] if result else None

    def resource_present(self, resource, fact_name, create_method='create'):
        """
        Generic implementation of the present state for the OneView resources.

        It checks if the resource needs to be created or updated.

        :arg dict resource: Resource to create or update.
        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg str create_method: Function of the OneView client that will be called for resource creation.
            Usually create or add.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """

        changed = False
        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        if not resource:
            resource = getattr(self.resource_client, create_method)(self.data)
            msg = self.MSG_CREATED
            changed = True

        else:
            merged_data = resource.copy()
            merged_data.update(self.data)

            if compare(resource, merged_data):
                msg = self.MSG_ALREADY_PRESENT
            else:
                resource = self.resource_client.update(merged_data)
                changed = True
                msg = self.MSG_UPDATED

        return dict(
            msg=msg,
            changed=changed,
            ansible_facts={fact_name: resource}
        )

    def resource_scopes_set(self, state, fact_name, scope_uris):
        """
        Generic implementation of the scopes update PATCH for the OneView resources.
        It checks if the resource needs to be updated with the current scopes.
        This method is meant to be run after ensuring the present state.
        :arg dict state: Dict containing the data from the last state results in the resource.
            It needs to have the 'msg', 'changed', and 'ansible_facts' entries.
        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg list scope_uris: List with all the scope URIs to be added to the resource.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if scope_uris is None:
            scope_uris = []
        resource = state['ansible_facts'][fact_name]
        operation_data = dict(operation='replace', path='/scopeUris', value=scope_uris)

        if resource['scopeUris'] is None or set(resource['scopeUris']) != set(scope_uris):
            state['ansible_facts'][fact_name] = self.resource_client.patch(resource['uri'], **operation_data)
            state['changed'] = True
            state['msg'] = self.MSG_UPDATED

        return state


class LIGMerger(object):
    # merges uplinksets in current resource and existing resource
    def merge_data(self, current_data, data):
        merged_data = dict_merge(current_data, data)

        if current_data.get('uplinkSets') and data.get('uplinkSets'):
            # merged_data['uplinkSets'] = merge_list_by_key(current_uplinksets, existing_uplinksets, key="name")
            merged_data['uplinkSets'] = self._merge_uplink_set(current_data, data)

        return merged_data

    # updates the attributes of uplinkset in existing resource if they already exists
    # appends the uplinksets which are present in current resource but not in existing resource
    def _merge_uplink_set(self, current_resource, data):
        existing_uplinksets = data['uplinkSets']
        current_uplinksets = current_resource['uplinkSets']
        current_uplinks_left = deepcopy(current_uplinksets)

        for index, existing_uplink in enumerate(existing_uplinksets):
            for current_uplink in current_uplinksets:
                if current_uplink['name'] == existing_uplink['name']:
                    current_uplinks_left.remove(current_uplink)  # removes the common uplinksets from current uplinksets

                    if not compare(current_uplink, existing_uplink):
                        existing_uplinksets[index] = dict_merge(current_uplink, existing_uplink)

            # checks to ignore extra parameters in uplink set to achieve idempotency
            if existing_uplink.get('logicalPortConfigInfos') and isinstance(existing_uplink['logicalPortConfigInfos'], list):
                for port_config in existing_uplink['logicalPortConfigInfos']:
                    if not port_config.get('desiredFecMode'):
                        port_config['desiredFecMode'] = "Auto"

        # appends the missing uplinks from current resource to existing resource based on name
        existing_uplinksets += current_uplinks_left

        return existing_uplinksets


class SPKeys(object):
    ID = 'id'
    NAME = 'name'
    DEVICE_SLOT = 'deviceSlot'
    CONNECTION_SETTINGS = 'connectionSettings'
    CONNECTIONS = 'connections'
    OS_DEPLOYMENT = 'osDeploymentSettings'
    OS_DEPLOYMENT_URI = 'osDeploymentPlanUri'
    ATTRIBUTES = 'osCustomAttributes'
    SAN = 'sanStorage'
    VOLUMES = 'volumeAttachments'
    PATHS = 'storagePaths'
    CONN_ID = 'connectionId'
    BOOT = 'boot'
    BIOS = 'bios'
    BOOT_MODE = 'bootMode'
    LOCAL_STORAGE = 'localStorage'
    SAS_LOGICAL_JBODS = 'sasLogicalJBODs'
    CONTROLLERS = 'controllers'
    LOGICAL_DRIVES = 'logicalDrives'
    SAS_LOGICAL_JBOD_URI = 'sasLogicalJBODUri'
    SAS_LOGICAL_JBOD_ID = 'sasLogicalJBODId'
    MODE = 'mode'
    MAC_TYPE = 'macType'
    MAC = 'mac'
    SERIAL_NUMBER_TYPE = 'serialNumberType'
    UUID = 'uuid'
    SERIAL_NUMBER = 'serialNumber'
    DRIVE_NUMBER = 'driveNumber'
    WWPN_TYPE = 'wwpnType'
    WWNN = 'wwnn'
    WWPN = 'wwpn'
    LUN_TYPE = 'lunType'
    LUN = 'lun'


class ServerProfileMerger(object):
    def merge_data(self, resource, data):
        merged_data = deepcopy(resource)
        merged_data = dict_merge(merged_data, data)

        merged_data = self._merge_bios_and_boot(merged_data, resource, data)
        merged_data = self._merge_connections(merged_data, resource, data)
        merged_data = self._merge_san_storage(merged_data, data, resource)
        merged_data = self._merge_os_deployment_settings(merged_data, resource, data)
        merged_data = self._merge_local_storage(merged_data, resource, data)

        return merged_data

    def _merge_bios_and_boot(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=SPKeys.BIOS):
            merged_data = self._merge_dict(merged_data, resource, data, key=SPKeys.BIOS)
        if self._should_merge(data, resource, key=SPKeys.BOOT):
            merged_data = self._merge_dict(merged_data, resource, data, key=SPKeys.BOOT)
        if self._should_merge(data, resource, key=SPKeys.BOOT_MODE):
            merged_data = self._merge_dict(merged_data, resource, data, key=SPKeys.BOOT_MODE)
        return merged_data

    def _merge_connections(self, merged_data, resource, data):
        # The below condition is added to handle connectionSettings in server profile json
        if data.get(SPKeys.CONNECTION_SETTINGS) and SPKeys.CONNECTIONS in data.get(SPKeys.CONNECTION_SETTINGS):
            existing_connections = resource[SPKeys.CONNECTION_SETTINGS][SPKeys.CONNECTIONS]
            params_connections = data[SPKeys.CONNECTION_SETTINGS][SPKeys.CONNECTIONS]
            merged_data[SPKeys.CONNECTION_SETTINGS][SPKeys.CONNECTIONS] = merge_list_by_key(
                existing_connections,
                params_connections,
                key=SPKeys.ID,
                replace_key='portId',
                replace_value='Auto'
            )

            merged_data[SPKeys.CONNECTION_SETTINGS] = self._merge_connections_boot(
                merged_data[SPKeys.CONNECTION_SETTINGS],
                resource[SPKeys.CONNECTION_SETTINGS]
            )

        if self._should_merge(data, resource, key=SPKeys.CONNECTIONS):
            existing_connections = resource[SPKeys.CONNECTIONS]
            params_connections = data[SPKeys.CONNECTIONS]
            merged_data[SPKeys.CONNECTIONS] = merge_list_by_key(existing_connections, params_connections, key=SPKeys.ID)

            merged_data = self._merge_connections_boot(merged_data, resource)
        return merged_data

    def _merge_connections_boot(self, merged_data, resource):
        existing_connection_map = {x[SPKeys.ID]: x.copy() for x in resource[SPKeys.CONNECTIONS]}
        for merged_connection in merged_data[SPKeys.CONNECTIONS]:
            conn_id = merged_connection[SPKeys.ID]
            existing_conn_has_boot = conn_id in existing_connection_map and SPKeys.BOOT in existing_connection_map[
                conn_id]
            if existing_conn_has_boot and SPKeys.BOOT in merged_connection:
                current_connection = existing_connection_map[conn_id]
                boot_settings_merged = deepcopy(current_connection[SPKeys.BOOT])
                boot_settings_merged = dict_merge(boot_settings_merged, merged_connection[SPKeys.BOOT])
                merged_connection[SPKeys.BOOT] = boot_settings_merged
        return merged_data

    def _merge_san_storage(self, merged_data, data, resource):
        if self._removed_data(data, resource, key=SPKeys.SAN):
            merged_data[SPKeys.SAN] = dict(volumeAttachments=[], manageSanStorage=False)
        elif self._should_merge(data, resource, key=SPKeys.SAN):
            merged_data = self._merge_dict(merged_data, resource, data, key=SPKeys.SAN)

            merged_data = self._merge_san_volumes(merged_data, resource, data)
        return merged_data

    def _merge_san_volumes(self, merged_data, resource, data):
        if self._should_merge(data[SPKeys.SAN], resource[SPKeys.SAN], key=SPKeys.VOLUMES):
            existing_volumes = resource[SPKeys.SAN][SPKeys.VOLUMES]
            params_volumes = data[SPKeys.SAN][SPKeys.VOLUMES]
            merged_volumes = merge_list_by_key(existing_volumes, params_volumes, key=SPKeys.ID)
            merged_data[SPKeys.SAN][SPKeys.VOLUMES] = merged_volumes

            merged_data = self._merge_san_storage_paths(merged_data, resource)
        return merged_data

    def _merge_san_storage_paths(self, merged_data, resource):

        existing_volumes_map = OrderedDict([(i[SPKeys.ID], i) for i in resource[SPKeys.SAN][SPKeys.VOLUMES]])
        merged_volumes = merged_data[SPKeys.SAN][SPKeys.VOLUMES]
        for merged_volume in merged_volumes:
            volume_id = merged_volume[SPKeys.ID]
            if volume_id in existing_volumes_map:
                if SPKeys.PATHS in merged_volume and SPKeys.PATHS in existing_volumes_map[volume_id]:
                    existent_paths = existing_volumes_map[volume_id][SPKeys.PATHS]

                    paths_from_merged_volume = merged_volume[SPKeys.PATHS]

                    merged_paths = merge_list_by_key(existent_paths, paths_from_merged_volume, key=SPKeys.CONN_ID)

                    merged_volume[SPKeys.PATHS] = merged_paths
        return merged_data

    def _merge_os_deployment_settings(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=SPKeys.OS_DEPLOYMENT):
            merged_data = self._merge_os_deployment_custom_attr(merged_data, resource, data)
        return merged_data

    def _merge_os_deployment_custom_attr(self, merged_data, resource, data):
        if SPKeys.ATTRIBUTES in data[SPKeys.OS_DEPLOYMENT]:
            existing_os_deployment = resource[SPKeys.OS_DEPLOYMENT]
            params_os_deployment = data[SPKeys.OS_DEPLOYMENT]
            merged_os_deployment = merged_data[SPKeys.OS_DEPLOYMENT]

            if self._removed_data(params_os_deployment, existing_os_deployment, key=SPKeys.ATTRIBUTES):
                merged_os_deployment[SPKeys.ATTRIBUTES] = params_os_deployment[SPKeys.ATTRIBUTES]
            else:
                existing_attributes = existing_os_deployment[SPKeys.ATTRIBUTES]
                params_attributes = params_os_deployment[SPKeys.ATTRIBUTES]

                merged_data[SPKeys.OS_DEPLOYMENT][SPKeys.ATTRIBUTES] = merge_list_by_key(
                    existing_attributes,
                    params_attributes,
                    key='name',
                )

#                 if compare_list(existing_attributes, params_attributes):
#                     merged_os_deployment[SPKeys.ATTRIBUTES] = existing_attributes

        return merged_data

    def _merge_local_storage(self, merged_data, resource, data):
        if self._removed_data(data, resource, key=SPKeys.LOCAL_STORAGE):
            merged_data[SPKeys.LOCAL_STORAGE] = dict(sasLogicalJBODs=[], controllers=[])
        elif self._should_merge(data, resource, key=SPKeys.LOCAL_STORAGE):
            merged_data = self._merge_sas_logical_jbods(merged_data, resource, data)
            merged_data = self._merge_controllers(merged_data, resource, data)
        return merged_data

    def _merge_sas_logical_jbods(self, merged_data, resource, data):
        if data.get(SPKeys.LOCAL_STORAGE) and SPKeys.SAS_LOGICAL_JBODS in data.get(SPKeys.LOCAL_STORAGE):
            existing_items = resource[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS]
            provided_items = data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS]
            merged_jbods = merge_list_by_key(existing_items, provided_items, key=SPKeys.ID, ignore_when_null=[SPKeys.SAS_LOGICAL_JBOD_URI])
            merged_data[SPKeys.LOCAL_STORAGE][SPKeys.SAS_LOGICAL_JBODS] = merged_jbods
        return merged_data

    def _merge_controllers(self, merged_data, resource, data):
        if self._should_merge(data[SPKeys.LOCAL_STORAGE], resource[SPKeys.LOCAL_STORAGE], key=SPKeys.CONTROLLERS):
            existing_items = resource[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS]
            provided_items = merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS]
            merged_controllers = merge_list_by_key(existing_items, provided_items, key=SPKeys.DEVICE_SLOT)
            merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS] = merged_controllers

            merged_data = self._merge_controller_drives(merged_data, resource)
        return merged_data

    def _merge_controller_drives(self, merged_data, resource):
        for current_controller in merged_data[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][:]:
            for existing_controller in resource[SPKeys.LOCAL_STORAGE][SPKeys.CONTROLLERS][:]:
                same_slot = current_controller.get(SPKeys.DEVICE_SLOT) == existing_controller.get(SPKeys.DEVICE_SLOT)
                same_mode = existing_controller.get(SPKeys.MODE) == existing_controller.get(SPKeys.MODE)
                if same_slot and same_mode and current_controller[SPKeys.LOGICAL_DRIVES]:

                    key_merge = self._define_key_to_merge_drives(current_controller)

                    if key_merge:
                        merged_drives = merge_list_by_key(existing_controller[SPKeys.LOGICAL_DRIVES],
                                                          current_controller[SPKeys.LOGICAL_DRIVES],
                                                          key=key_merge)
                        current_controller[SPKeys.LOGICAL_DRIVES] = merged_drives
        return merged_data

    def _define_key_to_merge_drives(self, controller):
        has_name = True
        has_logical_jbod_id = True
        for drive in controller[SPKeys.LOGICAL_DRIVES]:
            if not drive.get(SPKeys.NAME):
                has_name = False
            if not drive.get(SPKeys.SAS_LOGICAL_JBOD_ID):
                has_logical_jbod_id = False

        if has_name:
            return SPKeys.NAME
        elif has_logical_jbod_id:
            return SPKeys.SAS_LOGICAL_JBOD_ID
        return None

    def _removed_data(self, data, resource, key):
        return key in data and not data[key] and key in resource

    def _should_merge(self, data, resource, key):
        data_has_value = key in data and data[key]
        existing_resource_has_value = key in resource and resource[key]
        return data_has_value and existing_resource_has_value

    def _merge_dict(self, merged_data, resource, data, key):
        if resource[key]:
            merged_dict = deepcopy(resource[key])
            merged_dict.update(deepcopy(data[key]))
        merged_data[key] = merged_dict
        return merged_data


class ServerProfileReplaceNamesByUris(object):
    SCOPE_NOT_FOUND = 'Scope not found: '
    SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND = 'OS Deployment Plan not found: '
    SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND = 'Enclosure Group not found: '
    SERVER_PROFILE_NETWORK_NOT_FOUND = 'Network not found: '
    SERVER_HARDWARE_TYPE_NOT_FOUND = 'Server Hardware Type not found: '
    VOLUME_NOT_FOUND = 'Volume not found: '
    STORAGE_POOL_NOT_FOUND = 'Storage Pool not found: '
    STORAGE_SYSTEM_NOT_FOUND = 'Storage System not found: '
    STORAGE_VOLUME_TEMPLATE_NOT_FOUND = 'Storage volume template not found: '
    INTERCONNECT_NOT_FOUND = 'Interconnect not found: '
    FIRMWARE_DRIVER_NOT_FOUND = 'Firmware Driver not found: '
    SAS_LOGICAL_JBOD_NOT_FOUND = 'SAS logical JBOD not found: '
    ENCLOSURE_NOT_FOUND = 'Enclosure not found: '

    def replace(self, oneview_client, data):
        self.oneview_client = oneview_client
        self._replace_os_deployment_name_by_uri(data)
        self._replace_enclosure_group_name_by_uri(data)
        self._replace_networks_name_by_uri(data)
        self._replace_server_hardware_type_name_by_uri(data)
        self._replace_volume_attachment_names_by_uri(data)
        self._replace_enclosure_name_by_uri(data)
        self._replace_interconnect_name_by_uri(data)
        self._replace_firmware_baseline_name_by_uri(data)
        self._replace_sas_logical_jbod_name_by_uri(data)
        self._replace_initial_scope_name_by_uri(data)

    def _get_resource_uri_from_name(self, name, message, resource_client):
        resource_by_name = resource_client.get_by('name', name)
        if resource_by_name:
            return resource_by_name[0]['uri']
        else:
            raise OneViewModuleResourceNotFound(message + name)

    def _replace_name_by_uri(self, data, attr_name, message, resource_client,
                             replace_name_with='Uri'):
        attr_uri = attr_name.replace("Name", replace_name_with)
        if attr_name in data:
            name = data.pop(attr_name)
            uri = self._get_resource_uri_from_name(name, message, resource_client)
            data[attr_uri] = uri

    def _replace_initial_scope_name_by_uri(self, data):
        if data.get("initialScopeNames"):
            scope_uris = []
            resource_client = self.oneview_client.scopes
            for name in data.pop("initialScopeNames", []):
                scope = resource_client.get_by_name(name)
                if not scope:
                    raise OneViewModuleResourceNotFound(self.SCOPE_NOT_FOUND + name)
                scope_uris.append(scope["uri"])
            data["initialScopeUris"] = scope_uris

    def _replace_os_deployment_name_by_uri(self, data):
        if SPKeys.OS_DEPLOYMENT in data and data[SPKeys.OS_DEPLOYMENT]:
            self._replace_name_by_uri(data[SPKeys.OS_DEPLOYMENT], 'osDeploymentPlanName',
                                      self.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND,
                                      self.oneview_client.os_deployment_plans)

    def _replace_enclosure_group_name_by_uri(self, data):
        self._replace_name_by_uri(data, 'enclosureGroupName', self.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND,
                                  self.oneview_client.enclosure_groups)

    def _replace_networks_name_by_uri(self, data):
        if data.get("connections"):
            connections = data["connections"]
        elif data.get("connectionSettings") and data["connectionSettings"].get("connections"):
            connections = data["connectionSettings"]["connections"]
        else:
            return

        for connection in connections:
            if 'networkName' in connection:
                name = connection.pop('networkName')
                if name is not None:
                    connection['networkUri'] = self._get_network_by_name(name)['uri']

    def _replace_server_hardware_type_name_by_uri(self, data):
        self._replace_name_by_uri(data, 'serverHardwareTypeName', self.SERVER_HARDWARE_TYPE_NOT_FOUND,
                                  self.oneview_client.server_hardware_types)

    def _replace_volume_attachment_names_by_uri(self, data):
        volume_attachments = (data.get('sanStorage') or {}).get('volumeAttachments') or []

        if len(volume_attachments) > 0:
            for volume in volume_attachments:
                if not volume.get('volumeUri') and volume.get('volumeName'):
                    resource_by_name = self.oneview_client.volumes.get_by('name', volume['volumeName'])
                    if resource_by_name:
                        volume['volumeUri'] = resource_by_name[0]['uri']
                        del volume['volumeName']
                    else:
                        logger.debug("The volumeUri is null in the volumeAttachments list, it will be understood "
                                     "that the volume does not exist, so it will be created along with the server "
                                     "profile. Be warned that it will always trigger a new creation, so it will not "
                                     " be idempotent.")

                self._replace_name_by_uri(volume, 'volumeStoragePoolName', self.STORAGE_POOL_NOT_FOUND,
                                          self.oneview_client.storage_pools)
                self._replace_name_by_uri(volume, 'volumeStorageSystemName', self.STORAGE_SYSTEM_NOT_FOUND,
                                          self.oneview_client.storage_systems)

                # Support for API version 600 schema changes
                if volume.get('volume'):
                    self._replace_name_by_uri(volume['volume'], 'templateName',
                                              self.STORAGE_VOLUME_TEMPLATE_NOT_FOUND,
                                              self.oneview_client.storage_volume_templates)

                    if volume['volume'].get('properties'):
                        self._replace_name_by_uri(volume['volume']['properties'],
                                                  'storagePoolName',
                                                  self.STORAGE_POOL_NOT_FOUND,
                                                  self.oneview_client.storage_pools,
                                                  replace_name_with='')

    def _replace_enclosure_name_by_uri(self, data):
        self._replace_name_by_uri(data, 'enclosureName', self.ENCLOSURE_NOT_FOUND, self.oneview_client.enclosures)

    def _replace_interconnect_name_by_uri(self, data):
        connections = data.get('connections') or []
        if len(connections) > 0:
            for connection in connections:
                self._replace_name_by_uri(connection, 'interconnectName', self.INTERCONNECT_NOT_FOUND,
                                          self.oneview_client.interconnects)

    def _replace_firmware_baseline_name_by_uri(self, data):
        firmware = data.get('firmware') or {}
        self._replace_name_by_uri(firmware, 'firmwareBaselineName', self.FIRMWARE_DRIVER_NOT_FOUND,
                                  self.oneview_client.firmware_drivers)

    def _replace_sas_logical_jbod_name_by_uri(self, data):
        sas_logical_jbods = (data.get('localStorage') or {}).get('sasLogicalJBODs') or []
        if len(sas_logical_jbods) > 0:
            for jbod in sas_logical_jbods:
                self._replace_name_by_uri(jbod, 'sasLogicalJBODName', self.SAS_LOGICAL_JBOD_NOT_FOUND,
                                          self.oneview_client.sas_logical_jbods)

    def _get_network_by_name(self, name):
        fc_networks = self.oneview_client.fc_networks.get_by('name', name)
        if fc_networks:
            return fc_networks[0]

        fcoe_networks = self.oneview_client.fcoe_networks.get_by('name', name)
        if fcoe_networks:
            return fcoe_networks[0]

        network_sets = self.oneview_client.network_sets.get_by('name', name)
        if network_sets:
            return network_sets[0]

        ethernet_networks = self.oneview_client.ethernet_networks.get_by('name', name)
        if not ethernet_networks:
            raise OneViewModuleResourceNotFound(self.SERVER_PROFILE_NETWORK_NOT_FOUND + name)
        return ethernet_networks[0]
