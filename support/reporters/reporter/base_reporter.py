from abc import ABC, abstractmethod

class BaseReporter(ABC):
    def __init__(self, output_dir: str, name: str) -> None:
        self.__output_dir = output_dir
        self.__name = name
        self.__report_data = []

    def output_dir_value(self):
        return self.__output_dir

    def name_value(self):
        return self.__name

    def report_data_value(self):
        return self.__report_data
    
    def _add_data(self, content: dict):
        self.__report_data.append(content)

    @abstractmethod
    def add_content_to_report(self, desc: str, level: str):
        pass
