from typing import ClassVar

class TestReportDetails:
    __steps_details: ClassVar[list[dict[str, str]]] = []
    __steps_setup_details: ClassVar[list[dict[str, str]]] = []
    __steps_teardown_details: ClassVar[list[dict[str, str]]] = []
    __status: ClassVar[str] = ""

    @classmethod
    def get_steps(cls):
        return cls.__steps_details

    @classmethod
    def get_setup_steps(cls):
        return cls.__steps_setup_details

    @classmethod
    def get_teardown_steps(cls):
        return cls.__steps_teardown_details

    @classmethod
    def get_status(cls):
        return cls.__status

    @classmethod
    def set_status(cls, status):
        cls.__status = status

    @classmethod
    def clear(cls):
        cls.__steps_details.clear()        
        cls.__status = ""

    @classmethod
    def clear_all(cls):
        cls.__steps_details.clear()
        cls.__steps_setup_details.clear()
        cls.__steps_teardown_details.clear()
        cls.__status = ""

    @classmethod
    def add(cls, title, status, screenshot=None, setup=False, teardown=False):
        if setup:
            cls.__steps_setup_details.append({
                "title": title,
                "status": status,
                "screenshot": screenshot
            })
        
        elif teardown:
            cls.__steps_teardown_details.append({
                "title": title,
                "status": status,
                "screenshot": screenshot
            })

        else:
            cls.__steps_details.append({
                "title": title,
                "status": status,
                "screenshot": screenshot
            })
