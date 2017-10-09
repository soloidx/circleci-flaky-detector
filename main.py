# -*- coding:utf-8 -*-

# import os
from services.ci import CircleCIService
from services import reporter


class ReportChecker(object):
    """Main class for build checker"""
    ci_service = None
    reporting_service = None

    def get_ci_service(self):
        """Get the current service or create a default one"""
        if not self.ci_service:
            self.ci_service = CircleCIService()
        return self.ci_service

    def get_report_service(self):
        """Get the current service or create a default one"""
        if not self.reporting_service:
            self.reporting_service = reporter.SMTPService()
        return self.reporting_service

    def check(self):
        build_list = self.get_ci_service().get_build_list()
        for build in build_list:
            if build['status'] == 'fixed' and \
                    build['retry_of'] is not None:
                self.get_report_service().report(
                    user=build['author_name'],
                    branch=build['branch'],
                    revision=build['vcs_revision'],
                    build_url=build['build_url'])


def lambda_handler(event, context):
    checker = ReportChecker()
    checker.check()

if __name__ == '__main__':
    lambda_handler({}, None)
