#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2026 MostTimeLurker
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r"""
---
module: groups.py

short_description: handles groups (create, delete, ...) on your sonarqube instance
description:
  - because, why not

version_added: "0.0.1"
author:
  - "MostTimeLurker (@mosttimelurker)"
requirements:
  - python >= 3.x
  - sonarqube-api-v2 (optional, has built-in fallback)
options:
  sonar_host:
    description:
    type: str
    required: false (has default)

  sonar_token:
    description:
    type: str
    required: true

  group_name:
    description:
    type: str
    required: true

  group_desc:
    description:
    type: str
    required: false (has default)

  state:
    description: Desired state
    type: str
    choices: [present, absent]
    default: present

    
attributes:
  check_mode:
    support: none    
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
        group_name=dict(type='str', required=True),
        group_desc=dict(type='str', required=False, default=""),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    result = dict(
        changed=False,
        group_name='',
        group_desc='',
        state="",
        message=''
    )

    #########
    sonar_host = module.params["sonar_host"]
    sonar_token = module.params["sonar_token"]
    group_name = module.params["group_name"]
    group_desc = module.params["group_desc"]
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
        sonar_result = sonar.user_groups.create_group(name=group_name, description=group_desc)
      elif (state == "absent"):
         sonar_result = sonar.user_groups.delete_group(name=group_name)
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
    result['group_name'] = group_name
    result['group_desc'] = group_desc
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
