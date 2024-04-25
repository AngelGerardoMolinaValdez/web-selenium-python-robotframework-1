import os

class TestsOutputPath:
    __path = None
    __instance = None

    def __new__(cls) -> object:
        if cls.__path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            if not os.path.exists(os.path.join(base_path, "output")):
                os.mkdir(os.path.join(base_path, "output"))

            cls.__path = os.path.join(base_path, "output")
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def path(self) -> str:
        return self.__path


class TestsReportsPath:
    __path = None
    __instance = None

    def __new__(cls) -> object:
        if cls.__path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            if not os.path.exists(os.path.join(base_path, "output", "reports")):
                os.mkdir(os.path.join(base_path, "output", "reports"))

            cls.__path = os.path.join(base_path, "output", "reports")
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def path(self) -> str:
        return self.__path

class TestsSeleniumScreenShootsPath:
    __path = None
    __instance = None

    def __new__(cls) -> object:
        if cls.__path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            if not os.path.exists(os.path.join(base_path, "output", "selenium-screenshots")):
                os.mkdir(os.path.join(base_path, "output", "selenium-screenshots"))

            cls.__path = os.path.join(base_path, "output", "selenium-screenshots")
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def path(self) -> str:
        return self.__path
    
class TestsResultsPath:
    __path = None
    __instance = None

    def __new__(cls) -> object:
        if cls.__path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            if not os.path.exists(os.path.join(base_path, "output", "results")):
                os.mkdir(os.path.join(base_path, "output", "results"))

            cls.__path = os.path.join(base_path, "output", "results")
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def path(self) -> str:
        return self.__path
