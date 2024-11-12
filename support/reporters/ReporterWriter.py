import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reporter.base_reporter import BaseReporter
from entry_status import EntryStatus

class ReporterWriter:
    def add_entry_to_report(self, desc: str, status: EntryStatus, reporters: list[BaseReporter] | BaseReporter, **kwargs) -> None:
        self.__add_to_report(desc, status, reporters, kwargs)

    def __add_to_report(self, desc: str, status: str, reporters: list[BaseReporter] | BaseReporter, kwargs: dict):
        if type(reporters) is not list:
            reporters.add_content(desc, status)
            return

        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.add_content(desc, status)

    def __filter_reporters_by_tags(self, reporters: list[BaseReporter], tags: list | None) -> list[BaseReporter]:
        if tags is None:
            return reporters

        return [reporter for reporter in reporters if any(reporter_tag in tags for reporter_tag in reporter.tags)]

    def set_reporter_status(self, reporters: list[BaseReporter] | BaseReporter, status: EntryStatus, **kwargs):
        if type(reporters) is not list:
            reporters.status = status
            return

        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.status = status

    def set_reporter_message(self, reporters: list[BaseReporter]  | BaseReporter, message: str, **kwargs):
        if type(reporters) is not list:
            reporters.message = message
            return

        filtered_reporters = self.__filter_reporters_by_tags(reporters, kwargs.get("include"))

        for reporter in filtered_reporters:
            reporter.message = message
