
import logging
import requests
import uuid
import json

from nose2.events import Plugin
from nose2 import result


log = logging.getLogger('nose2.plugins.nose2-rt.rt')


class Rt(Plugin):
    configSection = 'rt'
    commandLineSwitch = ('RT', 'rt', 'Real-time status update via HTTP')

    def __init__(self):

        self.endpoint = self.config.as_str(
            'endpoint', '')

        self.uuid = uuid.uuid4()
        self.success = 0
        self.errors = 0
        self.failed = 0
        self.skipped = 0
        self.timeTaken = 0
        self.start = None
        self.stop = None
        self.test_outcome = None

    def post(self, payload):
        requests.post(self.endpoint, data=payload)

    def startTestRun(self, event):
        tests = self.getTests(event)
        self.post({
            'type': "startTestRun",
            'job_id': self.uuid,
            'tests': tests,
        })

    def startTest(self, event):
        self.test_outcome = None
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        self.post({
            'type': 'startTest',
            'job_id': self.uuid,
            'test': test_id,
            'startTime': event.startTime})

    def testOutcome(self, event):
        msg = ''
        if event.exc_info:
            msg = event.exc_info
        elif event.reason:
            msg = event.reason

        error_text = ''
        status = ''
        if event.outcome == result.ERROR:
            self.errors += 1
            error_text = msg
            status = 'error'
        elif event.outcome == result.FAIL and not event.expected:
            self.failed += 1
            error_text = msg
            status = 'failed'
        elif event.outcome == result.PASS and not event.expected:
            self.skipped += 1
            status = 'skipped'
        elif event.outcome == result.SKIP:
            self.skipped += 1
            status = 'skipped'
        elif event.outcome == result.FAIL and event.expected:
            self.skipped += 1
            error_text = msg
            status = 'skipped'
        elif event.outcome == result.PASS and event.expected:
            self.success += 1
            status = 'passed'

        self.test_outcome = status, error_text

    def stopTest(self, event):
        test = event.test
        test_id_str = test.id().split('\n')
        test_id = test_id_str[0]
        self.post({
            'type': 'stopTest',
            'job_id': self.uuid,
            'test': test_id,
            'stopTime': event.stopTime,
            'status': self.test_outcome[0],
            'msg': self.test_outcome[1]})

    def stopTestRun(self, event):
        self.success = str(self.success)
        self.errors = str(self.errors)
        self.failed = str(self.failed)
        self.skipped = str(self.skipped)
        self.timeTaken = "%.3f" % event.timeTaken
        self.post({
            'type': 'stopTestRun',
            'job_id': self.uuid,
            'tests_success': self.success,
            'tests_errors': self.errors,
            'tests_failed': self.failed,
            'tests_skipped': self.skipped,
            'job_time_taken': self.timeTaken})

    def getTests(self, event):
        suite = event.suite
        tests = {}
        for suite_data in suite:
            for test_data in suite_data:
                for test_list in test_data:
                    for test in test_list._tests:
                        test_data = (str(test).split(" "))
                        tests[str(test_data[0])] = str(test_data[1])[1:-1]
        print("RESULT")
        print(tests)
        return json.dumps(tests)