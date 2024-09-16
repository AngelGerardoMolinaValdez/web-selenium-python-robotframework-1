import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reporter.base_reporter import BaseReporter

class ReporterBuilder:
    def add_info_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "info")

    def add_pass_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "pass")

    def add_fail_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "fail")

    def add_debug_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "debug")

    def add_error_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "error")

    def add_warning_to_report(self, reporter: BaseReporter, desc: str) -> None:
        reporter.add_content_to_report(desc, "warning")
