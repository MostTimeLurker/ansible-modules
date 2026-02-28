#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2026 MostTimeLurker
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: permission_templates.py
"""

EXAMPLES = r"""
# Simple example
"""

RETURN = r"""
changed:
  message: Whatever SonarQube said
  returned: always
  type: bool
  sample: true
"""

from ansible.module_utils.basic import AnsibleModule
from requests.exceptions import ConnectionError

def run_module():
    module_args = dict(
        sonar_host=dict(type='str', default="http://localhost:9000/"),
        sonar_token=dict(type='str', required=True, no_log=True),
        name=dict(type='str', required=True),
        desc=dict(type='str', required=False, default=""),
        pattern=dict(type='str', required=False, default=""),
        state=dict(type='str', default='present', choices=['present', 'absent','update'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    result = dict(
        changed=False,
        name="",
        desc="",
        pattern="",
        state="",
        message=''
    )

    #########
    sonar_host = module.params["sonar_host"]
    sonar_token = module.params["sonar_token"]
    name = module.params["name"]
    desc = module.params["desc"]
    pattern = module.params["pattern"]
    state = module.params["state"]
    #########

    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    #########

    try:
        from sonarqube.community import SonarQubeClient
        from sonarqube.utils.exceptions import ValidationError
        from sonarqube.utils.exceptions import NotFoundError

        module.log("using sonarqube-libs from system")
    except ImportError:
        from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community import SonarQubeClient
        from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.exceptions import ValidationError
        from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.exceptions import NotFoundError

        module.log("using sonarqube-libs from built-in")


    #########

    #########
    try:
      sonar = SonarQubeClient(sonarqube_url=sonar_host, token=sonar_token)

      sonar_version = sonar.server.get_server_version()
      module.debug("SonarQube Server: " + sonar_version)
    except ConnectionError as e:
      module.fail_json(msg="ConnectionError: " + str(e))
    except Exception as e:
        module.fail_json(msg="GenericException: " + str(e))


    sonar_result = ""

    try:
        if (state == "present"):
            sonar_result = sonar.permissions.create_template(name=name, description=desc, projectKeyPattern=pattern)
        elif (state == "absent"):
            sonar_result = sonar.permissions.delete_template(templateName=name)
        elif (state == "update"):
           sonar_result = sonar.permissions.update_template(name=name, description=desc, projectKeyPattern=pattern)
        else:
            module.fail_json(msg="Invalid state: " + state)
    except ValidationError as e:
      module.fail_json(msg="ValidationError: " + str(e))
    except NotFoundError as e:
      module.fail_json(msg="NotFoundError: " + str(e))
    except ConnectionError as e:
      module.fail_json(msg="ConnectionError: " + str(e))
    except Exception as e:
      module.fail_json(msg="Exception: " + str(e))

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['name'] = name
    result['desc'] = desc
    result['pattern'] = pattern
    result['message'] = sonar_result
    result['changed'] = True
    result['state'] = state

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
##    if module.params['new']:
##        result['changed'] = True

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
