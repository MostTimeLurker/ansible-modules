#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.rest_client import RestClient
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.config import API_DUPLICATIONS_SHOW_ENDPOINT
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.common import GET


class SonarQubeDuplications(RestClient):
    """
    SonarQube duplications Operations
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarQubeDuplications, self).__init__(**kwargs)

    @GET(API_DUPLICATIONS_SHOW_ENDPOINT)
    def get_duplications(self, key, branch=None, pullRequest=None):
        """
        SINCE 4.4
        Get duplications. Require Browse permission on file's project

        :param key: File key
        :param branch: Branch key
        :param pullRequest: Pull request id
        :return:
        """
