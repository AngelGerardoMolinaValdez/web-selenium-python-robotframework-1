import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reporter.base_reporter import BaseReporter

class ReporterBuilder:
    def add_info_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "info", reporters, kwargs)

    def add_pass_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "pass", reporters, kwargs)

    def add_fail_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "fail", reporters, kwargs)

    def add_debug_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "debug", reporters, kwargs)

    def add_error_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "error", reporters, kwargs)

    def add_warning_to_report(self, desc: str, reporters: list[BaseReporter], **kwargs) -> None:
        self.__add_to_report(desc, "warning", reporters, kwargs)

    def __add_to_report(self, desc: str, status: str, reporters: list, kwargs: dict):
        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.add_content(desc, status)

    def __filter_reporters_by_tags(self, reporters: list[BaseReporter], tags: list | None) -> list[BaseReporter]:
        if tags is None:
            return reporters

        return [reporter for reporter in reporters if any(reporter_tag in tags for reporter_tag in reporter.tags)]

    def set_reporter_status(self, reporters: list[BaseReporter], status: str, **kwargs):
        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.status = status

    def set_reporter_message(self, reporters: list[BaseReporter], message: str, **kwargs):
        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.message = message
