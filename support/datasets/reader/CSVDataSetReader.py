import os
import csv
from robot.api.deco import keyword

class CSVDataSetReader:
    @keyword("Read Data Set", tags=["library", "dataset-reader"])
    def read_dataset(self, file_path: str, index: int, encoding: str = "utf-8") -> dict:
        self.__validate(file_path, index, encoding)

        with open(file_path, mode="r", encoding=encoding) as file:
            reader = list(csv.DictReader(file))
            return reader[index]

    @keyword("Read All Data Sets", tags=["library", "dataset-reader"])
    def read_all_datasets(self, file_path: str, encoding: str = "utf-8") -> list:
        self.__validate(file_path, index=None, encoding=encoding)

        with open(file_path, mode="r", encoding=encoding) as file:
            reader = list(csv.DictReader(file))
            return reader

    def __validate(self, file_path: str, index: int = None, encoding: str = "utf-8"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' was not found")

        try:
            with open(file_path, mode="r", encoding=encoding) as file:
                reader = list(csv.DictReader(file))
                if index is not None and index >= len(reader):
                    raise IndexError(f"The index {index} exceeds the total number of available rows ({len(reader)})")
        except csv.Error as e:
            raise csv.Error(f"Error processing the CSV file {file_path}. Error Message: {e}")
