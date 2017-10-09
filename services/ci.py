# -*- coding:utf-8 -*-
import urllib2
import json
import datetime

import settings

GITHUB_USER = 'soloidx'
GITHUB_REPO = 'repo'

BASE_URL = ''.join(['https://circleci.com/api/v1/project/{user}/',
                    '{repo}?circle-token={token}&limit=100'])

BASE_BUILD_URL = ''.join(['https://circleci.com/api/v1/project/{user}/',
                         '{repo}/{build}?circle-token={token}'])


class CircleCIService(object):
    """docstring for CircleCIService"""

    def get_datetime(self):
        return datetime.datetime.utcnow()

    def send_json_request(self, url_endpoint):
        headers = {'Accept': 'application/json'}
        req = urllib2.Request(url_endpoint, None, headers)
        raw_result = urllib2.urlopen(req)
        return raw_result

    def get_build_list(self):
        time_total_range = settings.MINUTES_EXTRA + settings.MINUTES_RANGE
        date_start = self.get_datetime()
        date_start -= datetime.timedelta(minutes=time_total_range)
        url_endpoint = BASE_URL.format(
            token=settings.get_secret('CIRCLE_CI_TOKEN'),
            user=GITHUB_USER,
            repo=GITHUB_REPO)
        raw_result = self.send_json_request(url_endpoint)
        if raw_result:
            raw_list = json.loads(raw_result.read())
        result_list = []
        if raw_list:
            for element in raw_list:
                element_date = datetime.datetime.strptime(
                    element['start_time'],
                    '%Y-%m-%dT%H:%M:%S.%fZ')
                if element_date > date_start:
                    result_list.append({
                        'vcs_revision': element['vcs_revision'],
                        'status': element['status'],
                        'start_time': element['start_time'],
                        'author_name': element['author_name'],
                        'branch': element['branch'],
                        'build_url': element['build_url'],
                        'retry_of': element['retry_of'],
                    })
        return result_list
