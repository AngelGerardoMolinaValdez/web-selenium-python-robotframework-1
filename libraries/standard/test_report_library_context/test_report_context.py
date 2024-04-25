from typing import ClassVar

class TestReportContext:
    __executed_from_listener: ClassVar[bool] = False
    __status_defined_in_keyword: ClassVar[bool] = False

    @classmethod
    def set_executed_from_listener(cls):
        cls.__executed_from_listener = True

    @classmethod
    def set_status_defined_in_keyword(cls):
        cls.__status_defined_in_keyword = True

    @classmethod
    def get_executed_from_listener(cls):
        return cls.__executed_from_listener

    @classmethod
    def get_status_defined_in_keyword(cls):
        return cls.__status_defined_in_keyword
