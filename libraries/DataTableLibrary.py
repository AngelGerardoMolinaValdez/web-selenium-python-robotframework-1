import os
import csv
from typing import Any
from dataclasses import dataclass, make_dataclass, asdict
from robot.api.deco import library

class CsvReader:
    __content: list[dict[str, Any]] = []

    @classmethod
    def read(cls, path: str) -> list:
        """Read the CSV file and return a list of dictionaries."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo de datos no existe: {path}")

        with open(path, 'r') as file:
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

@library
class DataTableLibrary:    
    def create_data_table(self, path: str, index: int) -> dataclass:
        """Crea un DataTable a partir de un archivo CSV."""
        CsvReader.read(path)
        test_data_row = CsvReader.get(index)
        DataTable: dataclass = make_dataclass("DataTable", test_data_row.keys())
        return DataTable(**test_data_row)

    def create_data_table_from_fields(self, **fields) -> dataclass:
        """Crea un DataTable a partir de un archivo CSV."""
        DataTable: dataclass = make_dataclass("DataTable", fields.keys())
        return DataTable(**fields)

    def update_data_table(self, data_table: dataclass, **fields) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable."""
        data_class_dict = asdict(data_table)
        data_class_dict.update(fields)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in data_class_dict.keys()]
        )
        return DataClass(**data_class_dict)

    def merge_data_tables(self, data_table: dataclass, another_data_table: dataclass) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable."""
        data_table_dict = asdict(data_table)
        another_data_table_dict = asdict(another_data_table)
        data_table_dict.update(another_data_table_dict)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in data_table_dict.keys()]
        )
        return DataClass(**data_table_dict)

    def unify_data_tables(self, data_table: dataclass, *data_tables) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable."""
        original_data_table_dict = asdict(data_table)
        for another_data_table in data_tables:
            another_data_table_dict = asdict(another_data_table)
            original_data_table_dict.update(another_data_table_dict)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in original_data_table_dict.keys()]
        )
        return DataClass(**original_data_table_dict)
