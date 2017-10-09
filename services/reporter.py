# -*- coding:utf-8 -*-
import settings


class BasicReportService(object):
    """docstring for BasicReportService"""

    def report(self, user, branch, revision, build_url):
        pass


class HipChatService(BasicReportService):
    """docstring for HipChatService"""

    def report(self, user, branch, revision, build_url):
        print 'Found in: %s' % build_url


class SMTPService(BasicReportService):
    """sending repports via SMTP"""

    def report(self, user, branch, revision, build_url):
        import smtplib
        from email.mime.text import MIMEText
        message = MIMEText(settings.MESSAGE_TEMPLATE.format(
            build_url=build_url,
            commit=revision,
            branch=branch,
            author=user))

        message_subject = '[Flaky] Flaky test report, build: %s'

        message['Subject'] = message_subject % revision
        message['From'] = settings.SMTP_FROM
        message['To'] = settings.SMTP_TO

        server = smtplib.SMTP(settings.SMTP_HOST)

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(
            settings.get_secret('SMTP_USERNAME'),
            settings.get_secret('SMTP_PASSWORD'))

        server.sendmail(
            settings.SMTP_FROM,
            settings.SMTP_TO,
            message.as_string())
        server.quit()
