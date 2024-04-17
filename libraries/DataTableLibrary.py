import os
from dataclasses import dataclass, make_dataclass, asdict
from file_readers import FileReaderType


class DataTableLibrary:    
    def create_data_table(self, path: str, index: int) -> dataclass:
        """Crea un DataTable a partir de un archivo CSV."""
        ext_file = os.path.splitext(path)[1]
        reader = FileReaderType[ext_file[1:].upper()].value
        reader.read(path)
        test_data_row = reader.get(index)
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
