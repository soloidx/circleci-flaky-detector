# -*- coding:utf-8 -*-

import unittest

from services import reporter


class TestHipChatService(unittest.TestCase):
    """Check all methods of the HipChatService class"""

    def test_HipChatService_class_should_exist(self):
        self.assertTrue(hasattr(reporter, 'HipChatService'))

    def test_HipChatService_class_should_have_report_method(self):
        report = reporter.HipChatService()
        self.assertTrue(hasattr(report, 'report'))
