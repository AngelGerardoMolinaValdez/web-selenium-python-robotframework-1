import csv  
from dataclasses import make_dataclass, dataclass
from datatable_repository import DataTableRepository
from datatable_errors import DataTableRowReferenceDoesNotExist

class DataTable:
    @classmethod
    def create(cls, path, index):  
        with open(path, 'r', encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)  
            headers = csv_reader.fieldnames
            DataClass = make_dataclass(
                "DataClass",
                [(field, str) for field in headers]
            )
            
            row_number, fields = list(enumerate(csv_reader))[index]
            new_data_class = DataClass(**fields)
            return new_data_class, row_number

    @classmethod
    def find_reference(cls, file_path: str, fieldname: str, value: str):
        """
        name -> el nombre del archivo
        fieldname -> el nombre de referencia a encontrar
        """
        matching_row = None
        with open(file_path, 'r', encoding="utf-8") as file_csv:
            csv_reader = csv.DictReader(file_csv)
            headers = csv_reader.fieldnames

            for row in csv_reader:
                if row[fieldname] == value:
                    matching_row = row

            DataClass = make_dataclass(
                "DataClass",
                [(field, str) for field in headers]
            )
            
            if matching_row is None:
                DataTableRowReferenceDoesNotExist(
                    f"No fue encontrada la file con el encabezado {fieldname}" +
                    f" en el archivo {file_path} con el valor {value}" +
                    " verifique que el nombre este bien escrito"
                )

            new_data_class = DataClass(**matching_row)
        return new_data_class

    @classmethod
    def save(cls, iteration: int, name: str, data_class: dataclass):
        DataTableRepository.save(iteration, name, data_class)
