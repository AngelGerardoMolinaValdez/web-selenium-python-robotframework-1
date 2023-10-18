import csv  
from dataclasses import make_dataclass  
from datatable_repository import DataTableRepository

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
            
            id_data_class, fields = list(enumerate(csv_reader))[index]
            new_data_class = DataClass(**fields)
            return new_data_class, id_data_class

    @classmethod
    def save(cls, data_class, id):
        DataTableRepository.save(data_class, id)
