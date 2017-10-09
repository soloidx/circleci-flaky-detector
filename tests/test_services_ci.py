# -*- coding:utf-8 -*-

import unittest
import urllib2
import datetime

import settings
from services import ci
from mock import patch, Mock, MagicMock

CIRCLE_CI_RESULT = '''[ {
  "build_url" : "https://circleci.com/gh/luceo/luceo/19560",
  "branch" : "ftw-318-fix-identificationDoublons-2",
  "username" : "luceo",
  "vcs_revision" : "b07c91818f754ba64539db70d60db690c039a559",
  "build_num" : 19560,
  "status" : "success",
  "stop_time" : "2015-12-03T21:45:20.319Z",
  "start_time" : "2015-12-03T21:31:24.449Z",
  "retry_of": null,
  "author_name" : "sakai135"
}, {
  "build_url" : "https://circleci.com/gh/luceo/luceo/19559",
  "branch" : "ftw-402-affectation-prototyping",
  "username" : "luceo",
  "vcs_revision" : "9116ce62e93e825ea95006ec683767c7846220b2",
  "build_num" : 19559,
  "status" : "failed",
  "stop_time" : "2015-12-03T21:40:33.094Z",
  "start_time" : "2015-12-03T21:13:52.782Z",
  "retry_of": 19558,
  "author_name" : "Gregory Wood"
}, {
  "build_url" : "https://circleci.com/gh/luceo/luceo/19558",
  "branch" : "ftw-402-affectation-prototyping",
  "username" : "luceo",
  "vcs_revision" : "9116ce62e93e825ea95006ec683767c7846220b1",
  "build_num" : 19558,
  "status" : "failed",
  "stop_time" : "2015-12-03T21:40:33.094Z",
  "start_time" : "2015-12-03T19:13:52.782Z",
  "retry_of": null,
  "author_name" : "Gregory Wood"
} ]'''

STATUS_OK = [
    {
        'vcs_revision': 'b07c91818f754ba64539db70d60db690c039a559',
        'status': 'success',
        'start_time': '2015-12-03T21:31:24.449Z',
        'author_name': 'sakai135',
        'branch': 'ftw-318-fix-identificationDoublons-2',
        'build_url': 'https://circleci.com/gh/luceo/luceo/19560',
        'retry_of': None,

    },
    {
        'vcs_revision': '9116ce62e93e825ea95006ec683767c7846220b2',
        'status': 'failed',
        'start_time': '2015-12-03T21:13:52.782Z',
        'author_name': 'Gregory Wood',
        'branch': 'ftw-402-affectation-prototyping',
        'build_url': 'https://circleci.com/gh/luceo/luceo/19559',
        'retry_of': 19558,
    },
    {
        'vcs_revision': '9116ce62e93e825ea95006ec683767c7846220b1',
        'status': 'failed',
        'start_time': '2015-12-03T19:13:52.782Z',
        'author_name': 'Gregory Wood',
        'branch': 'ftw-402-affectation-prototyping',
        'build_url': 'https://circleci.com/gh/luceo/luceo/19558',
        'retry_of': None,
    }
]


class TestCIService(unittest.TestCase):
    """Check for CI service metdods"""

    def test_CircleCIService_class_should_exist(self):
        self.assertTrue(hasattr(ci, 'CircleCIService'))

    def test_get_last_builds_should_exist(self):
        ci_service = ci.CircleCIService()
        self.assertTrue(hasattr(ci_service, 'get_build_list'))

    @patch.object(urllib2, 'urlopen', MagicMock())
    @patch.object(settings, 'get_secret', MagicMock())
    def test_get_last_builds_should_call_urllib2(self):
        url_return = Mock()
        url_return.read.return_value = '[]'
        urllib2.urlopen.return_value = url_return
        settings.get_secret.return_value = 'ci_token'
        ci_service = ci.CircleCIService()
        ci_service.get_build_list()
        str_url = ''.join(['https://circleci.com/api/v1/project/cbdr/',
                          'luceo?circle-token=ci_token&limit=100'])
        request, = urllib2.urlopen.call_args[0]
        settings.get_secret.assert_called_with('CIRCLE_CI_TOKEN')
        self.assertEqual(request.get_full_url(), str_url)

    @patch.object(urllib2, 'urlopen', MagicMock())
    @patch.object(ci.CircleCIService, 'get_datetime', MagicMock())
    def test_get_last_builds_should_return_a_list(self):
        url_return = Mock()
        url_return.read.return_value = CIRCLE_CI_RESULT
        urllib2.urlopen.return_value = url_return
        ci_service = ci.CircleCIService()
        ci_service.get_datetime.return_value = datetime.datetime(
            2015, 12, 03, 19, 32)
        new_list = ci_service.get_build_list()
        self.assertEqual(new_list, STATUS_OK)
