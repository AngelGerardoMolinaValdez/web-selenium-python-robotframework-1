import os
from robot.api.deco import keyword, not_keyword
from datatable import DataTable
from datatable_repository import DataTableRepository
from datatable_errors import DataTableDoesNotExist

DATA_DIR: str = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "data"
    )
)

@not_keyword
def find_file(name: str):
    for root, _, files in os.walk(DATA_DIR):
        for file_name in files:
            if file_name == name:
                return os.path.join(root, file_name)

    raise DataTableDoesNotExist(f"No existe el archivo {name}")

@keyword("Crear DataTable")
def create_data_table(path: str, index: int):
    data_class = DataTableRepository.find(index)
    if not data_class:
        file_path = find_file(path)
        data_class, index_from_datable = DataTable.create(file_path, index)
        DataTable.save(data_class, index_from_datable)
    return data_class
