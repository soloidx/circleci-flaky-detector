# -*- coding:utf-8 -*-

import unittest
from mock import MagicMock
from mock import patch

import main
from services.ci import CircleCIService
from services.reporter import BasicReportService

STATUS_OK = [
    {
        'vcs_revision': '001',
        'status': 'success',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 1',
        'branch': 'branch 1',
        'build_url': 'https://circleci.com/gh/test/test/22',
        'retry_of': None,
    },
    {
        'vcs_revision': '003',
        'status': 'fixed',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 1',
        'branch': 'branch 2',
        'build_url': 'https://circleci.com/gh/test/test/22',
        'retry_of': None,
    },
    {
        'vcs_revision': '002',
        'status': 'failed',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 1',
        'branch': 'branch 1',
        'build_url': 'https://circleci.com/gh/test/test/22',
        'retry_of': None,
    }
]

STATUS_FAIL = [
    {
        'vcs_revision': '001',
        'status': 'success',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 1',
        'branch': 'branch 1',
        'build_url': 'https://circleci.com/gh/test/test/23',
        'retry_of': None,
    },
    {
        'vcs_revision': '002',
        'status': 'fixed',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 1',
        'branch': 'branch 1',
        'build_url': 'https://circleci.com/gh/test/test/22',
        'retry_of': 001
    },
    {
        'vcs_revision': '003',
        'status': 'failed',
        'start_time': '2015-12-03T13:13:53.429Z',
        'author_name': 'Dev 3',
        'branch': 'branch 1',
        'build_url': 'https://circleci.com/gh/test/test/21',
        'retry_of': None
    }
]


@patch.object(CircleCIService, 'get_build_list', MagicMock())
@patch.object(BasicReportService, 'report', MagicMock())
class TestReportChecker(unittest.TestCase):
    """Check all methods of the ReportChecker class"""

    def test_ReportChecker_class_should_exist(self):
        self.assertTrue(hasattr(main, 'ReportChecker'))

    def test_ReportChecker_class_should_have_check_method(self):
        report = main.ReportChecker()
        self.assertTrue(hasattr(report, 'check'))

    def test_ReportChecker_should_get_ci_service(self):
        report = main.ReportChecker()
        self.assertTrue(hasattr(report, 'get_ci_service'))
        self.assertIsNotNone(report.get_ci_service())

    def test_ReportChecker_should_get_report_service(self):
        report = main.ReportChecker()
        self.assertTrue(hasattr(report, 'get_report_service'))
        self.assertIsNotNone(report.get_report_service())

    def test_ReportChecker_check_should_report_if_found_flaky_test(self):
        ci_mock_service = CircleCIService()
        ci_mock_service.get_build_list.return_value = STATUS_FAIL

        ci_mock_reporter = BasicReportService()
        ci_mock_reporter.report = MagicMock()

        report = main.ReportChecker()
        report.reporting_service = ci_mock_reporter
        report.check()
        ci_mock_reporter.report.assert_called_with(
            user='Dev 1', branch='branch 1', revision='002',
            build_url='https://circleci.com/gh/test/test/22')

    def test_ReportChecker_check_should_not_report_if_is_ok(self):
        ci_mock_service = CircleCIService()
        ci_mock_service.get_build_list.return_value = STATUS_OK

        ci_mock_reporter = BasicReportService()
        ci_mock_reporter.report = MagicMock()

        report = main.ReportChecker()
        report.reporting_service = ci_mock_reporter
        report.check()
        ci_mock_reporter.report.assert_not_called()
