import unittest
import requests
import uuid
import json
import datetime

from nose2.events import Plugin
from nose2 import result


class Rt(Plugin):
    configSection = 'rt'
    commandLineSwitch = (None, 'rt', 'Enable data collector for Testgr')

    def __init__(self):

        self.endpoint = self.config.as_str(
            'endpoint', '')
        self.show_errors = self.config.as_bool(
            'show_errors', '')

        self.uuid = str(uuid.uuid4())
        self.success = 0
        self.errors = 0
        self.failed = 0
        self.skipped = 0
        self.timeTaken = 0
        self.start = None
        self.stop = None
        self.test_outcome = None
        self.attrs = []
        self.tests = None
        self.addArgument(self.attrs, None, "rte", "With --rte \"your_environment\" option you can send "
                                                  "additional info to the Testgr sertver")

        group = self.session.pluginargs
        group.add_argument('--rt-job-report', action='store_true', dest='rt_job_report',
                           help='Send Testgr job result via email')

    def handleArgs(self, event):
        self.send_report_arg = event.args.rt_job_report

    def send_report(self):
        if self.send_report_arg is True:
            return "1"
        return "0"

    def post(self, payload):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            requests.post(self.endpoint, data=json.dumps(payload), headers=headers)
        except requests.exceptions.ConnectionError as error:
            if self.show_errors:
                print(error)
            else:
                pass

    def startTestRun(self, event):
        self.tests = self.getTests(event)
        if len(self.attrs) > 0:
            env = self.attrs[0]
        else:
            env = None
        self.post({
            'fw': "1",
            'type': "startTestRun",
            'job_id': self.uuid,
            'tests': self.tests[0],
            'test_uuids': self.tests[1],
            'env': env,
            'startTime': str(event.startTime)
        })

    def startTest(self, event):
        self.test_outcome = None
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        self.post({
            'fw': "1",
            'type': 'startTestItem',
            'job_id': self.uuid,
            'test': test_id,
            'uuid': self.tests[1][test_id],
            'startTime': str(event.startTime)})

    def testOutcome(self, event):
        msg = ''
        if event.exc_info:
            msg = event.exc_info
        elif event.reason:
            msg = event.reason

        error_text = ''
        status = ''
        if event.outcome == result.ERROR:
            error_text = msg
            status = 'error'
        elif event.outcome == result.FAIL and not event.expected:
            error_text = msg
            status = 'failed'
        elif event.outcome == result.PASS and not event.expected:
            status = 'skipped'
        elif event.outcome == result.SKIP:
            status = 'skipped'
        elif event.outcome == result.FAIL and event.expected:
            error_text = msg
            status = 'skipped'
        elif event.outcome == result.PASS and event.expected:
            status = 'passed'

        self.test_outcome = status, error_text

    def stopTest(self, event):
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        self.post({
            'fw': "1",
            'type': 'stopTestItem',
            'job_id': self.uuid,
            'test': test_id,
            'uuid': self.tests[1][test_id],
            'stopTime': str(event.stopTime),
            'status': str(self.test_outcome[0]),
            'msg': str(self.test_outcome[1])})

    def stopTestRun(self, event):
        self.timeTaken = "%.3f" % event.timeTaken
        self.post({
            'fw': "1",
            'type': 'stopTestRun',
            'job_id': self.uuid,
            'stopTime': str(event.stopTime),
            'timeTaken': self.timeTaken,
            'send_report': self.send_report()})

    def getTests(self, event):
        suite = event.suite
        tests = {}
        test_uuids = {}
        for suite_data in suite:
            for test_data in suite_data:
                for test_list in test_data:
                    if isinstance(test_list, unittest.suite.TestSuite):
                        for test in test_list._tests:
                            test_data = (str(test).split(" "))
                            tests[str(test_data[0])] = test.id()
                            test_uuids[test.id()] = str(uuid.uuid4())
                    else:
                        test_data = (str(test_list).split(" "))
                        tests[str(test_data[0])] = test_list.id()
                        test_uuids[test_list.id()] = str(uuid.uuid4())
        return tests, test_uuids
