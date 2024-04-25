import datetime
import os
from test_report_library_context.reports.report_types import ReportTypes
from test_report_library_context.test_report_details import TestReportDetails

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from test_paths import TestsReportsPath

class ReportCreator:
    def create_report(self, test_name, status, *formats):
        reports_path = TestsReportsPath().path()

        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name_report = test_name + " " + today.replace(":", "-")
        path_report = os.path.abspath(os.path.join(reports_path, test_name_report))
        os.mkdir(path_report)

        test_status = TestReportDetails.get_status() if status != "" else status
        steps = TestReportDetails.get_steps()
        setup_steps = TestReportDetails.get_setup_steps()
        teardown_steps = TestReportDetails.get_teardown_steps()

        for format in formats:
            ReportType = ReportTypes[format.upper()].value
            report = ReportType()
            report.create(test_name, test_status, steps, setup_steps, teardown_steps, path_report)
        
        TestReportDetails.clear()
