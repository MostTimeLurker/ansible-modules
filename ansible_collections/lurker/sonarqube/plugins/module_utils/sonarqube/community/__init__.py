#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import requests

#import ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube #as sonarqube

from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.utils.common import strip_trailing_slash
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.users import SonarQubeUsers
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.projects import SonarQubeProjects
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.user_groups import SonarQubeUserGroups
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.issues import SonarQubeIssues
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.measures import SonarQubeMeasures
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.notifications import SonarQubeNotifications
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_links import SonarQubeProjectLinks
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.permissions import SonarQubePermissions
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.ce import SonarQubeCe
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_branches import SonarQubeProjectBranches
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.qualitygates import SonarQubeQualityGates
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.components import SonarQubeComponents
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.rules import SonarQubeRules
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.qualityprofiles import SonarQubeQualityProfiles
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.duplications import SonarQubeDuplications
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.metrics import SonarQubeMetrics
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.hotspots import SonarQubeHotspots
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.new_code_periods import SonarQubeNewcodeperiods
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.settings import SonarQubeSettings
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.sources import SonarQubeSources
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.auth import SonarQubeAuth
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.favorites import SonarQubeFavorites
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.languages import SonarQubeLanguages
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.plugins import SonarQubePlugins
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_badges import SonarQubeProjectBadges
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_tags import SonarQubeProjectTags
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_pull_requests import SonarQubeProjectPullRequests
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_analyses import SonarQubeProjectAnalyses
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.server import SonarQubeServer
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.user_tokens import SonarQubeUserTokens
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.webhooks import SonarQubeWebhooks
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.webservices import SonarQubeWebservices
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.system import SonarQubeSystem
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.alm_integrations import SonarQubeAlmIntegrations
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.alm_settings import SonarQubeAlmSettings
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.monitoring import SonarQubeMonitoring
from  ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community.project_dump import SonarQubeProjectdump


class SonarQubeClient:
    """
    A Python Client for SonarQube Server APIs.
    """

    DEFAULT_URL = "http://localhost:9000"

    def __init__(self, sonarqube_url=None, username=None, password=None, token=None, verify=None, timeout=None):

        self.base_url = strip_trailing_slash(sonarqube_url or self.DEFAULT_URL)

        _session = requests.Session()
        if token:
            _session.auth = (token, "")
        elif username and password:
            _session.auth = (username, password)
        if verify is not None:
            _session.verify = verify

        self.session = _session
        self.timeout = timeout

    @property
    def users(self):
        """
        SonarQube users Operations

        :return:
        """
        return SonarQubeUsers(api=self)

    @property
    def user_groups(self):
        """
        SonarQube user_groups Operations

        :return:
        """
        return SonarQubeUserGroups(api=self)

    @property
    def projects(self):
        """
        SonarQube projects Operations

        :return:
        """
        return SonarQubeProjects(api=self)

    @property
    def measures(self):
        """
        SonarQube measures Operations

        :return:
        """
        return SonarQubeMeasures(api=self)

    @property
    def issues(self):
        """
        SonarQube issues Operations

        :return:
        """
        return SonarQubeIssues(api=self)

    @property
    def notifications(self):
        """
        SonarQube notifications Operations

        :return:
        """
        return SonarQubeNotifications(api=self)

    @property
    def project_links(self):
        """
        SonarQube project links Operations

        :return:
        """
        return SonarQubeProjectLinks(api=self)

    @property
    def permissions(self):
        """
        SonarQube permissions Operations

        :return:
        """
        return SonarQubePermissions(api=self)

    @property
    def ce(self):
        """
        SonarQube ce Operations

        :return:
        """
        return SonarQubeCe(api=self)

    @property
    def project_branches(self):
        """
        SonarQube project branches Operations

        :return:
        """
        return SonarQubeProjectBranches(api=self)

    @property
    def qualitygates(self):
        """
        SonarQube quality gates Operations

        :return:
        """
        return SonarQubeQualityGates(api=self)

    @property
    def components(self):
        """
        SonarQube components Operations

        :return:
        """
        return SonarQubeComponents(api=self)

    @property
    def rules(self):
        """
        SonarQube rules Operations

        :return:
        """
        return SonarQubeRules(api=self)

    @property
    def qualityprofiles(self):
        """
        SonarQube quality profiles Operations

        :return:
        """
        return SonarQubeQualityProfiles(api=self)

    @property
    def duplications(self):
        """
        SonarQube duplications Operations

        :return:
        """
        return SonarQubeDuplications(api=self)

    @property
    def metrics(self):
        """
        SonarQube metrics Operations

        :return:
        """
        return SonarQubeMetrics(api=self)

    @property
    def hotspots(self):
        """

        :return:
        """
        return SonarQubeHotspots(api=self)

    @property
    def new_code_periods(self):
        """
        SonarQube new code periods Operations

        :return:
        """
        return SonarQubeNewcodeperiods(api=self)

    @property
    def settings(self):
        """
        SonarQube settings Operations

        :return:
        """
        return SonarQubeSettings(api=self)

    @property
    def sources(self):
        """
        SonarQube sources Operations

        :return:
        """
        return SonarQubeSources(api=self)

    @property
    def auth(self):
        """
        SonarQube authentication Operations

        :return:
        """
        return SonarQubeAuth(api=self)

    @property
    def favorites(self):
        """
        SonarQube favorites Operations

        :return:
        """
        return SonarQubeFavorites(api=self)

    @property
    def languages(self):
        """
        SonarQube languages Operations

        :return:
        """
        return SonarQubeLanguages(api=self)

    @property
    def project_badges(self):
        """
        SonarQube project badges Operations

        :return:
        """
        return SonarQubeProjectBadges(api=self)

    @property
    def project_tags(self):
        """
        SonarQube project tags Operations

        :return:
        """
        return SonarQubeProjectTags(api=self)

    @property
    def project_pull_requests(self):
        """
        SonarQube project pull requests Operations

        :return:
        """
        return SonarQubeProjectPullRequests(api=self)

    @property
    def project_analyses(self):
        """
        SonarQube project analyses Operations

        :return:
        """
        return SonarQubeProjectAnalyses(api=self)

    @property
    def server(self):
        """
        SonarQube server Operations

        :return:
        """
        return SonarQubeServer(api=self)

    @property
    def user_tokens(self):
        """
        SonarQube user tokens Operations

        :return:
        """
        return SonarQubeUserTokens(api=self)

    @property
    def webhooks(self):
        """
        SonarQube webhooks Operations

        :return:
        """
        return SonarQubeWebhooks(api=self)

    @property
    def webservices(self):
        """
        SonarQube webservices Operations

        :return:
        """
        return SonarQubeWebservices(api=self)

    @property
    def system(self):
        """
        SonarQube system Operations

        :return:
        """
        return SonarQubeSystem(api=self)

    @property
    def plugins(self):
        """
        SonarQube plugins Operations

        :return:
        """
        return SonarQubePlugins(api=self)

    @property
    def alm_integrations(self):
        """
        ALM Integrations

        """
        return SonarQubeAlmIntegrations(api=self)

    @property
    def alm_settings(self):
        """
        ALM settings

        """
        return SonarQubeAlmSettings(api=self)

    @property
    def monitoring(self):
        return SonarQubeMonitoring(api=self)

    @property
    def project_dump(self):
        """
        Project export/import

        :return:
        """
        return SonarQubeProjectdump(api=self)
