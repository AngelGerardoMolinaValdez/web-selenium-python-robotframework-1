from typing import Union
from abc import ABC, abstractmethod

class BaseReporter(ABC):
    def __init__(self, name: str, tags: Union[list, None]) -> None:
        self.__message = ""
        self.__status = ""
        self.__name = name
        self.__tags = tags if tags is not None else []
        self.__report_data = []

    @property
    def name(self):
        return self.__name

    @property
    def tags(self):
        return self.__tags

    @property
    def message(self):
        return self.__message

    @property
    def status(self):
        return self.__status

    @message.setter
    def message(self, message: str):
        self.__message = message

    @status.setter
    def status(self, status: str):
        self.__status = status

    @property
    def content(self):
        return self.__report_data
    
    def _add_content(self, content: dict):
        self.__report_data.append(content)

    @abstractmethod
    def add_content(self, desc: str, level: str):
        pass
