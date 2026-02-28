#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.rest_client import RestClient
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.config import API_LANGUAGES_LIST_ENDPOINT
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.common import GET


class SonarQubeLanguages(RestClient):
    """
    SonarQube languages Operations
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarQubeLanguages, self).__init__(**kwargs)

    @GET(API_LANGUAGES_LIST_ENDPOINT)
    def get_supported_programming_languages(self, q=None):
        """
        SINCE 5.1
        List supported programming languages

        :param q: A pattern to match language keys/names against
        :return:
        """
