# -*- coding:utf-8 -*-
import json

with open('secrets.json') as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """get a variable from a secret file"""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} in the secrets.json file'.format(setting)
        raise NotImplementedError(error_msg)


SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
SMTP_FROM = 'from@example.com'
SMTP_TO = 'to@example.com'

MESSAGE_TEMPLATE = ''.join([
    'A new flaky test was appeared\n',
    'URL: {build_url}\n',
    'Commit: {commit}\n',
    'Branch: {branch}\n',
    'Author: {author}'
])

MINUTES_RANGE = 30
MINUTES_EXTRA = 10
