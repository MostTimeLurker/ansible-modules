from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.community import SonarQubeClient
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.enterprise.applications import SonarQubeApplications
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.enterprise.audit_logs import SonarQubeAuditLogs
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.enterprise.editions import SonarQubeEditions
from ansible_collections.lurker.sonarqube.plugins.module_utils.sonarqube.enterprise.views import SonarQubeViews


class SonarEnterpriseClient(SonarQubeClient):
    """
    A Python Client for SonarQube Enterprise Server APIs.
    """
    @property
    def applications(self):
        """
        SonarQube applications Operations

        :return:
        """
        return SonarQubeApplications(api=self)

    @property
    def audit_logs(self):
        return SonarQubeAuditLogs(api=self)

    @property
    def editions(self):
        """
        Manage SonarSource commercial editions

        """
        return SonarQubeEditions(api=self)

    @property
    def views(self):
        """
        Manage Portfolios

        """
        return SonarQubeViews(api=self)
