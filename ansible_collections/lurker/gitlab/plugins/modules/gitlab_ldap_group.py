#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2026 MostTimeLurker
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = r"""
---
module: groups.py
"""

XAMPLES = r"""
# Simple example
"""

RETURN = r"""
changed:
  message: Whatever GitLab said
  returned: always
  type: bool
  sample: true
"""

from ansible.module_utils.basic import AnsibleModule

# either
from ansible_collections.community.general.plugins.module_utils.gitlab import find_group, gitlab_authentication, GitlabDeleteError, GitlabCreateError
# or
#import gitlab

#### from the source
#### connecting to gitlab through ansible-gitlab
# gitlab_url = module.params['api_url']
# validate_certs = module.params['validate_certs']
# ca_path = module.params['ca_path']
# gitlab_user = module.params['api_username']
# gitlab_password = module.params['api_password']
# gitlab_token = module.params['api_token']
# gitlab_oauth_token = module.params['api_oauth_token']
# gitlab_job_token = module.params['api_job_token']


class GitLabGroupHelper(object):
    def __init__(self, module, gl):
        self._module = module
        self._gitlab = gl

    def add_ldap_to_group(self, gitlab_ldap_cn, gitlab_group_id, access_level):
        try:
            group = self._gitlab.groups.get(gitlab_group_id)
            add_ldap = group.ldap_group_links.create({
                 'provider': 'ldapmain',
                 'group_access': access_level,
                 'cn': gitlab_ldap_cn
            })

            if add_ldap:
                return add_ldap

        except (GitlabCreateError) as e:
            self._module.fail_json(
                msg="Failed to add member to the Group, Group ID %s: %s" % (gitlab_group_id, e))

    def remove_ldap_from_group(self, gitlab_ldap_cn, gitlab_group_id):
        try:
            group = self._gitlab.groups.get(gitlab_group_id)
            remove_ldap = group.ldap_group_links.delete(gitlab_ldap_cn, 'ldapmain')

            if remove_ldap:
                    return remove_ldap

        except (GitlabDeleteError) as e:
            self._module.fail_json(
                msg="Failed to remove member from GitLab group, ID %s: %s" % (gitlab_group_id, e))




def run_module():
    module_args = dict(
        gitlab_host=dict(type='str', default="http://localhost:80/"),
        gitlab_token=dict(type='str', required=True, no_log=True),
        group_name=dict(type='str', required=True),
        group_ldap_cn=dict(type='str', required=True),
        group_access=dict(type='str', default='guest', choices=['guest', 'reporter', 'developer', 'maintainer', 'owner']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    result = dict(
        changed=False,
        group_name='',
        group_ldap_cn='',
        group_access_level='',
        state="",
        message=''
    )

    #########
    gitlab_host = module.params["gitlab_host"]
    gitlab_token = module.params["gitlab_token"]
    group_name = module.params["group_name"]
    group_ldap_cn = module.params["group_ldap_cn"]
    group_access = module.params["group_access"]
    state = module.params["state"]
    #########

    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    #########

    if group_access:
        group_access_int = {
            'guest': gitlab.const.GUEST_ACCESS,
            'reporter': gitlab.const.REPORTER_ACCESS,
            'developer': gitlab.const.DEVELOPER_ACCESS,
            'maintainer': gitlab.const.MAINTAINER_ACCESS,
            'owner': gitlab.const.OWNER_ACCESS
        }

        group_access = group_access_int[group_access]


    # wont work, since the names dont match
    gl = gitlab_authentication(module)

    gitlab_group = find_group(gl, gitlab_group)

    # group doesn't exist
    if not gitlab_group:
        module.fail_json(msg="group '%s' not found." % gitlab_group)

    gitlab_group_id = gitlab_group.id

    group = GitLabGroupHelper(module, gl)
    gitlab_result = ""
    if state == 'present':
        if not module.check_mode:
            gitlab_result = group.add_ldap_to_group(group_ldap_cn, gitlab_group_id, group_access)
            # module.exit_json(changed=True, result="Successfully added cn '%s' to the group." % group_ldap_cn)
    else:
        if not module.check_mode:
            gitlab_result = group.remove_ldap_from_group(group_ldap_cn, gitlab_group_id)
            # module.exit_json(changed=True, result="Successfully removed cn '%s' from the group." % group_ldap_cn)



    #########

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['group_name'] = group_name
    result['group_ldap_cn'] = group_ldap_cn
    result['group_access'] = group_access
    result['message'] = gitlab_result
    result['changed'] = True
    result['state'] = state

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['state'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
