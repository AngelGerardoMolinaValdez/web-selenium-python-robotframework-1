import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'libraries', 'standard'))

from test_report_library_context.test_report_details import TestReportDetails
from test_report_library_context.test_report_context import TestReportContext
from test_report_library_context.reports.report_creator import ReportCreator

class TestsReportGenerator:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, *formats):
        self.__formats = formats
        TestReportContext.set_executed_from_listener()

    def end_test(self, name, attrs):
        if TestReportContext.get_status_defined_in_keyword():
            status = TestReportDetails.get_status()
        else:
            TestReportDetails.set_status(attrs['status'])
            status = TestReportDetails.get_status()

        ReportCreator().create_report(name, status, *self.__formats)
    
    def end_suite(self, name, attrs):
        TestReportDetails.clear_all()
