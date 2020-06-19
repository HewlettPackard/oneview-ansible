from ansible.module_utils.oneview import compare


class OneViewModuleCheckMode():
    MSG_CREATED = 'Resource created successfully.'
    MSG_UPDATED = 'Resource updated successfully.'
    MSG_DELETED = 'Resource deleted successfully.'
    MSG_ALREADY_PRESENT = 'Resource is already present.'
    MSG_ALREADY_ABSENT = 'Resource is already absent.'
    MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '
    MSG_MANDATORY_FIELD_MISSING = 'Missing mandatory field: name'
    HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'

    ONEVIEW_VALIDATE_ETAG_ARGS = dict(validate_etag=dict(type='bool', default=True))

    def check_resource_present(self, fact_name):
        """
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
        Generic implementation of the absent state for the OneView resources.

        It checks if the resource needs to be removed.

        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if self.current_resource:
            return {"changed": True, "msg": self.MSG_DELETED}
        else:
            return {"changed": False, "msg": self.MSG_ALREADY_ABSENT}

    def check_resource_scopes_set(self, state, fact_name, scope_uris):
        """
        Generic implementation of the scopes to check the update PATCH for the OneView resources.
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
