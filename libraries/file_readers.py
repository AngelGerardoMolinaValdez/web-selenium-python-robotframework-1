import os
import csv
import json
from typing import Any
from enum import Enum

class CsvReader:
    __content: list[dict[str, Any]] = []

    @classmethod
    def read(cls, path: str, encoding: str) -> list:
        """Read the CSV file and return a list of dictionaries."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo de datos no existe: {path}")

        with open(path, 'r', encoding=encoding) as file:
            cls.__content = list(csv.DictReader(file))
    
    @classmethod
    def get(cls, index: int) -> dict:
        try:
            index = int(index)
        except ValueError:
            raise ValueError(f"El índice {index} no es un número entero.")

        if index < 0 or index >= len(cls.__content):
            raise IndexError(f"El índice {index} está fuera de rango de las filas del archivo de datos.")

        return cls.__content[index]

class JsonReader:
    __content: list[dict[str, Any]] = []

    @classmethod
    def read(cls, path: str, encoding: str) -> dict:
        """El contenido del json debe ser una lista de diccionarios."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo de datos no existe: {path}")

        with open(path, 'r', encoding=encoding) as file:
            cls.__content = json.load(file)

    @classmethod
    def get(cls, index: int) -> Any:
        """Read the JSON file and return the value of the key."""
        try:
            index = int(index)
        except ValueError:
            raise ValueError(f"El índice {index} no es un número entero.")

        if index < 0 or index >= len(cls.__content):
            raise IndexError(f"El índice {index} está fuera de rango de las filas del archivo de datos.")

        return cls.__content[index]
    
class FileReaderType(Enum):
    CSV = CsvReader
    JSON = JsonReader
