#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.rest_client import RestClient
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.config import API_MONITORING_METRICS_ENDPOINT
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.common import GET


class SonarQubeMonitoring(RestClient):
    """
    SonarQube monitoring Operations
    """

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarQubeMonitoring, self).__init__(**kwargs)

    @GET(API_MONITORING_METRICS_ENDPOINT)
    def get_monitoring_metrics(self):
        """
        since 9.3
        Return monitoring metrics in Prometheus format. Support content type 'text/plain' (default) and
        'application/openmetrics-text'. this endpoint can be access using a Bearer token, that needs to
        be defined in sonar.properties with the 'sonar.web.systemPasscode' key.

        :return:
        """