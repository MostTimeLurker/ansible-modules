#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2026 MostTimeLurker
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type



from ansible.module_utils.basic import AnsibleModule
from requests.exceptions import ConnectionError

def run_module():
  
    module_args = dict(
        sonar_host=dict(type='str', default="http://localhost:9000/"),
        sonar_token=dict(type='str', required=True, no_log=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )


    sonar_host = module.params["sonar_host"]
    sonar_token = module.params["sonar_token"]


    if module.check_mode:
        module.exit_json(**facts)


    try:
        from sonarqube.community import SonarQubeClient

        module.log("using sonarqube-libs from system")
    except ImportError:
        from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community import SonarQubeClient

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

    permissiontemplates_fact = []
    defaulttemplates_fact = []
    permissions_fact = []
    try:
        templates = sonar.permissions.search_templates()
        for template in templates.get("permissionTemplates"):
            permissiontemplates_fact.append(template)
        for template in templates.get("defaultTemplates"):
            defaulttemplates_fact.append(template)
        for template in templates.get("permissions"):
            permissions_fact.append(template)
    except Exception as e:
        module.fail_json(msg="GenericException: " + str(e))

    #########

    module.exit_json(changed=False, ansible_facts={
        "sonarqube.templates.permissionTemplates": permissiontemplates_fact,
        "sonarqube.templates.defaultTemplates": defaulttemplates_fact,
        "sonarqube.templates.permissions": permissions_fact,
        "sonarqube.server_version": sonar_version})



def main():
    run_module()


if __name__ == '__main__':
    main()
